"""
normalizer.py — Data normalization stage.
 
Responsibilities:
- Strip whitespace from all string fields
- Title-case First, Last, City
- Uppercase State
- Cast DonationAmount to float
- Parse DonationDate to ISO 8601 string (YYYY-MM-DD)
- Preserve Zip as string with leading zeros intact
 
This module does NOT:
- Validate data correctness (T4's responsibility)
- Reject or drop rows
- Enforce required fields
- Add or remove columns
"""
import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
# Fields that receive title case formatting
TITLE_CASE_FIELDS = {"First", "Last", "City"}
 
# Fields that receive uppercase formatting — iterated in _normalize_state()
UPPER_CASE_FIELDS = {"State"}
 
# All string fields that should be whitespace-stripped
# Note: Zip is handled separately to preserve leading zeros
STRING_FIELDS = {"First", "Last", "Address1", "City", "State"}
 
# Excel epoch starts 1900-01-01 (with Lotus 1-2-3 leap year bug)
# Serials above this threshold are treated as Excel date serials
EXCEL_SERIAL_THRESHOLD = 10000
 
 
def _is_present(df: pd.DataFrame, col: str) -> bool:
    """Return True if column exists in DataFrame."""
    return col in df.columns
 
 
def _normalize_string_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from all standard string fields that exist."""
    for col in STRING_FIELDS:
        if _is_present(df, col):
            df[col] = df[col].astype(str).str.strip()
            # Restore actual NaN — astype(str) converts NaN to "nan"
            df[col] = df[col].where(df[col] != "nan", other=pd.NA)
    return df
 
 
def _normalize_title_case(df: pd.DataFrame) -> pd.DataFrame:
    """Apply title case to First, Last, City where present.
    pd.NA values propagate safely through .str.title()."""
    for col in TITLE_CASE_FIELDS:
        if _is_present(df, col):
            df[col] = df[col].str.title()
    return df
 
 
def _normalize_state(df: pd.DataFrame) -> pd.DataFrame:
    """Uppercase all fields in UPPER_CASE_FIELDS where present."""
    for col in UPPER_CASE_FIELDS:
        if _is_present(df, col):
            df[col] = df[col].str.upper()
    return df
 
 
def _normalize_zip(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Zip to a 5-digit string, preserving leading zeros.
 
    Handles:
    - String "01234" → "01234" (preserved)
    - Integer 1234   → "01234" (zero-padded)
    - String "37201" → "37201" (standard, unchanged)
    """
    if not _is_present(df, "Zip"):
        return df
 
    def _zip_to_string(val) -> str:
        if pd.isna(val):
            return pd.NA
        # Handle numeric types (Excel may store ZIP as integer,
        # dropping the leading zero — zfill restores it)
        if isinstance(val, (int, float)):
            return str(int(val)).zfill(5)
        # String — strip whitespace, zero-pad if purely numeric
        val = str(val).strip()
        if val.isdigit():
            return val.zfill(5)
        return val
 
    df["Zip"] = df["Zip"].apply(_zip_to_string)
    return df
 
 
def _normalize_donation_amount(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cast DonationAmount to float.
 
    - Handles string amounts with commas (e.g. "1,205.67")
    - Invalid values become NaN (not dropped — T4 handles rejection)
    """
    if not _is_present(df, "DonationAmount"):
        return df
 
    def _to_float(val):
        if pd.isna(val):
            return float("nan")
        try:
            # Remove commas from formatted numbers e.g. "1,205.67"
            cleaned = str(val).replace(",", "").strip()
            return float(cleaned)
        except (ValueError, TypeError):
            logger.debug("Could not cast DonationAmount value to float: '%s'", val)
            return float("nan")
 
    df["DonationAmount"] = df["DonationAmount"].apply(_to_float)
    return df
 
 
def _normalize_donation_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse DonationDate to ISO 8601 string (YYYY-MM-DD).
 
    Handles:
    - Excel date serials (integers above EXCEL_SERIAL_THRESHOLD)
    - Python datetime objects (returned by openpyxl data_only mode)
    - Standard string formats via pandas to_datetime (auto-inferred)
    - Natural language dates ("March 16, 2025")
    - Invalid values become NaN (not dropped)
 
    Note: infer_datetime_format was removed in pandas 2.2 — to_datetime()
    infers formats automatically without it.
 
    Note: broad except is intentional — date parsing libraries raise
    multiple exception types (ValueError, OverflowError, OSError etc.)
    """
    if not _is_present(df, "DonationDate"):
        return df
 
    def _parse_date(val) -> str:
        if pd.isna(val):
            return pd.NA
        try:
            # Excel date serial — integer above threshold
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                if val > EXCEL_SERIAL_THRESHOLD:
                    parsed = pd.Timestamp("1899-12-30") + pd.Timedelta(days=int(val))
                    return parsed.strftime("%Y-%m-%d")
 
            # pandas Timestamp or Python datetime — format directly
            if isinstance(val, (pd.Timestamp,)):
                return val.strftime("%Y-%m-%d")
 
            # All other formats (strings, datetime objects) —
            # pandas to_datetime auto-infers format in 2.x without deprecated flag
            parsed = pd.to_datetime(str(val))
            return parsed.strftime("%Y-%m-%d")
 
        except Exception:
            logger.debug("Could not parse DonationDate value: '%s'", val)
            return pd.NA
 
    df["DonationDate"] = df["DonationDate"].apply(_parse_date)
    return df
 
 
def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize all known canonical fields in the DataFrame.
 
    Operations are applied only to columns that exist — missing
    columns are silently skipped. No rows are added or removed.
    No columns are added or removed.
 
    Args:
        df: mapped DataFrame from T3-1 transformer
 
    Returns:
        DataFrame with normalized values, same shape as input.
    """
    df = df.copy()
 
    df = _normalize_string_fields(df)
    df = _normalize_title_case(df)
    df = _normalize_state(df)
    df = _normalize_zip(df)
    df = _normalize_donation_amount(df)
    df = _normalize_donation_date(df)
 
    return df
 