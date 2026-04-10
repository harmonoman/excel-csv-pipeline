import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
 
 
@pytest.fixture
def client():
    """Isolated TestClient per test — avoids shared state across test suite."""
    return TestClient(app)
 
 
def make_xlsx_file(
    filename: str = "test_file.xlsx",
    content: bytes = b"PK\x03\x04",
    mime: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
) -> tuple:
    """
    Helper: return a file tuple for multipart upload.
    PK header bytes simulate a zip-based xlsx at the boundary level.
    Content is intentionally minimal — this endpoint does not parse Excel content.
    """
    return (filename, io.BytesIO(content), mime)
 
 
# --- Valid upload ---
 
def test_valid_xlsx_upload_returns_200(client, tmp_path, monkeypatch):
    """Valid .xlsx file upload returns 200, correct response shape, and file is saved to disk."""
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
 
    response = client.post("/upload", files={"file": make_xlsx_file()})
 
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "file uploaded successfully"
    assert "filename" in data
    assert data["filename"].endswith(".xlsx")
 
    # Verify file was actually written to disk
    saved_files = list(tmp_path.iterdir())
    assert len(saved_files) == 1
    assert saved_files[0].name.endswith(".xlsx")
 
 
def test_uppercase_extension_accepted(client, tmp_path, monkeypatch):
    """Uppercase .XLSX extension must be accepted — extension check is case-insensitive."""
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
 
    response = client.post("/upload", files={"file": make_xlsx_file(filename="DATA.XLSX")})
 
    assert response.status_code == 200
 
 
# --- Extension validation ---
 
def test_invalid_extension_returns_400(client):
    """Non-xlsx file upload must be rejected with 400 and clear error message."""
    response = client.post(
        "/upload",
        files={"file": ("data.csv", io.BytesIO(b"col1,col2\n1,2"), "text/csv")},
    )
 
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "xlsx" in data["error"].lower()
 
 
# --- MIME type validation ---
 
def test_wrong_mime_type_returns_400(client):
    """File with .xlsx extension but wrong MIME type must be rejected."""
    response = client.post(
        "/upload",
        files={"file": make_xlsx_file(filename="sneaky.xlsx", mime="text/plain")},
    )
 
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "mime" in data["error"].lower()
 
 
# --- Empty file ---
 
def test_empty_file_returns_400(client):
    """
    Empty file upload must be rejected with 400.
    Empty check runs after MIME validation — file passes extension + MIME checks
    but is caught by the content length check after read().
    """
    response = client.post("/upload", files={"file": make_xlsx_file(content=b"")})
 
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "empty" in data["error"].lower()
 
 
# --- Missing file field ---
 
def test_missing_file_field_returns_422(client):
    """
    Request with no file field must return 422 (FastAPI enforces File(...) at framework level).
    This is intentional — 422 Unprocessable Entity is the correct HTTP response
    for a malformed request, distinct from 400 for invalid file content.
    """
    response = client.post("/upload")
 
    assert response.status_code == 422
 
 
# --- Path traversal ---
 
def test_path_traversal_in_filename_is_sanitized(client, tmp_path, monkeypatch):
    """
    Filename containing path traversal characters must be sanitized before saving.
    The file should still be accepted and saved — but only the basename is used.
    """
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
 
    response = client.post(
        "/upload",
        files={"file": make_xlsx_file(filename="../../etc/passwd.xlsx")},
    )
 
    assert response.status_code == 200
    # Saved filename must not contain directory traversal components
    saved_files = list(tmp_path.iterdir())
    assert len(saved_files) == 1
    assert ".." not in saved_files[0].name
    assert "etc" not in saved_files[0].name
 