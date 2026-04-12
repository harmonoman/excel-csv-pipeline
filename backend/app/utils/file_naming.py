"""
file_naming.py — Deterministic output file naming utility (T5-4).

Responsibilities:
- Sanitize input filenames to safe filesystem/URL strings
- Generate paired clean/rejected output filenames with UTC timestamp
- Ensure collision safety via second-precision timestamp

Output format:
    {YYYYMMDD_HHMMSS}_{sanitized_name}_clean.csv
    {YYYYMMDD_HHMMSS}_{sanitized_name}_rejected.csv

Used by:
- T5-1: clean CSV writer
- T5-2: rejected CSV writer
- T5-3: download response endpoint
"""
import re
from datetime import datetime, timezone
from pathlib import Path


# Fallback name if sanitization produces an empty string
_FALLBACK_NAME = "upload"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize an input filename to a safe, lowercase, underscore-separated string.

    Steps:
    1. Strip the file extension
    2. Lowercase
    3. Replace spaces and hyphens with underscores
    4. Remove all characters that are not letters, digits, or underscores
    5. Collapse consecutive underscores to one
    6. Strip leading/trailing underscores
    7. Return fallback if result is empty

    Args:
        filename: original uploaded filename (e.g. "My Donations (Final).xlsx")

    Returns:
        Safe string suitable for use in filenames and URLs
        (e.g. "my_donations_final")
    """
    # Strip extension — handle both "file.xlsx" and "file" (no extension)
    name = Path(filename).stem

    # Lowercase
    name = name.lower()

    # Replace spaces and hyphens with underscores
    name = re.sub(r'[\s\-]+', '_', name)

    # Remove all characters that are not letters, digits, or underscores
    name = re.sub(r'[^a-z0-9_]', '', name)

    # Collapse consecutive underscores
    name = re.sub(r'_+', '_', name)

    # Strip leading/trailing underscores
    name = name.strip('_')

    return name if name else _FALLBACK_NAME


def generate_output_filenames(input_filename: str) -> dict:
    """
    Generate a paired set of deterministic output filenames for a pipeline run.

    Both clean and rejected filenames share the same base identifier, making
    it easy to associate output pairs with their source upload.

    Timestamp is UTC second-precision — sufficient for MVP collision safety
    under single-server, sequential upload conditions.

    Known limitation: two uploads within the same second will produce identical
    filenames, risking file overwrite. Post-MVP mitigation: append microseconds
    or a short UUID suffix to the timestamp component.

    Args:
        input_filename: original uploaded filename (e.g. "donations.xlsx")

    Returns:
        {
            "base":     "20260412_143205_donations",
            "clean":    "20260412_143205_donations_clean.csv",
            "rejected": "20260412_143205_donations_rejected.csv",
        }
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    sanitized = sanitize_filename(input_filename)
    base = f"{timestamp}_{sanitized}"

    return {
        "base": base,
        "clean": f"{base}_clean.csv",
        "rejected": f"{base}_rejected.csv",
    }
