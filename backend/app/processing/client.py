"""
client.py — Client field injection stage.

Responsibilities:
- Create Client column derived from _source_sheet
- Strip whitespace from sheet name before assignment
- Preserve _source_sheet unchanged
- Ensure every row has a non-null, non-empty Client value

This module does NOT:
- Read Client from Excel cell values
- Validate client name quality or allowed values
- Drop rows
- Modify any other column
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def inject_client(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inject the Client column into the DataFrame using _source_sheet.

    Client is derived exclusively from the sheet tab name — never from
    Excel cell data. Sheet names are trimmed of whitespace before
    assignment. _source_sheet is preserved unchanged.

    If _source_sheet is null for any row, Client will be null for that
    row. This is logged as a warning — T4 validation will reject it.

    Args:
        df: normalized DataFrame from T3-2 containing _source_sheet

    Returns:
        DataFrame with Client column added. All other columns unchanged.
    """
    df = df.copy()

    # Early return for empty DataFrames — no rows to process
    if df.empty:
        df["Client"] = pd.Series(dtype=str)
        return df

    # Derive Client from _source_sheet — strip whitespace only.
    # No further normalization — validation is T4's responsibility.
    df["Client"] = df["_source_sheet"].str.strip()

    # Warn on any null or empty Client values — T4 will reject these rows
    # but visibility here helps diagnose upstream parser issues early.
    null_count = df["Client"].isna().sum()
    if null_count > 0:
        logger.warning(
            "%d row(s) have null _source_sheet — Client will be null for these rows",
            null_count,
        )

    empty_count = (df["Client"] == "").sum()
    if empty_count > 0:
        logger.warning(
            "%d row(s) have whitespace-only sheet name — Client will be empty string",
            empty_count,
        )

    return df
