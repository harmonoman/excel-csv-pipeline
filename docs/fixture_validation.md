# Fixture Validation Log — Donor Bureau Excel Pipeline

**Version:** 1.0  
**Status:** Closed via programmatic fixture approach — see deviation note below  
**Last updated:** 2026-04-12

---

## Purpose

This document is the audit trail that proves the fixture library covers every assumption and structural pattern defined in `input_contract.md`.

It is **not** a specification. It is evidence — a record of validation runs against fixture data. For the contract itself, see `/docs/input_contract.md`.

---

## Approach Deviation Note

The original T0-3 plan specified physical `.xlsx` fixture files to be validated before T2–T4 development began. The project took a deliberate and documented deviation from this approach.

**What was done instead:**

Rather than building a physical fixture library upfront, the team implemented `build_workbook()` — an in-memory programmatic fixture builder (`backend/app/tests/fixtures.py`) that constructs valid `.xlsx` workbooks at test time using openpyxl. All structural patterns required by the input contract were validated through this builder combined with dedicated integration tests and two milestone checkpoint reviews (E3 and E4).

**Why this was acceptable:**

- The in-memory approach provides identical structural coverage to physical files
- Every assumption in the contract is mapped to at least one passing test (see coverage map below)
- The E3 checkpoint review explicitly validated contract alignment, alias coverage, and real-world format handling
- The real-world Alpha Fund metadata format (3 rows before header) was confirmed against an actual client workbook and is exercised in `test_pipeline_integration_real_world_metadata_format`
- All violations discovered during development were documented and resolved in the E3 and E4 checkpoint reports

**What remains deferred:**

Physical `.xlsx` fixture files (T7-1) remain a post-MVP task. The pipeline has been validated against the contract through programmatic fixtures and checkpoint reviews, not physical files on disk.

---

## Assumption Coverage Map

Each assumption in `input_contract.md` section 5 is mapped to the test(s) that validate it.

| Assumption | Covered by | Status |
|---|---|---|
| Excel files are `.xlsx` | `test_invalid_extension_returns_400`, `test_wrong_mime_type_returns_400` | ✅ |
| File size < 10MB | In-memory fixtures — all under 10MB by construction | ✅ |
| UTF-8 compatible encoding | openpyxl default encoding — all test fixtures use UTF-8 | ✅ |
| Single workbook may contain multiple clients | `test_multi_sheet_mixed_templates_integration`, `test_pipeline_integration_real_world_metadata_format` | ✅ |
| Instructions sheet excluded from processing | `test_sheet_with_no_detectable_header_excluded`, `test_pipeline_integration_real_world_metadata_format`, `test_empty_workbook_returns_200_with_zero_rows` | ✅ |
| Header row within first N rows | `test_header_offset_row_3`, `test_header_offset_row_5` | ✅ |
| Minimum column threshold for header detection | `test_partial_match_below_threshold_excluded`, `test_partial_match_at_threshold_accepted` | ✅ |
| Metadata rows skipped without error | `test_metadata_row_does_not_trigger_header_detection`, `test_pipeline_integration_real_world_metadata_format` | ✅ |
| Sheets without valid header excluded + logged | `test_sheet_with_no_detectable_header_excluded` (confirms warning logged) | ✅ |
| Column names resolvable via mapping.json | `test_alias_match`, `test_case_insensitive_match`, `test_multi_sheet_different_aliases` | ✅ |
| Unmapped columns dropped and logged | `test_unknown_column_dropped` | ✅ |
| Client derived from sheet tab name | `test_single_sheet_client_assigned`, `test_multi_sheet_client_assigned_correctly` | ✅ |
| Sheet names normalized (whitespace trimmed) | `test_sheet_name_whitespace_stripped` | ✅ |
| DonationDate parseable across multiple formats | `test_donation_date_iso_format_parsed`, `test_donation_date_us_format_parsed`, `test_donation_date_natural_language_parsed`, `test_donation_date_excel_serial_parsed` | ✅ |
| DonationAmount numeric and > 0 | `test_amount_zero_rejected`, `test_amount_negative_rejected`, `test_amount_non_numeric_string_rejected` | ✅ |
| State is valid 2-letter US abbreviation | `test_valid_state_accepted`, `test_invalid_state_code_rejected`, `test_full_state_name_rejected` | ✅ |
| ZIP is 5-digit string, leading zeros preserved | `test_zip_leading_zero_preserved`, `test_zip_integer_padded_to_5_digits`, `test_zip_too_short_rejected`, `test_zip_too_long_rejected` | ✅ |
| Deterministic output for same input | `test_validation_is_deterministic`, `test_split_is_deterministic`, `test_injection_is_deterministic` | ✅ |

---

## Violations Log

Violations discovered during development and resolved through checkpoint reviews.

| # | Discovery point | Pattern / Assumption | Violation Description | Resolution | Status |
|---|---|---|---|---|---|
| 1 | E3 checkpoint | Multi-sheet alias handling | `concat → map` ordering caused NaN leakage when sheets used different column aliases | Moved `map_columns()` per-sheet inside `parse_workbook()` before concat | ✅ Resolved |
| 2 | E3 checkpoint | Contract ↔ config alias drift | `input_contract.md` documented `donation` alias not in `mapping.json`; three aliases in config undocumented in contract | Updated contract to match config (config is authoritative) | ✅ Resolved |
| 3 | E4 checkpoint | Empty workbook handling | `inject_client()` crashed with `KeyError: '_source_sheet'` on empty DataFrame | Added early return guard to `inject_client()` consistent with other stages | ✅ Resolved |

---

## Programmatic Fixture Builder

**Location:** `backend/app/tests/fixtures.py`  
**Function:** `build_workbook(sheets: list[dict]) -> io.BytesIO`

Supports construction of any workbook structure required by the contract including:
- Multiple sheets with distinct names (client segmentation)
- Metadata rows before the header
- Different column aliases per sheet (template variation)
- Variable header row positions
- Non-data sheets (Instructions)
- Empty sheets
- Sheets with no recognizable header

All integration tests use this builder directly. Physical `.xlsx` files on disk are not required for test execution.

---

## Completion Checklist

- [x] Every assumption in `input_contract.md` section 5 mapped to at least one passing test
- [x] Multi-sheet + multi-client behavior confirmed end-to-end
- [x] Mixed column aliases per sheet confirmed working (E3 arch fix)
- [x] Metadata row handling confirmed end-to-end (real Alpha Fund format)
- [x] Instructions/non-data sheet exclusion confirmed
- [x] All violations discovered and resolved (see violations log above)
- [x] Deviation from physical fixture approach documented
- [ ] Physical `.xlsx` fixture library (T7-1) — deferred to post-MVP

---

## Sign-Off

| Role | Date | Notes |
|---|---|---|
| Data Engineer | 2026-04-12 | Validated via programmatic fixtures and E3/E4 checkpoint reviews |
| Project Manager | 2026-04-12 | T0-3 closed — deviation approach accepted for MVP |

---

## References

- `/docs/input_contract.md` — specification this log validates against
- `/docs/checkpoints/e3_checkpoint_report.md` — alias drift and multi-sheet arch fix
- `/docs/checkpoints/e4_checkpoint_report.md` — empty workbook bug and test coverage
- `backend/app/tests/fixtures.py` — programmatic fixture builder
- T7-1 — physical fixture library (deferred to post-MVP)