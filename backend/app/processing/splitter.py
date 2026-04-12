"""
splitter.py — Row splitter stage (T4-3).

Responsibilities:
- Split validated DataFrame into clean_df and rejected_df
- Clean condition: _rejection_reason is NaN, empty string, or whitespace-only
- Rejected condition: _rejection_reason contains any non-empty value
- Drop all internal columns (_is_valid, _rejection_reason, _source_sheet) from clean_df
- Rename _rejection_reason → rejection_reason in rejected_df
- Reset index in both outputs

This module does NOT:
- Perform validation (T4-1/T4-2)
- Modify row values
- Enforce schema column order (T5-6)
- Re-run or recompute rejection reasons
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Internal columns produced by upstream stages — removed from clean output
INTERNAL_COLUMNS = ["_is_valid", "_rejection_reason", "_source_sheet"]


def _is_clean(series: pd.Series) -> pd.Series:
    """
    Return a boolean mask — True where the row is clean.

    A row is clean if _rejection_reason is:
    - NaN / None / pd.NA
    - empty string ""
    - whitespace-only string "   "

    Anything else indicates a rejection reason and marks the row as invalid.
    """
    # Null check covers NaN, None, pd.NA
    null_mask = series.isna()

    # String check — safe even on mixed-type columns
    str_series = series.astype(str)
    empty_mask = str_series.str.strip() == ""

    # "nan" artifact from float NaN being stringified
    # "<NA>" artifact from pd.NA in pandas string extension arrays
    nan_string_mask = str_series.str.strip().isin(["nan", "<NA>"])

    return null_mask | empty_mask | nan_string_mask


def split_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a validated DataFrame into clean and rejected DataFrames.

    Uses _rejection_reason as the source of truth for row classification —
    not _is_valid. This ensures the split logic is independent of the boolean
    flag and directly reflects the actual rejection content.

    Args:
        df: validated DataFrame containing _rejection_reason and _is_valid columns

    Returns:
        (clean_df, rejected_df)

        clean_df:
            - valid rows only
            - all internal columns removed (_is_valid, _rejection_reason, _source_sheet)
            - index reset to 0-based

        rejected_df:
            - invalid rows only
            - _rejection_reason renamed to rejection_reason
            - _is_valid and _source_sheet removed
            - index reset to 0-based
    """
    # Build clean mask from rejection_reason content — not from _is_valid flag
    clean_mask = _is_clean(df["_rejection_reason"])
    rejected_mask = ~clean_mask

    # Split — copy to prevent downstream mutation of shared data
    clean_df = df[clean_mask].copy()
    rejected_df = df[rejected_mask].copy()

    # Clean output: drop all internal columns
    clean_df = clean_df.drop(
        columns=[c for c in INTERNAL_COLUMNS if c in clean_df.columns],
        errors="ignore",
    ).reset_index(drop=True)

    # Rejected output: rename _rejection_reason, drop other internal columns
    rejected_df = rejected_df.drop(
        columns=[c for c in INTERNAL_COLUMNS if c != "_rejection_reason" and c in rejected_df.columns],
        errors="ignore",
    ).rename(columns={"_rejection_reason": "rejection_reason"}).reset_index(drop=True)

    clean_count = len(clean_df)
    rejected_count = len(rejected_df)
    logger.info(
        "Split complete — clean: %d, rejected: %d",
        clean_count, rejected_count,
    )

    return clean_df, rejected_df
