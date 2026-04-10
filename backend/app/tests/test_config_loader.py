import json
import pytest
from pathlib import Path
from app.config.loader import load_mapping_config, ConfigValidationError
 
 
VALID_CONFIG = {
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
 
 
def write_config(tmp_path: Path, config: dict) -> Path:
    """Helper: write a config dict to a temp file and return the path."""
    config_file = tmp_path / "mapping.json"
    config_file.write_text(json.dumps(config))
    return config_file
 
 
def test_valid_config_loads_successfully(tmp_path):
    """Valid config with all required fields loads without error."""
    config_file = write_config(tmp_path, VALID_CONFIG)
    config = load_mapping_config(config_file)
    assert config["header_scan_rows"] == 20
    assert "First" in config["fields"]
    assert "Last" in config["fields"]
 
 
def test_missing_header_scan_rows_raises(tmp_path):
    """Config missing header_scan_rows must fail at load time."""
    bad_config = {k: v for k, v in VALID_CONFIG.items() if k != "header_scan_rows"}
    config_file = write_config(tmp_path, bad_config)
    with pytest.raises(ConfigValidationError, match="header_scan_rows"):
        load_mapping_config(config_file)
 
 
def test_header_scan_rows_must_be_integer(tmp_path):
    """header_scan_rows must be an integer — string value must fail."""
    bad_config = {**VALID_CONFIG, "header_scan_rows": "20"}
    config_file = write_config(tmp_path, bad_config)
    with pytest.raises(ConfigValidationError, match="header_scan_rows must be an integer"):
        load_mapping_config(config_file)
 
 
def test_missing_canonical_field_raises(tmp_path):
    """Config missing a required canonical field must fail at load time."""
    bad_fields = {k: v for k, v in VALID_CONFIG["fields"].items() if k != "Last"}
    bad_config = {**VALID_CONFIG, "fields": bad_fields}
    config_file = write_config(tmp_path, bad_config)
    with pytest.raises(ConfigValidationError, match="Missing required field: Last"):
        load_mapping_config(config_file)
 
 
def test_empty_alias_list_raises(tmp_path):
    """A canonical field with an empty alias list must fail validation."""
    bad_fields = {**VALID_CONFIG["fields"], "City": []}
    bad_config = {**VALID_CONFIG, "fields": bad_fields}
    config_file = write_config(tmp_path, bad_config)
    with pytest.raises(ConfigValidationError, match="City"):
        load_mapping_config(config_file)
 
 
def test_all_seeded_aliases_present(tmp_path):
    """All seeded aliases must be correctly loaded for each canonical field."""
    config_file = write_config(tmp_path, VALID_CONFIG)
    config = load_mapping_config(config_file)
    assert "giftdate" in config["fields"]["DonationDate"]
    assert "st" in config["fields"]["State"]
    assert "lastname" in config["fields"]["Last"]
    assert "amount" in config["fields"]["DonationAmount"]
    assert "addr" in config["fields"]["Address1"]
 
 
def test_missing_fields_key_raises(tmp_path):
    """Config missing the fields key entirely must fail."""
    bad_config = {"header_scan_rows": 20}
    config_file = write_config(tmp_path, bad_config)
    with pytest.raises(ConfigValidationError, match="fields"):
        load_mapping_config(config_file)
 
 
def test_malformed_json_raises(tmp_path):
    """Corrupted mapping.json must fail cleanly at load time."""
    config_file = tmp_path / "mapping.json"
    config_file.write_text("{ this is not valid json }")
    with pytest.raises(Exception):
        load_mapping_config(config_file)
 