"""\nTests for app/processing/validator.py — T4-1 and T4-2 validators.\n\nT4-1 responsibilities:\n- Detect null, empty string, and whitespace-only values in required fields\n- Add _is_valid bool column\n- Add _rejection_reason string column\n- Never modify data values\n- Never drop rows\n\nT4-2 responsibilities:\n- Validate DonationAmount: numeric and > 0\n- Validate DonationDate: parseable as a valid date\n- Validate State: valid 2-letter US abbreviation\n- Validate Zip: exactly 5 digits\n\nDoes NOT:\n- Split into clean/rejected DataFrames (T4-3)\n- Enforce schema column order (T5-6)\n"""
import pandas as pd
from app.processing.validator import validate_rows

REQUIRED_FIELDS = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]


def make_valid_row(**overrides) -> dict:
    """Return a complete valid row dict, with optional field overrides."""
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
    }
    base.update(overrides)
    return base


def make_df(*rows) -> pd.DataFrame:
    """Build a DataFrame from one or more row dicts."""
    return pd.DataFrame(list(rows))


# ---------------------------------------------------------------------------
# Output contract tests
# ---------------------------------------------------------------------------

def test_validate_rows_adds_is_valid_column():
    """validate_rows always adds _is_valid column."""
    df = make_df(make_valid_row())
    result = validate_rows(df)
    assert "_is_valid" in result.columns


def test_validate_rows_adds_rejection_reason_column():
    """validate_rows always adds _rejection_reason column."""
    df = make_df(make_valid_row())
    result = validate_rows(df)
    assert "_rejection_reason" in result.columns


def test_validate_rows_does_not_modify_input():
    """validate_rows must not mutate the input DataFrame."""
    df = make_df(make_valid_row())
    original_columns = list(df.columns)
    validate_rows(df)
    assert list(df.columns) == original_columns


def test_validate_rows_preserves_row_count():
    """Row count must be identical before and after validation."""
    df = make_df(make_valid_row(), make_valid_row(First=None), make_valid_row(Last=""))
    result = validate_rows(df)
    assert len(result) == len(df)


def test_validate_rows_does_not_modify_data_values():
    """Values in existing columns must not be changed."""
    df = make_df(make_valid_row())
    result = validate_rows(df)
    assert result.iloc[0]["First"] == "John"
    assert result.iloc[0]["DonationAmount"] == 100.0


# ---------------------------------------------------------------------------
# Valid row tests
# ---------------------------------------------------------------------------

def test_complete_row_is_valid():
    """Row with all required fields present is marked valid."""
    df = make_df(make_valid_row())
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == True


def test_complete_row_has_empty_rejection_reason():
    """Valid row has empty string rejection reason."""
    df = make_df(make_valid_row())
    result = validate_rows(df)
    assert result.iloc[0]["_rejection_reason"] == ""


# ---------------------------------------------------------------------------
# Single missing field tests
# ---------------------------------------------------------------------------

def test_null_first_rejected():
    """Row with null First is rejected with correct reason."""
    df = make_df(make_valid_row(First=None))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: First" in result.iloc[0]["_rejection_reason"]


def test_null_last_rejected():
    """Row with null Last is rejected."""
    df = make_df(make_valid_row(Last=None))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: Last" in result.iloc[0]["_rejection_reason"]


def test_null_donation_amount_rejected():
    """Row with null DonationAmount is rejected."""
    df = make_df(make_valid_row(DonationAmount=None))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: DonationAmount" in result.iloc[0]["_rejection_reason"]


def test_null_client_rejected():
    """Row with null Client is rejected."""
    df = make_df(make_valid_row(Client=None))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: Client" in result.iloc[0]["_rejection_reason"]


# ---------------------------------------------------------------------------
# Whitespace handling tests
# ---------------------------------------------------------------------------

def test_empty_string_treated_as_missing():
    """Empty string is treated as missing."""
    df = make_df(make_valid_row(First=""))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: First" in result.iloc[0]["_rejection_reason"]


def test_whitespace_only_string_treated_as_missing():
    """Whitespace-only string is treated as missing."""
    df = make_df(make_valid_row(First="   "))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: First" in result.iloc[0]["_rejection_reason"]


def test_whitespace_only_city_treated_as_missing():
    """Whitespace-only City is treated as missing."""
    df = make_df(make_valid_row(City="\t\n"))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: City" in result.iloc[0]["_rejection_reason"]


def test_pandas_na_treated_as_missing():
    """pd.NA is treated as missing."""
    df = make_df(make_valid_row(Zip=pd.NA))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: Zip" in result.iloc[0]["_rejection_reason"]


# ---------------------------------------------------------------------------
# Multiple missing fields tests
# ---------------------------------------------------------------------------

def test_multiple_missing_fields_combined_reason():
    """Row missing First and Last has combined rejection reason."""
    df = make_df(make_valid_row(First=None, Last=None))
    result = validate_rows(df)
    reason = result.iloc[0]["_rejection_reason"]
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: First" in reason
    assert "Missing: Last" in reason


def test_multiple_missing_fields_comma_separated():
    """Multiple missing fields are comma-separated in rejection reason."""
    df = make_df(make_valid_row(First=None, Last=None))
    result = validate_rows(df)
    reason = result.iloc[0]["_rejection_reason"]
    assert "," in reason


def test_completely_empty_row_rejected():
    """Row with all required fields null is rejected with all reasons."""
    empty = {field: None for field in REQUIRED_FIELDS}
    df = make_df(empty)
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    reason = result.iloc[0]["_rejection_reason"]
    for field in REQUIRED_FIELDS:
        assert field in reason


def test_all_whitespace_row_rejected():
    """Row with all whitespace values is rejected."""
    whitespace = {field: "   " for field in REQUIRED_FIELDS}
    df = make_df(whitespace)
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False


# ---------------------------------------------------------------------------
# Mixed dataset tests
# ---------------------------------------------------------------------------

def test_mixed_dataset_row_count_conserved():
    """clean + rejected row counts equal input row count."""
    df = make_df(
        make_valid_row(),
        make_valid_row(First=None),
        make_valid_row(),
        make_valid_row(Last="", City=None),
    )
    result = validate_rows(df)
    valid_count = result["_is_valid"].sum()
    invalid_count = (~result["_is_valid"]).sum()
    assert valid_count + invalid_count == len(df)


def test_mixed_dataset_correct_classification():
    """Valid and invalid rows are classified correctly."""
    df = make_df(
        make_valid_row(),                          # valid
        make_valid_row(First=None),                # invalid
        make_valid_row(),                          # valid
        make_valid_row(Last="", State="   "),      # invalid
    )
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == True
    assert result.iloc[1]["_is_valid"] == False
    assert result.iloc[2]["_is_valid"] == True
    assert result.iloc[3]["_is_valid"] == False


def test_no_valid_rows_leak_into_rejected():
    """No valid row has a non-empty rejection reason."""
    df = make_df(
        make_valid_row(),
        make_valid_row(First=None),
        make_valid_row(),
    )
    result = validate_rows(df)
    valid_rows = result[result["_is_valid"] == True]
    assert (valid_rows["_rejection_reason"] == "").all()


def test_no_invalid_rows_leak_into_valid():
    """No invalid row is marked _is_valid = True."""
    df = make_df(
        make_valid_row(First=None),
        make_valid_row(Last=""),
        make_valid_row(),
    )
    result = validate_rows(df)
    invalid_rows = result[result["_is_valid"] == False]
    assert len(invalid_rows) == 2


# ---------------------------------------------------------------------------
# Determinism tests
# ---------------------------------------------------------------------------

def test_validation_is_deterministic():
    """Same input always produces same validation output."""
    df = make_df(
        make_valid_row(),
        make_valid_row(First=None),
        make_valid_row(Last="   "),
    )
    result_1 = validate_rows(df.copy())
    result_2 = validate_rows(df.copy())
    pd.testing.assert_frame_equal(result_1, result_2)


# ---------------------------------------------------------------------------
# Rejection reason ordering tests
# ---------------------------------------------------------------------------

def test_rejection_reason_field_order_matches_required_fields():
    """
    Rejection reasons appear in REQUIRED_FIELDS order, not arbitrary order.
    This ensures deterministic, human-readable rejection messages.
    """
    df = make_df(make_valid_row(Last=None, First=None))
    result = validate_rows(df)
    reason = result.iloc[0]["_rejection_reason"]
    first_pos = reason.index("First")
    last_pos = reason.index("Last")
    assert first_pos < last_pos


# ---------------------------------------------------------------------------
# Additional edge case tests
# ---------------------------------------------------------------------------

def test_numpy_nan_in_numeric_field_rejected():
    """
    numpy float NaN in a numeric column (e.g. DonationAmount after normalization)
    is correctly detected as missing. pd.isna() handles numpy NaN the same as
    other null types.
    """
    import numpy as np
    df = make_df(make_valid_row(DonationAmount=float("nan")))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Missing: DonationAmount" in result.iloc[0]["_rejection_reason"]


def test_empty_dataframe_returns_correct_structure():
    """
    Empty DataFrame (zero rows) returns a DataFrame with _is_valid and
    _rejection_reason columns — same structure as a non-empty result.
    Tested here directly in addition to the pipeline-level empty test.
    """
    df = pd.DataFrame(columns=["First", "Last", "Client"])
    result = validate_rows(df)
    assert "_is_valid" in result.columns
    assert "_rejection_reason" in result.columns
    assert len(result) == 0


# ---------------------------------------------------------------------------
# T4-2 additional edge cases identified in QA review
# ---------------------------------------------------------------------------

def test_t42_does_not_modify_data_values():
    """T4-2 validation only adds _is_valid and _rejection_reason — no data modified."""
    df = make_df(make_valid_row(DonationAmount=100.0, State="TN", Zip="37201"))
    result = validate_rows(df)
    assert result.iloc[0]["DonationAmount"] == 100.0
    assert result.iloc[0]["State"] == "TN"
    assert result.iloc[0]["Zip"] == "37201"


def test_amount_infinity_rejected():
    """float('inf') is not a valid donation amount and must be rejected."""
    df = make_df(make_valid_row(DonationAmount=float("inf")))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Invalid Amount" in result.iloc[0]["_rejection_reason"]


def test_state_whitespace_trimmed_then_accepted():
    """State with surrounding whitespace is trimmed before validation — 'TN' is valid."""
    df = make_df(make_valid_row(State="  TN  "))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == True
    assert "Invalid State" not in result.iloc[0]["_rejection_reason"]


def test_zip_stored_as_float_string_rejected():
    """
    ZIP '37201.0' (float stringified) fails isdigit() and is correctly rejected.
    Normalizer converts ZIP integers to zero-padded strings, but this confirms
    the validator handles any residual float-string ZIPs defensively.
    """
    df = make_df(make_valid_row(Zip="37201.0"))
    result = validate_rows(df)
    assert result.iloc[0]["_is_valid"] == False
    assert "Invalid Zip" in result.iloc[0]["_rejection_reason"]
