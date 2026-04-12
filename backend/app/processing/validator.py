"""
validator.py — Row validation stage.

Responsibilities (T4-1 + T4-2):
- T4-1: Detect null, empty string, and whitespace-only values in required fields
- T4-2: Validate type correctness and domain rules for key fields
- Mark each row as valid or invalid via _is_valid column
- Attach comma-separated rejection reasons via _rejection_reason column

This module does NOT:
- Split into clean/rejected DataFrames (T4-3)
- Enforce schema column order (T5-6)
- Modify or normalize data values
- Drop rows
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

# --- Required field list (T4-1) ---
REQUIRED_FIELDS = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]

# --- Valid US state abbreviations (T4-2) ---
VALID_US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC", "PR", "VI", "GU", "MP", "AS",
}

# --- T4-2 rejection messages ---
MSG_AMOUNT = "Invalid Amount"
MSG_DATE = "Invalid Date"
MSG_STATE = "Invalid State"
MSG_ZIP = "Invalid Zip"


# ===========================================================================
# T4-1 — Missing field detection
# ===========================================================================

def _build_missing_mask(df: pd.DataFrame, field: str) -> pd.Series:
    """
    Return a boolean Series — True where the field value is considered missing.

    A value is missing if it is:
    - null (NaN, None, pd.NA) — detected via pd.isna()
    - empty string ""
    - whitespace-only string "   "

    Vectorized: applied across the entire column at once.
    """
    col = df[field]

    # Primary null check — covers NaN, None, pd.NA, numpy NaN
    null_mask = col.isna()

    # String emptiness check — only applies to non-null values
    str_col = col.astype(str)
    empty_mask = str_col.str.strip() == ""

    # "nan" string can appear when object columns contain float NaN values.
    # "None" string can appear when Python None gets stringified.
    # Note: a literal cell value of "None" (e.g. a city named "None") would be
    # incorrectly flagged — this is an acceptable MVP trade-off documented here.
    nan_string_mask = str_col.str.strip().isin(["nan", "None"])

    return null_mask | empty_mask | nan_string_mask


def _validate_missing_fields(df: pd.DataFrame) -> list[pd.Series]:
    """
    T4-1: Build one boolean Series per required field indicating missing values.
    Returns list of reason Series in REQUIRED_FIELDS order for determinism.
    """
    reason_parts = []
    for field in REQUIRED_FIELDS:
        if field in df.columns:
            mask = _build_missing_mask(df, field)
        else:
            mask = pd.Series(True, index=df.index)
        reason_parts.append(
            mask.map({True: f"Missing: {field}", False: ""})
        )
    return reason_parts


# ===========================================================================
# T4-2 — Type and value validators
# ===========================================================================

def _validate_donation_amount(df: pd.DataFrame) -> pd.Series:
    """
    T4-2: DonationAmount must be numeric and > 0.
    Non-numeric values and zero/negative values are rejected.
    Returns a Series of "" (valid) or "Invalid Amount" (invalid).
    """
    if "DonationAmount" not in df.columns:
        return pd.Series("", index=df.index)

    def _check(val) -> str:
        if pd.isna(val):
            return ""  # Already caught by T4-1
        try:
            numeric = float(val)
            return "" if numeric > 0 else MSG_AMOUNT
        except (ValueError, TypeError):
            return MSG_AMOUNT

    return df["DonationAmount"].apply(_check)


def _validate_donation_date(df: pd.DataFrame) -> pd.Series:
    """
    T4-2: DonationDate must be parseable as a valid date.
    Normalizer has already attempted parsing — validate the result is not NaN
    and can be confirmed as a real date string.
    Returns a Series of "" (valid) or "Invalid Date" (invalid).
    """
    if "DonationDate" not in df.columns:
        return pd.Series("", index=df.index)

    def _check(val) -> str:
        if pd.isna(val):
            return ""  # Already caught by T4-1
        try:
            pd.to_datetime(str(val))
            return ""
        except Exception:
            return MSG_DATE

    return df["DonationDate"].apply(_check)


def _validate_state(df: pd.DataFrame) -> pd.Series:
    """
    T4-2: State must be a valid 2-letter US state abbreviation (uppercase).
    Whitespace is trimmed before checking — handles residual padding.
    Returns a Series of "" (valid) or "Invalid State" (invalid).
    """
    if "State" not in df.columns:
        return pd.Series("", index=df.index)

    def _check(val) -> str:
        if pd.isna(val):
            return ""  # Already caught by T4-1
        trimmed = str(val).strip()
        return "" if trimmed in VALID_US_STATES else MSG_STATE

    return df["State"].apply(_check)


def _validate_zip(df: pd.DataFrame) -> pd.Series:
    """
    T4-2: ZIP must be exactly 5 digits (string).
    Whitespace is trimmed before checking — leading zeros must be preserved.
    Returns a Series of "" (valid) or "Invalid Zip" (invalid).
    """
    if "Zip" not in df.columns:
        return pd.Series("", index=df.index)

    def _check(val) -> str:
        if pd.isna(val):
            return ""  # Already caught by T4-1
        trimmed = str(val).strip()
        return "" if (trimmed.isdigit() and len(trimmed) == 5) else MSG_ZIP

    return df["Zip"].apply(_check)


# ===========================================================================
# Main validation entry point
# ===========================================================================

def validate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate each row against all T4-1 and T4-2 rules.

    T4-1 — Required field presence:
        Checks all 9 required fields for null, empty, or whitespace-only values.

    T4-2 — Type and domain rules:
        DonationAmount: must be numeric and > 0
        DonationDate:   must be parseable as a valid date
        State:          must be a valid 2-letter US state abbreviation
        Zip:            must be exactly 5 digits

    Adds two columns to the output:
    - _is_valid: bool — True if all rules pass
    - _rejection_reason: str — comma-separated rejection messages,
      empty string if row is valid. Order is deterministic.

    Args:
        df: normalized DataFrame from T3-2 with Client injected by T3-3

    Returns:
        DataFrame with _is_valid and _rejection_reason columns added.
        Input row count and all existing values are preserved unchanged.
    """
    df = df.copy()

    # Early return for empty DataFrames — no rows to validate
    if df.empty:
        df["_rejection_reason"] = pd.Series(dtype=str)
        df["_is_valid"] = pd.Series(dtype=bool)
        return df

    # --- T4-1: missing field checks ---
    reason_parts = _validate_missing_fields(df)

    # --- T4-2: type and value checks ---
    reason_parts.append(_validate_donation_amount(df))
    reason_parts.append(_validate_donation_date(df))
    reason_parts.append(_validate_state(df))
    reason_parts.append(_validate_zip(df))

    # Combine all reason parts — filter empty strings, join with ", "
    reason_df = pd.concat(reason_parts, axis=1)

    df["_rejection_reason"] = reason_df.apply(
        lambda row: ", ".join(v for v in row if v != ""),
        axis=1,
    )
    df["_is_valid"] = df["_rejection_reason"] == ""

    valid_count = int(df["_is_valid"].sum())
    invalid_count = int((~df["_is_valid"]).sum())
    logger.info(
        "Validation complete — valid: %d, invalid: %d",
        valid_count, invalid_count,
    )

    return df
