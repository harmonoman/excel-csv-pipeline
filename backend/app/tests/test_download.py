"""
Tests for T5-3 — download response + summary.

Tests cover:
- /upload returns exact response schema with download links
- /download/{filename} serves generated CSV files
- 404 for non-existent files
- Path traversal prevention
- Row count integrity (total = clean + rejected)
- Repeat upload produces different filenames
"""
import io
import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.tests.fixtures import build_workbook

client = TestClient(app)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def make_valid_workbook() -> bytes:
    """Build a minimal valid workbook with one clean and one rejected row."""
    buf = build_workbook([{
        "name": "Alpha Fund",
        "rows": [
            ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
            ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
            ["Jane", None, "456 Oak Ave", "Memphis", "XX", "1234", "bad-date", "-50"],
        ]
    }])
    return buf.read()


def make_xlsx_upload(content: bytes, filename: str = "donations.xlsx"):
    return ("file", (filename, content, XLSX_MIME))


# ===========================================================================
# /upload response schema
# ===========================================================================

def test_upload_returns_exact_schema():
    """Response must contain exactly: total_rows, clean_rows, rejected_rows,
    clean_file, rejected_file — no extra fields."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"total_rows", "clean_rows", "rejected_rows", "clean_file", "rejected_file"}


def test_upload_total_rows_equals_clean_plus_rejected():
    """total_rows must always equal clean_rows + rejected_rows."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    assert response.status_code == 200
    body = response.json()
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]


def test_upload_clean_file_is_download_path():
    """clean_file must be a /download/ path."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    body = response.json()
    assert body["clean_file"].startswith("/download/")


def test_upload_rejected_file_is_download_path():
    """rejected_file must be a /download/ path."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    body = response.json()
    assert body["rejected_file"].startswith("/download/")


def test_upload_clean_file_ends_with_clean_csv():
    """clean_file path must end with _clean.csv."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    body = response.json()
    assert body["clean_file"].endswith("_clean.csv")


def test_upload_rejected_file_ends_with_rejected_csv():
    """rejected_file path must end with _rejected.csv."""
    content = make_valid_workbook()
    response = client.post("/upload", files=[make_xlsx_upload(content)])
    body = response.json()
    assert body["rejected_file"].endswith("_rejected.csv")


# ===========================================================================
# /download/{filename} — file serving
# ===========================================================================

def test_download_clean_file_returns_200():
    """Uploading a file then downloading the clean CSV returns HTTP 200."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    clean_path = upload.json()["clean_file"]
    response = client.get(clean_path)
    assert response.status_code == 200


def test_download_clean_file_is_valid_csv():
    """Downloaded clean CSV can be parsed as a valid DataFrame."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    clean_path = upload.json()["clean_file"]
    response = client.get(clean_path)
    df = pd.read_csv(io.StringIO(response.text))
    assert len(df.columns) > 0


def test_download_clean_file_has_correct_schema():
    """Downloaded clean CSV has the expected OUTPUT_SCHEMA columns."""
    from app.processing.schema import OUTPUT_SCHEMA
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    clean_path = upload.json()["clean_file"]
    response = client.get(clean_path)
    df = pd.read_csv(io.StringIO(response.text))
    assert list(df.columns) == OUTPUT_SCHEMA


def test_download_clean_file_row_count_matches_summary():
    """Row count in downloaded clean CSV matches clean_rows in summary."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    body = upload.json()
    clean_path = body["clean_file"]
    response = client.get(clean_path)
    df = pd.read_csv(io.StringIO(response.text))
    assert len(df) == body["clean_rows"]


def test_download_rejected_file_returns_200():
    """Downloading rejected CSV returns HTTP 200."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    rejected_path = upload.json()["rejected_file"]
    response = client.get(rejected_path)
    assert response.status_code == 200


def test_download_rejected_file_has_rejection_reason():
    """Downloaded rejected CSV has rejection_reason column."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    rejected_path = upload.json()["rejected_file"]
    response = client.get(rejected_path)
    df = pd.read_csv(io.StringIO(response.text))
    assert "rejection_reason" in df.columns


def test_download_rejected_file_row_count_matches_summary():
    """Row count in rejected CSV matches rejected_rows in summary."""
    content = make_valid_workbook()
    upload = client.post("/upload", files=[make_xlsx_upload(content)])
    body = upload.json()
    rejected_path = body["rejected_file"]
    response = client.get(rejected_path)
    df = pd.read_csv(io.StringIO(response.text))
    assert len(df) == body["rejected_rows"]


# ===========================================================================
# 404 and security
# ===========================================================================

def test_download_nonexistent_file_returns_404():
    """Requesting a file that does not exist returns HTTP 404."""
    response = client.get("/download/does_not_exist.csv")
    assert response.status_code == 404


def test_download_path_traversal_rejected():
    """Path traversal attempt in filename is rejected safely."""
    response = client.get("/download/../../etc/passwd")
    assert response.status_code in (400, 404)


def test_download_path_traversal_with_csv_extension_rejected():
    """Path traversal with .csv extension is rejected."""
    response = client.get("/download/../../../etc/passwd.csv")
    assert response.status_code in (400, 404)


# ===========================================================================
# Repeat upload determinism
# ===========================================================================

def test_repeat_upload_produces_different_filenames():
    """Uploading the same file twice produces different output filenames."""
    import time
    content = make_valid_workbook()
    upload1 = client.post("/upload", files=[make_xlsx_upload(content)])
    # Sleep required — timestamp is second-precision, >1s gap guarantees different filenames
    time.sleep(1.1)
    upload2 = client.post("/upload", files=[make_xlsx_upload(content)])
    assert upload1.json()["clean_file"] != upload2.json()["clean_file"]
    assert upload1.json()["rejected_file"] != upload2.json()["rejected_file"]


def test_repeat_upload_produces_same_row_counts():
    """Uploading the same file twice produces identical row counts."""
    content = make_valid_workbook()
    upload1 = client.post("/upload", files=[make_xlsx_upload(content)])
    upload2 = client.post("/upload", files=[make_xlsx_upload(content)])
    assert upload1.json()["total_rows"] == upload2.json()["total_rows"]
    assert upload1.json()["clean_rows"] == upload2.json()["clean_rows"]
    assert upload1.json()["rejected_rows"] == upload2.json()["rejected_rows"]
