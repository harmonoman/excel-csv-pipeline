"""
writer.py — Output CSV writers (T5-1, T5-2).

Responsibilities:
- Write clean_df to a warehouse-ready CSV (T5-1)
- Write rejected_df to a rejected rows CSV (T5-2)

These functions are pure output boundaries:
- They do NOT validate schema (T5-6 responsibility)
- They do NOT generate filenames (T5-4 responsibility)
- They do NOT log (T5-5 responsibility)
- They do NOT transform data — only serialize

Column order is enforced explicitly before writing to guard against any
upstream reordering. This is belt-and-suspenders given T5-6 has already
enforced schema, but makes the writer self-contained and trustworthy.
"""
import pandas as pd
from pathlib import Path

from app.processing.schema import OUTPUT_SCHEMA

# Rejected CSV includes all clean columns plus rejection_reason
REJECTED_SCHEMA = OUTPUT_SCHEMA + ["rejection_reason"]


def write_clean_csv(clean_df: pd.DataFrame, output_path: Path) -> Path:
    """
    Write clean_df to a CSV file at output_path.

    Column order is enforced to exactly match OUTPUT_SCHEMA regardless
    of the column order in the incoming DataFrame.

    Args:
        clean_df: schema-enforced clean DataFrame from T5-6
        output_path: fully resolved Path where the CSV will be written

    Returns:
        Path to the written file (same as output_path)
    """
    # Enforce column order explicitly — belt-and-suspenders after T5-6
    cols = [c for c in OUTPUT_SCHEMA if c in clean_df.columns]
    df = clean_df[cols]

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    return output_path


def write_rejected_csv(rejected_df: pd.DataFrame, output_path: Path) -> Path:
    """
    Write rejected_df to a CSV file at output_path.

    Preserves all original data columns plus rejection_reason.
    Column order: OUTPUT_SCHEMA columns first, then rejection_reason last.

    Args:
        rejected_df: rejected rows DataFrame from T4-3 splitter,
                     containing original columns + rejection_reason
        output_path: fully resolved Path where the CSV will be written

    Returns:
        Path to the written file (same as output_path)
    """
    # Build column order: schema columns present + rejection_reason last.
    # rejection_reason is expected to always be present — the splitter guarantees it.
    # If absent (upstream contract violation), the column is omitted from output
    # rather than crashing. This is a silent failure mode — callers should ensure
    # the splitter contract is upheld before calling this function.
    cols = [c for c in OUTPUT_SCHEMA if c in rejected_df.columns]
    if "rejection_reason" in rejected_df.columns:
        cols = cols + ["rejection_reason"]

    df = rejected_df[cols]

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    return output_path
