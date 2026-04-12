"""
Tests for app/utils/file_naming.py — T5-4 deterministic file naming.

Responsibilities:
- sanitize_filename(): clean input filename to safe filesystem string
- generate_output_filenames(): produce paired clean/rejected filenames with timestamp

Output format: {YYYYMMDD_HHMMSS}_{sanitized_name}_clean.csv / _rejected.csv
"""
import re
import time
from app.utils.file_naming import sanitize_filename, generate_output_filenames


# ---------------------------------------------------------------------------
# sanitize_filename() tests
# ---------------------------------------------------------------------------

def test_basic_filename_sanitized():
    """Standard xlsx filename is lowercased and extension stripped."""
    assert sanitize_filename("donations.xlsx") == "donations"


def test_spaces_replaced_with_underscores():
    """Spaces are replaced with underscores."""
    assert sanitize_filename("My Donations.xlsx") == "my_donations"


def test_special_characters_removed():
    """Special characters are removed."""
    assert sanitize_filename("client@data#2024!.xlsx") == "clientdata2024"


def test_parentheses_removed():
    """Parentheses and their contents are handled — parens removed, text kept."""
    assert sanitize_filename("My Donations (Final).xlsx") == "my_donations_final"


def test_uppercase_lowercased():
    """Uppercase letters are lowercased."""
    assert sanitize_filename("ALPHA_FUND.xlsx") == "alpha_fund"


def test_extension_stripped():
    """The .xlsx extension is stripped from the output."""
    result = sanitize_filename("data.xlsx")
    assert not result.endswith(".xlsx")
    assert not result.endswith(".csv")


def test_only_safe_characters_in_output():
    """Output contains only letters, numbers, and underscores."""
    result = sanitize_filename("My File (2024) - Final Version!.xlsx")
    assert re.match(r'^[a-z0-9_]+$', result), f"Unsafe characters in: {result}"


def test_consecutive_underscores_collapsed():
    """Multiple consecutive underscores are collapsed to one."""
    result = sanitize_filename("file  name.xlsx")  # double space
    assert "__" not in result


def test_leading_trailing_underscores_stripped():
    """Leading and trailing underscores are stripped."""
    result = sanitize_filename("  donations  .xlsx")
    assert not result.startswith("_")
    assert not result.endswith("_")


def test_empty_filename_returns_fallback():
    """Empty or all-special-char filename returns a safe fallback."""
    result = sanitize_filename("!!@@##.xlsx")
    assert len(result) > 0
    assert re.match(r'^[a-z0-9_]+$', result)


def test_filename_without_extension_handled():
    """Filename without .xlsx extension is still sanitized correctly."""
    result = sanitize_filename("donations")
    assert result == "donations"


def test_path_traversal_sanitized():
    """
    Path traversal input is neutralized — Path().stem discards directory
    components, leaving only the base filename stem which is then sanitized.
    """
    result = sanitize_filename("../../etc/passwd.xlsx")
    assert result == "passwd"
    assert ".." not in result
    assert "/" not in result


# ---------------------------------------------------------------------------
# generate_output_filenames() tests
# ---------------------------------------------------------------------------

TIMESTAMP_PATTERN = re.compile(r'^\d{8}_\d{6}$')
FILENAME_PATTERN = re.compile(r'^\d{8}_\d{6}_[a-z0-9_]+_(clean|rejected)\.csv$')


def test_returns_dict_with_required_keys():
    """Output dict contains 'clean', 'rejected', and 'base' keys."""
    result = generate_output_filenames("donations.xlsx")
    assert "clean" in result
    assert "rejected" in result
    assert "base" in result


def test_clean_filename_format():
    """Clean filename matches expected pattern."""
    result = generate_output_filenames("donations.xlsx")
    assert FILENAME_PATTERN.match(result["clean"]), f"Bad format: {result['clean']}"


def test_rejected_filename_format():
    """Rejected filename matches expected pattern."""
    result = generate_output_filenames("donations.xlsx")
    assert FILENAME_PATTERN.match(result["rejected"]), f"Bad format: {result['rejected']}"


def test_clean_ends_with_clean_csv():
    """Clean filename ends with _clean.csv."""
    result = generate_output_filenames("donations.xlsx")
    assert result["clean"].endswith("_clean.csv")


def test_rejected_ends_with_rejected_csv():
    """Rejected filename ends with _rejected.csv."""
    result = generate_output_filenames("donations.xlsx")
    assert result["rejected"].endswith("_rejected.csv")


def test_clean_and_rejected_share_base():
    """Clean and rejected filenames both start with the same base."""
    result = generate_output_filenames("donations.xlsx")
    assert result["clean"].startswith(result["base"])
    assert result["rejected"].startswith(result["base"])


def test_base_contains_timestamp():
    """Base identifier contains a valid timestamp component."""
    result = generate_output_filenames("donations.xlsx")
    # Base format: YYYYMMDD_HHMMSS_sanitized_name
    parts = result["base"].split("_")
    timestamp = f"{parts[0]}_{parts[1]}"
    assert TIMESTAMP_PATTERN.match(timestamp), f"Bad timestamp: {timestamp}"


def test_base_contains_sanitized_filename():
    """Base identifier contains the sanitized input filename."""
    result = generate_output_filenames("My Donations.xlsx")
    assert "my_donations" in result["base"]


def test_no_xlsx_extension_in_output():
    """Output filenames do not contain .xlsx extension."""
    result = generate_output_filenames("donations.xlsx")
    assert ".xlsx" not in result["clean"]
    assert ".xlsx" not in result["rejected"]
    assert ".xlsx" not in result["base"]


def test_complex_filename_sanitized_in_output():
    """Complex input filename is correctly sanitized in the output."""
    result = generate_output_filenames("My Donations (Final).xlsx")
    assert "my_donations_final" in result["clean"]
    assert "my_donations_final" in result["rejected"]


def test_multiple_uploads_produce_different_filenames():
    """
    Two successive calls produce different filenames — timestamp uniqueness.
    Uses 1-second sleep to guarantee different timestamps.
    """
    result_1 = generate_output_filenames("donations.xlsx")
    # Sleep is required — timestamp is second-precision, so we need >1s gap
    # to guarantee different timestamps. Do not remove.
    time.sleep(1.1)
    result_2 = generate_output_filenames("donations.xlsx")
    assert result_1["clean"] != result_2["clean"]
    assert result_1["base"] != result_2["base"]


def test_no_spaces_in_any_filename():
    """No spaces in any output filename."""
    result = generate_output_filenames("My File Name.xlsx")
    assert " " not in result["clean"]
    assert " " not in result["rejected"]
    assert " " not in result["base"]


def test_only_safe_characters_in_filenames():
    """Output filenames contain only safe filesystem/URL characters."""
    result = generate_output_filenames("client@data#2024!.xlsx")
    for key in ("clean", "rejected", "base"):
        val = result[key]
        # Allow letters, digits, underscores, dots (for .csv), hyphens not expected
        assert re.match(r'^[a-z0-9_.]+$', val), f"Unsafe chars in {key}: {val}"
