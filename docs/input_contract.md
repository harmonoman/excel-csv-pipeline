# Input Contract — Donor Bureau Excel Pipeline

**Version:** 1.0  
**Status:** MVP  
**Last updated:** 2026-04-08  

This document is the source of truth for the expected structure of incoming Excel workbooks. All pipeline components (parser, transformer, validator) must conform to these expectations. Any new file format introduced must be validated against this contract before being accepted into the pipeline.

---

## 1. File-Level Structure

| Property | Expectation |
|---|---|
| Format | `.xlsx` only |
| Upload unit | One workbook = one upload batch |
| Client segmentation | Each sheet tab = one distinct client dataset |
| Client identifier | Sheet tab name is the authoritative source of the `Client` value |
| File size | Under 10MB (in-memory processing) |
| Encoding | UTF-8 compatible |

---

## 2. Sheet-Level Structure

### 2.1 Metadata Rows

Each sheet may contain one or more metadata rows **before** the real header row.

**Confirmed real-world example (Alpha Fund sheet):**

```
Row 1: "Prepared for internal review"
Row 2: "Client: Alpha Fund"
Row 3: (empty)
Row 4: First | LastName | Address1 | City | ST | Zip | GiftDate | Amount  ← real header
Row 5+: data
```

**Rules:**
- Metadata rows must be skipped during ingestion
- Metadata rows are never treated as headers or data
- Any "Client: X" label appearing in the sheet body is ignored — `Client` is always derived from the sheet tab name only

### 2.2 Header Detection

- The real header row is the **first row** containing a minimum threshold of recognizable column aliases from `mapping.json`
- Header row is **not guaranteed to be row 1**
- Detection scans the first **N rows** (configurable via `mapping.json` → `header_scan_rows`)
- Threshold: a row must contain **≥ 2 mapped columns** to be accepted as the header
- Detection stops at the first row meeting the threshold (no scoring or ranking)
- Sheets with no detectable header within the first N rows are excluded from processing and a warning is logged

### 2.3 Data Rows

- Data rows begin immediately after the detected header row
- Empty rows within the data range are skipped
- Sheets with a valid header but zero data rows are skipped without error

---

## 3. Column-Level Structure

### 3.1 Required Output Fields and Known Source Aliases

All aliases are treated as **case-insensitive**. Column names are normalized (lowercased, whitespace trimmed) before alias matching.

| Output Field | Known Source Aliases |
|---|---|
| `First` | `first`, `first_name`, `fname` |
| `Last` | `last`, `lastname`, `last_name`, `lname` |
| `Address1` | `address1`, `address`, `addr` |
| `City` | `city` |
| `State` | `state`, `st` |
| `Zip` | `zip`, `zip_code`, `zipcode` |
| `DonationDate` | `donationdate`, `giftdate`, `date`, `gift_date` |
| `DonationAmount` | `donationamount`, `amount`, `gift_amount`, `donation` |
| `Client` | **Derived from sheet tab name — never a source column** |

### 3.2 Unmapped Columns

- Unmapped columns are allowed in source files
- They are silently dropped during the mapping stage
- Dropped column names are logged for traceability

### 3.3 Column Name Treatment

- All source column names are normalized to lowercase and trimmed before alias lookup
- Matching is case-insensitive
- Leading/trailing whitespace in column names is ignored

---

## 4. Explicitly Out of Scope (MVP)

The following are not supported and will produce undefined behavior if present:

- Merged cells
- Multi-row headers
- Embedded images or charts
- Password-protected sheets
- Non-tabular layouts
- Formulas in data cells (values will be read as-is)

---

## 5. Structural Assumptions

| # | Assumption |
|---|---|
| 1 | Metadata rows appear before the header row (observed: rows 1–3 metadata, row 4 header in Alpha Fund sheet) |
| 2 | Sheet tab names are descriptive and usable as client identifiers |
| 3 | Any "Client: X" label in the sheet body is redundant and ignored |
| 4 | Column naming varies across clients and templates but is resolvable via `mapping.json` |
| 5 | No merged cells or heavily styled Excel artifacts are present in the data range |
| 6 | A single workbook may contain sheets from multiple clients (one per tab) |
| 7 | All sheets in a workbook follow the same structural pattern (metadata rows → header → data) |

---

## 6. Maintenance

- Any new column alias observed in a real-world file must be added to this document **and** to `mapping.json` before that file is accepted into the pipeline
- Any new structural pattern (e.g., header offset beyond N rows) must be validated and documented here before the pipeline is adjusted
- This document must be reviewed against the full fixture library once T7-1 is complete
