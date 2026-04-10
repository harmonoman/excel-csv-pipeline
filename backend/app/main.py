import os
import uuid
from pathlib import Path
 
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
 
from app.config.loader import ConfigValidationError, load_mapping_config
 
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
 
 
def get_upload_dir() -> Path:
    """
    Return upload directory from environment variable or default.
    Allows tests to override via monkeypatch.
    """
    upload_dir = Path(os.getenv("UPLOAD_DIR", DEFAULT_UPLOAD_DIR))
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir
 
 
def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Consistent error response shape across all failure modes."""
    return JSONResponse(
        status_code=status_code,
        content={"error": message},
    )
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
 
 
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept an .xlsx file upload.
 
    Validates:
    - File is present and non-empty
    - File extension is .xlsx (case-insensitive)
    - MIME type matches expected xlsx type
 
    Does NOT parse, map, or validate Excel content.
    That is the responsibility of T2-2 and beyond.
    """
    # Sanitize filename — strip any directory components to prevent path traversal
    raw_filename = file.filename or ""
    filename = Path(raw_filename).name
 
    # Validate extension (case-insensitive)
    if not filename.lower().endswith(ALLOWED_EXTENSION):
        suffix = Path(filename).suffix or "no extension"
        return error_response(
            f"invalid file type — only .xlsx files are accepted, got: '{suffix}'"
        )
 
    # Validate MIME type (defensive second check)
    if file.content_type != ALLOWED_MIME_TYPE:
        return error_response(
            f"invalid mime type — expected xlsx content type, got: '{file.content_type}'"
        )
 
    # Read file content
    content = await file.read()
 
    # Validate file is not empty
    # Note: empty check must come after read() — UploadFile does not expose size before reading
    if len(content) == 0:
        return error_response("empty file — uploaded file contains no content")
 
    # Save to upload directory with unique filename (uuid prefix prevents collisions)
    upload_dir = get_upload_dir()
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    destination = upload_dir / unique_filename
    destination.write_bytes(content)
 
    return JSONResponse(
        status_code=200,
        content={
            "message": "file uploaded successfully",
            "filename": unique_filename,
        },
    )
