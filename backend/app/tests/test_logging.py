"""
Tests for T5-5 — basic logging layer.

Validates:
- log_pipeline_metrics() emits a structured PIPELINE_METRICS log line
- Log line contains all required fields: file, total_rows, clean_rows,
  rejected_rows, processing_time_ms
- Integration: full /upload request emits the metrics log line
- Edge cases: empty workbook, all rows rejected
"""
import io
import logging
import re
from fastapi.testclient import TestClient

from app.main import app
from app.logging_utils.metrics import log_pipeline_metrics
from app.tests.fixtures import build_workbook

client = TestClient(app)
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


# ---------------------------------------------------------------------------
# Unit tests — log_pipeline_metrics()
# ---------------------------------------------------------------------------

def test_metrics_log_contains_pipeline_metrics_tag(caplog):
    """Log line must contain PIPELINE_METRICS tag for easy grepping."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics(
            file_name="donations.xlsx",
            total_rows=10,
            clean_rows=8,
            rejected_rows=2,
            processing_time_ms=123,
        )
    assert any("PIPELINE_METRICS" in r.message for r in caplog.records)


def test_metrics_log_contains_filename(caplog):
    """Log line must include the uploaded filename."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics(
            file_name="alpha_fund.xlsx",
            total_rows=5,
            clean_rows=5,
            rejected_rows=0,
            processing_time_ms=50,
        )
    assert any("alpha_fund.xlsx" in r.message for r in caplog.records)


def test_metrics_log_contains_total_rows(caplog):
    """Log line must include total_rows value."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("f.xlsx", 42, 40, 2, 100)
    assert any("total_rows=42" in r.message for r in caplog.records)


def test_metrics_log_contains_clean_rows(caplog):
    """Log line must include clean_rows value."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("f.xlsx", 42, 40, 2, 100)
    assert any("clean_rows=40" in r.message for r in caplog.records)


def test_metrics_log_contains_rejected_rows(caplog):
    """Log line must include rejected_rows value."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("f.xlsx", 42, 40, 2, 100)
    assert any("rejected_rows=2" in r.message for r in caplog.records)


def test_metrics_log_contains_processing_time(caplog):
    """Log line must include processing_time_ms value."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("f.xlsx", 10, 10, 0, 342)
    assert any("processing_time_ms=342" in r.message for r in caplog.records)


def test_metrics_log_single_line(caplog):
    """Metrics must be emitted as a single log record — not split across lines."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("f.xlsx", 10, 8, 2, 99)
    metrics_records = [r for r in caplog.records if "PIPELINE_METRICS" in r.message]
    assert len(metrics_records) == 1


def test_metrics_log_zero_rows(caplog):
    """Empty workbook (zero rows) still emits a valid metrics log line."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("empty.xlsx", 0, 0, 0, 5)
    assert any("PIPELINE_METRICS" in r.message for r in caplog.records)
    assert any("total_rows=0" in r.message for r in caplog.records)


def test_metrics_log_all_rejected(caplog):
    """All rows rejected still emits a valid metrics log line."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        log_pipeline_metrics("bad_data.xlsx", 20, 0, 20, 88)
    assert any("clean_rows=0" in r.message for r in caplog.records)
    assert any("rejected_rows=20" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Integration tests — /upload emits metrics log
# ---------------------------------------------------------------------------

def make_valid_workbook() -> bytes:
    buf = build_workbook([{
        "name": "Alpha Fund",
        "rows": [
            ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
            ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
            ["Jane", None, "456 Oak Ave", "Memphis", "XX", "1234", "bad-date", "-50"],
        ]
    }])
    return buf.read()


def make_empty_workbook() -> bytes:
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Instructions"
    ws.append(["This sheet has no data"])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def make_xlsx_upload(content: bytes, filename: str = "donations.xlsx"):
    return ("file", (filename, content, XLSX_MIME))


def test_upload_emits_pipeline_metrics_log(caplog):
    """Full /upload request emits a PIPELINE_METRICS log line."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        client.post("/upload", files=[make_xlsx_upload(make_valid_workbook())])
    assert any("PIPELINE_METRICS" in r.message for r in caplog.records)


def test_upload_metrics_log_contains_filename(caplog):
    """PIPELINE_METRICS log includes the uploaded filename."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        client.post("/upload", files=[make_xlsx_upload(make_valid_workbook(), "test_upload.xlsx")])
    assert any("test_upload.xlsx" in r.message for r in caplog.records)


def test_upload_metrics_log_row_counts_match_response(caplog):
    """PIPELINE_METRICS log row counts match the API response."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        response = client.post("/upload", files=[make_xlsx_upload(make_valid_workbook())])
    body = response.json()
    metrics_record = next(r for r in caplog.records if "PIPELINE_METRICS" in r.message)
    assert f"total_rows={body['total_rows']}" in metrics_record.message
    assert f"clean_rows={body['clean_rows']}" in metrics_record.message
    assert f"rejected_rows={body['rejected_rows']}" in metrics_record.message


def test_upload_metrics_log_processing_time_positive(caplog):
    """PIPELINE_METRICS log includes a positive processing_time_ms."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        client.post("/upload", files=[make_xlsx_upload(make_valid_workbook())])
    metrics_record = next(r for r in caplog.records if "PIPELINE_METRICS" in r.message)
    # Extract processing_time_ms value and confirm it's > 0
    match = re.search(r'processing_time_ms=(\d+)', metrics_record.message)
    assert match is not None
    assert int(match.group(1)) > 0


def test_upload_empty_workbook_emits_metrics(caplog):
    """Empty workbook upload still emits PIPELINE_METRICS log with zero rows."""
    with caplog.at_level(logging.INFO, logger="app.logging_utils.metrics"):
        client.post("/upload", files=[make_xlsx_upload(make_empty_workbook())])
    assert any("PIPELINE_METRICS" in r.message for r in caplog.records)
    assert any("total_rows=0" in r.message for r in caplog.records)
