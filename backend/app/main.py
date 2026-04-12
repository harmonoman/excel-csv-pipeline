"""
main.py — FastAPI application entry point.

Responsibilities:
- Startup config validation
- File upload endpoint with pipeline execution
- Centralized exception handling (T4-4)

Error classification:
- PipelineError  → HTTP 400 (client/pipeline error, structured response)
- Exception      → HTTP 500 (unexpected system failure, safe generic response)
- Validation     → HTTP 200 (row-level failures are expected pipeline output)
"""
import io
import logging
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import JSONResponse

from app.config.loader import ConfigValidationError, load_mapping_config
from app.processing.parser import parse_workbook
from app.processing.pipeline import PipelineError, run_pipeline

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
DEFAULT_UPLOAD_DIR = "/tmp/donor-bureau/uploads"

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

def get_upload_dir() -> Path:
    """
    Return upload directory from environment variable or default.
    Allows tests to override via monkeypatch.
    """
    upload_dir = Path(os.getenv("UPLOAD_DIR", DEFAULT_UPLOAD_DIR))
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


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


# ===========================================================================
# Routes
# ===========================================================================

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept an .xlsx file upload, run the full ingestion pipeline, and
    return a structured summary of clean and rejected rows.

    Pre-pipeline validation (HTTP 400 flat response):
    - File extension must be .xlsx
    - MIME type must match xlsx
    - File must not be empty

    Pipeline execution:
    - parse + map (per sheet)
    - normalize → inject_client → validate → split → enforce_schema

    Response:
    - HTTP 200 with summary (even if rows are rejected — that is expected)
    - HTTP 400 if pipeline fails (PipelineError — bad file, bad structure)
    - HTTP 500 if unexpected exception occurs
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

    # --- Save file ---
    upload_dir = get_upload_dir()
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    destination = upload_dir / unique_filename
    destination.write_bytes(content)

    logger.info("File received — filename=%s size=%d bytes", filename, len(content))

    # --- Parse workbook ---
    # Wrap parse separately so parse failures map to stage="parse"
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
    # PipelineError and unexpected exceptions bubble up to exception handlers
    result = run_pipeline(parsed_df, mapping_config)

    summary = result["summary"]
    logger.info(
        "Pipeline complete — file=%s total=%d clean=%d rejected=%d",
        filename,
        summary["total_rows"],
        summary["clean_rows"],
        summary["rejected_rows"],
    )

    return JSONResponse(
        status_code=200,
        content={
            "summary": summary,
            "filename": unique_filename,
        },
    )
