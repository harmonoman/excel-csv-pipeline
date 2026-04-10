"""
transformer.py — Column mapping engine.
 
Responsibilities:
- Map source column names to canonical schema using aliases from mapping.json
- Drop unmapped columns
- Preserve _source_sheet column
- Tolerate missing canonical fields (validation is T4's responsibility)
 
This module does NOT:
- Validate data completeness or field values
- Normalize data values (T3-2)
- Inject the Client field (T3-3)
- Raise errors for missing fields
"""
import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
PROTECTED_COLUMNS = {"_source_sheet"}
 
 
def _build_reverse_lookup(mapping_config: dict) -> dict[str, str]:
    """
    Build a reverse lookup from normalized alias → canonical field name.
 
    Example:
        {"first_name": "First", "fname": "First", "first": "First", ...}
 
    First occurrence wins if aliases overlap across fields (shouldn't happen
    in a well-formed config but logged as a warning if detected).
    """
    lookup = {}
    for canonical, aliases in mapping_config["fields"].items():
        for alias in aliases:
            normalized = alias.lower().strip()
            if normalized in lookup:
                logger.warning(
                    "Alias collision in mapping.json: '%s' maps to both '%s' and '%s' — '%s' wins",
                    normalized, lookup[normalized], canonical, lookup[normalized],
                )
            else:
                lookup[normalized] = canonical
    return lookup
 
 
def map_columns(df: pd.DataFrame, mapping_config: dict) -> pd.DataFrame:
    """
    Map source DataFrame column names to canonical schema.
 
    - Source columns are matched case-insensitively against aliases
    - Unmapped columns are dropped
    - _source_sheet is always preserved
    - Missing canonical fields are tolerated (not added as empty columns)
    - If multiple source columns resolve to the same canonical field,
      the first occurrence (left-to-right) wins
    - Column mapping runs even on empty DataFrames (zero rows) so that
      downstream stages always receive canonical column names
 
    Note: _source_sheet will appear last in the output column order.
    The schema enforcement layer (T5-6) enforces final column ordering.
 
    Args:
        df: parsed DataFrame from T2-2 parser
        mapping_config: loaded and validated mapping.json config
 
    Returns:
        DataFrame with canonical column names, unmapped columns removed.
    """
    # Only skip if there are no columns at all — not if there are no rows.
    # An empty DataFrame with columns must still have its columns renamed
    # so downstream stages receive canonical names.
    if df.columns.empty:
        return df
 
    reverse_lookup = _build_reverse_lookup(mapping_config)
 
    rename_map = {}
    seen_canonical = set()
 
    for col in df.columns:
        # Always preserve protected columns
        if col in PROTECTED_COLUMNS:
            continue
 
        normalized = col.lower().strip()
        canonical = reverse_lookup.get(normalized)
 
        if canonical is None:
            logger.debug("Dropping unmapped column: '%s'", col)
            continue
 
        if canonical in seen_canonical:
            logger.debug(
                "Column '%s' maps to '%s' but already claimed — dropping duplicate",
                col, canonical,
            )
            continue
 
        rename_map[col] = canonical
        seen_canonical.add(canonical)
 
    # Keep only mapped columns + protected columns.
    # _source_sheet appears last — T5-6 enforces final column ordering.
    keep_cols = list(rename_map.keys()) + [
        col for col in df.columns if col in PROTECTED_COLUMNS
    ]
 
    result = df[keep_cols].rename(columns=rename_map)
 
    return result
 