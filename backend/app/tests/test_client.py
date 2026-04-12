"""
Tests for app/processing/client.py — Client field injection stage.

Responsibilities (ONLY):
- Create Client column from _source_sheet
- Strip whitespace from sheet name before assignment
- Preserve _source_sheet unchanged
- Ensure every row has a non-null, non-empty Client value

Does NOT:
- Validate client name quality or allowed values
- Drop rows
- Modify any other column
"""
import logging
import pandas as pd
from app.processing.client import inject_client


def make_df(data: dict) -> pd.DataFrame:
    """Helper: build a DataFrame from a dict of column→values."""
    return pd.DataFrame(data)


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_single_sheet_client_assigned():
    """All rows in a single-sheet DataFrame get the correct Client value."""
    df = make_df({
        "First": ["John", "Jane"],
        "Last": ["Doe", "Smith"],
        "_source_sheet": ["Alpha Fund", "Alpha Fund"],
    })
    result = inject_client(df)
    assert "Client" in result.columns
    assert list(result["Client"]) == ["Alpha Fund", "Alpha Fund"]


def test_multi_sheet_client_assigned_correctly():
    """Rows from different sheets get their respective sheet names as Client."""
    df = make_df({
        "First": ["John", "Jane", "Alice"],
        "_source_sheet": ["Alpha Fund", "Liberty PAC", "Alpha Fund"],
    })
    result = inject_client(df)
    assert result.iloc[0]["Client"] == "Alpha Fund"
    assert result.iloc[1]["Client"] == "Liberty PAC"
    assert result.iloc[2]["Client"] == "Alpha Fund"


def test_sheet_name_whitespace_stripped():
    """Leading/trailing whitespace in sheet name is stripped before assignment."""
    df = make_df({
        "First": ["John"],
        "_source_sheet": ["  Alpha Fund  "],
    })
    result = inject_client(df)
    assert result.iloc[0]["Client"] == "Alpha Fund"


def test_source_sheet_preserved_unchanged():
    """_source_sheet column is not modified — only Client is added."""
    df = make_df({
        "First": ["John"],
        "_source_sheet": ["  Alpha Fund  "],
    })
    result = inject_client(df)
    assert result.iloc[0]["_source_sheet"] == "  Alpha Fund  "


def test_client_column_added_not_overwritten():
    """Client column is created fresh — no existing column is overwritten."""
    df = make_df({
        "First": ["John"],
        "_source_sheet": ["Alpha Fund"],
    })
    assert "Client" not in df.columns
    result = inject_client(df)
    assert "Client" in result.columns


def test_no_null_client_values():
    """Every row must have a non-null Client value."""
    df = make_df({
        "First": ["John", "Jane", "Alice"],
        "_source_sheet": ["Alpha Fund", "Liberty PAC", "Heritage Trust"],
    })
    result = inject_client(df)
    assert result["Client"].notna().all()


def test_no_empty_string_client_values():
    """No row should have an empty string Client value."""
    df = make_df({
        "First": ["John"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = inject_client(df)
    assert (result["Client"] != "").all()


def test_no_other_columns_modified():
    """inject_client must not modify any column other than adding Client."""
    df = make_df({
        "First": ["John"],
        "Last": ["Doe"],
        "DonationAmount": [100.0],
        "_source_sheet": ["Alpha Fund"],
    })
    original_values = {
        "First": df["First"].tolist(),
        "Last": df["Last"].tolist(),
        "DonationAmount": df["DonationAmount"].tolist(),
        "_source_sheet": df["_source_sheet"].tolist(),
    }
    result = inject_client(df)
    assert result["First"].tolist() == original_values["First"]
    assert result["Last"].tolist() == original_values["Last"]
    assert result["DonationAmount"].tolist() == original_values["DonationAmount"]
    assert result["_source_sheet"].tolist() == original_values["_source_sheet"]


def test_injection_is_deterministic():
    """Same input always produces same Client values."""
    df = make_df({
        "First": ["John", "Jane"],
        "_source_sheet": ["Alpha Fund", "Liberty PAC"],
    })
    result_1 = inject_client(df.copy())
    result_2 = inject_client(df.copy())
    pd.testing.assert_frame_equal(result_1, result_2)


def test_multiple_clients_all_distinct():
    """Multiple distinct sheet names produce distinct Client values."""
    df = make_df({
        "First": ["John", "Jane", "Alice", "Bob"],
        "_source_sheet": [
            "Alpha Fund",
            "Liberty PAC",
            "Heritage Trust",
            "Patriot Group",
        ],
    })
    result = inject_client(df)
    assert set(result["Client"].unique()) == {
        "Alpha Fund", "Liberty PAC", "Heritage Trust", "Patriot Group"
    }


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

def test_null_source_sheet_produces_null_client_with_warning(caplog):
    """
    Null _source_sheet propagates to null Client.
    This is a defensive case — the parser always populates _source_sheet,
    but if it doesn't, Client will be null and T4 will reject the row.
    A warning must be logged so the upstream issue is visible.
    """
    df = make_df({
        "First": ["John", "Jane"],
        "_source_sheet": [None, "Alpha Fund"],
    })
    with caplog.at_level(logging.WARNING, logger="app.processing.client"):
        result = inject_client(df)

    assert pd.isna(result.iloc[0]["Client"])
    assert result.iloc[1]["Client"] == "Alpha Fund"
    assert len(result) == 2  # row not dropped
    assert "null" in caplog.text.lower()


def test_whitespace_only_sheet_name_produces_empty_client_with_warning(caplog):
    """
    Sheet name containing only whitespace strips to empty string.
    A warning must be logged — T4 will reject this row.
    Row must not be dropped here.
    """
    df = make_df({
        "First": ["John"],
        "_source_sheet": ["   "],
    })
    with caplog.at_level(logging.WARNING, logger="app.processing.client"):
        result = inject_client(df)

    assert result.iloc[0]["Client"] == ""
    assert len(result) == 1  # row not dropped
    assert "empty" in caplog.text.lower() or "whitespace" in caplog.text.lower()


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------

def test_multi_sheet_integration():
    """
    Integration: simulates a real post-normalization DataFrame from multiple
    sheets. Verifies correct Client assignment, no data loss, and
    _source_sheet consistency.
    """
    df = make_df({
        "First": ["John", "Jane", "Alice"],
        "Last": ["Doe", "Smith", "Johnson"],
        "DonationAmount": [100.0, 200.0, 500.0],
        "_source_sheet": ["Alpha Fund", "Alpha Fund", "Liberty PAC"],
    })

    result = inject_client(df)

    assert len(result) == 3
    assert result.iloc[0]["Client"] == "Alpha Fund"
    assert result.iloc[1]["Client"] == "Alpha Fund"
    assert result.iloc[2]["Client"] == "Liberty PAC"
    assert result.iloc[0]["_source_sheet"] == "Alpha Fund"
    assert result.iloc[2]["_source_sheet"] == "Liberty PAC"
    assert result["Client"].notna().all()
    assert result.iloc[0]["First"] == "John"
    assert result.iloc[2]["DonationAmount"] == 500.0


def test_empty_dataframe_returns_client_column():
    """Empty DataFrame input returns DataFrame with Client column — no crash."""
    df = pd.DataFrame(columns=["First", "Last", "_source_sheet"])
    result = inject_client(df)
    assert "Client" in result.columns
    assert len(result) == 0
