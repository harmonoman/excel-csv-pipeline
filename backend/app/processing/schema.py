"""
schema.py — Final schema enforcement stage (T5-6).

Responsibilities:
- Verify ALL required output columns are present — raise PipelineError if any missing
- Drop any extra columns not in OUTPUT_SCHEMA
- Enforce exact column order
- Never mutate input DataFrame

This is the hard gate between the pipeline and output generation.
If the schema is wrong, this stage fails loudly — no silent fixes,
no partial outputs, no inferred columns.

This module does NOT:
- Normalize column names (mapping stage responsibility)
- Fill missing values
- Validate data content (T4 responsibility)
- Write CSV files (T5-1, T5-2 responsibility)
"""
import pandas as pd

from app.processing.errors import PipelineError

OUTPUT_SCHEMA = [
    "First",
    "Last",
    "Address1",
    "City",
    "State",
    "Zip",
    "DonationDate",
    "DonationAmount",
    "Client",
]


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce the exact output schema on clean_df before CSV writing.

    Checks:
    1. All required columns are present — raises PipelineError if any missing
    2. Extra columns are dropped
    3. Column order matches OUTPUT_SCHEMA exactly

    This is the last line of defense before data leaves the pipeline.
    Failures here indicate an upstream bug — a required canonical column
    was lost somewhere between mapping and splitting.

    Args:
        df: clean DataFrame from T4-3 splitter

    Returns:
        DataFrame with exactly OUTPUT_SCHEMA columns in exact order.

    Raises:
        PipelineError(stage="schema", error_type="MissingColumn"):
            if any required column is absent from the DataFrame.
    """
    df = df.copy()

    # Early return for empty DataFrames — no rows to enforce schema on.
    # An empty clean_df is a valid pipeline result (e.g. all rows rejected,
    # or workbook with no parseable sheets). Return with correct column structure.
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_SCHEMA)

    # Hard check — every required column must be present.
    # Raises on the first missing column found in OUTPUT_SCHEMA order — deterministic.
    for col in OUTPUT_SCHEMA:
        if col not in df.columns:
            raise PipelineError(
                stage="schema",
                error_type="MissingColumn",
                error_message=f"Missing required column: {col}",
            )

    # Select and reorder — drops any extra columns implicitly
    return df[OUTPUT_SCHEMA].reset_index(drop=True)
