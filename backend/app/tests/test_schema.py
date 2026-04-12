"""
Tests for app/processing/schema.py — T5-6 final schema enforcement.

Schema enforcement responsibilities:
- Verify ALL required columns are present — raise PipelineError if any missing
- Drop any extra columns not in OUTPUT_SCHEMA
- Enforce exact column order
- Never mutate input DataFrame
- Pass empty DataFrames with correct schema structure

Does NOT:
- Normalize column names (mapping stage responsibility)
- Fill missing values
- Validate data content (T4 responsibility)
"""
import pandas as pd
import pytest
from app.processing.schema import enforce_schema, OUTPUT_SCHEMA
from app.processing.errors import PipelineError


def make_valid_df(**overrides) -> pd.DataFrame:
    """Return a single-row DataFrame with all required schema columns."""
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
# Happy path
# ---------------------------------------------------------------------------

def test_valid_df_passes_schema_enforcement():
    """DataFrame with all required columns passes without error."""
    df = make_valid_df()
    result = enforce_schema(df)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == OUTPUT_SCHEMA


def test_column_order_enforced():
    """Output columns are in exact OUTPUT_SCHEMA order regardless of input order."""
    # Build df with columns in reverse order
    df = make_valid_df()[list(reversed(OUTPUT_SCHEMA))]
    result = enforce_schema(df)
    assert list(result.columns) == OUTPUT_SCHEMA


def test_data_values_preserved():
    """Data values are not modified by schema enforcement."""
    df = make_valid_df()
    result = enforce_schema(df)
    assert result.iloc[0]["First"] == "John"
    assert result.iloc[0]["DonationAmount"] == 100.0
    assert result.iloc[0]["Client"] == "Alpha Fund"


def test_does_not_mutate_input():
    """enforce_schema must not modify the input DataFrame."""
    df = make_valid_df()
    original_columns = list(df.columns)
    enforce_schema(df)
    assert list(df.columns) == original_columns


# ---------------------------------------------------------------------------
# Missing column → hard failure
# ---------------------------------------------------------------------------

def test_missing_column_raises_pipeline_error():
    """DataFrame missing a required column raises PipelineError."""
    df = make_valid_df().drop(columns=["Address1"])
    with pytest.raises(PipelineError) as exc_info:
        enforce_schema(df)
    assert exc_info.value.stage == "schema"


def test_missing_column_error_names_the_column():
    """PipelineError message identifies which column is missing."""
    df = make_valid_df().drop(columns=["Address1"])
    with pytest.raises(PipelineError) as exc_info:
        enforce_schema(df)
    assert "Address1" in exc_info.value.error_message


def test_missing_column_error_type_is_missing_column():
    """PipelineError error_type is MissingColumn."""
    df = make_valid_df().drop(columns=["DonationAmount"])
    with pytest.raises(PipelineError) as exc_info:
        enforce_schema(df)
    assert exc_info.value.error_type == "MissingColumn"


def test_missing_first_column_raises():
    df = make_valid_df().drop(columns=["First"])
    with pytest.raises(PipelineError) as exc_info:
        enforce_schema(df)
    assert "First" in exc_info.value.error_message


def test_missing_client_column_raises():
    """Client column is required — missing it must raise."""
    df = make_valid_df().drop(columns=["Client"])
    with pytest.raises(PipelineError) as exc_info:
        enforce_schema(df)
    assert "Client" in exc_info.value.error_message


def test_multiple_missing_columns_raises_on_first():
    """Multiple missing columns — raises on the first one found."""
    df = make_valid_df().drop(columns=["First", "Last", "City"])
    with pytest.raises(PipelineError):
        enforce_schema(df)


# ---------------------------------------------------------------------------
# Extra columns → removed
# ---------------------------------------------------------------------------

def test_extra_columns_are_dropped():
    """Columns not in OUTPUT_SCHEMA are silently dropped."""
    df = make_valid_df()
    df["_source_sheet"] = "Alpha Fund"
    df["random_extra_col"] = "should be gone"
    result = enforce_schema(df)
    assert "_source_sheet" not in result.columns
    assert "random_extra_col" not in result.columns


def test_only_schema_columns_remain():
    """Output contains exactly and only the OUTPUT_SCHEMA columns."""
    df = make_valid_df()
    df["extra_1"] = "x"
    df["extra_2"] = "y"
    result = enforce_schema(df)
    assert set(result.columns) == set(OUTPUT_SCHEMA)


# ---------------------------------------------------------------------------
# Empty DataFrame
# ---------------------------------------------------------------------------

def test_empty_df_with_correct_columns_passes():
    """Empty DataFrame with correct columns passes schema enforcement."""
    df = pd.DataFrame(columns=OUTPUT_SCHEMA)
    result = enforce_schema(df)
    assert list(result.columns) == OUTPUT_SCHEMA
    assert len(result) == 0


def test_empty_df_missing_columns_still_returns_correct_schema():
    """
    Empty DataFrame (zero rows) passes even if columns are missing or wrong.
    An empty clean_df is a valid result — all rows may have been rejected,
    or the workbook had no parseable data. Schema is enforced on structure only.
    Returns an empty DataFrame with the correct OUTPUT_SCHEMA columns.
    """
    df = pd.DataFrame(columns=["First", "Last"])  # missing most columns
    result = enforce_schema(df)
    assert list(result.columns) == OUTPUT_SCHEMA
    assert len(result) == 0


# ---------------------------------------------------------------------------
# Case sensitivity
# ---------------------------------------------------------------------------

def test_lowercase_column_names_rejected():
    """Lowercase column names are NOT normalized — schema enforcement fails."""
    df = pd.DataFrame({col.lower(): ["value"] for col in OUTPUT_SCHEMA})
    with pytest.raises(PipelineError):
        enforce_schema(df)


def test_mixed_case_column_names_rejected():
    """Mixed case column names are NOT normalized — schema enforcement fails."""
    df = make_valid_df().rename(columns={"First": "first", "Last": "LAST"})
    with pytest.raises(PipelineError):
        enforce_schema(df)


# ---------------------------------------------------------------------------
# Multi-row dataset
# ---------------------------------------------------------------------------

def test_multi_row_df_passes():
    """Multi-row DataFrame with correct schema passes."""
    rows = [make_valid_df().iloc[0].to_dict() for _ in range(5)]
    df = pd.DataFrame(rows)
    result = enforce_schema(df)
    assert len(result) == 5
    assert list(result.columns) == OUTPUT_SCHEMA


def test_schema_enforcement_is_deterministic():
    """Same input always produces same schema output."""
    df = make_valid_df()
    df["extra"] = "x"
    result_1 = enforce_schema(df.copy())
    result_2 = enforce_schema(df.copy())
    pd.testing.assert_frame_equal(result_1, result_2)


# ---------------------------------------------------------------------------
# Additional tests from QA review
# ---------------------------------------------------------------------------

def test_row_count_is_conserved():
    """enforce_schema never drops rows — output row count equals input."""
    rows = [make_valid_df().iloc[0].to_dict() for _ in range(10)]
    df = pd.DataFrame(rows)
    result = enforce_schema(df)
    assert len(result) == len(df)


def test_non_contiguous_index_is_reset():
    """
    If clean_df arrives with a non-contiguous index (e.g. rows 0, 2, 4 after
    splitting), enforce_schema resets it to 0-based. Downstream CSV writers
    must not receive gaps in the index.
    """
    df = make_valid_df()
    # Simulate non-contiguous index from splitter
    df.index = [5]
    result = enforce_schema(df)
    assert list(result.index) == [0]
