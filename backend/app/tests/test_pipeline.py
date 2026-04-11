"""
Tests for app/processing/pipeline.py — pipeline orchestrator.

Orchestrator responsibilities (ONLY):
- Execute stages in correct order
- Pass output of each stage to the next
- Halt immediately on any stage failure
- Return structured result dict

NOTE: map_columns no longer lives in the pipeline orchestrator.
It is called per-sheet inside parse_workbook() before concatenation.
Pipeline input is already canonically mapped.
"""
import pytest
import pandas as pd
from unittest.mock import patch
from app.processing.pipeline import run_pipeline, PipelineError
from app.tests.fixtures import build_workbook


# --- Shared minimal config ---
MAPPING_CONFIG = {
    "header_scan_rows": 20,
    "fields": {
        "First": ["first_name", "fname", "first"],
        "Last": ["lastname", "last_name", "lname", "last"],
        "Address1": ["address1", "address", "addr"],
        "City": ["city"],
        "State": ["st", "state", "state_code"],
        "Zip": ["zip", "zip_code", "zipcode"],
        "DonationDate": ["giftdate", "gift_date", "donationdate", "donation_date", "date"],
        "DonationAmount": ["amount", "donationamount", "donation_amount", "gift_amount"],
    },
}


# ---------------------------------------------------------------------------
# Happy path — mocked stages verify execution order and return structure
# ---------------------------------------------------------------------------

def test_pipeline_executes_stages_in_correct_order():
    """
    All stages execute in correct order with mocked implementations.
    Input df already has canonical column names (mapping happened in parser).
    Verifies orchestrator calls stages sequentially and chains outputs correctly.
    """
    # Input already has canonical names — mapping happened in parse_workbook
    canonical_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    normalized_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    client_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"], "Client": ["Alpha Fund"]})
    validated_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"], "Client": ["Alpha Fund"], "_is_valid": [True]})
    clean_df = pd.DataFrame({"First": ["John"], "Client": ["Alpha Fund"]})
    rejected_df = pd.DataFrame()
    schema_df = pd.DataFrame({"First": ["John"], "Client": ["Alpha Fund"]})

    with patch("app.processing.pipeline.normalize", return_value=normalized_df) as mock_normalize, \
         patch("app.processing.pipeline.inject_client", return_value=client_df) as mock_client, \
         patch("app.processing.pipeline.validate_rows", return_value=validated_df) as mock_validate, \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)) as mock_split, \
         patch("app.processing.pipeline.enforce_schema", return_value=schema_df) as mock_schema:

        result = run_pipeline(canonical_df, MAPPING_CONFIG)

        # Verify each stage was called exactly once
        mock_normalize.assert_called_once()
        mock_client.assert_called_once()
        mock_validate.assert_called_once()
        mock_split.assert_called_once()
        mock_schema.assert_called_once()

        # Verify correct chaining — each stage received the previous stage's output
        pd.testing.assert_frame_equal(mock_normalize.call_args[0][0], canonical_df)
        pd.testing.assert_frame_equal(mock_client.call_args[0][0], normalized_df)
        pd.testing.assert_frame_equal(mock_validate.call_args[0][0], client_df)
        pd.testing.assert_frame_equal(mock_split.call_args[0][0], validated_df)
        pd.testing.assert_frame_equal(mock_schema.call_args[0][0], clean_df)


def test_pipeline_returns_correct_result_structure():
    """run_pipeline returns dict with clean_df, rejected_df, and summary."""
    canonical_df = pd.DataFrame({"First": ["John", "Jane"], "_source_sheet": ["Alpha Fund", "Alpha Fund"]})
    clean_df = pd.DataFrame({"First": ["John"]})
    rejected_df = pd.DataFrame({"First": ["Jane"], "rejection_reason": ["Missing: Last"]})
    schema_df = pd.DataFrame({"First": ["John"]})

    with patch("app.processing.pipeline.normalize", return_value=canonical_df), \
         patch("app.processing.pipeline.inject_client", return_value=canonical_df), \
         patch("app.processing.pipeline.validate_rows", return_value=canonical_df), \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)), \
         patch("app.processing.pipeline.enforce_schema", return_value=schema_df):

        result = run_pipeline(canonical_df, MAPPING_CONFIG)

        assert "clean_df" in result
        assert "rejected_df" in result
        assert "summary" in result
        assert isinstance(result["clean_df"], pd.DataFrame)
        assert isinstance(result["rejected_df"], pd.DataFrame)
        assert result["summary"]["total_rows"] == 2
        assert result["summary"]["clean_rows"] == 1
        assert result["summary"]["rejected_rows"] == 1
        assert result["summary"]["total_rows"] == (
            result["summary"]["clean_rows"] + result["summary"]["rejected_rows"]
        )


def test_pipeline_empty_dataframe_completes_without_error():
    """Empty DataFrame (zero rows) completes all stages without error."""
    empty_df = pd.DataFrame(columns=["First", "Last", "_source_sheet"])

    result = run_pipeline(empty_df, MAPPING_CONFIG)

    assert result["summary"]["total_rows"] == 0
    assert result["summary"]["clean_rows"] == 0
    assert result["summary"]["rejected_rows"] == 0
    assert isinstance(result["clean_df"], pd.DataFrame)
    assert isinstance(result["rejected_df"], pd.DataFrame)


# ---------------------------------------------------------------------------
# Failure propagation — any stage failure halts pipeline
# ---------------------------------------------------------------------------

def test_pipeline_halts_on_normalize_stage_failure():
    """Exception in normalize stage halts pipeline and raises PipelineError."""
    canonical_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})

    with patch("app.processing.pipeline.normalize", side_effect=RuntimeError("normalize failed")), \
         patch("app.processing.pipeline.inject_client") as mock_client:

        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(canonical_df, MAPPING_CONFIG)

        mock_client.assert_not_called()
        assert exc_info.value.stage == "normalize"


def test_pipeline_halts_on_validate_stage_failure():
    """Exception in validate_rows stage halts pipeline and raises PipelineError."""
    canonical_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})

    with patch("app.processing.pipeline.normalize", return_value=canonical_df), \
         patch("app.processing.pipeline.inject_client", return_value=canonical_df), \
         patch("app.processing.pipeline.validate_rows", side_effect=Exception("validator crashed")), \
         patch("app.processing.pipeline.split_rows") as mock_split:

        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(canonical_df, MAPPING_CONFIG)

        mock_split.assert_not_called()
        assert exc_info.value.stage == "validate_rows"


def test_pipeline_halts_on_enforce_schema_failure():
    """Exception in enforce_schema stage halts pipeline and raises PipelineError."""
    canonical_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    clean_df = pd.DataFrame({"First": ["John"]})
    rejected_df = pd.DataFrame()

    with patch("app.processing.pipeline.normalize", return_value=canonical_df), \
         patch("app.processing.pipeline.inject_client", return_value=canonical_df), \
         patch("app.processing.pipeline.validate_rows", return_value=canonical_df), \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)), \
         patch("app.processing.pipeline.enforce_schema", side_effect=RuntimeError("schema crash")):

        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(canonical_df, MAPPING_CONFIG)

        assert exc_info.value.stage == "enforce_schema"


def test_pipeline_error_contains_stage_and_message():
    """PipelineError exposes stage name, error type, and original message."""
    canonical_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})

    with patch("app.processing.pipeline.normalize", side_effect=ValueError("normalize blew up")):
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(canonical_df, MAPPING_CONFIG)

    error = exc_info.value
    assert error.stage == "normalize"
    assert error.error_type == "ValueError"
    assert "normalize blew up" in error.error_message


# ---------------------------------------------------------------------------
# Integration tests — real fixtures, no mocks
# ---------------------------------------------------------------------------

def test_pipeline_integration_full_flow():
    """
    Integration: real workbook through full pipeline with no mocks.
    Verifies correct clean/rejected counts, summary accuracy,
    output structure, and deterministic results.
    """
    from app.processing.parser import parse_workbook

    wb = build_workbook([{
        "name": "Alpha Fund",
        "rows": [
            ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
            ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
            ["Jane", "Smith", "456 Oak Ave", "Memphis", "TN", "38101", "2024-01-02", "200.00"],
            ["Alice", None, "789 Pine Rd", "Knoxville", "TN", "37901", "2024-01-03", "300.00"],
        ],
    }])

    parsed_df = parse_workbook(wb, MAPPING_CONFIG)
    result = run_pipeline(parsed_df, MAPPING_CONFIG)

    assert result["summary"]["clean_rows"] + result["summary"]["rejected_rows"] == result["summary"]["total_rows"]
    assert result["summary"]["clean_rows"] == 2
    assert result["summary"]["rejected_rows"] == 1

    clean = result["clean_df"]
    assert isinstance(clean, pd.DataFrame)
    assert "First" in clean.columns
    assert "Client" in clean.columns
    assert clean.iloc[0]["Client"] == "Alpha Fund"
    assert "_source_sheet" not in clean.columns
    assert "_is_valid" not in clean.columns
    assert "_rejection_reason" not in clean.columns

    rejected = result["rejected_df"]
    assert isinstance(rejected, pd.DataFrame)
    assert "rejection_reason" in rejected.columns
    assert len(rejected) == 1

    # Determinism
    wb2 = build_workbook([{
        "name": "Alpha Fund",
        "rows": [
            ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
            ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
            ["Jane", "Smith", "456 Oak Ave", "Memphis", "TN", "38101", "2024-01-02", "200.00"],
            ["Alice", None, "789 Pine Rd", "Knoxville", "TN", "37901", "2024-01-03", "300.00"],
        ],
    }])
    parsed_df2 = parse_workbook(wb2, MAPPING_CONFIG)
    result2 = run_pipeline(parsed_df2, MAPPING_CONFIG)
    assert result["summary"] == result2["summary"]


def test_pipeline_integration_real_world_metadata_format():
    """
    Integration: confirmed real-world Alpha Fund format with metadata rows
    before the header AND multi-sheet workbook with different column aliases
    per sheet.

    Now that mapping happens per-sheet inside parse_workbook(), sheets with
    different aliases (fname/lname vs First/Last) are correctly handled —
    each sheet is mapped to canonical names before concatenation.

    Structure:
        Alpha Fund  — 3 metadata rows, header row 4, aliases: First/Last/GiftDate/Amount
        Liberty PAC — no metadata, aliases: fname/lname/gift_date/gift_amount
        Instructions — no valid header, excluded
    """
    from app.processing.parser import parse_workbook

    wb = build_workbook([
        {
            "name": "Alpha Fund",
            "rows": [
                ["Prepared for internal review", None, None, None, None, None, None, None],
                ["Client: Alpha Fund", None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
                ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
                ["Jane", "Smith", "456 Oak Ave", "Memphis", "TN", "38101", "2024-01-02", "200.00"],
            ],
        },
        {
            "name": "Liberty PAC",
            "rows": [
                # Different aliases — now correctly handled by per-sheet mapping
                ["fname", "lname", "address1", "city", "st", "zip", "gift_date", "gift_amount"],
                ["Alice", "Johnson", "789 Pine Rd", "Austin", "TX", "78701", "2024-01-03", "500.00"],
                # Invalid row — missing Last name
                ["Bob", None, "321 Elm St", "Dallas", "TX", "75201", "2024-01-04", "300.00"],
            ],
        },
        {
            "name": "Instructions",
            "rows": [
                ["This sheet contains setup instructions", None],
                ["Do not modify or delete this tab", None],
            ],
        },
    ])

    parsed_df = parse_workbook(wb, MAPPING_CONFIG)
    result = run_pipeline(parsed_df, MAPPING_CONFIG)

    # Instructions sheet excluded (no recognizable header)
    # Alpha Fund: 2 valid rows
    # Liberty PAC: 1 valid (Alice), 1 rejected (Bob — missing Last)
    assert result["summary"]["total_rows"] == 4
    assert result["summary"]["clean_rows"] == 3
    assert result["summary"]["rejected_rows"] == 1
    assert (
        result["summary"]["clean_rows"] + result["summary"]["rejected_rows"]
        == result["summary"]["total_rows"]
    )

    clean = result["clean_df"]
    assert isinstance(clean, pd.DataFrame)
    assert "Client" in clean.columns
    assert "_source_sheet" not in clean.columns
    assert "_is_valid" not in clean.columns
    assert set(clean["Client"].unique()) == {"Alpha Fund", "Liberty PAC"}

    rejected = result["rejected_df"]
    assert len(rejected) == 1
    assert "rejection_reason" in rejected.columns