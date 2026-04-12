"""
Tests for app/processing/splitter.py — T4-3 row splitter.

Splitter responsibilities (ONLY):
- Split validated DataFrame into clean_df and rejected_df
- Clean condition: rejection_reason is NaN, empty string, or whitespace-only
- Rejected condition: rejection_reason contains any non-empty value
- Drop rejection_reason and internal columns from clean_df
- Preserve rejection_reason in rejected_df
- Never modify row values
- Never re-run validation

Does NOT:
- Perform validation (T4-1/T4-2)
- Enforce schema (T5-6)
"""
import pandas as pd
from app.processing.splitter import split_rows


REQUIRED_FIELDS = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]


def make_valid_row(**overrides) -> dict:
    base = {
        "First": "John",
        "Last": "Doe",
        "Address1": "123 Main St",
        "City": "Nashville",
        "State": "TN",
        "Zip": "37201",
        "DonationDate": "2024-01-01",
        "DonationAmount": 100.0,
        "Client": "Alpha Fund",
        "_source_sheet": "Alpha Fund",
        "_is_valid": True,
        "_rejection_reason": "",
    }
    base.update(overrides)
    return base


def make_rejected_row(**overrides) -> dict:
    base = make_valid_row()
    base["_is_valid"] = False
    base["_rejection_reason"] = "Missing: Last"
    base.update(overrides)
    return base


def make_df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


# ---------------------------------------------------------------------------
# Row conservation (mandatory)
# ---------------------------------------------------------------------------

def test_row_count_conserved_mixed():
    """clean + rejected row counts must equal input row count."""
    df = make_df(
        make_valid_row(),
        make_rejected_row(),
        make_valid_row(),
        make_rejected_row(_rejection_reason="Invalid Amount"),
    )
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) + len(rejected_df) == len(df)


def test_row_count_conserved_all_clean():
    """All valid rows — rejected_df empty, clean_df has all rows."""
    df = make_df(make_valid_row(), make_valid_row(), make_valid_row())
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 3
    assert len(rejected_df) == 0


def test_row_count_conserved_all_rejected():
    """All invalid rows — clean_df empty, rejected_df has all rows."""
    df = make_df(
        make_rejected_row(),
        make_rejected_row(_rejection_reason="Invalid State"),
    )
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 0
    assert len(rejected_df) == 2


def test_single_valid_row():
    """Single valid row goes to clean_df."""
    df = make_df(make_valid_row())
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 1
    assert len(rejected_df) == 0


def test_single_rejected_row():
    """Single invalid row goes to rejected_df."""
    df = make_df(make_rejected_row())
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 0
    assert len(rejected_df) == 1


# ---------------------------------------------------------------------------
# No leakage between outputs
# ---------------------------------------------------------------------------

def test_no_row_appears_in_both_outputs():
    """No row index appears in both clean_df and rejected_df."""
    df = make_df(make_valid_row(), make_rejected_row(), make_valid_row())
    clean_df, rejected_df = split_rows(df)
    # After reset_index, indices are 0-based in each df
    # Verify by checking values — clean rows have empty rejection reason
    assert clean_df["First"].tolist() == ["John", "John"]
    assert len(rejected_df) == 1


def test_clean_rows_are_valid():
    """All rows in clean_df were marked valid."""
    df = make_df(
        make_valid_row(First="Alice"),
        make_rejected_row(First="Bob"),
        make_valid_row(First="Carol"),
    )
    clean_df, rejected_df = split_rows(df)
    assert "Alice" in clean_df["First"].tolist()
    assert "Carol" in clean_df["First"].tolist()
    assert "Bob" not in clean_df["First"].tolist()


def test_rejected_rows_are_invalid():
    """All rows in rejected_df were marked invalid."""
    df = make_df(
        make_valid_row(First="Alice"),
        make_rejected_row(First="Bob"),
    )
    clean_df, rejected_df = split_rows(df)
    assert "Bob" in rejected_df["First"].tolist()
    assert "Alice" not in rejected_df["First"].tolist()


# ---------------------------------------------------------------------------
# Clean condition — NaN, empty, whitespace-only treated as clean
# ---------------------------------------------------------------------------

def test_empty_string_rejection_reason_treated_as_clean():
    """Row with empty string rejection_reason goes to clean_df."""
    df = make_df(make_valid_row(_rejection_reason=""))
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 1
    assert len(rejected_df) == 0


def test_whitespace_only_rejection_reason_treated_as_clean():
    """Row with whitespace-only rejection_reason goes to clean_df."""
    df = make_df(make_valid_row(_rejection_reason="   "))
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 1
    assert len(rejected_df) == 0


def test_nan_rejection_reason_treated_as_clean():
    """Row with NaN rejection_reason goes to clean_df."""
    df = make_df(make_valid_row(_rejection_reason=float("nan")))
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 1
    assert len(rejected_df) == 0


# ---------------------------------------------------------------------------
# Column structure guarantees
# ---------------------------------------------------------------------------

def test_clean_df_drops_rejection_reason():
    """clean_df must not contain rejection_reason column."""
    df = make_df(make_valid_row())
    clean_df, _ = split_rows(df)
    assert "rejection_reason" not in clean_df.columns
    assert "_rejection_reason" not in clean_df.columns


def test_clean_df_drops_internal_columns():
    """clean_df must not contain _is_valid or _source_sheet."""
    df = make_df(make_valid_row())
    clean_df, _ = split_rows(df)
    assert "_is_valid" not in clean_df.columns
    assert "_source_sheet" not in clean_df.columns


def test_rejected_df_has_rejection_reason():
    """rejected_df must contain rejection_reason column."""
    df = make_df(make_rejected_row())
    _, rejected_df = split_rows(df)
    assert "rejection_reason" in rejected_df.columns


def test_rejected_df_rejection_reason_never_empty():
    """Every row in rejected_df must have a non-empty rejection_reason."""
    df = make_df(
        make_rejected_row(_rejection_reason="Missing: First"),
        make_rejected_row(_rejection_reason="Invalid Amount, Invalid State"),
    )
    _, rejected_df = split_rows(df)
    assert (rejected_df["rejection_reason"] != "").all()
    assert rejected_df["rejection_reason"].notna().all()


def test_rejected_df_drops_internal_columns():
    """rejected_df must not contain _is_valid or _source_sheet."""
    df = make_df(make_rejected_row())
    _, rejected_df = split_rows(df)
    assert "_is_valid" not in rejected_df.columns
    assert "_source_sheet" not in rejected_df.columns


# ---------------------------------------------------------------------------
# Data integrity
# ---------------------------------------------------------------------------

def test_clean_df_values_unchanged():
    """Data values in clean_df are not modified."""
    df = make_df(make_valid_row(First="John", DonationAmount=250.0))
    clean_df, _ = split_rows(df)
    assert clean_df.iloc[0]["First"] == "John"
    assert clean_df.iloc[0]["DonationAmount"] == 250.0


def test_rejected_df_values_unchanged():
    """Data values in rejected_df are not modified."""
    df = make_df(make_rejected_row(First="Bob", _rejection_reason="Missing: Last"))
    _, rejected_df = split_rows(df)
    assert rejected_df.iloc[0]["First"] == "Bob"
    assert rejected_df.iloc[0]["rejection_reason"] == "Missing: Last"


def test_input_not_mutated():
    """Input DataFrame is not modified by split_rows."""
    df = make_df(make_valid_row(), make_rejected_row())
    original_columns = list(df.columns)
    original_len = len(df)
    split_rows(df)
    assert list(df.columns) == original_columns
    assert len(df) == original_len


# ---------------------------------------------------------------------------
# Index integrity
# ---------------------------------------------------------------------------

def test_clean_df_index_reset():
    """clean_df index is reset to 0-based after split."""
    df = make_df(make_rejected_row(), make_valid_row(), make_valid_row())
    clean_df, _ = split_rows(df)
    assert list(clean_df.index) == [0, 1]


def test_rejected_df_index_reset():
    """rejected_df index is reset to 0-based after split."""
    df = make_df(make_valid_row(), make_rejected_row(), make_rejected_row())
    _, rejected_df = split_rows(df)
    assert list(rejected_df.index) == [0, 1]


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_split_is_deterministic():
    """Same input always produces same split output."""
    df = make_df(
        make_valid_row(),
        make_rejected_row(_rejection_reason="Missing: First"),
        make_valid_row(),
    )
    clean_1, rejected_1 = split_rows(df.copy())
    clean_2, rejected_2 = split_rows(df.copy())
    pd.testing.assert_frame_equal(clean_1, clean_2)
    pd.testing.assert_frame_equal(rejected_1, rejected_2)


# ---------------------------------------------------------------------------
# Additional edge case tests identified in QA review
# ---------------------------------------------------------------------------

def test_pd_na_rejection_reason_treated_as_clean():
    """pd.NA in rejection_reason is treated as clean — distinct from float nan."""
    df = make_df(make_valid_row(_rejection_reason=pd.NA))
    clean_df, rejected_df = split_rows(df)
    assert len(clean_df) == 1
    assert len(rejected_df) == 0


def test_empty_dataframe_returns_two_empty_dataframes():
    """Empty input DataFrame returns two empty DataFrames without error."""
    df = pd.DataFrame(columns=["First", "Last", "_rejection_reason", "_is_valid", "_source_sheet"])
    clean_df, rejected_df = split_rows(df)
    assert isinstance(clean_df, pd.DataFrame)
    assert isinstance(rejected_df, pd.DataFrame)
    assert len(clean_df) == 0
    assert len(rejected_df) == 0


def test_multi_reason_rejection_preserved_exactly():
    """Row with combined rejection reason is routed correctly and reason preserved exactly."""
    reason = "Missing: First, Invalid Amount, Invalid State"
    df = make_df(make_rejected_row(_rejection_reason=reason))
    _, rejected_df = split_rows(df)
    assert len(rejected_df) == 1
    assert rejected_df.iloc[0]["rejection_reason"] == reason
