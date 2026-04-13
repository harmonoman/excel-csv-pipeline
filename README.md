# Excel → CSV Donation Pipeline

A production-quality MVP data pipeline that ingests Excel workbooks containing donation data, validates and normalizes every row, and outputs a warehouse-ready clean CSV alongside a rejected rows report.

---

## What it does

Upload a `.xlsx` workbook with one or more sheets. The system parses every sheet, maps column aliases to a canonical schema, normalizes values, validates each row, and produces two downloadable CSV files:

- `clean_donations.csv` — fully valid rows, ready for warehouse ingestion
- `rejected_rows.csv` — invalid rows with a per-row rejection reason

**What it does not do (MVP scope):** authentication, background job queues, S3 storage, async processing, or schema versioning. All processing is synchronous and local.

---

## Output schema

Every row in the clean CSV conforms exactly to this column order:

| Field | Type | Notes |
|---|---|---|
| `First` | string | title-cased |
| `Last` | string | title-cased |
| `Address1` | string | whitespace-trimmed |
| `City` | string | title-cased |
| `State` | string | 2-letter US abbreviation, uppercased |
| `Zip` | string | exactly 5 digits, leading zeros preserved |
| `DonationDate` | string | ISO 8601 (YYYY-MM-DD) |
| `DonationAmount` | float | must be > 0 and finite |
| `Client` | string | derived from sheet tab name |

---

## Architecture

```
Browser (React + Vite)
        ↓  POST /upload (multipart .xlsx)
FastAPI backend
        ↓
Parser         — reads all sheets, detects header row per sheet, maps aliases
Normalizer     — title case, uppercase state, ISO dates, ZIP padding
Client inject  — assigns Client from sheet tab name
Validator      — null checks (T4-1) + type/domain rules (T4-2)
Splitter       — partitions rows into clean / rejected DataFrames
Schema gate    — enforces exact OUTPUT_SCHEMA column order
CSV writers    — writes clean + rejected CSVs to /tmp/donor-bureau/outputs/
        ↓
API response   — { total_rows, clean_rows, rejected_rows, clean_file, rejected_file }
        ↓
Browser        — displays summary, renders download links
        ↓  GET /download/{filename}
Browser downloads CSV
```

**Container layout:** backend and frontend run as separate Docker containers. The VS Code dev container attaches to the backend container only. The frontend container starts alongside it automatically via `docker compose up`.

---

## API endpoints

### `POST /upload`

Accepts a multipart `.xlsx` file upload. Runs the full pipeline synchronously and returns download links.

**Request:** `multipart/form-data`, field name `file`, `.xlsx` only.

**Response (200):**
```json
{
  "total_rows": 120,
  "clean_rows": 100,
  "rejected_rows": 20,
  "clean_file": "/download/{filename}_clean.csv",
  "rejected_file": "/download/{filename}_rejected.csv"
}
```

**Error responses:**
- `400` — wrong file type, empty file, or pipeline failure (structured `error` object)
- `422` — missing `file` field in request
- `500` — unexpected system failure (safe generic message, no stack trace)

### `GET /download/{filename}`

Serves a generated CSV file by name.

- `200` — CSV file content
- `400` — unsafe filename (path traversal rejected)
- `404` — file not found

### `GET /health`

Returns `{"status": "ok"}`. Used for container health checks.

---

## Data contract

The full input contract is documented in [`/docs/input_contract.md`](docs/input_contract.md). Key rules:

**File:** `.xlsx` only. One workbook = one upload batch. Each sheet tab = one client dataset.

**Header detection:** Header row is not required to be row 1. The parser scans the first 20 rows and selects the first row with ≥ 2 recognizable column aliases. Metadata rows before the header are automatically skipped.

**Column aliases** (`mapping.json` is authoritative):

| Output field | Accepted source aliases |
|---|---|
| `First` | `first`, `first_name`, `fname` |
| `Last` | `last`, `lastname`, `last_name`, `lname` |
| `Address1` | `address1`, `address`, `addr` |
| `City` | `city` |
| `State` | `state`, `st`, `state_code` |
| `Zip` | `zip`, `zip_code`, `zipcode` |
| `DonationDate` | `donationdate`, `giftdate`, `date`, `gift_date`, `donation_date` |
| `DonationAmount` | `donationamount`, `amount`, `gift_amount`, `donation_amount` |
| `Client` | derived from sheet tab name — never a source column |

Column names are matched case-insensitively with whitespace trimmed. Unmapped columns are silently dropped.

**Validation rules:**
- All 9 output fields must be present and non-empty
- `DonationAmount` must be numeric, finite, and > 0
- `DonationDate` must be parseable as a valid date (ISO, US format, natural language, Excel serial all accepted)
- `State` must be a valid 2-letter US abbreviation
- `Zip` must be exactly 5 digits

---

## Pipeline stages

| Stage | Module | Responsibility |
|---|---|---|
| Parse + Map | `parser.py` + `transformer.py` | Detect header, map aliases to canonical names per sheet before concatenation |
| Normalize | `normalizer.py` | Whitespace, title case, uppercase state, ISO date, ZIP string padding |
| Client inject | `client.py` | Add `Client` column from `_source_sheet` (sheet tab name) |
| Validate | `validator.py` | T4-1 missing field checks + T4-2 type/domain rules; adds `_is_valid` and `_rejection_reason` |
| Split | `splitter.py` | Partition into `clean_df` and `rejected_df` based on `_rejection_reason` |
| Schema gate | `schema.py` | Enforce exact `OUTPUT_SCHEMA` column set and order; raise on missing columns |
| Write | `writer.py` | Serialize to UTF-8 CSV (no BOM, no index column) |
| Orchestrate | `pipeline.py` | Execute stages in strict order; halt on any failure |
| Observe | `logging_utils/metrics.py` | Emit one `[PIPELINE_METRICS]` log line per upload |

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, react-dropzone |
| Backend | Python 3.12, FastAPI, uvicorn |
| Processing | pandas, openpyxl |
| Dependency management | uv |
| Testing | pytest, httpx (FastAPI TestClient) |
| Containerization | Docker, Docker Compose |

---

## Project structure

```
excel-csv-pipeline/
├── .devcontainer/
│   └── devcontainer.json          — attaches VS Code to backend container
├── .github/workflows/
│   └── ci.yml                     — runs uv run pytest on push/PR
├── Dockerfile                     — Python 3.12 backend image
├── docker-compose.yml             — backend (8000) + frontend (5173)
│
├── backend/
│   ├── pyproject.toml             — dependencies + pytest config
│   ├── conftest.py
│   └── app/
│       ├── main.py                — FastAPI app, /upload, /download, /health
│       ├── config/
│       │   ├── mapping.json       — canonical field aliases (source of truth)
│       │   └── loader.py          — config validation on startup
│       ├── processing/
│       │   ├── parser.py          — multi-sheet parse + header detection
│       │   ├── transformer.py     — alias → canonical column mapping
│       │   ├── normalizer.py      — value normalization
│       │   ├── client.py          — Client field injection
│       │   ├── validator.py       — T4-1 null + T4-2 type/domain validation
│       │   ├── splitter.py        — clean/rejected split
│       │   ├── schema.py          — final schema enforcement
│       │   ├── pipeline.py        — stage orchestrator
│       │   └── errors.py          — PipelineError definition
│       ├── output/
│       │   └── writer.py          — CSV serialization
│       ├── utils/
│       │   └── file_naming.py     — deterministic UTC timestamp filenames
│       ├── logging_utils/
│       │   └── metrics.py         — PIPELINE_METRICS structured log line
│       └── tests/
│           ├── fixtures.py        — in-memory workbook builder (unit tests)
│           ├── integration/
│           │   ├── test_full_pipeline.py   — T7-2: 9 end-to-end tests
│           │   └── test_edge_cases.py      — T7-3: 8 edge case tests
│           └── test_*.py          — 268 unit tests across all pipeline stages
│
├── frontend/
│   ├── package.json               — React 18, react-dropzone, Vite
│   ├── vite.config.js             — proxies /upload and /download to backend
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── UploadDropzone.jsx — drag-and-drop upload with xlsx validation
│           └── UploadResult.jsx   — summary display + download links
│
└── docs/
    ├── input_contract.md          — file + column + validation contract
    └── fixture_catalog.md         — fixture library documentation
```

---

## How to run

### Prerequisites

- Docker Desktop
- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Start everything

```bash
docker compose up
```

This starts two containers:
- **backend** at `http://localhost:8000`
- **frontend** at `http://localhost:5173`

Open `http://localhost:5173` in your browser.

### Open in dev container (VS Code)

Open the project folder in VS Code, then select **Reopen in Container** when prompted (or run `Dev Containers: Reopen in Container` from the command palette).

The dev container attaches to the **backend** container. Python dependencies are installed automatically via `uv sync --dev` on first build.

### Run tests

Inside the dev container terminal:

```bash
cd /workspace/backend
uv run pytest
```

Run only integration tests:

```bash
uv run pytest app/tests/integration/ -v
```

Run only unit tests:

```bash
uv run pytest app/tests/ --ignore=app/tests/integration -v
```

---

## Testing strategy

The test suite has 285 tests across three layers, all passing.

### Unit tests (268)

Each pipeline stage is tested in isolation with programmatic in-memory workbooks. No filesystem, no API layer.

| File | What it tests |
|---|---|
| `test_parser.py` | Header detection, metadata row skipping, multi-sheet concat |
| `test_transformer.py` | Alias mapping, case-insensitive matching, unknown column dropping |
| `test_normalizer.py` | Title case, ZIP padding, date parsing, type casting |
| `test_validator.py` | T4-1 null checks, T4-2 type/domain rules, infinity rejection |
| `test_splitter.py` | Clean/rejected partitioning, no row leakage |
| `test_schema.py` | Schema enforcement, missing column detection |
| `test_writer.py` | CSV output format, UTF-8, no index column |
| `test_pipeline.py` | Stage ordering, error propagation, full flow |
| `test_logging.py` | PIPELINE_METRICS log line emission |
| `test_download.py` | API response schema, download endpoint |
| `test_error_handling.py` | HTTP error codes, structured error responses |

### Integration tests (17)

Real `.xlsx` fixtures uploaded through the real API. No mocks. CSV output downloaded and validated.

**T7-2 — Full pipeline** (`test_full_pipeline.py`, 9 tests):
- Happy path (all valid rows)
- Header offset (metadata rows before header)
- All rejected (missing required columns)
- Empty workbook (header only, zero rows)
- Mixed data (multiple date formats)
- Multi-sheet (3 sheets, different aliases per sheet)
- Deterministic output (same fixture → identical CSV content)
- Row conservation invariant across all fixtures
- Schema invariant across all fixtures

**T7-3 — Edge cases** (`test_edge_cases.py`, 8 tests):
- All rows rejected
- All rows clean
- Single row clean
- Single row rejected
- Header-only sheet
- 10,000 row throughput (9,000 clean / 1,000 rejected)
- Row conservation invariant across all edge case fixtures
- Schema invariant across all edge case fixtures

### Fixture library

12 `.xlsx` fixture files in `backend/app/tests/fixtures/`. Each is documented in [`/docs/fixture_catalog.md`](docs/fixture_catalog.md).

| Fixture | Purpose |
|---|---|
| `fixture_perfect.xlsx` | Happy path baseline, 5 valid rows |
| `fixture_header_offset.xlsx` | Metadata rows before header (real-world Alpha Fund format) |
| `fixture_missing_columns.xlsx` | Missing `Last` and `Zip` — all rows rejected |
| `fixture_mixed_dates.xlsx` | ISO, US format, natural language, Excel serial dates |
| `fixture_zip_edge_cases.xlsx` | Leading zeros, invalid length, non-numeric ZIPs |
| `fixture_multi_sheet.xlsx` | 3 sheets, 3 alias sets, 1 metadata offset |
| `fixture_empty_sheet.xlsx` | Valid header, zero data rows |
| `fixture_no_header.xlsx` | No detectable header — sheet excluded with warning |
| `fixture_single_row_clean.xlsx` | 1 valid row |
| `fixture_single_row_rejected.xlsx` | 1 invalid row (missing First) |
| `fixture_large_10k.xlsx` | 10,000 rows (9,000 clean, 1,000 rejected) |
| `fixture_large.xlsx` | 1,000 rows, all clean |

---

## Frontend

React + Vite single-page app. No TypeScript, no UI framework.

**Upload flow:**
1. User drags and drops or clicks to select a `.xlsx` file
2. Client-side extension check (`.xlsx` only, 0-byte files rejected)
3. On submit: `POST /upload` via `FormData`, loading state shown
4. On success: summary card (total / clean / rejected row counts) + download links
5. On error: readable error message, retry available

The Vite dev server proxies `/upload` and `/download` to the FastAPI backend at `http://localhost:8000`, avoiding CORS issues in local development.

---

## MVP constraints

These are documented decisions, not gaps:

- **Synchronous processing only.** No Celery, no background jobs, no async queues. One request blocks until processing completes.
- **Local filesystem storage.** Output CSVs are written to `/tmp/donor-bureau/outputs/` inside the backend container. Files are not persisted across container restarts.
- **No authentication.** Any user can upload.
- **No deduplication.** The same file uploaded twice produces two independent output pairs.
- **Second-precision file naming.** Two uploads within the same second produce the same filename. This is a documented MVP trade-off.
- **No CORS configuration.** The Vite proxy handles CORS avoidance in development. Production deployment would require adding `CORSMiddleware` to FastAPI.

---

## Known design decisions

**React + Vite, no TypeScript.** The component surface is small (two components). TypeScript adds toolchain complexity with no payoff at MVP scale.

**pandas for processing.** Sufficient for the synchronous MVP workload. PySpark is on the production roadmap for large-scale processing.

**openpyxl for Excel parsing.** Reads `.xlsx` in read-only mode with `data_only=True` for reliable value extraction without formula evaluation.

**Per-sheet mapping before concatenation.** Aliases are resolved per sheet before `pd.concat`. This prevents NaN leakage when sheets use different aliases for the same canonical field.

**`PipelineError` in `errors.py`.** Decoupled from `pipeline.py` to avoid circular imports with stage modules that need to raise it.

**Fixture-driven integration tests.** Real `.xlsx` files through the real API. No mocks in any integration test. Same fixtures reused across T7-2 and T7-3 test suites.

---

## Production roadmap

- AWS S3 for output file persistence
- Snowflake ingestion endpoint
- Async processing (Celery + SQS)
- User authentication
- CORS configuration for deployment
- Upload history dashboard
- CloudWatch logging integration
- Schema versioning + audit trail
