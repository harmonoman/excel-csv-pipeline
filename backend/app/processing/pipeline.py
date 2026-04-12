"""
pipeline.py — Central pipeline orchestrator.

Responsibilities:
- Execute all pipeline stages in strict order
- Pass output of each stage as input to the next
- Halt immediately on any stage failure
- Return structured result dict

This module does NOT:
- Implement transformation logic
- Validate or normalize data
- Make decisions about data correctness

Pipeline flow:
    parse+map (per sheet) → normalize → client_injection → validate → split → enforce_schema → output

NOTE: Column mapping (alias → canonical) happens inside parse_workbook() per sheet,
before concatenation. This ensures sheets with different column aliases all produce
identical canonical column names before being combined.
"""
import logging

import pandas as pd

from app.processing.normalizer import normalize
from app.processing.client import inject_client
from app.processing.validator import validate_rows
from app.processing.splitter import split_rows
from app.processing.schema import enforce_schema

logger = logging.getLogger(__name__)


# PipelineError lives in errors.py to avoid circular imports with stage modules
# that need to raise it (e.g. schema.py). Re-exported here for backward compatibility
# so existing callers (main.py, tests) can still import from pipeline.
from app.processing.errors import PipelineError  # noqa: F401


def _run_stage(stage_name: str, fn, *args, **kwargs):
    """
    Execute a single pipeline stage with structured error handling.

    If the stage raises any exception, wraps it in PipelineError and
    re-raises immediately — no swallowing, no partial state.
    """
    logger.info("Pipeline stage starting: %s", stage_name)
    try:
        result = fn(*args, **kwargs)
        logger.info("Pipeline stage complete: %s", stage_name)
        return result
    except PipelineError:
        raise
    except Exception as e:
        logger.error(
            "Pipeline stage failed: %s — [%s] %s",
            stage_name, type(e).__name__, str(e),
        )
        raise PipelineError(
            stage=stage_name,
            error_type=type(e).__name__,
            error_message=str(e),
        ) from e


def run_pipeline(df: pd.DataFrame, config: dict) -> dict:
    """
    Execute the full ingestion pipeline against a parsed + mapped DataFrame.

    Input df is expected to already have canonical column names — mapping
    happens inside parse_workbook() per sheet before concatenation.

    Stages execute in strict order. Any failure halts the pipeline
    immediately and raises PipelineError — no partial output is returned.

    Args:
        df: parsed and mapped DataFrame from parse_workbook()
        config: loaded and validated mapping.json config (passed to stages that need it)

    Returns:
        {
            "clean_df": DataFrame of valid rows (schema enforced),
            "rejected_df": DataFrame of invalid rows with rejection_reason,
            "summary": {
                "total_rows": int,
                "clean_rows": int,
                "rejected_rows": int,
            }
        }

    Raises:
        PipelineError: if any stage fails, with stage name and error context
    """
    total_rows = len(df)
    logger.info("Pipeline started — %d input rows", total_rows)

    # Stage 1: normalize values (whitespace, casing, types, dates)
    df = _run_stage("normalize", normalize, df)

    # Stage 2: inject Client field from sheet name
    df = _run_stage("inject_client", inject_client, df)

    # Stage 3: validate each row against schema rules
    df = _run_stage("validate_rows", validate_rows, df)

    # Stage 4: split into clean and rejected DataFrames
    clean_df, rejected_df = _run_stage("split_rows", split_rows, df)

    # Stage 5: enforce final output schema on clean rows
    clean_df = _run_stage("enforce_schema", enforce_schema, clean_df)

    summary = {
        "total_rows": total_rows,
        "clean_rows": len(clean_df),
        "rejected_rows": len(rejected_df),
    }

    logger.info(
        "Pipeline complete — clean: %d, rejected: %d",
        summary["clean_rows"],
        summary["rejected_rows"],
    )

    return {
        "clean_df": clean_df,
        "rejected_df": rejected_df,
        "summary": summary,
    }
