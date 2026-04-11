"""
Tests for app/processing/pipeline.py — pipeline orchestrator.
 
Orchestrator responsibilities (ONLY):
- Execute stages in correct order
- Pass output of each stage to the next
- Halt immediately on any stage failure
- Return structured result dict
 
Does NOT:
- Implement transformation logic
- Validate data
- Modify DataFrames beyond passing them through stages
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
    Verifies the orchestrator calls stages sequentially and passes
    output of each as input to the next.
    """
    raw_df = pd.DataFrame({"first": ["John"], "_source_sheet": ["Alpha Fund"]})
    mapped_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    normalized_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    client_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"], "Client": ["Alpha Fund"]})
    validated_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"], "Client": ["Alpha Fund"], "_is_valid": [True]})
    clean_df = pd.DataFrame({"First": ["John"], "Client": ["Alpha Fund"]})
    rejected_df = pd.DataFrame()
    schema_df = pd.DataFrame({"First": ["John"], "Client": ["Alpha Fund"]})
 
    with patch("app.processing.pipeline.map_columns", return_value=mapped_df) as mock_map, \
         patch("app.processing.pipeline.normalize", return_value=normalized_df) as mock_normalize, \
         patch("app.processing.pipeline.inject_client", return_value=client_df) as mock_client, \
         patch("app.processing.pipeline.validate_rows", return_value=validated_df) as mock_validate, \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)) as mock_split, \
         patch("app.processing.pipeline.enforce_schema", return_value=schema_df) as mock_schema:
 
        result = run_pipeline(raw_df, MAPPING_CONFIG)
 
        # Verify each stage was called exactly once
        mock_map.assert_called_once()
        mock_normalize.assert_called_once()
        mock_client.assert_called_once()
        mock_validate.assert_called_once()
        mock_split.assert_called_once()
        mock_schema.assert_called_once()
 
        # Verify correct chaining — each stage received the previous stage's output
        pd.testing.assert_frame_equal(mock_map.call_args[0][0], raw_df)
        pd.testing.assert_frame_equal(mock_normalize.call_args[0][0], mapped_df)
        pd.testing.assert_frame_equal(mock_client.call_args[0][0], normalized_df)
        pd.testing.assert_frame_equal(mock_validate.call_args[0][0], client_df)
        pd.testing.assert_frame_equal(mock_split.call_args[0][0], validated_df)
        pd.testing.assert_frame_equal(mock_schema.call_args[0][0], clean_df)
 
 
def test_pipeline_returns_correct_result_structure():
    """run_pipeline returns dict with clean_df, rejected_df, and summary."""
    raw_df = pd.DataFrame({"first": ["John", "Jane"], "_source_sheet": ["Alpha Fund", "Alpha Fund"]})
    clean_df = pd.DataFrame({"First": ["John"]})
    rejected_df = pd.DataFrame({"First": ["Jane"], "rejection_reason": ["Missing: Last"]})
    schema_df = pd.DataFrame({"First": ["John"]})
 
    with patch("app.processing.pipeline.map_columns", return_value=raw_df), \
         patch("app.processing.pipeline.normalize", return_value=raw_df), \
         patch("app.processing.pipeline.inject_client", return_value=raw_df), \
         patch("app.processing.pipeline.validate_rows", return_value=raw_df), \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)), \
         patch("app.processing.pipeline.enforce_schema", return_value=schema_df):
 
        result = run_pipeline(raw_df, MAPPING_CONFIG)
 
        # Keys present
        assert "clean_df" in result
        assert "rejected_df" in result
        assert "summary" in result
 
        # DataFrame types
        assert isinstance(result["clean_df"], pd.DataFrame)
        assert isinstance(result["rejected_df"], pd.DataFrame)
 
        # Summary counts
        assert result["summary"]["total_rows"] == 2
        assert result["summary"]["clean_rows"] == 1
        assert result["summary"]["rejected_rows"] == 1
        assert result["summary"]["total_rows"] == (
            result["summary"]["clean_rows"] + result["summary"]["rejected_rows"]
        )
 
 
def test_pipeline_empty_dataframe_completes_without_error():
    """
    Empty DataFrame (zero rows) completes all stages without error.
    Returns clean_rows: 0 and rejected_rows: 0.
    """
    empty_df = pd.DataFrame(columns=["first", "last", "_source_sheet"])
 
    result = run_pipeline(empty_df, MAPPING_CONFIG)
 
    assert result["summary"]["total_rows"] == 0
    assert result["summary"]["clean_rows"] == 0
    assert result["summary"]["rejected_rows"] == 0
    assert isinstance(result["clean_df"], pd.DataFrame)
    assert isinstance(result["rejected_df"], pd.DataFrame)
 
 
# ---------------------------------------------------------------------------
# Failure propagation — any stage failure halts pipeline
# ---------------------------------------------------------------------------
 
def test_pipeline_halts_on_map_stage_failure():
    """Exception in map_columns stage halts pipeline and raises PipelineError."""
    raw_df = pd.DataFrame({"first": ["John"], "_source_sheet": ["Alpha Fund"]})
 
    with patch("app.processing.pipeline.map_columns", side_effect=ValueError("bad config")), \
         patch("app.processing.pipeline.normalize") as mock_normalize:
 
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw_df, MAPPING_CONFIG)
 
        # Pipeline halted — no downstream stages called
        mock_normalize.assert_not_called()
        assert exc_info.value.stage == "map_columns"
        assert "bad config" in str(exc_info.value)
 
 
def test_pipeline_halts_on_normalize_stage_failure():
    """Exception in normalize stage halts pipeline and raises PipelineError."""
    raw_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
 
    with patch("app.processing.pipeline.map_columns", return_value=raw_df), \
         patch("app.processing.pipeline.normalize", side_effect=RuntimeError("normalize failed")), \
         patch("app.processing.pipeline.inject_client") as mock_client:
 
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw_df, MAPPING_CONFIG)
 
        mock_client.assert_not_called()
        assert exc_info.value.stage == "normalize"
 
 
def test_pipeline_halts_on_validate_stage_failure():
    """Exception in validate_rows stage halts pipeline and raises PipelineError."""
    raw_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
 
    with patch("app.processing.pipeline.map_columns", return_value=raw_df), \
         patch("app.processing.pipeline.normalize", return_value=raw_df), \
         patch("app.processing.pipeline.inject_client", return_value=raw_df), \
         patch("app.processing.pipeline.validate_rows", side_effect=Exception("validator crashed")), \
         patch("app.processing.pipeline.split_rows") as mock_split:
 
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw_df, MAPPING_CONFIG)
 
        mock_split.assert_not_called()
        assert exc_info.value.stage == "validate_rows"
 
 
def test_pipeline_halts_on_enforce_schema_failure():
    """Exception in enforce_schema stage halts pipeline and raises PipelineError."""
    raw_df = pd.DataFrame({"First": ["John"], "_source_sheet": ["Alpha Fund"]})
    clean_df = pd.DataFrame({"First": ["John"]})
    rejected_df = pd.DataFrame()
 
    with patch("app.processing.pipeline.map_columns", return_value=raw_df), \
         patch("app.processing.pipeline.normalize", return_value=raw_df), \
         patch("app.processing.pipeline.inject_client", return_value=raw_df), \
         patch("app.processing.pipeline.validate_rows", return_value=raw_df), \
         patch("app.processing.pipeline.split_rows", return_value=(clean_df, rejected_df)), \
         patch("app.processing.pipeline.enforce_schema", side_effect=RuntimeError("schema crash")):
 
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw_df, MAPPING_CONFIG)
 
        assert exc_info.value.stage == "enforce_schema"
 
 
def test_pipeline_error_contains_stage_and_message():
    """PipelineError exposes stage name, error type, and original message."""
    raw_df = pd.DataFrame({"first": ["John"], "_source_sheet": ["Alpha Fund"]})
 
    with patch("app.processing.pipeline.map_columns", side_effect=ValueError("alias missing")):
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw_df, MAPPING_CONFIG)
 
    error = exc_info.value
    assert error.stage == "map_columns"
    assert error.error_type == "ValueError"
    assert "alias missing" in error.error_message
 
 
# ---------------------------------------------------------------------------
# Integration test — real fixture, no mocks
# ---------------------------------------------------------------------------
 
def test_pipeline_integration_full_flow():
    """
    Integration: real workbook through full pipeline with no mocks.
    Verifies correct clean/rejected counts, summary accuracy,
    output structure, and deterministic results.
    """
    wb = build_workbook([{
        "name": "Alpha Fund",
        "rows": [
            ["First", "Last", "Address1", "City", "State", "Zip", "GiftDate", "Amount"],
            ["John", "Doe", "123 Main St", "Nashville", "TN", "37201", "2024-01-01", "100.00"],
            ["Jane", "Smith", "456 Oak Ave", "Memphis", "TN", "38101", "2024-01-02", "200.00"],
            # Invalid row — missing Last name
            ["Alice", None, "789 Pine Rd", "Knoxville", "TN", "37901", "2024-01-03", "300.00"],
        ],
    }])
 
    from app.processing.parser import parse_workbook
    parsed_df = parse_workbook(wb, MAPPING_CONFIG)
    result = run_pipeline(parsed_df, MAPPING_CONFIG)
 
    assert "clean_df" in result
    assert "rejected_df" in result
    assert "summary" in result
 
    # Row conservation
    total = result["summary"]["total_rows"]
    assert result["summary"]["clean_rows"] + result["summary"]["rejected_rows"] == total
 
    # Alice row rejected (missing Last)
    assert result["summary"]["clean_rows"] == 2
    assert result["summary"]["rejected_rows"] == 1
 
    # Clean output types and content
    clean = result["clean_df"]
    assert isinstance(clean, pd.DataFrame)
    assert "First" in clean.columns
    assert "Client" in clean.columns
    assert clean.iloc[0]["Client"] == "Alpha Fund"
 
    # Internal columns must not appear in clean output
    assert "_source_sheet" not in clean.columns
    assert "_is_valid" not in clean.columns
    assert "_rejection_reason" not in clean.columns
 
    # Rejected output has rejection_reason
    rejected = result["rejected_df"]
    assert isinstance(rejected, pd.DataFrame)
    assert "rejection_reason" in rejected.columns
    assert len(rejected) == 1
 
    # Determinism — same input produces same output
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
 