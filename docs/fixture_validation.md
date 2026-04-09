# Fixture Validation Log — Donor Bureau Excel Pipeline

**Version:** 0.1 (placeholder)  
**Status:** Deferred — awaiting fixture library (T7-1)  
**Last updated:** 2026-04-09  

---

## Purpose

This document is the audit trail that proves the fixture library covers every assumption and structural pattern defined in `input_contract.md`.

It is **not** a specification. It is evidence — a record of manual validation runs against real fixture files. For the contract itself, see `/docs/input_contract.md`.

---

## Status

This document is intentionally incomplete at this stage of the project.

**Reason for deferral:** The fixture library (T7-1) has not yet been built. Validating against fixtures that don't exist yet would produce a false sense of coverage.

**Do not fill this document in until T7-1 is complete.**

---

## Trigger for Completion

This document must be fully completed **before development begins on any T2, T3, or T4 ticket.** The entire backend processing pipeline is built on the assumptions validated here. Specifically:

- **T2-2** (parser) depends on validated header detection, metadata row behavior, and sheet structure
- **T3-1** (column mapping) depends on confirmed alias coverage across all known templates
- **T3-2** (normalization) depends on confirmed date format variations and ZIP edge cases
- **T4-2** (type validators) depends on confirmed data format assumptions for dates, amounts, states, and ZIPs

If a fixture reveals a structural pattern or data format that contradicts the input contract, it must be resolved here before any dependent ticket begins. Building processing logic against unvalidated assumptions is a known and avoidable risk.

**Rule for solo developer MVP: complete T0-3 immediately after T7-1, before writing any backend processing code.**

**Completion checklist:**
- [ ] T7-1 fixture library is merged and reviewed
- [ ] All fixtures listed in the validation table below
- [ ] Every assumption in `input_contract.md` section 5 is mapped to at least one fixture
- [ ] All violations documented and resolved
- [ ] Sign-off recorded at the bottom of this document

---

## Validation Table (to be completed)

For each fixture file, each sheet must be validated against the input contract and assumptions checklist. Record results here.

| Fixture File | Sheet Name | Header Row (expected) | Client Value (expected) | Template Variation | Header Detected | Mapping Compatible | Violations |
|---|---|---|---|---|---|---|---|
| fixture_multi_sheet.xlsx | — | — | — | — | — | — | — |
| fixture_header_offset.xlsx | — | — | — | — | — | — | — |
| fixture_metadata.xlsx | — | — | — | — | — | — | — |
| fixture_no_header.xlsx | — | — | — | — | — | — | — |
| fixture_instructions.xlsx | — | — | — | — | — | — | — |
| fixture_aliases.xlsx | — | — | — | — | — | — | — |
| fixture_missing_required.xlsx | — | — | — | — | — | — | — |
| fixture_extra_columns.xlsx | — | — | — | — | — | — | — |
| fixture_dates.xlsx | — | — | — | — | — | — | — |
| fixture_zip.xlsx | — | — | — | — | — | — | — |
| fixture_large.xlsx | — | — | — | — | — | — | — |

> Add rows as new fixtures are introduced. Any fixture not in this table is not considered validated.

---

## Assumption Coverage Map (to be completed)

Each assumption in `input_contract.md` section 5 must be traceable to at least one fixture. Flag any assumption that cannot be covered.

| Assumption | Fixture(s) | Status |
|---|---|---|
| Excel files are .xlsx | — | pending |
| File size < 10MB | — | pending |
| UTF-8 compatible encoding | — | pending |
| Single workbook may contain multiple clients | — | pending |
| Instructions sheet excluded from processing | — | pending |
| Header row within first N rows | — | pending |
| Minimum column threshold for header detection | — | pending |
| Metadata rows skipped without error | — | pending |
| Sheets without valid header excluded + logged | — | pending |
| Column names resolvable via mapping.json | — | pending |
| Unmapped columns dropped and logged | — | pending |
| Client derived from sheet tab name | — | pending |
| Sheet names normalized before assignment | — | pending |
| DonationDate parseable across multiple formats | — | pending |
| DonationAmount numeric and > 0 | — | pending |
| State is valid 2-letter US abbreviation | — | pending |
| ZIP is 5-digit string, leading zeros preserved | — | pending |
| Deterministic output for same input | — | pending |

---

## Violations Log (to be completed)

Record any mismatch found between a fixture file and the input contract. Each violation must be resolved before T2-2 development begins.

| # | Fixture File | Sheet | Violation Description | Resolution | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## Sign-Off

To be completed after all fixtures are validated and all violations are resolved.

| Role | Name | Date |
|---|---|---|
| Data Engineer | — | — |
| Project Manager | — | — |

---

## References

- `/docs/input_contract.md` — specification this log validates against
- `backend/tests/fixtures/` — fixture file location
- T7-1 — fixture library ticket
- T2-2 — first ticket blocked on this validation being complete
