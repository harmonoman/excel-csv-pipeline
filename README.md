# Excel → CSV Pipeline
## Overview

This project provides a simple interface for uploading Excel workbooks (with multiple sheets) containing donation data and transforming them into a single, clean, standardized CSV file ready for ingestion into a data warehouse.

The system is designed as an MVP with a clear path to production scalability.

## Goals
- Accept Excel workbooks with inconsistent formats
- Normalize and standardize donation data
- Enforce a strict schema
- Reject invalid records (no nulls allowed)
- Output a warehouse-ready CSV file
- Provide visibility into rejected records

## Final Output Schema

All records MUST conform to the following structure:

`First`, `Last`, `Address1`, `City`, `State`, `Zip`, `DonationDate`, `DonationAmount`, `Client`

## Rules

- All fields are required
- No null or missing values
- Invalid rows are excluded from final output

## Architecture (MVP)
```
Frontend (React)
    ↓
FastAPI Backend
    ↓
Pandas Processing Layer
    ↓
CSV Output + Error Report
```

## Tech Stack
### Frontend
- React
- Tailwind CSS
- React Dropzone (optional)
### Backend
- Python
- FastAPI
### Data Processing
- Pandas
- OpenPyXL
### Tooling
- Docker
- Git + GitHub
- Pytest

## How It Works
1. Upload
    - User uploads an Excel workbook (.xlsx) via the UI.
2. Ingestion
    - All sheets are read dynamically
    - Columns are normalized (lowercase, trimmed)
3. Column Mapping
    - A configuration-driven mapping system standardizes column names.

    - Example:
        ```
        "first_name" → First
        "zip_code" → Zip
        "amount" → DonationAmount
        ```
4. Transformation
    - Combine all sheets
    - Trim whitespace
    - Normalize casing
    - Convert types (dates, numeric values)
    - Add Client field (filename or user input)
5. Validation

    Each row must pass:

    - No missing fields
    - Valid date format
    - DonationAmount > 0
    - Valid ZIP and State format
6. Output

    Two files are generated:

        ✅ clean_donations.csv
            - Fully valid records
            - Ready for warehouse ingestion
        ❌ rejected_rows.csv
            - Invalid records
            - Includes error reasons per row

## Testing Strategy
### Unit Tests
- Column mapping logic
- Data transformations
- Validation rules
### Integration Tests
- Full pipeline using sample Excel files
- Output schema validation
### Edge Cases
- Missing columns
- Mixed formats across sheets
- Empty rows
- Invalid data types

## Project Structure
```
donor-bureau-pipeline/
│
├── frontend/
│   └── React app
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── processing/
│   │   │   ├── parser.py
│   │   │   ├── transformer.py
│   │   │   ├── validator.py
│   │   ├── config/
│   │   │   └── mapping.json
│   │   └── tests/
│
├── docker/
├── .github/workflows/
├── README.md
```

## Running the Project (MVP)

> **Prerequisites:** Docker Desktop and the VS Code Dev Containers extension (or any editor with dev container support).

### Start the dev container
Open the project in VS Code and select **Reopen in Container** when prompted (or run `Dev Containers: Reopen in Container` from the command palette). Dependencies are installed automatically on first build.

### Backend
    uvicorn app.main:app --reload

### Frontend
    cd frontend
    npm run dev

### Running tests
    uv run pytest

## Recurring File Handling

The system is designed to handle recurring uploads by:

- Using flexible column mapping
- Supporting multiple sheet formats
- Applying consistent validation rules

No manual cleanup should be required between uploads.

## Future Enhancements (Production Roadmap)
### Infrastructure
- AWS S3 for file storage
- Snowflake for data warehouse ingestion
- API Gateway + Lambda for serverless processing
### Scalability
- Asynchronous processing (Celery / queues)
- PySpark for large datasets
### Features
- User authentication
- Upload history dashboard
- Data quality metrics
- Real-time processing status
### Observability
- Logging (CloudWatch)
- Error tracking
- Processing metrics (rows processed, rejected, etc.)
### Data Governance
- Schema versioning
- Audit trails
- Configurable validation rules

## Known Limitations (MVP)
- Local file storage only
- No authentication
- Limited handling of extremely large files
- Manual download of outputs

## Success Criteria
- Users can upload Excel files without preprocessing
- Output CSV is 100% warehouse-ready
- Invalid data is clearly identified and isolated
- Pipeline works consistently across varied formats

## Design Philosophy
- Strict schema enforcement → prevents downstream failures
- Config-driven mapping → reduces manual work
- Transparency → users see exactly what failed and why
- Extensibility → easy path to production scaling

## TL;DR

Upload Excel → System cleans + validates → Get clean CSV + error report

Built with:

- React (UI)
- FastAPI (backend)
- Pandas (processing)

Designed to scale into a full production data pipeline.