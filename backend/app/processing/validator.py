"""
validator.py — Row validation stage.

Responsibilities:
- Detect null, empty string, and whitespace-only values in required fields
- Mark each row as valid or invalid via _is_valid column
- Attach comma-separated rejection reasons via _rejection_reason column

This module does NOT:
- Validate data types or value ranges (T4-2)
- Split into clean/rejected DataFrames (T4-3)
- Enforce schema column order (T5-6)
- Modify or normalize data values
- Drop rows
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]


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
    # Convert to string safely, then strip and check for empty
    str_col = col.astype(str)
    empty_mask = str_col.str.strip() == ""

    # "nan" string can appear when object columns contain float NaN values.
    # "None" string can appear when Python None gets stringified.
    # Note: a literal cell value of "None" (e.g. a city named "None") would be
    # incorrectly flagged — this is an acceptable MVP trade-off documented here.
    nan_string_mask = str_col.str.strip().isin(["nan", "None"])

    return null_mask | empty_mask | nan_string_mask


def validate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate each row against required field presence rules.

    For each required field, checks whether the value is null, empty,
    or whitespace-only. Adds two columns to the output:

    - _is_valid: bool — True if all required fields are present
    - _rejection_reason: str — comma-separated "Missing: <field>" reasons,
      empty string if row is valid. Field order matches REQUIRED_FIELDS
      for deterministic, human-readable output.

    Uses vectorized pandas operations — no row-by-row iteration.

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

    # Build a missing mask per field — only for fields present in df
    # Fields absent from df are flagged as "Missing column: <field>"
    missing_masks = {}
    for field in REQUIRED_FIELDS:
        if field in df.columns:
            missing_masks[field] = _build_missing_mask(df, field)
        else:
            # Column entirely absent — every row is missing this field
            missing_masks[field] = pd.Series(True, index=df.index)

    # Build rejection reason per row — vectorized concatenation
    # Reasons are in REQUIRED_FIELDS order for determinism
    reason_parts = []
    for field in REQUIRED_FIELDS:
        mask = missing_masks[field]
        # Where field is missing, reason is "Missing: <field>", else ""
        reason_parts.append(
            mask.map({True: f"Missing: {field}", False: ""})
        )

    # Combine parts — filter out empty strings, join with ", "
    reason_df = pd.concat(reason_parts, axis=1)
    reason_df.columns = REQUIRED_FIELDS

    df["_rejection_reason"] = reason_df.apply(
        lambda row: ", ".join(v for v in row if v != ""),
        axis=1,
    )
    df["_is_valid"] = df["_rejection_reason"] == ""

    valid_count = df["_is_valid"].sum()
    invalid_count = (~df["_is_valid"]).sum()
    logger.info(
        "Validation complete — valid: %d, invalid: %d",
        valid_count, invalid_count,
    )

    return df
