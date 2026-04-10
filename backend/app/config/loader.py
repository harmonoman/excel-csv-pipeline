import json
from pathlib import Path
 
 
REQUIRED_FIELDS = [
    "First",
    "Last",
    "Address1",
    "City",
    "State",
    "Zip",
    "DonationDate",
    "DonationAmount",
]
 
 
class ConfigValidationError(Exception):
    """Raised when mapping.json fails validation at startup."""
    pass
 
 
def load_mapping_config(config_path: Path) -> dict:
    """
    Load and validate mapping.json from the given path.
 
    Raises ConfigValidationError immediately if the config is invalid.
    This is intentional — the pipeline must not start with a broken config.
    """
    with open(config_path) as f:
        config = json.load(f)
 
    # Validate top-level keys exist first
    if "header_scan_rows" not in config:
        raise ConfigValidationError(
            "mapping.json is missing required key: header_scan_rows"
        )
 
    if "fields" not in config:
        raise ConfigValidationError(
            "mapping.json is missing required key: fields"
        )
 
    # Validate header_scan_rows type
    if not isinstance(config["header_scan_rows"], int):
        raise ConfigValidationError(
            f"header_scan_rows must be an integer, got {type(config['header_scan_rows']).__name__}"
        )
 
    # Validate all required canonical fields are present
    for field in REQUIRED_FIELDS:
        if field not in config["fields"]:
            raise ConfigValidationError(
                f"Missing required field: {field}"
            )
 
    # Validate no canonical field has an empty alias list
    for field, aliases in config["fields"].items():
        if not isinstance(aliases, list) or len(aliases) == 0:
            raise ConfigValidationError(
                f"Field '{field}' must have at least one alias, got: {aliases}"
            )
 
    return config
 