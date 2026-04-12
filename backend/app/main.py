"""
main.py — FastAPI application entry point.

Responsibilities:
- Startup config validation
- File upload endpoint with full pipeline execution and CSV output
- File download endpoint for generated CSVs
- Centralized exception handling (T4-4)

Error classification:
- PipelineError  → HTTP 400 (client/pipeline error, structured response)
- Exception      → HTTP 500 (unexpected system failure, safe generic response)
- Validation     → HTTP 200 (row-level failures are expected pipeline output)
"""
import io
import logging
import os
import re
import time
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from app.config.loader import ConfigValidationError, load_mapping_config
from app.output.writer import write_clean_csv, write_rejected_csv
from app.processing.parser import parse_workbook
from app.processing.pipeline import PipelineError, run_pipeline
from app.utils.file_naming import generate_output_filenames
from app.logging_utils.metrics import log_pipeline_metrics

logger = logging.getLogger(__name__)

# --- Config startup validation ---
CONFIG_PATH = Path(__file__).parent / "config" / "mapping.json"

try:
    mapping_config = load_mapping_config(CONFIG_PATH)
except ConfigValidationError as e:
    raise RuntimeError(f"Invalid mapping config — pipeline cannot start: {e}")

# --- Constants ---
ALLOWED_EXTENSION = ".xlsx"
ALLOWED_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# DEFAULT_UPLOAD_DIR is intentionally not used — raw uploads are processed
# in-memory (BytesIO) and not persisted to disk. Reserved for future use
# if raw upload persistence is added post-MVP.
DEFAULT_OUTPUT_DIR = "/tmp/donor-bureau/outputs"

# Safe filename pattern — only letters, digits, underscores, hyphens, dots
_SAFE_FILENAME_RE = re.compile(r'^[a-zA-Z0-9_\-\.]+$')

# --- App ---
app = FastAPI(
    title="Excel CSV Pipeline",
    description="Excel to CSV donation data pipeline",
    version="0.1.0",
)


# ===========================================================================
# T4-4 — Centralized exception handlers
# ===========================================================================

@app.exception_handler(PipelineError)
async def pipeline_error_handler(request: Request, exc: PipelineError) -> JSONResponse:
    """
    Handle PipelineError — structured errors from any pipeline stage.

    Returns HTTP 400 with stage, error type, and message.
    Never exposes stack traces.
    """
    logger.error(
        "Pipeline error — stage=%s type=%s message=%s",
        exc.stage, exc.error_type, exc.error_message,
    )
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "type": exc.error_type,
                "stage": exc.stage,
                "message": exc.error_message,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all unexpected exceptions — runtime failures, code bugs, etc.

    Returns HTTP 500 with a safe generic message.
    Never exposes internal details or stack traces.
    """
    logger.error(
        "Unexpected error — type=%s message=%s",
        type(exc).__name__, str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "stage": "unknown",
                "message": "An unexpected error occurred. Please try again or contact support.",
            }
        },
    )


# ===========================================================================
# Helpers
# ===========================================================================

def get_output_dir() -> Path:
    """
    Return output directory for generated CSVs.
    Allows tests to override via monkeypatch.
    """
    output_dir = Path(os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def error_response(message: str, status_code: int = 400, stage: str = "upload") -> JSONResponse:
    """
    Structured error response for pre-pipeline validation failures.
    Uses the same schema as PipelineError responses for consistency:
    {"error": {"type": ..., "stage": ..., "message": ...}}
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": "ValidationError",
                "stage": stage,
                "message": message,
            }
        },
    )


def is_safe_filename(filename: str) -> bool:
    """
    Return True if filename contains only safe characters.
    Rejects path traversal attempts and unsafe characters.
    """
    # Reject empty, path separators, and traversal sequences
    if not filename or "/" in filename or "\\" in filename or ".." in filename:
        return False
    return bool(_SAFE_FILENAME_RE.match(filename))


# ===========================================================================
# Routes
# ===========================================================================

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept an .xlsx file upload, run the full ingestion pipeline, write
    output CSVs, and return a structured response with download links.

    Pre-pipeline validation (HTTP 400):
    - File extension must be .xlsx
    - MIME type must match xlsx
    - File must not be empty

    Pipeline execution:
    - parse + map (per sheet)
    - normalize → inject_client → validate → split → enforce_schema

    Output:
    - clean CSV written to output directory
    - rejected CSV written to output directory

    Response schema (HTTP 200):
    {
        "total_rows": int,
        "clean_rows": int,
        "rejected_rows": int,
        "clean_file": "/download/{filename}",
        "rejected_file": "/download/{filename}"
    }
    """
    # --- Pre-pipeline file validation ---
    raw_filename = file.filename or ""
    filename = Path(raw_filename).name

    if not filename.lower().endswith(ALLOWED_EXTENSION):
        suffix = Path(filename).suffix or "no extension"
        return error_response(
            f"invalid file type — only .xlsx files are accepted, got: '{suffix}'"
        )

    if file.content_type != ALLOWED_MIME_TYPE:
        return error_response(
            f"invalid mime type — expected xlsx content type, got: '{file.content_type}'"
        )

    content = await file.read()

    if len(content) == 0:
        return error_response("empty file — uploaded file contains no content")

    logger.info("File received — filename=%s size=%d bytes", filename, len(content))

    # --- Start timing (covers parse + pipeline + output writing) ---
    _start = time.perf_counter()

    # --- Parse workbook ---
    try:
        source = io.BytesIO(content)
        parsed_df = parse_workbook(source, mapping_config)
    except Exception as e:
        logger.error(
            "Parse failed — file=%s type=%s message=%s",
            filename, type(e).__name__, str(e),
        )
        raise PipelineError(
            stage="parse",
            error_type="InvalidFile",
            error_message=f"Unable to read Excel file: {type(e).__name__}",
        ) from e

    # --- Run pipeline ---
    # Note: if run_pipeline() raises PipelineError, the exception handler
    # returns before reaching log_pipeline_metrics(). This is intentional —
    # there are no valid row counts to log when the pipeline fails.
    result = run_pipeline(parsed_df, mapping_config)

    # --- Write output files ---
    output_dir = get_output_dir()
    filenames = generate_output_filenames(filename)

    clean_path = output_dir / filenames["clean"]
    rejected_path = output_dir / filenames["rejected"]

    write_clean_csv(result["clean_df"], clean_path)
    write_rejected_csv(result["rejected_df"], rejected_path)

    summary = result["summary"]
    _processing_time_ms = int((time.perf_counter() - _start) * 1000)

    logger.info(
        "Pipeline complete — file=%s total=%d clean=%d rejected=%d",
        filename,
        summary["total_rows"],
        summary["clean_rows"],
        summary["rejected_rows"],
    )

    log_pipeline_metrics(
        file_name=filename,
        total_rows=summary["total_rows"],
        clean_rows=summary["clean_rows"],
        rejected_rows=summary["rejected_rows"],
        processing_time_ms=_processing_time_ms,
    )

    return JSONResponse(
        status_code=200,
        content={
            "total_rows": summary["total_rows"],
            "clean_rows": summary["clean_rows"],
            "rejected_rows": summary["rejected_rows"],
            "clean_file": f"/download/{filenames['clean']}",
            "rejected_file": f"/download/{filenames['rejected']}",
        },
    )


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Serve a generated CSV file by filename.

    Security:
    - Filename is validated against a strict safe character pattern
    - Path traversal attempts (../) are rejected with 400
    - Non-existent files return 404

    Returns:
    - 200 with CSV file content
    - 400 if filename is unsafe
    - 404 if file does not exist
    """
    if not is_safe_filename(filename):
        return error_response(
            f"invalid filename: '{filename}'",
            status_code=400,
            stage="download",
        )

    output_dir = get_output_dir()
    file_path = output_dir / filename

    if not file_path.exists():
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "type": "NotFound",
                    "stage": "download",
                    "message": f"File not found: '{filename}'",
                }
            },
        )

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=filename,
    )
