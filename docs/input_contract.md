# Input Contract — Donor Bureau Excel Pipeline

**Version:** 1.2  
**Status:** MVP  
**Last updated:** 2026-04-10  

This document is the **source of truth** for the expected structure of incoming Excel workbooks. It includes both the formal input contract (specification) and the **operational/testable assumptions** that the pipeline relies on.  

All pipeline components (parser, transformer, validator) **must conform to these expectations**. Any new file format introduced must be validated against this contract before acceptance.

---

## 1. File-Level Structure

| Property | Expectation |
|---|---|
| Format | `.xlsx` only |
| Upload unit | One workbook = one upload batch |
| Client segmentation | Each sheet tab = one distinct client dataset |
| Client identifier | Sheet tab name is authoritative for `Client` column |
| File size | Under 10MB (fits in-memory processing) |
| Encoding | UTF-8 compatible |

---

## 2. Sheet-Level Structure

### 2.1 Metadata Rows

- Metadata rows may appear **before the real header row** (e.g., "Prepared for internal review", "Client: Alpha Fund").  
- Metadata rows **must be skipped during ingestion**.  
- Any in-sheet client label is ignored; `Client` is always derived from the sheet tab name.

**Example (Alpha Fund sheet):**
```
Row 1: "Prepared for internal review"
Row 2: "Client: Alpha Fund"
Row 3: (empty)
Row 4: First | LastName | Address1 | City | ST | Zip | GiftDate | Amount ← header
Row 5+: data
```

### 2.2 Header Detection

- Header row = **first row containing ≥ 2 recognizable columns** from `mapping.json`.  
- Header row is **not guaranteed to be row 1**; scan first **N rows** (configurable in `mapping.json`).  
- Sheets with no detectable header within first N rows are **excluded from processing** and logged.  

### 2.3 Data Rows

- Begin immediately after the detected header row.  
- Empty rows are skipped.  
- Sheets with valid headers but zero data rows are skipped without error.

---

## 3. Column-Level Structure

### 3.1 Required Output Fields and Source Aliases

All column names are **case-insensitive**; whitespace trimmed before mapping.

| Output Field | Known Source Aliases |
|---|---|
| `First` | first, first_name, fname |
| `Last` | last, lastname, last_name, lname |
| `Address1` | address1, address, addr |
| `City` | city |
| `State` | state, st, state_code |
| `Zip` | zip, zip_code, zipcode |
| `DonationDate` | donationdate, giftdate, date, gift_date, donation_date |
| `DonationAmount` | donationamount, amount, gift_amount, donation_amount |
| `Client` | **Derived from sheet tab name — never a source column** |

### 3.2 Unmapped Columns

- Allowed in source files.  
- Silently dropped during mapping stage.  
- Dropped columns logged for traceability.

### 3.3 Column Name Treatment

- All names normalized: lowercase, trimmed.  
- Case-insensitive alias matching.  
- Leading/trailing whitespace ignored.

---

## 4. Explicitly Out-of-Scope (MVP)

The following are **not supported** and may break the pipeline:

- Merged cells  
- Multi-row headers  
- Embedded images/charts  
- Password-protected sheets  
- Non-tabular layouts  
- Formulas in data cells (values read as-is)

---

## 5. Operational Assumptions & Testable Rules

These assumptions are **linked to fixtures** and **unit/integration tests**. They define conditions that **must be true for the pipeline to function correctly**.

### 5.1 File-Level Assumptions

| Assumption | Testable via fixture |
|---|---|
| Excel files are `.xlsx` | yes (`fixture_format.xlsx`) |
| File size < 10MB | yes (`fixture_large.xlsx`) |
| UTF-8 compatible encoding | yes (`fixture_encoding.xlsx`) |
| Single workbook may contain multiple clients | yes (`fixture_multi_sheet.xlsx`) |

### 5.2 Sheet / Header Structure

| Assumption | Testable via fixture |
|---|---|
| Header row may appear within first N rows | yes (`fixture_header_offset.xlsx`) |
| Minimum threshold of recognizable columns present | yes (`fixture_column_variation.xlsx`) |
| Metadata rows before header are ignored | yes (`fixture_metadata.xlsx`) |
| Sheets without valid header → rejected + warning | yes (`fixture_no_header.xlsx`) |
| Non-data sheets (e.g., Instructions) excluded | yes (`fixture_instructions.xlsx`) |

### 5.3 Column / Mapping Assumptions

| Assumption | Testable via fixture |
|---|---|
| Column names resolvable via `mapping.json` | yes (`fixture_aliases.xlsx`) |
| Required fields must be mappable | yes (`fixture_missing_required.xlsx`) |
| Unmapped columns allowed, dropped + logged | yes (`fixture_extra_columns.xlsx`) |

### 5.4 Client Field Assumptions

| Assumption | Testable via fixture |
|---|---|
| Client = sheet tab name | yes (`fixture_multi_sheet.xlsx`) |
| Sheet names normalized (trim whitespace) | yes (`fixture_whitespace_sheet.xlsx`) |
| In-sheet client labels ignored | yes (`fixture_metadata.xlsx`) |

### 5.5 Data-Level Assumptions

| Assumption | Testable via fixture |
|---|---|
| `DonationDate` parseable (MM/DD/YYYY, YYYY-MM-DD, text, Excel serial) | yes (`fixture_dates.xlsx`) |
| `DonationAmount` numeric > 0 | yes (`fixture_amounts.xlsx`) |
| `State` = valid 2-letter US code | yes (`fixture_states.xlsx`) |
| `ZIP` = 5-digit string, leading zeros preserved | yes (`fixture_zip.xlsx`) |

### 5.6 Processing Assumptions

| Assumption | Testable via fixture |
|---|---|
| Deterministic output for same input | yes (`fixture_deterministic.xlsx`) |
| Rejected rows only for visibility, not resubmission | yes (`fixture_rejected.xlsx`) |
| Multi-template workbooks handled | yes (`fixture_multi_template.xlsx`) |

---

## 6. Maintenance Guidelines

- Any new column alias must be added **to this document** and `mapping.json`.  
- New structural patterns (e.g., header beyond N rows) must be **validated and documented**.  
- Review this contract against the full fixture library **after T7-1 is complete**.  
- Ensure all assumptions remain **linked to test fixtures** for automated CI validation.

---

## 7. References

- `mapping.json` — alias mapping configuration  
- Fixture library (T7-1) — used for unit and integration tests  
- Pipeline tickets (T0–T7) — reference workflow and validation rules