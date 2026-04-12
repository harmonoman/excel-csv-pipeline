"""
Tests for app/output/writer.py — T5-1 clean CSV writer + T5-2 rejected CSV writer.

Writer responsibilities:
- Write clean_df to a warehouse-ready CSV (T5-1)
- Write rejected_df to a rejected rows CSV (T5-2)
- Enforce exact column order
- No index column
- UTF-8 encoding, no BOM
- Deterministic output

Does NOT:
- Validate schema (T5-6)
- Generate filenames (T5-4)
- Log (T5-5)
- Return HTTP responses (T5-3)
"""
import pandas as pd
from pathlib import Path
from app.output.writer import write_clean_csv, write_rejected_csv
from app.processing.schema import OUTPUT_SCHEMA


def make_clean_df(**overrides) -> pd.DataFrame:
    """Return a valid single-row clean DataFrame matching OUTPUT_SCHEMA."""
    base = {
        "First": ["John"],
        "Last": ["Doe"],
        "Address1": ["123 Main St"],
        "City": ["Nashville"],
        "State": ["TN"],
        "Zip": ["37201"],
        "DonationDate": ["2024-01-01"],
        "DonationAmount": [100.0],
        "Client": ["Alpha Fund"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


# ---------------------------------------------------------------------------
# Column order enforcement
# ---------------------------------------------------------------------------

def test_column_order_matches_schema(tmp_path):
    """CSV header must exactly match OUTPUT_SCHEMA column order."""
    df = make_clean_df()[list(reversed(OUTPUT_SCHEMA))]  # shuffled input
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert list(result.columns) == OUTPUT_SCHEMA


def test_all_schema_columns_present(tmp_path):
    """All OUTPUT_SCHEMA columns are present in the written CSV."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert set(result.columns) == set(OUTPUT_SCHEMA)


# ---------------------------------------------------------------------------
# No index column
# ---------------------------------------------------------------------------

def test_no_index_column_in_csv(tmp_path):
    """CSV must not contain an unnamed index column."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert "Unnamed: 0" not in result.columns
    assert result.columns[0] == "First"


def test_first_column_is_first(tmp_path):
    """First column in the CSV is 'First'."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    raw = out.read_text(encoding="utf-8")
    first_line = raw.splitlines()[0]
    assert first_line.startswith("First")


# ---------------------------------------------------------------------------
# Deterministic output
# ---------------------------------------------------------------------------

def test_deterministic_output(tmp_path):
    """Same DataFrame written twice produces identical file contents."""
    df = make_clean_df()
    out1 = tmp_path / "clean_1.csv"
    out2 = tmp_path / "clean_2.csv"
    write_clean_csv(df.copy(), out1)
    write_clean_csv(df.copy(), out2)
    assert out1.read_bytes() == out2.read_bytes()


def test_row_order_preserved(tmp_path):
    """Row order from the input DataFrame is preserved in the output."""
    df = pd.DataFrame({
        "First": ["Alice", "Bob", "Carol"],
        "Last": ["A", "B", "C"],
        "Address1": ["1 A St", "2 B St", "3 C St"],
        "City": ["Nashville", "Memphis", "Knoxville"],
        "State": ["TN", "TN", "TN"],
        "Zip": ["37201", "38101", "37901"],
        "DonationDate": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "DonationAmount": [100.0, 200.0, 300.0],
        "Client": ["Alpha Fund", "Alpha Fund", "Alpha Fund"],
    })
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert list(result["First"]) == ["Alice", "Bob", "Carol"]


# ---------------------------------------------------------------------------
# Encoding
# ---------------------------------------------------------------------------

def test_utf8_encoding_no_bom(tmp_path):
    """File is UTF-8 encoded with no BOM."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    raw_bytes = out.read_bytes()
    # BOM is \xef\xbb\xbf — must not be present
    assert not raw_bytes.startswith(b'\xef\xbb\xbf')


def test_utf8_special_characters_preserved(tmp_path):
    """UTF-8 special characters in data are preserved correctly."""
    df = make_clean_df(First=["Zoë"], City=["Résumé City"])
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out, encoding="utf-8")
    assert result.iloc[0]["First"] == "Zoë"
    assert result.iloc[0]["City"] == "Résumé City"


# ---------------------------------------------------------------------------
# Return value
# ---------------------------------------------------------------------------

def test_returns_path_to_written_file(tmp_path):
    """write_clean_csv returns the Path of the written file."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    result = write_clean_csv(df, out)
    assert result == out


def test_file_exists_after_write(tmp_path):
    """File exists on disk after writing."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    assert out.exists()


# ---------------------------------------------------------------------------
# Empty DataFrame edge case
# ---------------------------------------------------------------------------

def test_empty_dataframe_writes_header_only(tmp_path):
    """Empty DataFrame produces a CSV with only the header row."""
    df = pd.DataFrame(columns=OUTPUT_SCHEMA)
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    assert out.exists()
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1  # header only
    assert lines[0] == ",".join(OUTPUT_SCHEMA)


def test_empty_dataframe_header_matches_schema(tmp_path):
    """Empty CSV header matches OUTPUT_SCHEMA exactly."""
    df = pd.DataFrame(columns=OUTPUT_SCHEMA)
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert list(result.columns) == OUTPUT_SCHEMA


# ---------------------------------------------------------------------------
# Multi-row data integrity
# ---------------------------------------------------------------------------

def test_multi_row_data_values_preserved(tmp_path):
    """Data values are not modified during CSV writing."""
    df = make_clean_df()
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out, dtype={"Zip": str})
    assert result.iloc[0]["First"] == "John"
    assert result.iloc[0]["DonationAmount"] == 100.0
    assert result.iloc[0]["Zip"] == "37201"


def test_leading_zero_zip_preserved(tmp_path):
    """ZIP codes with leading zeros are preserved as strings."""
    df = make_clean_df(Zip=["01234"])
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out, dtype={"Zip": str})
    assert result.iloc[0]["Zip"] == "01234"


# ===========================================================================
# T5-2 — Rejected CSV writer tests
# ===========================================================================

def make_rejected_df(**overrides) -> pd.DataFrame:
    """Return a single-row rejected DataFrame with all schema columns + rejection_reason."""
    base = {
        "First": ["Jane"],
        "Last": ["Smith"],
        "Address1": ["456 Oak Ave"],
        "City": ["Memphis"],
        "State": ["XX"],
        "Zip": ["1234"],
        "DonationDate": ["not a date"],
        "DonationAmount": [-50.0],
        "Client": ["Liberty PAC"],
        "rejection_reason": ["Invalid State, Invalid Zip, Invalid Date, Invalid Amount"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


# ---------------------------------------------------------------------------
# Column structure
# ---------------------------------------------------------------------------

def test_rejected_csv_contains_rejection_reason_column(tmp_path):
    """rejected CSV must contain a rejection_reason column."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert "rejection_reason" in result.columns


def test_rejected_csv_rejection_reason_is_last_column(tmp_path):
    """rejection_reason must be the last column in the rejected CSV."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert result.columns[-1] == "rejection_reason"


def test_rejected_csv_contains_schema_columns(tmp_path):
    """Rejected CSV contains all OUTPUT_SCHEMA columns."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    for col in OUTPUT_SCHEMA:
        assert col in result.columns, f"Missing schema column: {col}"


def test_rejected_csv_no_index_column(tmp_path):
    """Rejected CSV must not contain an unnamed index column."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert "Unnamed: 0" not in result.columns


# ---------------------------------------------------------------------------
# Data integrity
# ---------------------------------------------------------------------------

def test_rejected_csv_rejection_reason_preserved(tmp_path):
    """Rejection reason text is preserved exactly in output."""
    reason = "Missing: Last, Invalid State"
    df = make_rejected_df(rejection_reason=[reason])
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert result.iloc[0]["rejection_reason"] == reason


def test_rejected_csv_data_values_preserved(tmp_path):
    """Data values from the rejected row are preserved unchanged."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert result.iloc[0]["First"] == "Jane"
    assert result.iloc[0]["Client"] == "Liberty PAC"


def test_rejected_csv_row_order_preserved(tmp_path):
    """Row order from the input DataFrame is preserved in rejected CSV."""
    df = pd.DataFrame({
        "First": ["Alice", "Bob"],
        "Last": ["A", "B"],
        "Address1": ["1 St", "2 St"],
        "City": ["City1", "City2"],
        "State": ["XX", "YY"],
        "Zip": ["1234", "5678"],
        "DonationDate": ["bad", "worse"],
        "DonationAmount": [0, -1],
        "Client": ["Client A", "Client B"],
        "rejection_reason": ["Invalid State", "Invalid Amount"],
    })
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert list(result["First"]) == ["Alice", "Bob"]


# ---------------------------------------------------------------------------
# Encoding + file
# ---------------------------------------------------------------------------

def test_rejected_csv_utf8_no_bom(tmp_path):
    """Rejected CSV is UTF-8 with no BOM."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    raw_bytes = out.read_bytes()
    assert not raw_bytes.startswith(b'\xef\xbb\xbf')


def test_rejected_csv_file_exists(tmp_path):
    """File exists on disk after writing."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    assert out.exists()


def test_rejected_csv_returns_path(tmp_path):
    """write_rejected_csv returns the Path of the written file."""
    df = make_rejected_df()
    out = tmp_path / "rejected.csv"
    result = write_rejected_csv(df, out)
    assert result == out


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_rejected_csv_deterministic(tmp_path):
    """Same rejected DataFrame written twice produces identical file contents."""
    df = make_rejected_df()
    out1 = tmp_path / "rejected_1.csv"
    out2 = tmp_path / "rejected_2.csv"
    write_rejected_csv(df.copy(), out1)
    write_rejected_csv(df.copy(), out2)
    assert out1.read_bytes() == out2.read_bytes()


# ---------------------------------------------------------------------------
# Empty DataFrame edge case
# ---------------------------------------------------------------------------

def test_rejected_empty_dataframe_writes_header_only(tmp_path):
    """Empty rejected DataFrame writes header row only."""
    df = pd.DataFrame(columns=OUTPUT_SCHEMA + ["rejection_reason"])
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    assert out.exists()
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1  # header only
    assert "rejection_reason" in lines[0]


# ---------------------------------------------------------------------------
# Additional tests from QA review
# ---------------------------------------------------------------------------

def test_clean_csv_row_count_conserved(tmp_path):
    """Row count is preserved — write_clean_csv never drops rows."""
    rows = [make_clean_df().iloc[0].to_dict() for _ in range(5)]
    df = pd.DataFrame(rows)
    out = tmp_path / "clean.csv"
    write_clean_csv(df, out)
    result = pd.read_csv(out)
    assert len(result) == len(df)


def test_rejected_csv_row_count_conserved(tmp_path):
    """Row count is preserved — write_rejected_csv never drops rows."""
    rows = [make_rejected_df().iloc[0].to_dict() for _ in range(5)]
    df = pd.DataFrame(rows)
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)
    result = pd.read_csv(out)
    assert len(result) == len(df)


def test_rejected_csv_missing_rejection_reason_omits_column(tmp_path):
    """
    If rejection_reason column is absent (upstream contract violation),
    write_rejected_csv omits it silently rather than crashing.
    Documents the known silent failure mode.
    """
    df = make_rejected_df().drop(columns=["rejection_reason"])
    out = tmp_path / "rejected.csv"
    write_rejected_csv(df, out)  # must not raise
    result = pd.read_csv(out)
    assert "rejection_reason" not in result.columns
    assert out.exists()
