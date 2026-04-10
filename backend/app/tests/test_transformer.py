"""
Tests for app/processing/transformer.py — column mapping engine.
 
Mapping stage responsibilities (ONLY):
- Map source column names to canonical schema using mapping.json aliases
- Drop unmapped columns
- Preserve _source_sheet
- Tolerate missing canonical fields (validation is T4's job)
 
Does NOT:
- Validate data completeness
- Normalize values
- Inject Client field
"""
import pandas as pd
from app.processing.transformer import map_columns
 
 
# --- Shared config ---
MAPPING_CONFIG = {
    "header_scan_rows": 20,
    "fields": {
        "First": ["first_name", "fname", "first"],
        "Last": ["lastname", "last_name", "lname", "last"],
        "Address1": ["address1", "address", "addr"],
        "City": ["city"],
        "State": ["st", "state", "state_code"],
        "Zip": ["zip", "zip_code", "zipcode"],
        "DonationDate": ["giftdate", "gift_date", "donationdate", "donation_date", "date"],
        "DonationAmount": ["amount", "donationamount", "donation_amount", "gift_amount"],
    },
}
 
 
def make_df(data: dict) -> pd.DataFrame:
    """Helper: build a DataFrame from a dict of column→values."""
    return pd.DataFrame(data)
 
 
# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------
 
def test_exact_alias_match():
    """Source column exactly matching an alias maps to canonical name."""
    df = make_df({"first": ["John"], "last": ["Doe"], "_source_sheet": ["Alpha Fund"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert "Last" in result.columns
    assert result.iloc[0]["First"] == "John"
 
 
def test_alias_match():
    """Non-exact alias maps to canonical name."""
    df = make_df({"fname": ["John"], "lname": ["Doe"], "_source_sheet": ["Alpha Fund"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert "Last" in result.columns
    assert result.iloc[0]["First"] == "John"
 
 
def test_case_insensitive_match():
    """Mapping is case-insensitive — input columns already normalized by parser
    but alias lookup must also be case-insensitive for safety."""
    df = make_df({"FNAME": ["John"], "LNAME": ["Doe"], "_source_sheet": ["Alpha Fund"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert "Last" in result.columns
 
 
def test_unknown_column_dropped():
    """Columns with no alias match are silently dropped."""
    df = make_df({
        "first": ["John"],
        "random_col": ["should be dropped"],
        "another_unknown": ["also dropped"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    assert "random_col" not in result.columns
    assert "another_unknown" not in result.columns
    assert "First" in result.columns
 
 
def test_missing_canonical_field_tolerated():
    """Missing canonical field does not raise — simply absent from output."""
    df = make_df({"first": ["John"], "_source_sheet": ["Alpha Fund"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert "Last" not in result.columns
 
 
def test_all_canonical_fields_mapped():
    """All canonical fields map correctly when all aliases are present."""
    df = make_df({
        "first": ["John"],
        "last": ["Doe"],
        "address1": ["123 Main St"],
        "city": ["Nashville"],
        "st": ["TN"],
        "zip": ["37201"],
        "giftdate": ["2024-01-01"],
        "amount": ["100.00"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    for field in ["First", "Last", "Address1", "City", "State", "Zip", "DonationDate", "DonationAmount"]:
        assert field in result.columns, f"Expected canonical field '{field}' missing from output"
 
 
def test_source_sheet_preserved():
    """_source_sheet column is always preserved regardless of mapping."""
    df = make_df({"first": ["John"], "_source_sheet": ["Heritage Trust"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "_source_sheet" in result.columns
    assert result.iloc[0]["_source_sheet"] == "Heritage Trust"
 
 
def test_duplicate_aliases_first_occurrence_wins():
    """
    If multiple source columns map to the same canonical field,
    the first occurrence (left-to-right) wins. No error raised.
    """
    df = make_df({
        "first_name": ["John"],    # maps to First
        "fname": ["Jane"],         # also maps to First — should be dropped
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert list(result.columns).count("First") == 1
    assert result.iloc[0]["First"] == "John"
 
 
def test_output_contains_only_canonical_and_source_sheet():
    """Output must contain only canonical fields + _source_sheet. Nothing else."""
    df = make_df({
        "first": ["John"],
        "last": ["Doe"],
        "random_extra": ["drop me"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    allowed = {"First", "Last", "_source_sheet"}
    assert set(result.columns).issubset(allowed)
 
 
def test_data_values_unchanged():
    """Mapping renames columns only — data values must not be modified."""
    df = make_df({
        "first": ["  John  "],   # value has whitespace — must NOT be stripped here
        "amount": ["100.00"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    assert result.iloc[0]["First"] == "  John  "
    assert result.iloc[0]["DonationAmount"] == "100.00"
 
 
def test_empty_dataframe_columns_still_renamed():
    """
    Empty DataFrame (zero rows) with valid columns must still have
    columns renamed to canonical names. Downstream stages always
    expect canonical column names regardless of row count.
    """
    df = pd.DataFrame(columns=["first", "last", "_source_sheet"])
    result = map_columns(df, MAPPING_CONFIG)
    assert isinstance(result, pd.DataFrame)
    assert result.empty
    # Columns must be renamed even with zero rows
    assert "First" in result.columns
    assert "Last" in result.columns
    assert "_source_sheet" in result.columns
    assert "first" not in result.columns
    assert "last" not in result.columns
 
 
def test_only_unmapped_columns_returns_source_sheet_only():
    """
    DataFrame with only unmapped columns (plus _source_sheet) returns
    a DataFrame containing only _source_sheet — no canonical fields.
    """
    df = make_df({
        "random_col_1": ["x"],
        "random_col_2": ["y"],
        "_source_sheet": ["Alpha Fund"],
    })
    result = map_columns(df, MAPPING_CONFIG)
    assert list(result.columns) == ["_source_sheet"]
    assert result.iloc[0]["_source_sheet"] == "Alpha Fund"
 
 
def test_source_sheet_absent_from_input():
    """
    If _source_sheet is absent from input (defensive case),
    mapping proceeds without error and _source_sheet is simply not in output.
    """
    df = make_df({"first": ["John"], "last": ["Doe"]})
    result = map_columns(df, MAPPING_CONFIG)
    assert "First" in result.columns
    assert "Last" in result.columns
    assert "_source_sheet" not in result.columns
 
 
def test_mapping_is_deterministic():
    """Same input always produces same output — mapping is deterministic."""
    df = make_df({
        "fname": ["John"],
        "lname": ["Doe"],
        "gift_amount": ["100.00"],
        "_source_sheet": ["Alpha Fund"],
    })
    result_1 = map_columns(df.copy(), MAPPING_CONFIG)
    result_2 = map_columns(df.copy(), MAPPING_CONFIG)
    pd.testing.assert_frame_equal(result_1, result_2)
 