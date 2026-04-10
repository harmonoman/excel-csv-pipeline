"""
Tests for app/processing/normalizer.py — data normalization stage.
 
Normalization responsibilities (ONLY):
- Strip whitespace from all string fields
- Title-case First, Last, City
- Uppercase State
- Cast DonationAmount to float
- Parse DonationDate to ISO 8601 string (YYYY-MM-DD)
- Preserve ZIP as string with leading zeros intact
 
Does NOT:
- Validate data correctness
- Reject rows
- Enforce required fields
- Add or remove columns
"""
import datetime
import pandas as pd
from app.processing.normalizer import normalize
 
 
def make_df(data: dict) -> pd.DataFrame:
    """Helper: build a DataFrame from a dict of column→values."""
    return pd.DataFrame(data)
 
 
# ---------------------------------------------------------------------------
# Whitespace stripping
# ---------------------------------------------------------------------------
 
def test_whitespace_stripped_from_string_fields():
    """Leading/trailing whitespace is stripped from all string fields."""
    df = make_df({
        "First": ["  John  "],
        "Last": ["  Doe  "],
        "City": ["  Nashville  "],
        "State": ["  TN  "],
        "Zip": ["  37201  "],
        "_source_sheet": ["Alpha Fund"],
    })
    result = normalize(df)
    assert result.iloc[0]["First"] == "John"
    assert result.iloc[0]["Last"] == "Doe"
    assert result.iloc[0]["City"] == "Nashville"
    assert result.iloc[0]["State"] == "TN"
    assert result.iloc[0]["Zip"] == "37201"
 
 
def test_null_value_in_name_field_does_not_crash():
    """Null/NA values in string fields are handled safely without error."""
    df = make_df({
        "First": [None, "Jane"],
        "Last": ["Doe", None],
        "_source_sheet": ["Alpha Fund", "Alpha Fund"],
    })
    result = normalize(df)
    assert len(result) == 2
    assert pd.isna(result.iloc[0]["First"])
    assert result.iloc[1]["First"] == "Jane"
    assert pd.isna(result.iloc[1]["Last"])
 
 
# ---------------------------------------------------------------------------
# Title case
# ---------------------------------------------------------------------------
 
def test_first_name_title_cased():
    """First is converted to title case."""
    df = make_df({"First": ["john"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["First"] == "John"
 
 
def test_last_name_title_cased():
    """Last is converted to title case."""
    df = make_df({"Last": ["doe"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["Last"] == "Doe"
 
 
def test_city_title_cased():
    """City is converted to title case."""
    df = make_df({"City": ["new york"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["City"] == "New York"
 
 
def test_multi_word_city_title_cased():
    """Multi-word city names are fully title-cased."""
    df = make_df({"City": ["los angeles"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["City"] == "Los Angeles"
 
 
# ---------------------------------------------------------------------------
# State uppercase
# ---------------------------------------------------------------------------
 
def test_state_uppercased():
    """State is converted to uppercase."""
    df = make_df({"State": ["ny"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["State"] == "NY"
 
 
def test_state_already_uppercase_unchanged():
    """State already in uppercase remains unchanged."""
    df = make_df({"State": ["TN"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["State"] == "TN"
 
 
# ---------------------------------------------------------------------------
# DonationAmount casting
# ---------------------------------------------------------------------------
 
def test_donation_amount_string_cast_to_float():
    """DonationAmount as string is cast to float."""
    df = make_df({"DonationAmount": ["100"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationAmount"] == 100.0
    assert isinstance(result.iloc[0]["DonationAmount"], float)
 
 
def test_donation_amount_integer_cast_to_float():
    """DonationAmount as integer is cast to float."""
    df = make_df({"DonationAmount": [100], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationAmount"] == 100.0
    assert isinstance(result.iloc[0]["DonationAmount"], float)
 
 
def test_donation_amount_decimal_string_cast_to_float():
    """DonationAmount as decimal string with comma is cast to float."""
    df = make_df({"DonationAmount": ["1,205.67"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationAmount"] == 1205.67
 
 
def test_donation_amount_invalid_value_becomes_nan():
    """
    Invalid DonationAmount (non-numeric) becomes NaN after cast.
    Rejection is T4's responsibility — normalizer must not drop the row.
    """
    df = make_df({"DonationAmount": ["abc"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert pd.isna(result.iloc[0]["DonationAmount"])
    assert len(result) == 1
 
 
# ---------------------------------------------------------------------------
# DonationDate parsing
# ---------------------------------------------------------------------------
 
def test_donation_date_iso_format_parsed():
    """ISO format date (YYYY-MM-DD) is parsed correctly."""
    df = make_df({"DonationDate": ["2024-01-15"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationDate"] == "2024-01-15"
 
 
def test_donation_date_us_format_parsed():
    """US format date (MM/DD/YYYY) is parsed correctly."""
    df = make_df({"DonationDate": ["01/15/2024"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationDate"] == "2024-01-15"
 
 
def test_donation_date_natural_language_parsed():
    """Natural language date ('March 16, 2025') is parsed correctly."""
    df = make_df({"DonationDate": ["March 16, 2025"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationDate"] == "2025-03-16"
 
 
def test_donation_date_excel_serial_parsed():
    """Excel date serial (integer) is parsed correctly."""
    # Excel serial 45353 = 2024-03-02 (verified against 1899-12-30 epoch)
    df = make_df({"DonationDate": [45353], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationDate"] == "2024-03-02"
 
 
def test_donation_date_python_datetime_object_parsed():
    """
    Python datetime object (returned by openpyxl data_only mode) is
    parsed correctly without error.
    """
    dt = datetime.datetime(2024, 3, 15)
    df = make_df({"DonationDate": [dt], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["DonationDate"] == "2024-03-15"
 
 
def test_donation_date_invalid_value_becomes_nan():
    """
    Unparseable date becomes NaN. Row must not be dropped.
    Rejection is T4's responsibility.
    """
    df = make_df({"DonationDate": ["not a date"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert pd.isna(result.iloc[0]["DonationDate"])
    assert len(result) == 1
 
 
# ---------------------------------------------------------------------------
# ZIP code preservation (critical)
# ---------------------------------------------------------------------------
 
def test_zip_leading_zero_preserved():
    """ZIP code with leading zero must remain a string with zero intact."""
    df = make_df({"Zip": ["01234"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["Zip"] == "01234"
    assert isinstance(result.iloc[0]["Zip"], str)
 
 
def test_zip_integer_padded_to_5_digits():
    """
    ZIP code stored as integer (e.g. Excel dropped the leading zero)
    is zero-padded back to 5 digits.
    """
    df = make_df({"Zip": [1234], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["Zip"] == "01234"
    assert isinstance(result.iloc[0]["Zip"], str)
 
 
def test_zip_standard_5_digit_preserved():
    """Standard 5-digit ZIP is preserved as string."""
    df = make_df({"Zip": ["37201"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["Zip"] == "37201"
    assert isinstance(result.iloc[0]["Zip"], str)
 
 
# ---------------------------------------------------------------------------
# Missing column handling
# ---------------------------------------------------------------------------
 
def test_missing_column_does_not_raise():
    """Normalization skips missing columns silently without error."""
    df = make_df({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert result.iloc[0]["First"] == "John"
    assert "City" not in result.columns
 
 
def test_all_missing_columns_does_not_raise():
    """DataFrame with only _source_sheet normalizes without error."""
    df = make_df({"_source_sheet": ["Alpha Fund"]})
    result = normalize(df)
    assert "_source_sheet" in result.columns
    assert len(result) == 1
 
 
def test_no_columns_added_by_normalizer():
    """Normalizer must not add any new columns to the DataFrame."""
    df = make_df({
        "First": ["John"],
        "Last": ["Doe"],
        "_source_sheet": ["Alpha Fund"],
    })
    input_columns = set(df.columns)
    result = normalize(df)
    assert set(result.columns) == input_columns
 
 
def test_source_sheet_untouched():
    """_source_sheet value is never modified by normalizer."""
    df = make_df({"_source_sheet": ["  Alpha Fund  "], "First": ["John"]})
    result = normalize(df)
    # _source_sheet must not be stripped or title-cased
    assert result.iloc[0]["_source_sheet"] == "  Alpha Fund  "
 
 
# ---------------------------------------------------------------------------
# Multiple rows
# ---------------------------------------------------------------------------
 
def test_normalization_applied_to_all_rows():
    """Normalization applies consistently to every row in the DataFrame."""
    df = make_df({
        "First": ["john", "JANE", "  alice  "],
        "State": ["ny", "ca", "tn"],
        "_source_sheet": ["Alpha Fund", "Alpha Fund", "Alpha Fund"],
    })
    result = normalize(df)
    assert list(result["First"]) == ["John", "Jane", "Alice"]
    assert list(result["State"]) == ["NY", "CA", "TN"]
 