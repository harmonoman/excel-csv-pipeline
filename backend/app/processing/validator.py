"""
validator.py — Row validation stage.
 
Stub implementation — full logic implemented in T4-1 and T4-2.
 
Responsibilities (when complete):
- Check each row for null/missing required fields
- Check data types and value rules
- Add _is_valid and _rejection_reason columns
"""
import pandas as pd
 
REQUIRED_FIELDS = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]
 
 
def _is_missing(value) -> bool:
    """
    Return True if a value is considered missing.
    Handles: None, pd.NA, numpy NaN, empty string, whitespace-only string.
    Uses pd.isna() as the primary null check — covers all pandas null types.
    """
    if pd.isna(value):
        return True
    return str(value).strip() in ("", "None", "nan")
 
 
def validate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate each row against required field and type rules.
 
    Adds two columns:
    - _is_valid: bool — True if row passes all checks
    - _rejection_reason: str — comma-separated failure reasons, empty if valid
 
    Stub: currently checks only for null/missing required fields.
    Full implementation in T4-1 and T4-2.
    """
    df = df.copy()
    reasons = []
 
    for _, row in df.iterrows():
        row_reasons = []
        for field in REQUIRED_FIELDS:
            if field not in df.columns:
                row_reasons.append(f"Missing column: {field}")
            elif _is_missing(row.get(field)):
                row_reasons.append(f"Missing: {field}")
        reasons.append(", ".join(row_reasons))
 
    df["_rejection_reason"] = reasons
    df["_is_valid"] = df["_rejection_reason"] == ""
    return df
 