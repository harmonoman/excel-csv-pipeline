# Fixture Catalog — Donor Bureau Pipeline

**Version:** 1.0  
**Location:** `backend/tests/fixtures/`  
**Status:** T7-1 complete

All fixtures are deterministic `.xlsx` files. Same fixture always produces the same pipeline output. Each fixture maps to one or more assumptions in `input_contract.md`.

---

## fixture_perfect.xlsx

**Purpose:** Happy path baseline. Validates that a clean, well-formed single-sheet workbook flows through the entire pipeline without any rejections.

**Structure:**
- Sheet: `Green Valley Fund`
- Header row: 1
- Data rows: 5
- All canonical column aliases (`First`, `Last`, `Address1`, `City`, `State`, `Zip`, `GiftDate`, `Amount`)
- All values valid

**Expected outcome:**
- `total_rows`: 5
- `clean_rows`: 5
- `rejected_rows`: 0
- `Client` = `"Green Valley Fund"` on all rows

**Contract assumptions validated:**
- File-level: single sheet, header at row 1
- Column mapping: canonical aliases resolve correctly
- Client injection: derived from sheet tab name

---

## fixture_header_offset.xlsx

**Purpose:** Validates header detection when metadata rows precede the real header. Mirrors the confirmed real-world Alpha Fund format.

**Structure:**
- Sheet: `Alpha Fund`
- Row 1: `"Prepared for internal review"` (metadata)
- Row 2: `"Client: Alpha Fund"` (metadata)
- Row 3: empty
- Row 4: real header (`First`, `Last`, `Address1`, `City`, `State`, `Zip`, `GiftDate`, `Amount`)
- Rows 5–7: data

**Expected outcome:**
- `total_rows`: 3
- `clean_rows`: 3
- `rejected_rows`: 0
- Metadata rows not present in output

**Contract assumptions validated:**
- §2.1: Metadata rows must be skipped
- §2.2: Header not guaranteed to be row 1
- §2.2: Detection scans first N rows (header_scan_rows=20)
- §2.2: First row with ≥2 alias matches is accepted as header

---

## fixture_missing_columns.xlsx

**Purpose:** Validates that rows with structurally absent required fields are rejected at the validation stage — not silently dropped or corrupted.

**Structure:**
- Sheet: `Incomplete Fund`
- Header row: 1
- Columns present: `First`, `Address1`, `City`, `State`, `GiftDate`, `Amount`
- Columns absent: `Last`, `Zip`
- Data rows: 3

**Expected outcome:**
- `total_rows`: 3
- `clean_rows`: 0
- `rejected_rows`: 3
- Each rejection reason contains `"Missing: Last"` and `"Missing: Zip"`

**Contract assumptions validated:**
- §3.1: Required fields; absent columns generate missing-field rejections
- Mapping stage: missing canonical columns are tolerated (not an error)
- Validation stage: missing fields produce rejection reasons

---

## fixture_mixed_dates.xlsx

**Purpose:** Validates the normalizer's date parsing robustness across all format variations expected in real-world workbooks.

**Structure:**
- Sheet: `Date Test Fund`
- Header row: 1
- Data rows: 5
- `GiftDate` values:
  - Row 1: `"2024-01-15"` — ISO 8601
  - Row 2: `"01/20/2024"` — US MM/DD/YYYY
  - Row 3: `"March 5, 2024"` — natural language
  - Row 4: `45291` — Excel serial date (resolves to `2023-12-31` via openpyxl; Lotus 1-2-3 leap year offset applies)
  - Row 5: `"not-a-date"` — intentionally invalid

**Expected outcome:**
- `total_rows`: 5
- `clean_rows`: 4
- `rejected_rows`: 1
- Row 5 rejection reason: `"Missing: DonationDate"` — the normalizer converts unparseable date strings to `NaN` before validation; T4-1 fires on NaN before T4-2 can fire `"Invalid Date"`

**Contract assumptions validated:**
- §3.1 / data assumptions: DonationDate values are parseable into valid dates
- Normalizer handles ISO, US format, natural language, and Excel serial
- Invalid dates produce `"Invalid Date"` rejection reason

---

## fixture_zip_edge_cases.xlsx

**Purpose:** Validates ZIP code handling — leading zero preservation, type coercion, and length enforcement.

**Structure:**
- Sheet: `Zip Test Fund`
- Header row: 1
- Data rows: 6
- `Zip` values:
  - Row 1: `"01234"` — 5-digit with leading zero (valid)
  - Row 2: `12345` — standard 5-digit integer (valid)
  - Row 3: `"60601"` — standard string (valid)
  - Row 4: `"123A"` — non-numeric 4-char string (invalid, not padded)
  - Row 5: `"123456"` — 6 digits (invalid, too long)
  - Row 6: `"1234X"` — non-numeric (invalid)

**Note:** A 4-digit numeric string like `"1234"` is NOT a reliable invalid case — the normalizer pads short numeric strings with `zfill(5)` (producing `"01234"`), making it valid. Use non-numeric strings to test rejection.

**Expected outcome:**
- `total_rows`: 6
- `clean_rows`: 3
- `rejected_rows`: 3 (`"123A"`, `"123456"`, `"1234X"` — all `"Invalid Zip"`)
- Row 1 clean CSV `Zip` = `"01234"` (leading zero preserved)
- Row 2 clean CSV `Zip` = `"12345"` (integer normalized to string)

**Contract assumptions validated:**
- §3.1 data assumptions: ZIP codes are 5-digit strings, leading zeros preserved
- Normalizer: integer ZIPs padded to 5 digits with `zfill`
- Validator: rejects ZIPs that are not exactly 5 digits

---

## fixture_multi_sheet.xlsx

**Purpose:** Validates multi-client, multi-template workbook ingestion. Each sheet uses different column aliases and one has a metadata offset header. This is the most structurally complex fixture.

**Structure:**
- Sheet 1: `Horizon PAC`
  - Header row: 1
  - Aliases: `First`, `Last`, `Address1`, `City`, `State`, `Zip`, `GiftDate`, `Amount`
  - Data rows: 3

- Sheet 2: `Liberty Fund`
  - Header row: 1
  - Aliases: `fname`, `lname`, `addr`, `city`, `st`, `zip_code`, `gift_date`, `gift_amount`
  - Data rows: 2

- Sheet 3: `Eagle Society`
  - Row 1: `"Report period: Q1 2024"` (metadata)
  - Row 2: header — `first_name`, `last_name`, `address1`, `city`, `state_code`, `zipcode`, `donation_date`, `donation_amount`
  - Data rows: 2

**Expected outcome:**
- `total_rows`: 7
- `clean_rows`: 7
- `rejected_rows`: 0
- `Client` values: `"Horizon PAC"`, `"Liberty Fund"`, `"Eagle Society"` per sheet origin
- `_source_sheet` correctly reflects origin sheet for all rows

**Contract assumptions validated:**
- §1: Each sheet tab = distinct client dataset
- §2.2: Header detection works across different alias sets
- §3.1: All alias variations in `mapping.json` resolve to canonical columns
- §3.3: Column names case-insensitive, whitespace-trimmed
- Client injection: sheet name used, never cell data

---

## fixture_empty_sheet.xlsx

**Purpose:** Validates graceful handling of a sheet with a valid header but no data rows. Should be skipped without error, producing zero rows.

**Structure:**
- Sheet: `Empty Fund`
- Header row: 1 (valid header present)
- Data rows: 0

**Expected outcome:**
- `total_rows`: 0
- `clean_rows`: 0
- `rejected_rows`: 0
- No exception raised
- Clean CSV contains header row only

**Contract assumptions validated:**
- §2.3: Sheets with valid header but zero data rows are skipped without error
- Output layer: clean/rejected CSVs always written, even with zero data rows

---

## fixture_large.xlsx

**Purpose:** Performance sanity check. Validates that the synchronous pipeline handles 1,000 rows without memory issues, unexpected errors, or unreasonable processing time.

**Structure:**
- Sheet: `Large Fund`
- Header row: 1
- Data rows: 1,000
- All rows valid
- States cycle across 10 valid US abbreviations
- ZIP codes: 5-digit strings from `10001` to `11000`

**Expected outcome:**
- `total_rows`: 1000
- `clean_rows`: 1000
- `rejected_rows`: 0
- Processing completes in under 10 seconds

**Contract assumptions validated:**
- MVP constraint: synchronous processing, in-memory, under 10MB
- No performance regression from scale

---


## fixture_no_header.xlsx

**Purpose:** Validates that a sheet with no detectable header is excluded from processing with a warning logged — not an error or crash. Directly validates contract §2.2.

**Structure:**
- Sheet: `No Header Sheet`
- Rows: 5 (all narrative/label content)
- No row contains ≥2 recognizable column aliases
- Contents: `"Monthly Report"`, `"Internal Use Only"`, `"Prepared by Finance Team"`, date labels, ref labels

**Expected outcome:**
- `total_rows`: 0
- `clean_rows`: 0
- `rejected_rows`: 0
- No exception raised
- Warning logged: `"No valid header found in sheet 'No Header Sheet' — sheet excluded from processing"`

**Contract assumptions validated:**
- §2.2: Sheets with no detectable header within first N rows are excluded + warning logged
- Parser: warning logged, not an exception
- Empty DataFrame returned when no valid sheets found

---
## Fixture–Contract Mapping Summary

| Fixture | Contract Section | Assumption Validated |
|---|---|---|
| `fixture_perfect.xlsx` | §1, §3.1 | Happy path, canonical aliases, client from sheet name |
| `fixture_header_offset.xlsx` | §2.1, §2.2 | Metadata rows skipped, header not row 1 |
| `fixture_missing_columns.xlsx` | §3.1 | Missing required fields → validation rejection |
| `fixture_mixed_dates.xlsx` | §3.1 data assumptions | Date format variety parsed correctly |
| `fixture_zip_edge_cases.xlsx` | §3.1 data assumptions | ZIP preservation, length enforcement |
| `fixture_multi_sheet.xlsx` | §1, §2.2, §3.1, §3.3 | Multi-sheet, multi-alias, header detection, client injection |
| `fixture_empty_sheet.xlsx` | §2.3 | Empty sheet skipped without error |
| `fixture_no_header.xlsx` | §2.2 | Sheet with no detectable header excluded + warning |
| `fixture_large.xlsx` | MVP constraints | Synchronous in-memory processing at scale |

---

## Reuse in T7-2 and T7-3

**T7-2 (Integration tests — full pipeline):**
Each fixture is designed for direct use with the FastAPI `TestClient`. Load the fixture file, POST to `/upload`, and assert `total_rows`, `clean_rows`, and `rejected_rows` match the expected counts documented above.

**T7-3 (Edge case coverage):**
`fixture_empty_sheet.xlsx` covers the all-zero row count edge case. `fixture_missing_columns.xlsx` covers the all-rejected edge case. `fixture_large.xlsx` covers the performance edge case. `fixture_zip_edge_cases.xlsx` and `fixture_mixed_dates.xlsx` cover the data-format edge cases.