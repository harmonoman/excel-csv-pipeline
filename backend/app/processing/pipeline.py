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
    parse → map → normalize → client_injection → validate → split → enforce_schema → output
"""
import logging
from typing import Any
 
import pandas as pd
 
from app.processing.transformer import map_columns
from app.processing.normalizer import normalize
from app.processing.client import inject_client
from app.processing.validator import validate_rows
from app.processing.splitter import split_rows
from app.processing.schema import enforce_schema
 
logger = logging.getLogger(__name__)
 
 
class PipelineError(Exception):
    """
    Raised when any pipeline stage fails.
 
    Preserves the originating stage name, exception type, and message
    so callers can return structured error responses without losing context.
    """
 
    def __init__(self, stage: str, error_type: str, error_message: str):
        self.stage = stage
        self.error_type = error_type
        self.error_message = error_message
        super().__init__(f"Pipeline failed at stage '{stage}': [{error_type}] {error_message}")
 
 
def _run_stage(stage_name: str, fn, *args, **kwargs) -> Any:
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
        # Already wrapped — re-raise as-is
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
    Execute the full ingestion pipeline against a parsed DataFrame.
 
    Stages execute in strict order. Any failure halts the pipeline
    immediately and raises PipelineError — no partial output is returned.
 
    Args:
        df: parsed DataFrame from T2-2 parser (raw, pre-mapping)
        config: loaded and validated mapping.json config
 
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
 
    # Stage 1: map source columns to canonical names
    df = _run_stage("map_columns", map_columns, df, config)
 
    # Stage 2: normalize values (whitespace, casing, types, dates)
    df = _run_stage("normalize", normalize, df)
 
    # Stage 3: inject Client field from sheet name
    df = _run_stage("inject_client", inject_client, df)
 
    # Stage 4: validate each row against schema rules
    df = _run_stage("validate_rows", validate_rows, df)
 
    # Stage 5: split into clean and rejected DataFrames
    clean_df, rejected_df = _run_stage("split_rows", split_rows, df)
 
    # Stage 6: enforce final output schema on clean rows
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
 