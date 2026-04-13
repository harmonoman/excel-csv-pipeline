"""
test_full_pipeline.py — T7-2 Full Pipeline Integration Tests

Tests the complete pipeline end-to-end using real .xlsx fixtures and real
API endpoints — no mocks, no internal function calls.

Flow under test:
    upload → parse → map → normalize → validate → split → schema → CSV → download

Fixtures used (all from backend/tests/fixtures/):
    fixture_perfect.xlsx       — all rows valid, header row 1
    fixture_header_offset.xlsx — metadata rows before header, all rows valid
    fixture_missing_columns.xlsx — missing Last + Zip, all rows rejected
    fixture_mixed_dates.xlsx   — 4 valid + 1 rejected (invalid date)
    fixture_multi_sheet.xlsx   — 3 sheets, different aliases, all rows valid
    fixture_empty_sheet.xlsx   — valid header, zero data rows

Every test asserts file CONTENT, not filenames (timestamps vary per run).
"""
import io
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.main import app

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FIXTURE_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures"

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Exact output schema required by input_contract.md and enforced by schema.py
CLEAN_SCHEMA = [
    "First", "Last", "Address1", "City",
    "State", "Zip", "DonationDate", "DonationAmount", "Client",
]

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def upload_fixture(filename: str) -> dict:
    """
    POST a fixture file to /upload and return the parsed JSON response.
    Asserts HTTP 200 before returning — any upstream failure fails here.
    """
    path = FIXTURE_DIR / filename
    with open(path, "rb") as f:
        content = f.read()

    response = client.post(
        "/upload",
        files=[("file", (filename, content, XLSX_MIME))],
    )
    assert response.status_code == 200, (
        f"Upload of '{filename}' failed with {response.status_code}: {response.text}"
    )
    return response.json()


def download_csv(download_path: str) -> pd.DataFrame:
    """
    GET a /download/{filename} path and return the CSV contents as a DataFrame.
    Asserts HTTP 200 before returning.
    """
    response = client.get(download_path)
    assert response.status_code == 200, (
        f"Download of '{download_path}' failed with {response.status_code}"
    )
    # dtype={"Zip": str} prevents pandas from coercing numeric-looking ZIPs
    # (e.g. "37201") to int64 on read — they must remain strings per contract.
    return pd.read_csv(io.StringIO(response.text), dtype={"Zip": str})


def assert_response_schema(body: dict, fixture_name: str) -> None:
    """Assert the API response contains all required top-level keys."""
    required = {"total_rows", "clean_rows", "rejected_rows", "clean_file", "rejected_file"}
    missing = required - set(body.keys())
    assert not missing, (
        f"[{fixture_name}] API response missing keys: {missing}"
    )


def assert_row_conservation(body: dict, fixture_name: str) -> None:
    """Assert clean + rejected == total — no rows lost or duplicated."""
    assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"], (
        f"[{fixture_name}] Row count mismatch: "
        f"total={body['total_rows']} != "
        f"clean={body['clean_rows']} + rejected={body['rejected_rows']}"
    )


def assert_clean_schema(df: pd.DataFrame, fixture_name: str) -> None:
    """Assert clean CSV has exactly the required columns in the correct order."""
    actual = list(df.columns)
    assert actual == CLEAN_SCHEMA, (
        f"[{fixture_name}] Clean CSV schema mismatch.\n"
        f"  Expected: {CLEAN_SCHEMA}\n"
        f"  Got:      {actual}"
    )


def assert_rejected_schema(df: pd.DataFrame, fixture_name: str) -> None:
    """Assert every row in rejected CSV has a non-empty rejection_reason."""
    assert "rejection_reason" in df.columns, (
        f"[{fixture_name}] Rejected CSV missing 'rejection_reason' column"
    )
    empty_reasons = df[df["rejection_reason"].isna() | (df["rejection_reason"].str.strip() == "")]
    assert empty_reasons.empty, (
        f"[{fixture_name}] {len(empty_reasons)} rejected rows have empty rejection_reason"
    )


# ---------------------------------------------------------------------------
# T7-2 Integration Tests
# ---------------------------------------------------------------------------

def test_full_pipeline_happy_path():
    """
    fixture_perfect.xlsx — all 5 rows valid, zero rejections.

    Validates:
    - 200 response with correct structure
    - clean_rows = 5, rejected_rows = 0
    - Clean CSV has exact schema
    - Clean CSV has 5 rows of data
    - Rejected CSV has header only (zero data rows)
    - Client = "Green Valley Fund" on all rows (from sheet tab name)
    """
    body = upload_fixture("fixture_perfect.xlsx")
    assert_response_schema(body, "fixture_perfect")
    assert_row_conservation(body, "fixture_perfect")

    assert body["total_rows"] == 5
    assert body["clean_rows"] == 5
    assert body["rejected_rows"] == 0

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "fixture_perfect")
    assert len(clean_df) == 5, f"Expected 5 clean rows, got {len(clean_df)}"

    # Verify normalizer ran correctly — title case, ZIP preservation
    assert clean_df.iloc[0]["First"] == "Alice"
    assert clean_df.iloc[0]["Last"] == "Anderson"
    # ZIP values must be 5-character strings (leading zeros preserved, no numeric coercion)
    assert not pd.api.types.is_numeric_dtype(clean_df["Zip"]), "Zip must be stored as string, not numeric"
    assert all(len(str(z)) == 5 for z in clean_df["Zip"]), (
        f"All ZIPs must be 5 characters, got: {list(clean_df['Zip'])}"
    )

    # Client must be derived from the sheet tab name — never from cell data
    assert (clean_df["Client"] == "Green Valley Fund").all(), (
        f"Expected all Client values to be 'Green Valley Fund', "
        f"got: {clean_df['Client'].unique()}"
    )

    rejected_df = download_csv(body["rejected_file"])
    assert len(rejected_df) == 0, (
        f"Expected 0 rejected rows, got {len(rejected_df)}"
    )
    assert "rejection_reason" in rejected_df.columns, (
        "Rejected CSV must contain rejection_reason column even when empty"
    )


def test_full_pipeline_header_offset():
    """
    fixture_header_offset.xlsx — 3 metadata rows before header, all 3 data rows valid.

    Validates:
    - Parser correctly detects header at row 4 (not row 1)
    - Metadata rows are not present in output
    - All data rows flow through to clean CSV
    - Client = "Alpha Fund"
    """
    body = upload_fixture("fixture_header_offset.xlsx")
    assert_response_schema(body, "fixture_header_offset")
    assert_row_conservation(body, "fixture_header_offset")

    assert body["total_rows"] == 3, (
        f"Expected 3 data rows (metadata must be excluded), got {body['total_rows']}"
    )
    assert body["clean_rows"] == 3
    assert body["rejected_rows"] == 0

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "fixture_header_offset")
    assert len(clean_df) == 3

    assert (clean_df["Client"] == "Alpha Fund").all(), (
        f"Expected Client = 'Alpha Fund', got: {clean_df['Client'].unique()}"
    )


def test_full_pipeline_all_rejected():
    """
    fixture_missing_columns.xlsx — Last and Zip columns absent, all 3 rows rejected.

    Validates:
    - clean_rows = 0, rejected_rows = 3
    - Every rejected row has non-empty rejection_reason
    - Rejection reasons reference both missing fields
    - Clean CSV has header only (zero data rows)
    """
    body = upload_fixture("fixture_missing_columns.xlsx")
    assert_response_schema(body, "fixture_missing_columns")
    assert_row_conservation(body, "fixture_missing_columns")

    assert body["total_rows"] == 3
    assert body["clean_rows"] == 0, (
        f"Expected 0 clean rows (all must be rejected), got {body['clean_rows']}"
    )
    assert body["rejected_rows"] == 3

    rejected_df = download_csv(body["rejected_file"])
    assert_rejected_schema(rejected_df, "fixture_missing_columns")
    assert len(rejected_df) == 3

    # Every row must reference both missing fields
    for _, row in rejected_df.iterrows():
        reason = row["rejection_reason"]
        assert "Missing: Last" in reason, (
            f"Expected 'Missing: Last' in rejection reason, got: '{reason}'"
        )
        assert "Missing: Zip" in reason, (
            f"Expected 'Missing: Zip' in rejection reason, got: '{reason}'"
        )

    clean_df = download_csv(body["clean_file"])
    assert len(clean_df) == 0, (
        f"Expected 0 clean rows, got {len(clean_df)}"
    )
    assert_clean_schema(clean_df, "fixture_missing_columns")


def test_full_pipeline_empty_workbook():
    """
    fixture_empty_sheet.xlsx — valid header, zero data rows.

    Validates:
    - Pipeline handles an empty sheet without error
    - total_rows = 0, clean_rows = 0, rejected_rows = 0
    - Clean CSV exists with correct schema but zero data rows
    """
    body = upload_fixture("fixture_empty_sheet.xlsx")
    assert_response_schema(body, "fixture_empty_sheet")
    assert_row_conservation(body, "fixture_empty_sheet")

    assert body["total_rows"] == 0
    assert body["clean_rows"] == 0
    assert body["rejected_rows"] == 0

    clean_df = download_csv(body["clean_file"])
    assert list(clean_df.columns) == CLEAN_SCHEMA
    assert len(clean_df) == 0


def test_full_pipeline_mixed_data():
    """
    fixture_mixed_dates.xlsx — 4 valid rows + 1 invalid date row.

    Validates:
    - clean_rows = 4, rejected_rows = 1
    - Multiple date formats parsed correctly in clean rows
    - Invalid date row rejected with appropriate reason
    - Row conservation holds
    """
    body = upload_fixture("fixture_mixed_dates.xlsx")
    assert_response_schema(body, "fixture_mixed_dates")
    assert_row_conservation(body, "fixture_mixed_dates")

    assert body["total_rows"] == 5
    assert body["clean_rows"] == 4
    assert body["rejected_rows"] == 1

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "fixture_mixed_dates")
    assert len(clean_df) == 4

    # All clean donation dates must be parseable — normalizer produced ISO strings
    for val in clean_df["DonationDate"]:
        try:
            pd.to_datetime(str(val))
        except Exception:
            pytest.fail(f"Clean CSV contains unparseable DonationDate: '{val}'")

    rejected_df = download_csv(body["rejected_file"])
    assert_rejected_schema(rejected_df, "fixture_mixed_dates")
    assert len(rejected_df) == 1

    # The invalid date row is rejected at T4-1 (normalizer converts to NaN first)
    reason = rejected_df.iloc[0]["rejection_reason"]
    assert "Missing: DonationDate" in reason, (
        f"Expected 'Missing: DonationDate' in rejection reason, got: '{reason}'"
    )


def test_full_pipeline_multi_sheet():
    """
    fixture_multi_sheet.xlsx — 3 sheets, different aliases, one with metadata offset.

    Validates:
    - All 7 rows across 3 sheets are parsed and processed
    - Each sheet's alias set maps correctly to canonical columns
    - Client values reflect sheet tab names (not cell data)
    - Schema is enforced consistently across all sheets
    """
    body = upload_fixture("fixture_multi_sheet.xlsx")
    assert_response_schema(body, "fixture_multi_sheet")
    assert_row_conservation(body, "fixture_multi_sheet")

    assert body["total_rows"] == 7
    assert body["clean_rows"] == 7
    assert body["rejected_rows"] == 0

    clean_df = download_csv(body["clean_file"])
    assert_clean_schema(clean_df, "fixture_multi_sheet")
    assert len(clean_df) == 7

    # All three sheet tab names must appear as Client values
    client_values = set(clean_df["Client"].unique())
    expected_clients = {"Horizon PAC", "Liberty Fund", "Eagle Society"}
    assert client_values == expected_clients, (
        f"Expected Client values {expected_clients}, got {client_values}"
    )

    # Row count per client must match fixture structure
    counts = clean_df["Client"].value_counts().to_dict()
    assert counts.get("Horizon PAC") == 3, f"Expected 3 Horizon PAC rows, got {counts.get('Horizon PAC')}"
    assert counts.get("Liberty Fund") == 2, f"Expected 2 Liberty Fund rows, got {counts.get('Liberty Fund')}"
    assert counts.get("Eagle Society") == 2, f"Expected 2 Eagle Society rows, got {counts.get('Eagle Society')}"


def test_full_pipeline_deterministic_output():
    """
    Run fixture_perfect.xlsx twice and compare CSV contents.

    Validates:
    - Same input always produces identical output data
    - Filenames may match (second-precision timestamps) but content is identical
    - Pipeline is free of randomness, ordering drift, or state leakage
    """
    body1 = upload_fixture("fixture_perfect.xlsx")
    body2 = upload_fixture("fixture_perfect.xlsx")

    # Note: filenames may be identical if both uploads complete within the same
    # second — this is a known MVP limitation (second-precision timestamps).
    # The determinism assertion is on CSV *content*, not filenames.

    clean1 = download_csv(body1["clean_file"])
    clean2 = download_csv(body2["clean_file"])

    pd.testing.assert_frame_equal(
        clean1.reset_index(drop=True),
        clean2.reset_index(drop=True),
        check_like=False,  # enforce column order
        obj="Clean CSV (run 1 vs run 2)",
    )

    rejected1 = download_csv(body1["rejected_file"])
    rejected2 = download_csv(body2["rejected_file"])

    pd.testing.assert_frame_equal(
        rejected1.reset_index(drop=True),
        rejected2.reset_index(drop=True),
        obj="Rejected CSV (run 1 vs run 2)",
    )


def test_full_pipeline_row_conservation_invariant():
    """
    Verify the row conservation invariant holds across all fixtures.

    clean_rows + rejected_rows == total_rows for every upload — no row
    is ever silently lost, duplicated, or miscounted.
    """
    fixtures = [
        "fixture_perfect.xlsx",
        "fixture_header_offset.xlsx",
        "fixture_missing_columns.xlsx",
        "fixture_mixed_dates.xlsx",
        "fixture_multi_sheet.xlsx",
        "fixture_empty_sheet.xlsx",
    ]
    for fixture in fixtures:
        body = upload_fixture(fixture)
        assert body["total_rows"] == body["clean_rows"] + body["rejected_rows"], (
            f"Row conservation violated for {fixture}: "
            f"total={body['total_rows']} != "
            f"clean={body['clean_rows']} + rejected={body['rejected_rows']}"
        )


def test_full_pipeline_clean_schema_invariant():
    """
    Verify the clean CSV schema is exactly correct across all fixtures.

    Schema enforcement must hold regardless of which aliases were used in
    the source file, how many sheets were present, or which rows were rejected.
    """
    fixtures = [
        "fixture_perfect.xlsx",
        "fixture_header_offset.xlsx",
        "fixture_mixed_dates.xlsx",
        "fixture_multi_sheet.xlsx",
    ]
    for fixture in fixtures:
        body = upload_fixture(fixture)
        if body["clean_rows"] > 0:
            clean_df = download_csv(body["clean_file"])
            assert_clean_schema(clean_df, fixture)
        else:
            # Even with zero clean rows the CSV must exist with correct headers
            clean_df = download_csv(body["clean_file"])
            assert list(clean_df.columns) == CLEAN_SCHEMA, (
                f"[{fixture}] Empty clean CSV has wrong schema: {list(clean_df.columns)}"
            )
