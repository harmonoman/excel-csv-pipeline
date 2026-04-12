"""
metrics.py — Pipeline metrics logging utility (T5-5).

Responsibilities:
- Emit a single structured PIPELINE_METRICS log line per upload
- Capture: filename, total_rows, clean_rows, rejected_rows, processing_time_ms

This is purely an observability layer.
It does NOT:
- affect pipeline behavior
- modify data
- return values
- raise exceptions
"""
import logging

logger = logging.getLogger(__name__)


def log_pipeline_metrics(
    file_name: str,
    total_rows: int,
    clean_rows: int,
    rejected_rows: int,
    processing_time_ms: int,
) -> None:
    """
    Emit a single structured PIPELINE_METRICS log line.

    Format:
        [PIPELINE_METRICS] file=donations.xlsx total_rows=120 clean_rows=100
        rejected_rows=20 processing_time_ms=342

    This function is a fire-and-forget observability call. It never raises
    and never affects control flow. All values are logged as-is — no
    transformation or validation is performed here.

    Args:
        file_name:          original uploaded filename
        total_rows:         total rows parsed from workbook
        clean_rows:         rows that passed validation
        rejected_rows:      rows that failed validation
        processing_time_ms: end-to-end processing time in milliseconds
    """
    logger.info(
        "[PIPELINE_METRICS] file=%s total_rows=%d clean_rows=%d "
        "rejected_rows=%d processing_time_ms=%d",
        file_name,
        total_rows,
        clean_rows,
        rejected_rows,
        processing_time_ms,
    )