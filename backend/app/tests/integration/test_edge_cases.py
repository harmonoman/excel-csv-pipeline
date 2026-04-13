"""
test_edge_cases.py — T7-3 Edge Case Integration Tests

Validates pipeline stability and correctness under degenerate and extreme
input conditions — all-rejected, all-clean, single row, header-only, and
large file throughput.

All tests use real .xlsx fixtures and real API endpoints.
No mocks, no internal function calls, no filename assertions.

Fixtures used (all from backend/tests/fixtures/):
    fixture_missing_columns.xlsx     — all rows rejected (no Last or Zip columns)
    fixture_perfect.xlsx             — all rows valid, zero rejections
    fixture_single_row_clean.xlsx    — exactly 1 valid data row
    fixture_single_row_rejected.xlsx — exactly 1 invalid data row
    fixture_empty_sheet.xlsx         — valid header, zero data rows
    fixture_large_10k.xlsx           — 10,000 rows, mixed valid/invalid
"""
import io
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FIXTURE_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures"

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

CLEAN_SCHEMA = [
    "First", "Last", "Address1", "City",
    "State", "Zip", "DonationDate", "DonationAmount", "Client",
]

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def upload_fixture(filename: str) -> dict:
    """POST a real fixture file to /upload, assert 200, return parsed JSON."""
    path = FIXTURE_DIR / filename
    with open(path, "rb") as f:
        content = f.read()
    response = client.post(
        "/upload",
        files=[("file", (filename, content, XLSX_MIME))],
    )
    assert response.status_code == 200, (
        f"Upload of '{filename}' failed — "
        f"status={response.status_code}: {response.text}"
    )
    return response.json()


def download_csv(download_path: str) -> pd.DataFrame:
    """GET /download/{filename}, assert 200, return CSV as DataFrame."""
    response = client.get(download_path)
    assert response.status_code == 200, (
        f"Download of '{download_path}' failed — status={response.status_code}"
    )
    # dtype={"Zip": str} prevents numeric coercion of 5-digit ZIP strings
    return pd.read_csv(io.StringIO(response.text), dtype={"Zip": str})


def assert_clean_schema(df: pd.DataFrame, label: str) -> None:
    """Assert clean CSV has exactly CLEAN_SCHEMA columns in correct order."""
    assert list(df.columns) == CLEAN_SCHEMA, (
        f"[{label}] Clean CSV schema mismatch.\n"
        f"  Expected: {CLEAN_SCHEMA}\n"
        f"  Got:      {list(df.columns)}"
    )


def assert_rejection_reasons_present(df: pd.DataFrame, label: str) -> None:
    """Assert every row in rejected CSV has a non-empty rejection_reason."""
    assert "rejection_reason" in df.columns, (
        f"[{label}] Rejected CSV missing 'rejection_reason' column"
    )
    empty = df[df["rejection_reason"].isna() | (df["rejection_reason"].str.strip() == "")]
    assert empty.empty, (
        f"[{label}] {len(empty)} rejected rows have empty rejection_reason"
    )


# ---------------------------------------------------------------------------
# T7-3 Edge Case Tests
# ---------------------------------------------------------------------------

def test_edge_all_rows_rejected():
    """
    fixture_missing_columns.xlsx — all 3 rows fail validation.

    Validates:
    - clean_rows = 0, rejected_rows = total_rows
    - Clean CSV has correct schema with zero data rows
    - Every rejected row has a non-empty rejection_reason
    - Row conservation: total = clean + rejected
    """
    body = upload_fixture("fixture_missing_columns.xlsx")

    assert body["total_rows"] == body["rejected_rows"], (
        f"Expected all rows rejected: "
        f"total={body['total_rows']} rejected={body['rejected_rows']}"
    )
    assert body["clean_rows"] == 0, (
        f"Expected 0 clean rows, got {body['clean_rows']}"
    )
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]

    # Clean CSV must exist with correct schema — zero data rows
    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "all_rejected/clean")
    assert len(clean_df) == 0, (
        f"Clean CSV must have zero data rows, got {len(clean_df)}"
    )

    # Rejected CSV must have all rows, each with a reason
    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == body["total_rows"], (
        f"Rejected CSV must contain all {body['total_rows']} rows, "
        f"got {len(rejected_df)}"
    )
    assert_rejection_reasons_present(rejected_df, "all_rejected/rejected")


def test_edge_all_rows_clean():
    """
    fixture_perfect.xlsx — all 5 rows pass validation.

    Validates:
    - rejected_rows = 0, clean_rows = total_rows
    - Rejected CSV has correct schema with zero data rows
    - rejection_reason column exists even when empty
    - Row conservation: total = clean + rejected
    """
    body = upload_fixture("fixture_perfect.xlsx")

    assert body["rejected_rows"] == 0, (
        f"Expected 0 rejected rows, got {body['rejected_rows']}"
    )
    assert body["clean_rows"] == body["total_rows"], (
        f"Expected all rows clean: "
        f"total={body['total_rows']} clean={body['clean_rows']}"
    )
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]

    # Clean CSV must have all rows
    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "all_clean/clean")
    assert len(clean_df) == body["total_rows"], (
        f"Clean CSV must contain all {body['total_rows']} rows, "
        f"got {len(clean_df)}"
    )

    # Rejected CSV must exist with correct schema — zero data rows
    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == 0, (
        f"Rejected CSV must have zero data rows, got {len(rejected_df)}"
    )
    assert "rejection_reason" in rejected_df.columns, (
        "Rejected CSV must contain rejection_reason column even when empty"
    )


def test_edge_single_row_clean():
    """
    fixture_single_row_clean.xlsx — exactly 1 valid data row.

    Validates:
    - Pipeline does not crash on minimal input
    - total_rows = 1, clean_rows = 1, rejected_rows = 0
    - Clean CSV has exactly 1 data row with correct schema
    - Rejected CSV has header only
    """
    body = upload_fixture("fixture_single_row_clean.xlsx")

    assert body["total_rows"] == 1, (
        f"Expected total_rows=1, got {body['total_rows']}"
    )
    assert body["clean_rows"] == 1
    assert body["rejected_rows"] == 0
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "single_row_clean/clean")
    assert len(clean_df) == 1, (
        f"Expected exactly 1 clean row, got {len(clean_df)}"
    )

    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == 0
    assert "rejection_reason" in rejected_df.columns


def test_edge_single_row_rejected():
    """
    fixture_single_row_rejected.xlsx — exactly 1 invalid data row (missing First).

    Validates:
    - Pipeline does not crash on minimal rejected input
    - total_rows = 1, clean_rows = 0, rejected_rows = 1
    - Clean CSV has header only
    - Rejected CSV has exactly 1 row with a non-empty rejection_reason
    """
    body = upload_fixture("fixture_single_row_rejected.xlsx")

    assert body["total_rows"] == 1
    assert body["clean_rows"] == 0
    assert body["rejected_rows"] == 1
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "single_row_rejected/clean")
    assert len(clean_df) == 0

    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == 1, (
        f"Expected exactly 1 rejected row, got {len(rejected_df)}"
    )
    assert_rejection_reasons_present(rejected_df, "single_row_rejected/rejected")

    # Confirm the specific rejection — first name is missing
    reason = rejected_df.iloc[0]["rejection_reason"]
    assert "Missing: First" in reason, (
        f"Expected 'Missing: First' in rejection reason, got: '{reason}'"
    )


def test_edge_header_only_sheet():
    """
    fixture_empty_sheet.xlsx — valid header row, zero data rows.

    Validates:
    - Pipeline does not crash on a structurally valid but empty sheet
    - total_rows = 0, clean_rows = 0, rejected_rows = 0
    - Both output CSVs exist with correct schema
    - No data rows in either output
    """
    body = upload_fixture("fixture_empty_sheet.xlsx")

    assert body["total_rows"] == 0, (
        f"Expected total_rows=0 for header-only sheet, got {body['total_rows']}"
    )
    assert body["clean_rows"] == 0
    assert body["rejected_rows"] == 0
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"]

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "header_only/clean")
    assert len(clean_df) == 0, (
        f"Clean CSV must have zero rows for header-only input, got {len(clean_df)}"
    )

    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == 0, (
        f"Rejected CSV must have zero rows for header-only input, got {len(rejected_df)}"
    )
    assert "rejection_reason" in rejected_df.columns


def test_edge_large_file_throughput():
    """
    fixture_large_10k.xlsx — 10,000 data rows, mixed valid/invalid.

    Validates:
    - Pipeline handles large files without error or crash
    - Row conservation holds at scale
    - Both output CSVs are generated and downloadable
    - Clean CSV schema is correct at scale

    Note: no timing threshold asserted — MVP uses synchronous processing.
    This test validates stability and correctness only, not performance.
    """
    body = upload_fixture("fixture_large_10k.xlsx")

    assert body["total_rows"] == 10000, (
        f"Expected 10000 total rows, got {body['total_rows']}"
    )
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"], (
        f"Row conservation violated at scale: "
        f"total={body['total_rows']} != "
        f"clean={body['clean_rows']} + rejected={body['rejected_rows']}"
    )
    assert body["clean_rows"] == 9000, (
        f"Expected 9000 clean rows (every 10th row has invalid state 'XX'), "
        f"got {body['clean_rows']}"
    )
    assert body["rejected_rows"] == 1000, (
        f"Expected 1000 rejected rows (every 10th row has invalid state 'XX'), "
        f"got {body['rejected_rows']}"
    )

    # Both files must be downloadable and match summary counts
    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "large_10k/clean")
    assert len(clean_df) == body["clean_rows"], (
        f"Clean CSV row count mismatch: "
        f"expected {body['clean_rows']}, got {len(clean_df)}"
    )

    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == body["rejected_rows"], (
        f"Rejected CSV row count mismatch: "
        f"expected {body['rejected_rows']}, got {len(rejected_df)}"
    )
    assert_rejection_reasons_present(rejected_df, "large_10k/rejected")


def test_edge_row_conservation_invariant():
    """
    Row conservation across all edge case fixtures.

    clean_rows + rejected_rows == total_rows for every edge case including
    zero-row, single-row, all-rejected, all-clean, and large file inputs.
    """
    fixtures = [
        "fixture_missing_columns.xlsx",      # all rejected
        "fixture_perfect.xlsx",              # all clean
        "fixture_single_row_clean.xlsx",     # 1 clean
        "fixture_single_row_rejected.xlsx",  # 1 rejected
        "fixture_empty_sheet.xlsx",          # 0 rows
        "fixture_large_10k.xlsx",            # 10k rows
    ]
    for fixture in fixtures:
        body = upload_fixture(fixture)
        assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"], (
            f"Row conservation violated for {fixture}: "
            f"total={body['total_rows']} != "
            f"clean={body['clean_rows']} + rejected={body['rejected_rows']}"
        )


def test_edge_schema_invariant():
    """
    Clean CSV schema must be exactly correct across all edge case fixtures,
    including when clean_rows = 0 (header-only output).
    """
    fixtures = [
        "fixture_missing_columns.xlsx",   # clean_rows = 0
        "fixture_perfect.xlsx",           # clean_rows = 5
        "fixture_single_row_clean.xlsx",  # clean_rows = 1
        "fixture_empty_sheet.xlsx",       # clean_rows = 0
    ]
    for fixture in fixtures:
        body = upload_fixture(fixture)
        clean_df = download_csv(body["clean_file"])
        assert_clean_schema(clean_df, fixture)
