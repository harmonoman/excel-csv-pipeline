import io
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Isolated TestClient per test — avoids shared state across test suite."""
    return TestClient(app)


XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def make_real_xlsx() -> bytes:
    """Build a minimal but valid xlsx workbook in memory using openpyxl."""
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"])
    ws.append(["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def make_xlsx_file(
    filename: str = "test_file.xlsx",
    content: bytes = None,
    mime: str = XLSX_MIME,
) -> tuple:
    """
    Helper: return a file tuple for multipart upload.
    Defaults to a real valid xlsx — required since the endpoint now runs the full pipeline.
    Pass content=b"" for empty file tests or custom bytes for MIME-only tests.
    """
    if content is None:
        content = make_real_xlsx()
    return (filename, io.BytesIO(content), mime)


# --- Valid upload ---

def test_valid_xlsx_upload_returns_200(client, tmp_path, monkeypatch):
    """Valid .xlsx file upload returns 200 with correct flat response schema."""
    response = client.post("/upload", files={"file": make_xlsx_file()})

    assert response.status_code == 200
    data = response.json()
    assert "total_rows" in data
    assert "clean_rows" in data
    assert "rejected_rows" in data
    assert "clean_file" in data
    assert "rejected_file" in data


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
    assert "xlsx" in data["error"]["message"].lower()


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
    assert "mime" in data["error"]["message"].lower()


# --- Empty file ---

def test_empty_file_returns_400(client):
    """
    Empty file upload must be rejected with 400.
    Empty check runs after MIME validation — file passes extension + MIME checks
    but is caught by the content length check after read().
    """
    response = client.post("/upload", files={"file": make_xlsx_file(content=b"", mime=XLSX_MIME)})

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "empty" in data["error"]["message"].lower()


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
    Filename containing path traversal characters is sanitized by Path().name
    before use. The upload succeeds and the output filenames are safe.
    """
    response = client.post(
        "/upload",
        files={"file": make_xlsx_file(filename="../../etc/passwd.xlsx")},
    )

    assert response.status_code == 200
    data = response.json()
    # Output filenames must not contain path traversal components
    assert ".." not in data["clean_file"]
    assert ".." not in data["rejected_file"]
    assert "etc" not in data["clean_file"]
