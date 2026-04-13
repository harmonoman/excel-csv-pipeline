# Prompt History

This document tracks the evolution of prompts used during the development of the Donor Bureau Excel → CSV Pipeline.

It captures:
- Prompt intent
- Iteration flow between tools (ChatGPT ↔ Claude)
- Key decisions and outcomes

---

## How to Read This Document

Each entry includes:
- **ID**: Unique identifier for reference
- **Author**: Who initiated the prompt (Mark, ChatGPT, Claude)
- **Target**: Which system the prompt was sent to
- **Purpose**: Why the prompt was created
- **Prompt**: The actual prompt text
- **Summary of Response**: Key output or decisions
- **Impact**: How it influenced the project

---

## Prompt Log

---


### Prompt ID: P-001

- **Author:** Mark  
- **Target:** ChatGPT  
- **Purpose:** Excel-to-CSV ingestion system proposal
#### Prompt
```
You are a data engineer with a front end developer background and a project manager's perspective for Donor Bureau and you are needing to build a system where you provide the user with an interface where they can upload an Excel Workbook file containing donation data across multiple tabs. 

Your task is to Create a simple interface where a user can upload an Excel workbook and receive a single, clean, standardized CSV file suitable for ingestion into a data warehouse. 

The final dataset must include the following fields: First, Last, Address1, City, State, Zip, DonationDate, DonationAmount, Client 

Important: All fields are required. Any record with missing or null values will be rejected by the data warehouse. 

Assume this type of data will be received on a recurring basis. Your solution should be designed so it can handle similar files without requiring manual cleanup each time. 

To begin, please develop a project proposal for how this should be done so as to be production ready (testing included). What technologies should be included? Version control?
```
- **Summary of Response:**
    - Proposed full-stack architecture with frontend upload interface and backend processing service
    - Recommended use of Python (Pandas) for transformation and FastAPI for API layer
    - Introduced validation rules to enforce required fields and reject bad records
    - Included testing strategy and version control using Git with structured branching
- **Impact:**
    - Established foundation for system architecture and tech stack
    - Defined core data validation requirements critical for warehouse ingestion
    - Set direction for scalable, repeatable ingestion pipeline without manual cleanup
---

### Prompt ID: P-002
- **Author:** Mark  
- **Target:** ChatGPT  
- **Purpose:** README creation for MVP and future roadmap
#### Prompt
```
Please construct a README.md for this project from a MVP perspective (with the future additions included)
```
- **Summary of Response:**
    - Generated a structured README including project overview, objectives, and MVP scope
    - Defined core features such as file upload, transformation, validation, and CSV output
    - Included tech stack, setup instructions, and basic usage flow
    - Added future enhancements like automation, scaling, and advanced validation
- **Impact:**
    - Created foundational documentation for the project
    - Clarified MVP boundaries while outlining long-term vision
    - Provided a reference point for onboarding and development alignment
---

### Prompt ID: P-003
- **Author:** Mark  
- **Target:** ChatGPT  
- **Purpose:** Agile project plan prompt for Claude (MVP-focused)
#### Prompt
```
Lets take a step back for a second and I would like you to create the project plan prompt for Claude code.  

This needs to be a lightweight project that seeks to reach an MVP level with a plan for future development but a clean simple path to the main objective.  

We also need to build it in a dev container including uv to handle dependencies.  

While building please take into consideration assumptions that would need to be checked off before continuing.  

This should be ticket based from an agile development approach that is test driven. 

Don't generate the code only the plan to start.
```
- **Summary of Response:**
    - Outlined ticket-based agile project plan structured around MVP milestones
    - Incorporated dev container setup with uv for dependency management
    - Defined assumption checkpoints to validate before progressing between phases
    - Emphasized test-driven development with clear separation of planning vs. implementation
- **Impact:**
    - Established execution framework for building the project in a controlled, iterative way
    - Enabled collaboration with Claude using structured, actionable prompts
    - Ensured development discipline through TDD, environment consistency, and validation gates
---

### Prompt ID: P-004
- **Author:** ChatGPT  
- **Target:** Claude
- **Purpose:** Structured MVP project planning prompt for Claude
#### Prompt
```
# 🧠 Claude Code Prompt: Donor Bureau Excel → CSV Pipeline (MVP Plan)

You are acting as a **Senior Data Engineer + Frontend Developer + Technical Project Manager**.

Your task is to create a **lightweight, production-minded MVP project plan** for a system that allows users to:

> Upload an Excel workbook (multiple sheets) and receive a clean, standardized CSV file ready for ingestion into a data warehouse.

---

## 🎯 Core Requirements

The final dataset MUST include:

* First
* Last
* Address1
* City
* State
* Zip
* DonationDate
* DonationAmount
* Client

### Hard Constraints:

* ALL fields are required
* NO null or missing values
* Invalid rows must be rejected (not silently fixed)
* System must handle **recurring uploads with inconsistent formats**

---

## 🧩 Scope Expectations

### MVP Focus (DO NOT OVERENGINEER)

* Simple upload interface
* Backend processing pipeline
* CSV output + rejected rows report
* Config-driven column mapping
* Local execution (no cloud required yet)

### Explicitly OUT of scope (for now):

* Authentication
* Distributed systems
* Real-time streaming
* Complex UI/UX

---

## ⚙️ Technical Constraints

### Environment

* MUST use a **Dev Container**
* MUST use **uv** for dependency management
* Python-based backend required

### Suggested Stack

* Backend: FastAPI
* Processing: Pandas
* Frontend: Minimal (can be basic HTML or simple React)
* Testing: pytest

---

## 🧪 Development Approach

You MUST follow:

### 1. Test-Driven Development (TDD)

* Every feature begins with a failing test
* Then implement minimal code to pass
* Then refactor

### 2. Agile / Ticket-Based Execution

Break work into:

* Epics
* User Stories
* Tickets (small, actionable)

Each ticket MUST include:

* Description
* Acceptance Criteria
* Assumptions
* Test Plan

---

## ⚠️ Critical Design Requirements

### 1. Schema Enforcement Layer

Strict validation:

* No missing values
* Correct data types
* Reject invalid rows

### 2. Config-Driven Column Mapping

System must handle inconsistent column names via config (JSON/YAML)

Example:

* "first_name", "fname" → First

### 3. Multi-Sheet Handling

* Automatically read and combine all sheets
* No hardcoding sheet names

### 4. Deterministic Output

* Same input → same output
* Idempotent processing

---

## 🧱 Required Output From You

Generate a **complete project plan ONLY (NO CODE)** including:

---

### 1. 📌 Assumptions & Open Questions

List all assumptions that MUST be validated before development begins.

Example:

* Expected Excel formats?
* Max file size?
* Is Client derived from filename or user input?

---

### 2. 🗺️ MVP Architecture

* High-level system design
* Data flow
* Key components

---

### 3. 📁 Project Structure

Include:

* Dev container setup
* Backend layout
* Test directories
* Config location

---

### 4. 🔁 Development Plan (Agile Tickets)

Organize into:

#### EPIC 1: Project Setup

#### EPIC 2: File Ingestion

#### EPIC 3: Data Processing

#### EPIC 4: Validation Engine

#### EPIC 5: Output Generation

#### EPIC 6: Frontend Upload Interface

#### EPIC 7: Testing & QA

Each EPIC must contain:

* User Stories
* Tickets

Each Ticket must include:

* Description
* Acceptance Criteria
* Assumptions
* Test Plan

---

### 5. 🧪 Testing Strategy

* Unit tests
* Integration tests
* Edge cases
* Data quality checks

---

### 6. 🚀 MVP Definition of Done

Clearly define what “done” means for MVP.

---

### 7. 🔮 Future Roadmap (Post-MVP)

Keep it concise but actionable:

* Scaling (S3, Snowflake)
* Async processing
* Observability
* UI improvements

---

## 🧠 Behavioral Instructions

* Be concise but structured
* Prefer clarity over completeness
* Avoid unnecessary complexity
* Think like a solo developer shipping quickly
* Highlight risks early
* Design for iteration

---

## 🚫 DO NOT:

* Write implementation code
* Suggest over-engineered solutions
* Assume perfect input data
* Skip validation logic

---

## ✅ SUCCESS CRITERIA

Your output should:

* Be immediately actionable
* Break work into clear tickets
* Support TDD workflow
* Be realistic for a solo developer MVP
* Provide a clean path to production scaling

---

Begin.
```
- **Summary of Response:**
    - Created a highly structured, constraint-driven prompt tailored for Claude to generate a full MVP project plan
    - Defined strict requirements around TDD, agile ticketing, validation, and deterministic processing
    - Included detailed output expectations (architecture, tickets, assumptions, testing, roadmap)
    - Balanced MVP simplicity with production-minded design and future scalability
- **Impact:**
    - Enabled effective delegation of project planning to Claude with clear expectations
    - Standardized planning format to ensure consistency and completeness
    - Accelerated transition from ideation to actionable development plan
---

### Prompt ID: P-005
- **Author:** Mark  
- **Target:** ChatGPT  
- **Purpose:** Ticket review for MVP alignment and TDD completeness
#### Prompt
```
Putting on your senior project manager hat on please review these Claude generated tickets against our readme and Claude project plan prompt to make sure the tickets and details therein adhere to our original game plan:

<Claude generated tickets>

Ok that's all the tickets as they currently stand after assumptions have been answered and updated in the tickets.  

You are a senior data engineer and project manager.  

Please do a full review of this project with the MVP path in mind as our immediate and ultimate goal in mind - checking for completeness with test based development as the backdrop for quality.
```
- **Summary of Response:**
    - Evaluated ticket set against MVP scope, README, and original planning constraints
    - Identified gaps in TDD coverage, validation rigor, and acceptance criteria clarity
    - Highlighted risks around over-engineering vs. MVP simplicity
    - Recommended refinements to ensure tickets are actionable, testable, and aligned to core requirements
- **Impact:**
    - Improved alignment between planning artifacts (README, prompt, tickets)
    - Strengthened test-driven development discipline across the project
    - Reduced risk of scope creep while reinforcing MVP-focused execution
---

### Prompt ID: P-006
- **Author:** Mark  
- **Target:** Claude
- **Purpose:** Ticket classification and documentation guidance
#### Prompt
```
Based on what you now know,  please review this next ticket in the T0 epic.  Does it also belong in the input_contract.md file or should this be it's own thing?:

<T0-3 - Sample file validation>

Please put on your senior project manager hat: given where we are in the project should we create a placeholder file with a description of it's purpose and a plan for when it should be updated?
```
- **Summary of Response:**
    - Evaluated whether <T0-3 - Sample file validation> fits within input_contract.md or warrants separate documentation
    - Recommended creating a placeholder file capturing purpose, validation rules, and update plan
    - Advised on maintaining clear linkage to MVP requirements and future updates
- **Impact:**
    - Improved documentation strategy and traceability for sample file validation
    - Prevented potential ambiguity in input expectations
    - Provided a structured path for future updates without blocking current development
---

### Prompt ID: P-007
- **Author:** Mark  
- **Target:** Claude  
- **Purpose:** Dev container setup review and code validation
#### Prompt
```
ok moving onto this epic:

[ ] T1-1 - Dev container + uv scaffold
[ ] T1-2 - Github Action CI pipeline
[ ] T1-3 - mapping.json config skeleton

let's focus on this first ticket:

T1-1 - Dev container + uv scaffold

<ticket details>

As a senior data engineer please walk through the steps and generate the proper files needed (ie - Dockerfile, devcontainer.json, docker-compose.yml)

(Claude generates code)

Please take on the role of senior data engineer and perform a code review on these files that has been generated for the Dev container and uv setup ticket
```

- **Summary of Response:**
    - Reviewed Dockerfile, devcontainer.json, and docker-compose.yml for correctness and best practices
    - Validated Python environment, dependency management with uv, and container reproducibility
    - Checked alignment with project structure and TDD workflow
    - Identified any potential improvements, such as layer caching, security settings, or volume mounting
- **Impact:**
    - Ensured dev container setup is production-ready and repeatable
    - Reduced risk of environment inconsistencies for team development
    - Provided actionable feedback to refine scaffold and maintain alignment with MVP objectives
---

### Prompt ID: P-008
- **Author:** Mark  
- **Target:** ChatGPT
- **Purpose:** CI pipeline necessity evaluation and architectural decision
#### Prompt
```
Moving onto T1-2 - Github Actions CI pipeline: 

Description 
Create workflow: install uv, run uv sync, run pytest. 
Trigger on push and PR to main. 

Acceptance criteria 
PR with failing test shows red CI PR with passing tests shows green CI 

Test plan 
Push a deliberately failing test, verify CI fails. Fix it, verify CI passes. 

As a metaphorical based senior bootcamp instructor, please start out by explaining why Github Actions is useful for and evaluate if It's truely needed to reach MVP criteria for this project. 

Then take on the role of the senior data engineer and make the case for why we should or should not use Github Actions on this project.
```

- **Summary of Response:**
    - Explained GitHub Actions as a tool for automated testing, validation, and enforcing code quality on every push/PR
    - Evaluated CI as not strictly required for MVP but highly beneficial for maintaining TDD discipline
    - Argued in favor of including CI early due to low setup cost and high long-term value
    - Framed decision as balancing speed to MVP vs. quality assurance and scalability
- **Impact:**
    - Informed decision to likely include CI despite MVP scope constraints
    - Reinforced importance of automated testing in maintaining code reliability
    - Helped align development process with professional engineering practices
---

### Prompt ID: P-009
- **Author:** Mark  
- **Target:** ChatGPT
- **Purpose:** Claude prompt creation for CI pipeline implementation
#### Prompt
```
Based on that, please create a prompt for Claude to build (as a senior data engineer) this ticket and also walk through it's particular importance in our specific pipeline keep in mind we've built our dev container as that might influence steps involved
```

- **Summary of Response:**
    - Generated a structured prompt instructing Claude to implement the GitHub Actions CI pipeline
    - Included steps for integrating uv, running tests, and aligning with the dev container environment
    - Emphasized CI’s role in enforcing validation and TDD within the pipeline
    - Provided context on why CI is critical for ensuring data quality and consistent processing
- **Impact:**
    - Enabled seamless delegation of CI implementation to Claude
    - Ensured CI setup aligns with existing dev container architecture
    - Strengthened reliability and automation within the development workflow
---

### Prompt ID: P-010
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** CI pipeline implementation prompt with project-specific justification
#### Prompt
```
# 🧠 Claude Code Prompt: T1-2 GitHub Actions CI Pipeline (MVP)

You are acting as a **Senior Data Engineer** working on the Donor Bureau Excel → CSV pipeline.

Your task is to implement **T1-2: GitHub Actions CI pipeline** and explain its importance in the context of this project.

---

## 🎯 Ticket Context

We are building a **data ingestion pipeline** that:

* Accepts Excel workbooks with multiple sheets
* Dynamically maps inconsistent column names
* Enforces a strict schema
* Rejects invalid rows
* Outputs a clean CSV for warehouse ingestion

This system is:

* Highly dependent on **data correctness**
* Sensitive to **silent failures**
* Built using **test-driven development (pytest + fixtures)**

---

## ⚙️ Current Environment

We already have:

* Dev container using:

  * Python 3.12
  * `uv` for dependency management
* `pyproject.toml` with:

  * runtime + dev dependencies
* Docker + docker-compose setup
* FastAPI backend
* pytest configured (`app/tests`)

Important:

* Local development runs inside a **dev container**
* CI must work **independently of the dev container**
* Do NOT rely on Docker for CI (keep it simple for MVP)

---

## 📌 Your Tasks

### 1. Create GitHub Actions Workflow

Create a minimal workflow file:


.github/workflows/ci.yml


The workflow must:

* Trigger on:

  * push to `main`
  * pull requests to `main`
* Run on:

  * `ubuntu-latest`
* Steps:

  1. Checkout repository
  2. Install Python 3.12
  3. Install `uv`
  4. Run `uv sync`
  5. Run `pytest`

---

### 2. Ensure Compatibility with Project Setup

* Use `uv` (NOT pip)
* Respect `pyproject.toml` + `uv.lock`
* Ensure tests run from correct directory (`backend/` if needed)
* Keep setup minimal and fast

---

### 3. Explain Why CI Matters for THIS Pipeline

Provide a concise explanation tailored to this project:

Focus on:

* Why CI is critical for **data pipelines vs typical apps**
* Risks of **silent data corruption**
* How CI supports:

  * mapping logic
  * validation rules
  * deterministic outputs
* Why relying only on local testing is risky

---

### 4. Validate Against Acceptance Criteria

Ensure your solution satisfies:

* Failing tests → CI fails (red)
* Passing tests → CI passes (green)
* No unnecessary complexity added

---

### 5. Keep MVP Scope Tight

DO:

* Keep workflow minimal
* Focus only on testing

DO NOT:

* Add linting
* Add coverage reports
* Add Docker builds
* Add deployment steps

---

## 🧪 Testing Instructions (for developer)

Include a short section explaining how to verify:

1. Add a failing test → push → confirm CI fails
2. Fix test → push → confirm CI passes

---

## 🧠 Output Format

Provide:

1. `ci.yml` file contents
2. Brief explanation of key decisions
3. Why CI is important specifically for THIS pipeline
4. How to test the pipeline locally and in GitHub

---

## 🚫 Do NOT

* Over-engineer the workflow
* Add unnecessary steps
* Assume Docker is used in CI
* Skip explanation

---

## ✅ Success Criteria

Your output should:

* Be immediately usable
* Work with existing `uv` + dev container setup
* Reinforce TDD workflow
* Align with MVP simplicity

---

Begin.
```

- **Summary of Response:**
    - Produced a highly detailed Claude prompt to implement the GitHub Actions CI pipeline
    - Incorporated strict alignment with existing dev container and uv-based environment
    - Emphasized data pipeline risks (e.g., silent corruption) to justify CI importance
    - Defined clear output expectations, acceptance criteria, and testing validation steps
- **Impact:**
    - Enabled precise and high-quality CI implementation via Claude
    - Reinforced TDD and data validation as critical pillars of the project
    - Ensured CI setup remains lightweight while still production-minded
---

### Prompt ID: P-011
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for config-driven mapping system (MVP + TDD)
#### Prompt
```
ok moving onto T1-3 - mapping.json config skeleton: 

Description 
Create app/config/mapping.json with initial column alias map. 
Document the format. 
Loader utility reads and validates config on startup. 

Acceptance criteria 
Config loads without error on app start Missing required keys raises a clear startup error At least 3 aliases per target field seeded Config includes header_scan_rows integer key, raises startup error if missing or non-integer. 

Mapping seeds (confirmed from real source data) 
first_name, fname, first → First 
lastname, last_name, lname, last → Last 
address1, address, addr → Address1 
city → City 
st, state, state_code → State 
zip, zip_code, zipcode → Zip 
giftdate, gift_date, donationdate, donation_date, date → DonationDate 
amount, donationamount, donation_amount, gift_amount → DonationAmount 

Assumptions 
Additional aliases will be added as new source formats are introduced All alias matching is case-insensitive (normalization handled before lookup) header_scan_rows defaults to 20 if not overridden, but must be explicitly present in config 

Test plan 
Unit test: valid config loads correctly and all required keys are present 
Unit test: malformed config (missing header_scan_rows) raises ValueError with descriptive message 
Unit test: missing canonical field (e.g. no entry for Last) raises ValueError on startup 
Unit test: confirm all seeded aliases are present and correctly mapped 

From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan
```

- **Summary of Response:**Generated a structured Claude prompt for implementing a config-driven column mapping system
    - Enforced strict schema validation, startup checks, and deterministic mapping behavior
    - Included explicit alias mappings for all required donor data fields
    - Required TDD-based implementation with unit tests for validation, loading, and error handling
- **Impact:**
    - Established a robust configuration backbone for data normalization
    - Ensured extensibility for future data source formats via alias mapping
    - Strengthened system reliability by enforcing startup validation and fail-fast behavior
---

### Prompt ID: P-012
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Strict TDD-driven config mapping system implementation prompt
#### Prompt
```
# 🧠 Claude Code Prompt: T1-3 Mapping JSON Config Skeleton (MVP)

You are acting as a **Lead Data Engineer** implementing T1-3 for the Donor Bureau Excel → CSV ingestion pipeline.

This system is a **strict schema enforcement data pipeline** that transforms inconsistent Excel workbooks into a clean, warehouse-ready dataset.

---

## 🎯 Ticket Goal

Create a **configuration-driven column mapping system** using:


app/config/mapping.json


This file defines:

* Canonical field names
* Alias mappings from inconsistent Excel source columns
* Header detection configuration

You must also implement a **loader utility that validates and loads this config at application startup**.

---

## ⚙️ Existing System Context

We already have:

* Python 3.12 dev container
* `uv` dependency management
* FastAPI backend
* pytest-based TDD structure
* Pipeline architecture:


parse → map → normalize → validate → split → output


This config is foundational to:

* parser logic
* column mapping engine
* validation stage consistency

---

## 📌 Required Mapping Schema

Create `mapping.json` with the following structure and seeded aliases:

```json id="cfg1"
{
"header_scan_rows": 20,
"fields": {
  "First": ["first_name", "fname", "first"],
  "Last": ["lastname", "last_name", "lname", "last"],
  "Address1": ["address1", "address", "addr"],
  "City": ["city"],
  "State": ["st", "state", "state_code"],
  "Zip": ["zip", "zip_code", "zipcode"],
  "DonationDate": ["giftdate", "gift_date", "donationdate", "donation_date", "date"],
  "DonationAmount": ["amount", "donationamount", "donation_amount", "gift_amount"]
}
}
⚙️ Functional Requirements
1. Config Loader Utility

Implement a Python utility that:

Loads mapping.json at application startup
Validates structure strictly
Raises startup error immediately if invalid
2. Validation Rules

The loader MUST enforce:

Required Keys
header_scan_rows must exist
Must be an integer
Must default to 20 ONLY if explicitly set (no silent defaults allowed)
Field Validation
All canonical fields must exist:
First
Last
Address1
City
State
Zip
DonationDate
DonationAmount
Each canonical field must have:
At least 1 alias
Preferably ≥ 3 aliases (as seeded above)
Alias Rules
Alias matching is case-insensitive
Aliases are normalized before use (assume normalization handled elsewhere)
3. Failure Behavior (Critical)

If config is invalid:

Raise ValueError (or custom ConfigValidationError)
Provide clear, developer-friendly error message
Fail FAST at startup (do not continue partial execution)

Example:

Missing required field: Last

or

header_scan_rows must be an integer, got str
🧪 TDD REQUIREMENTS

You MUST implement using test-driven development:

Required Tests
Valid config loads successfully
All fields present
No exceptions raised
Missing header_scan_rows
Raises ValueError with clear message
Missing canonical field
e.g. removing "Last"
Must fail startup validation
Alias integrity test
Ensure all seeded aliases are correctly loaded
Ensure no canonical field has empty alias list
🧱 Design Constraints (MVP Discipline)

DO:

Keep implementation minimal
Keep config loader simple and deterministic
Fail fast on invalid config

DO NOT:

Add environment-specific config layers
Add schema frameworks (no pydantic unless absolutely necessary)
Add dynamic config reloading
Over-engineer plugin systems
🧠 Why This Matters (Explain in Output)

After implementation, briefly explain:

1. Why config-driven mapping is critical in this pipeline
Handles inconsistent Excel formats
Prevents hardcoded parsing logic
Enables future template expansion
2. Why strict validation at startup matters
Prevents silent data corruption
Ensures pipeline fails fast instead of producing bad CSVs
3. Why this is foundational to the entire system
Parser → mapping → validation all depend on this file
🧪 Acceptance Criteria

Your implementation is complete when:

mapping.json loads without error
invalid config fails fast at startup
all tests pass
all canonical fields are present
all alias mappings are validated
system is ready for parser integration (T2-2)
🚫 Do NOT
Skip validation logic
Assume config correctness
Allow partial loads
Add unnecessary abstraction layers
✅ Success Definition

This ticket is successful when:

A developer can change mapping.json and immediately see failures if the config is invalid—without running any pipeline logic.

Begin.
```

- **Summary of Response:**
    - Produced a strict MVP-aligned prompt for Claude to implement a config-driven mapping system with startup  validation  
    - Enforced deterministic schema rules, alias normalization expectations, and fail-fast behavior  
    - Required full TDD coverage including validation, missing keys, and alias integrity checks  
    - Positioned config layer as foundational dependency for entire ingestion pipeline  

- **Impact:**
    - Established robust contract for data normalization and schema enforcement  
    - Strengthened pipeline reliability by enforcing early failure on invalid config  
    - Ensured extensibility for future Excel formats while maintaining strict MVP discipline
---

### Prompt ID: P-013
- **Author:** Mark
- **Target:** Claude
- **Purpose:** Full system review and QA validation with next-step recommendations
#### Prompt
```
In the role of senior data engineer / qa please review all the files, correct and recommend next steps
```

- **Summary of Response:**
    - Performed holistic review of existing project files across dev container, CI pipeline, and config-driven mapping system
    - Identified alignment with MVP architecture and TDD workflow expectations
    - Flagged potential gaps or inconsistencies in validation, test coverage, or configuration robustness
    - Provided corrections and recommendations to improve reliability, maintainability, and pipeline correctness
- **Impact:**
    - Validated overall system cohesion across multiple epics and tickets
    - Strengthened confidence in MVP readiness and production-minded design
    - Produced actionable next steps to guide continued development and reduce architectural drift
---

### Prompt ID: P-014
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Alignment check between ingestion epics and fixture validation contract
#### Prompt
```
Ok moving into E2- File ingestion: 

T2-1 - FastAPI / upload endpoint 
T2-2 - Multi-sheet parser 

where are we in relation to our fixture_validation.md file:
(file contents)
```

- **Summary of Response:**
    - Mapped ingestion tickets (FastAPI upload endpoint + multi-sheet parser) against existing fixture validation rules
    - Assessed whether current implementation assumptions align with validation contract requirements
    - Identified dependencies between ingestion layer and fixture-based test data expectations
    - Highlighted potential gaps in enforcing validation rules during file parsing and upload flow
- **Impact:**
    - Ensured ingestion design remains consistent with predefined validation standards
    - Strengthened dependency awareness between upload, parsing, and validation layers
    - Helped prevent drift between test fixtures and actual pipeline behavior
---

### Prompt ID: P-015
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for FastAPI upload endpoint with QA constraints
#### Prompt
```
Please take this senior project manager evaluation and pass a prompt to Claude as a senior data engineer to take the contradictions into account by consulting your prompt and advising / generating the necessary code to accomplish the first ticket while keeping our test based MVP front of mind:

T2-1 - FastAPI / upload endpoint:

Description
POST /upload accepts multipart .xlsx. Validates extension and MIME type. Saves to temp dir. Returns 400 on non-xlsx.

Acceptance criteria
Valid .xlsx → 200 + processing starts
.csv upload → 400 with descriptive error
Empty file → 400

Test plan
pytest with httpx test client. Three fixtures: valid xlsx, wrong extension, empty file.
```

- **Summary of Response:**
    - Generated a structured prompt for Claude to implement a FastAPI /upload endpoint under strict TDD constraints
    - Included explicit validation rules for file type, MIME checking, and empty file handling
    - Ensured consistency between acceptance criteria and test plan using pytest + httpx
    - Emphasized MVP scope and prevention of over-engineering while supporting future ingestion pipeline expansion
- **Impact:**
    - Enabled direct implementation path for file ingestion entry point
    - Strengthened alignment between QA expectations and backend implementation
    - Reinforced strict validation behavior as first gate in the data pipeline
---

### Prompt ID: P-016
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Strict MVP FastAPI upload endpoint implementation prompt (decoupled ingestion layer)
#### Prompt
```
# 🧠 Claude Code Prompt — T2-1 FastAPI Upload Endpoint (MVP + Future-Proof)

You are acting as a **Senior Data Engineer** implementing T2-1 for the Donor Bureau Excel ingestion pipeline.

This system is a **test-driven, schema-enforcing data pipeline** that ingests Excel workbooks and ultimately produces a clean, warehouse-ready CSV.

---

# ⚠️ Important Architectural Context (Read First)

We are currently in an **early ingestion stage (E2 - File Ingestion)**.

We have:

* Dev container (Python 3.12 + uv)
* FastAPI backend
* pytest framework
* Mapping config system (T1-3 complete or in progress)
* Input contract defined (authoritative schema rules)

We do NOT yet have:

* Completed fixture validation system (T7-1 not finished)
* Verified real-world edge-case dataset coverage

---

## 🚨 Key Engineering Constraint

The fixture validation system is NOT blocking this ticket.

However:

> We must avoid baking in brittle assumptions about Excel structure at this stage.

So:

* T2-1 should be **pure ingestion + validation of file boundary rules only**
* It must NOT depend on parsing logic or fixture-derived assumptions
* It must remain stable even as T2-2 parser evolves later

---

# 🎯 Ticket Goal

Implement:

```http id="h7k3ld"
POST /upload

This endpoint must:

Accept .xlsx files via multipart upload
Reject invalid files early (before parsing)
Save valid files to a temporary directory
Return structured HTTP responses
📌 MVP Scope (IMPORTANT)

This is NOT a processing endpoint yet.

DO:

Validate file type
Validate file presence
Save file
Return success response placeholder

DO NOT:

Parse Excel sheets
Apply mapping logic
Validate rows
Transform data
Depend on fixture system
📥 Input Rules
Accept:
.xlsx only
non-empty file
valid multipart upload
Reject with HTTP 400:
.csv or any non-xlsx file
empty file upload
missing file field
🧪 Required Tests (TDD FIRST)

Using pytest + httpx, implement:

1. Valid XLSX upload
returns 200
file is saved to temp directory
2. Invalid extension (.csv)
returns 400
error message clearly states invalid file type
3. Empty file upload
returns 400
error message indicates empty file
🧱 Implementation Requirements
FastAPI Endpoint
Use UploadFile + File(...)
Validate extension using filename + MIME type (defensive check both)

Store files in:

/tmp/donor-bureau/uploads/
Ensure unique filenames (timestamp or uuid)
Response Schema (MVP)

On success:

{
  "message": "file uploaded successfully",
  "filename": "<stored_filename>"
}

On error:

{
  "error": "<human readable reason>"
}
⚙️ Engineering Constraints (Critical)
1. Keep it minimal

No overengineering:

No background jobs
No parsing pipeline hooks
No mapping system integration
2. Fixture system awareness (IMPORTANT)

You are NOT allowed to assume:

sheet structure
header position
column formats
data validity

This is intentional — those rules belong to T2-2 and beyond.

3. Separation of concerns

This endpoint is ONLY responsible for:

“Is this a valid Excel file we should accept into the system?”

NOT:

“What is inside the Excel file?”

🧪 Test Strategy (TDD Alignment)

Tests should validate:

HTTP status codes
File rejection behavior
File persistence
No parsing logic is invoked

Use:

httpx.AsyncClient or FastAPI TestClient
temporary directories (tmp_path fixture preferred`
🧠 Why This Ticket Matters (Explain After Implementation)

After coding, explain briefly:

1. Why upload validation is isolated from parsing
prevents coupling ingestion with business logic
avoids brittle assumptions about Excel structure
2. Why this design supports future T2-2 parser
parser can evolve independently
upload layer remains stable
3. Why fixture validation is NOT needed here yet
this layer only validates file boundary conditions
fixtures matter only when interpreting content (T2-2+)
🚫 DO NOT
Do not parse Excel files
Do not reference mapping.json
Do not validate column structure
Do not assume header formats
Do not introduce fixture dependency
Do not overbuild abstractions
✅ Success Criteria

This ticket is complete when:

All 3 tests pass
Invalid files are rejected cleanly
Valid files are stored safely
Endpoint is minimal and future-proof
No coupling to downstream pipeline logic exists

Begin.
```

- **Summary of Response:**
    - Produced a tightly constrained MVP prompt for implementing a FastAPI `/upload` endpoint using strict TDD principles  
    - Enforced clear separation between ingestion (file boundary validation) and downstream parsing logic  
    - Defined explicit test cases for valid, invalid, and empty file uploads using pytest + httpx  
    - Emphasized decoupling from fixture system and mapping logic to prevent premature architectural coupling  
- **Impact:**
    - Established clean architectural boundary for ingestion layer (T2-1)  
    - Prevented early over-engineering and coupling to future parsing/validation systems  
    - Ensured scalable foundation for upcoming T2-2 multi-sheet parsing stage
---

### Prompt ID: P-017
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for QA-focused code review
#### Prompt
```
Now please generate a prompt for Claude directing it do a code review of what it just generated as senior level testers and qa
```

- **Summary of Response:**
    - Generated a structured prompt instructing Claude to perform a QA-focused code review
    - Emphasized validation of TDD adherence, test coverage, and edge case handling
    - Directed focus toward failure modes, error handling, and alignment with acceptance criteria
    - Included expectation for actionable feedback and recommended improvements
- **Impact:**
    - Introduced formal QA review step into development workflow
    - Strengthened code reliability and test completeness before progression
    - Reinforced discipline of validating implementation against original ticket requirements
---

### Prompt ID: P-018
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Comprehensive QA and test review prompt for upload endpoint
#### Prompt
```
# 🧠 Claude Code Prompt — Senior QA / Test Review (T2-1 Upload Endpoint)

You are acting as a **Senior QA Engineer + Senior Data Engineer** reviewing the implementation of:

> **T2-1 — FastAPI /upload endpoint**

Your role is to perform a **deep, critical code review** focused on:

* correctness
* test coverage
* edge cases
* failure handling
* alignment with MVP architecture

---

# 🎯 Review Objectives

You must evaluate BOTH:

1. **Application Code**
2. **Test Suite (pytest + httpx)**

Your goal is to determine:

> “Is this implementation safe, correct, and production-ready for MVP?”

---

# 📌 Context Reminder

This endpoint is intentionally **limited in scope**:

It should ONLY:

* accept `.xlsx` uploads
* validate file presence + type
* reject invalid uploads
* store valid files to temp directory

It must NOT:

* parse Excel contents
* depend on mapping.json
* assume sheet structure
* implement any pipeline logic

---

# ⚠️ Critical Constraints to Validate

## 1. Separation of Concerns

* No parsing logic inside endpoint
* No coupling to future pipeline stages
* Clean boundary between ingestion and processing

---

## 2. Validation Correctness

Check:

### File validation

* Extension check (.xlsx)
* MIME type validation (defensive)
* Case sensitivity handled (e.g. `.XLSX`)

### Empty file handling

* Detects zero-byte file correctly

### Missing file

* Proper FastAPI validation behavior

---

## 3. Error Handling Quality

Evaluate:

* Are error messages clear and actionable?
* Are HTTP status codes correct?
* Are failure modes consistent?

Examples:

* `.csv` upload → 400
* empty file → 400
* missing file → 422 or 400 (justify choice)

---

## 4. File Handling Safety

Check for:

* Unique filename generation (collision prevention)
* Safe file writing (no overwrite risk)
* Directory existence handling
* No path traversal vulnerabilities

---

## 5. Test Coverage Depth

Critically evaluate tests:

### Required Coverage

* valid `.xlsx` upload
* invalid extension (.csv)
* empty file

### Look for Missing Cases

* uppercase extension (`.XLSX`)
* wrong MIME type but correct extension
* correct MIME but wrong extension
* missing file field
* large file (boundary consideration, not required to implement)

---

## 6. Test Quality (not just presence)

Evaluate:

* Are tests deterministic?
* Are assertions meaningful?
* Are failure messages helpful?
* Are temp directories isolated (e.g. `tmp_path`)?
* Are tests independent (no shared state)?

---

## 7. Alignment with MVP Philosophy

Ensure:

* No overengineering
* No unnecessary abstraction
* No premature pipeline integration

---

## 8. Future Compatibility (T2-2 Parser)

Evaluate whether current design:

* Allows parser to plug in cleanly later
* Avoids needing refactor when parsing is introduced
* Keeps endpoint stable as system evolves

---

# 🧪 Output Requirements

Provide your review in this structure:

---

## 1. ✅ What Was Done Well

* Highlight strong design decisions
* Note alignment with MVP + TDD

---

## 2. ⚠️ Issues / Risks Identified

Categorize by severity:

### 🔴 Critical (must fix before merge)

### 🟡 Medium (should fix soon)

### 🟢 Minor (nice to improve)

---

## 3. 🧪 Test Coverage Gaps

* Missing test scenarios
* Weak assertions
* Edge cases not covered

---

## 4. 🔧 Suggested Improvements

* Specific, actionable fixes
* Keep within MVP scope

---

## 5. 🧠 Final Verdict

Choose one:

* ✅ Ready to merge
* ⚠️ Merge with fixes
* ❌ Not ready

Provide reasoning.

---

# 🚫 DO NOT

* Rewrite the entire implementation
* Introduce new architecture
* Suggest non-MVP features
* Over-engineer solutions

---

# ✅ Success Criteria

A strong review will:

* Catch subtle bugs and edge cases
* Strengthen test reliability
* Ensure strict separation of concerns
* Improve production readiness WITHOUT expanding scope

---

Begin review.
```

- **Summary of Response:**
    - Created a detailed QA review prompt directing Claude to evaluate both implementation and tests
    - Structured review criteria around validation, error handling, file safety, and separation of concerns
    - Included explicit edge cases and test gaps to assess robustness
    - Defined clear output format with severity-based issue categorization and final merge verdict
- **Impact:**
    - Formalized high-quality QA review process before merging critical ingestion logic
    - Increased likelihood of catching subtle bugs and edge case failures early
    - Reinforced MVP discipline while ensuring production readiness
---

### Prompt ID: P-019
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for multi-sheet parser implementation (MVP + TDD)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 

T2-2 - Multi-sheet parser: 

Description 
parser.py reads all sheets dynamically using openpyxl, detects the correct header row within each sheet, and normalizes column names. 
Header detection scans the first N rows (configurable, e.g., 10–20) to identify a valid header row based on matching known column aliases from mapping.json. 
Each sheet is parsed into a DataFrame, tagged with a _source_sheet column, and all valid sheets are concatenated into a single DataFrame.

Acceptance Criteria 
All sheets in the workbook are processed dynamically (no hardcoding) 
Header row is correctly detected even if not in row 1 
Header detection: 
- Scan first N rows 
- Select first row with ≥ 2 mapped columns 
- Stop immediately (no ranking/scoring) 
Column names are normalized: 
lowercase 
trimmed whitespace 
_source_sheet column is present for all rows 
Empty sheets (no data after header) are skipped without error 
Sheets with no detectable valid header: 
Are excluded from processing 
Generate a logged warning (not a silent skip) 
Final output is a single concatenated DataFrame from all valid sheets 
Pre-header metadata rows (e.g. client label, review notes) are correctly skipped and do not interfere with header detection 

Assumptions 
Header row may appear within the first N rows (not guaranteed to be row 1) 
Each sheet represents a distinct client dataset 
Sheet names are not hardcoded and are used later for Client field injection 
Column aliases defined in mapping.json are sufficient to identify headers Workbook size is small enough (<10MB) for in-memory processing 

Test Plan 
Unit Tests 
1-sheet workbook with header in row 1 
1-sheet workbook with header offset (e.g., row 3 or 5) 
3-sheet workbook with: different schemas per sheet different header row positions 
Sheet with extra whitespace in headers (e.g., " First Name ") 

Edge Cases 
Sheet with no data → skipped 
Sheet with no detectable header → excluded + warning logged 
Sheet with partial column matches: 
Below threshold → rejected 
Above threshold → accepted 

Integration Test 
Multi-sheet workbook containing multiple template formats: 
All valid sheets correctly parsed and concatenated 
_source_sheet correctly reflects origin of each row
```

- **Summary of Response:**
    - Generated a detailed Claude prompt for implementing a dynamic multi-sheet Excel parser using openpyxl
    - Enforced strict header detection logic based on alias matching from mapping.json
    - Incorporated TDD requirements with unit and integration tests covering varied sheet structures and edge cases
    - Emphasized MVP simplicity, deterministic behavior, and clear logging for skipped or invalid sheets
- **Impact:**
    - Defined core ingestion logic enabling transformation of multi-sheet Excel files into unified datasets
    - Ensured robustness against inconsistent real-world file formats through configurable header detection
    - Maintained alignment with MVP scope while preparing system for downstream normalization and validation
---

### Prompt ID: P-020
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Multi-sheet parser implementation prompt with strict MVP and TDD constraints
#### Prompt
```
# 🧠 Claude Code Prompt — T2-2 Multi-Sheet Parser (MVP + TDD + Future-Safe)

You are acting as a **Lead Data Engineer** implementing:

> **T2-2 — Multi-sheet parser**

for the Donor Bureau Excel → CSV ingestion pipeline.

---

# 🎯 Project Context (Critical)

This is a **data pipeline system**, not a typical web app.

Key properties:

* Input data is **inconsistent and semi-structured**
* Column names vary across clients
* Header rows may not be in row 1
* Workbooks may contain multiple sheets (multiple clients)

---

## ⚠️ Current System State

We have:

* Upload endpoint complete (T2-1)
* mapping.json config system (T1-3)
* Input contract defined (source of truth)
* pytest + TDD framework in place

We do NOT yet have:

* Fully validated fixture library (T7-1 incomplete)
* Completed fixture validation log

---

## 🚨 Critical Engineering Constraint

You MUST account for this:

> We are implementing the parser BEFORE full fixture validation is complete.

Therefore:

* Build **correct, minimal, contract-aligned logic**
* Avoid overfitting to hypothetical edge cases
* Avoid hardcoding assumptions not defined in `input_contract.md`
* Keep implementation **flexible and test-driven**

---

# 🎯 Ticket Goal

Implement:

```id="parserfile"
app/parser.py

This module must:

Read all sheets dynamically using openpyxl
Detect header row per sheet using mapping.json
Normalize column names
Convert each valid sheet into a pandas DataFrame
Add _source_sheet column
Concatenate all valid sheets into one DataFrame
⚙️ Functional Requirements
1. Sheet Processing
Iterate through ALL sheets dynamically
No sheet names are hardcoded
Each sheet processed independently
2. Header Detection Logic (CORE)

For each sheet:

Scan first N rows (from mapping.json.header_scan_rows)
Normalize each row’s cell values:
lowercase
strip whitespace
For each row:
count how many values match known aliases (from mapping.json)

Header row is:

FIRST row with ≥ 2 alias matches

Stop immediately when found
No ranking or scoring
3. Metadata Handling
All rows before detected header are ignored
These are treated as metadata (e.g., “Prepared for internal review”)
Must NOT interfere with detection logic
4. Column Normalization

After header detection:

Normalize column names:
lowercase
strip whitespace

Example:

" First Name " → "first name"
5. DataFrame Construction
Data starts immediately AFTER header row
Convert rows into pandas DataFrame
Add:
_source_sheet = <sheet_name>
Sheet name should be preserved as-is (normalization handled later)
6. Sheet Inclusion Rules
Include sheet if:
Header detected
At least 1 data row exists
Skip sheet if:
No header detected → log warning
Header exists but no data rows → silently skip
7. Final Output
Concatenate all valid DataFrames
Return a single DataFrame
🧪 TDD REQUIREMENTS (MANDATORY)

You MUST write tests BEFORE implementation.

Required Unit Tests
1. Single sheet, header in row 1
Parsed correctly
Columns normalized
_source_sheet added
2. Header offset (row 3 or 5)
Header correctly detected
Metadata rows ignored
3. Multi-sheet workbook
Different schemas per sheet
Different header positions
All valid sheets included
4. Header whitespace normalization
" First Name " → normalized correctly
Edge Case Tests
5. Sheet with no data
Skipped without error
6. Sheet with no detectable header
Excluded
Warning logged
7. Partial column match
< 2 matches → rejected
≥ 2 matches → accepted
Integration Test
Multi-sheet workbook with mixed templates
Output is single DataFrame
_source_sheet correctly assigned
⚙️ Implementation Constraints (MVP Discipline)

DO:

Use openpyxl
Use pandas
Use mapping.json as single source of truth for aliases
Keep logic simple and deterministic

DO NOT:

Implement column mapping (T3-1 responsibility)
Inject Client field (T3-3 responsibility)
Perform validation (T4 responsibility)
Handle async processing
Over-engineer abstraction layers
🧠 Logging Requirements
Log warning when:
Sheet has no detectable header

Example:

WARNING: No valid header found in sheet 'Sheet2'
🧠 Design Principles (CRITICAL)
1. Parser is NOT validator
Do not reject rows
Do not enforce schema completeness
2. Parser is NOT transformer
Do not map to canonical field names
Do not normalize values beyond column names
3. Parser must be composable
Output should cleanly feed into T3-1 mapping stage
🧠 Why This Matters (Explain After Implementation)

Explain briefly:

1. Why header detection is the hardest part of Excel ingestion
variability across templates
lack of structure
2. Why we avoid overfitting before fixture validation
prevents brittle logic
allows system to evolve safely
3. How this parser enables downstream pipeline stages
mapping
normalization
validation
🚫 DO NOT
Hardcode sheet names
Assume header is row 1
Assume consistent schemas
Couple parser to mapping/validation stages
Add unnecessary abstractions
✅ Success Criteria

This ticket is complete when:

All tests pass
Header detection works for offset rows
Multi-sheet parsing works
Invalid sheets are safely excluded
Output is a single DataFrame
Implementation remains simple and adaptable

Begin.
```

- **Summary of Response:**
    - Produced a comprehensive Claude prompt for implementing a multi-sheet Excel parser with strict TDD requirements  
    - Defined deterministic header detection logic driven by mapping.json aliases  
    - Enforced clear separation between parsing, mapping, and validation responsibilities  
    - Included extensive unit and integration test scenarios covering real-world inconsistencies  

- **Impact:**
    - Established core parsing engine for handling messy, multi-sheet Excel inputs  
    - Ensured flexibility and resilience prior to full fixture validation completion  
    - Maintained strong alignment with MVP scope while enabling downstream pipeline stages
--- 

### Prompt ID: P-021
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA review prompt for multi-sheet parser reliability and test coverage
#### Prompt
```
# 🧠 Claude Code Prompt — Senior QA / Test Review (T2-2 Multi-Sheet Parser)

You are acting as a **Senior QA Engineer + Lead Data Engineer** performing a deep code review of:

> **T2-2 — Multi-sheet parser (parser.py)**

Your responsibility is to evaluate both:

* Implementation correctness
* Test quality and coverage

---

# 🎯 Review Objective

Determine:

> “Is this parser reliable, testable, and safe to build upon for downstream pipeline stages?”

This is a **high-risk component** of a data pipeline — subtle bugs here will silently corrupt downstream data.

---

# 📌 Context Reminder

This parser must:

* Dynamically read all sheets
* Detect header rows within first N rows
* Ignore metadata rows before header
* Normalize column names
* Add `_source_sheet`
* Concatenate valid sheets

It must NOT:

* Perform column mapping (T3-1)
* Perform validation (T4)
* Assume perfect data
* Overfit to unvalidated fixture assumptions

---

# ⚠️ Critical Areas to Evaluate

## 1. Header Detection Logic (HIGHEST RISK)

Evaluate:

* Does it correctly scan ONLY first N rows?
* Does it stop at FIRST valid match (≥ 2 aliases)?
* Does it avoid ranking/scoring complexity?
* Are aliases matched case-insensitively?

Check for bugs like:

* false positives from metadata rows
* incorrect threshold logic
* scanning entire sheet instead of N rows

---

## 2. Mapping.json Usage

* Is `header_scan_rows` respected?
* Are aliases loaded correctly?
* Is alias matching normalized (lowercase + trimmed)?

---

## 3. Metadata Handling

* Are rows before header truly ignored?
* Could metadata accidentally be interpreted as header?

Example risk:


"Client: Alpha Fund"


Should NOT trigger header detection

---

## 4. Column Normalization

Verify:

* lowercase applied
* whitespace trimmed
* consistent across all sheets

---

## 5. DataFrame Construction

Check:

* Data starts AFTER header row
* `_source_sheet` is correctly added
* Sheet name preserved accurately

---

## 6. Sheet Inclusion / Exclusion Rules

### Correct behavior:

* No header → skip + log warning
* Header but no data → skip silently
* Valid sheet → included

Check:

* Are warnings logged properly?
* Are sheets incorrectly included/excluded?

---

## 7. Concatenation Logic

* Are multiple sheets combined correctly?
* Are column mismatches handled (pandas default behavior acceptable for MVP)?
* Is output deterministic?

---

## 8. Separation of Concerns

Ensure:

* No mapping logic present
* No validation logic present
* No Client field injection
* Parser remains composable for T3/T4

---

# 🧪 Test Suite Review

## 1. Required Coverage

Ensure tests exist for:

* header in row 1
* header offset (row 3–5)
* multi-sheet parsing
* whitespace in headers
* no header → skipped
* no data → skipped
* partial match threshold logic

---

## 2. Edge Case Strength

Look for missing tests:

* metadata rows mimicking headers
* mixed valid + invalid sheets
* sheets with only 1 matching alias
* sheets with duplicate column names
* empty workbook (if handled)

---

## 3. Test Quality

Evaluate:

* Are tests deterministic?
* Are fixtures realistic?
* Are assertions strong (not just shape checks)?
* Is `_source_sheet` explicitly validated?

---

## 4. Fixture Strategy

Even though T7-1 is not complete:

* Are tests simulating realistic Excel structures?
* Are they aligned with input_contract.md?

---

# ⚠️ Common Failure Patterns to Detect

Actively look for:

* Overfitting to assumed structure
* Hardcoded column names
* Header detection too permissive or too strict
* Silent failures (no logging)
* Parser doing transformation work prematurely

---

# 🧪 Output Requirements

Provide your review in this structure:

---

## 1. ✅ What Was Done Well

* Strong design choices
* Alignment with MVP + TDD
* Clean separation of concerns

---

## 2. 🔴 Critical Issues (Must Fix)

* Bugs or logic flaws
* Violations of acceptance criteria
* Anything that risks incorrect parsing

---

## 3. 🟡 Medium Issues (Should Fix Soon)

* Edge case gaps
* Test weaknesses
* Minor logic concerns

---

## 4. 🟢 Minor Improvements

* Code clarity
* Logging improvements
* Small refactors within MVP scope

---

## 5. 🧪 Test Coverage Gaps

* Missing scenarios
* Weak assertions
* Missing edge-case validation

---

## 6. 🔧 Suggested Fixes

* Specific, actionable improvements
* Keep strictly within MVP scope

---

## 7. 🧠 Final Verdict

Choose one:

* ✅ Ready to merge
* ⚠️ Merge with fixes
* ❌ Not ready

Provide reasoning.

---

# 🚫 DO NOT

* Rewrite the entire parser
* Add new architecture
* Introduce T3/T4 logic
* Suggest non-MVP enhancements

---

# ✅ Success Criteria

A strong review will:

* Catch subtle header detection bugs
* Strengthen test reliability
* Prevent future pipeline breakage
* Ensure safe progression to T3 (mapping stage)

---

Begin review.
```

- **Summary of Response:**
    - Created a comprehensive QA prompt targeting high-risk parser logic and test coverage
    - Focused heavily on header detection correctness, metadata handling, and sheet inclusion rules
    - Included detailed evaluation criteria for both implementation and pytest suite quality
    - Structured output to prioritize critical issues, test gaps, and merge readiness
- **Impact:**
    - Introduced rigorous QA validation for the most complex part of the ingestion pipeline
    - Reduced risk of silent data corruption from parsing errors
    - Strengthened readiness for transition into mapping and validation stages
---

### Prompt ID: P-022
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for column mapping engine (T3-1)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T3-1 - Column mapping engine

# Description
transformer.py maps source columns to canonical schema using mapping.json.
Mapping is case-insensitive and alias-driven.
Missing columns are allowed at this stage and deferred to validation.

# Acceptance Criteria
- Known aliases map correctly to canonical names
- Unmapped columns are dropped
- Missing canonical columns do NOT raise error here
- Mapping is deterministic and case-insensitive

# Assumptions
Presence of required fields is NOT guaranteed at mapping stage and must be enforced downstream.

# Test plan
Unit tests covering:
- exact match
- alias match
- unknown column
- missing required
- case-insensitive match
```

- ***Summary of Response:**
    - Generated a Claude implementation prompt for a column mapping engine based on alias-driven schema normalization
    - Defined deterministic mapping rules using mapping.json as the source of truth
    - Clarified separation of concerns by deferring validation of required fields to downstream stages
    - Included explicit unit test coverage requirements for mapping behavior and edge cases
- **Impact:**
    - Established clean transformation layer between parsing (T2-2) and validation (T4)
    - Ensured consistent, deterministic column normalization across heterogeneous Excel inputs
    - Reinforced MVP discipline by separating mapping logic from validation responsibilities
---

### Prompt ID: P-023
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** T3-1 column mapping engine implementation prompt with strict MVP + TDD separation from validation
#### Prompt
```
# 🧠 Claude Code Prompt — T3-1 Column Mapping Engine (MVP + TDD + Pipeline Discipline)

You are acting as a **Lead Data Engineer** implementing:

> **T3-1 — Column Mapping Engine**

for the Donor Bureau Excel → CSV ingestion pipeline.

---

# 🎯 Project Context (Critical)

This system is a **data pipeline**, not a typical application.

Pipeline flow:


parse → map → normalize → validate → split → output


You are implementing the **mapping stage**.

---

## ⚠️ Upstream + Downstream Awareness

### Input (from T2-2 parser):

* pandas DataFrame
* column names are:

  * lowercase
  * whitespace-trimmed
* may vary across sheets
* includes `_source_sheet`

### Output (to T3-2 normalization):

* DataFrame with **canonical column names**
* unmapped columns removed
* missing required fields STILL allowed

---

## 🚨 Critical Engineering Constraint

This stage is **NOT responsible for validation**.

That means:

* Missing required columns → ALLOWED
* Invalid values → ALLOWED
* Empty fields → ALLOWED

👉 All enforcement happens in **T4 (validators)**

---

# 🎯 Ticket Goal

Implement:

``` id="transformerfile"
app/transformer.py

This module must:

Map source column names → canonical schema
Use mapping.json as source of truth
Drop unmapped columns
Preserve only mapped canonical fields (+ _source_sheet)
⚙️ Functional Requirements
1. Mapping Behavior
Mapping is alias-driven
Case-insensitive matching
Deterministic (same input → same output)

Example:

Source Column	Canonical Output
first_name	First
fname	First
first	First
2. Column Matching Rules
Input columns already normalized (lowercase, trimmed)
Aliases from mapping.json should also be normalized before comparison
3. Output Schema Behavior
Only include:
canonical fields that are present in input
_source_sheet (must be preserved)
Drop:
all unmapped columns
4. Missing Fields (IMPORTANT)

If a canonical field is NOT present:

DO NOT raise error
DO NOT create empty column
Simply omit it

👉 Validation happens later (T4)

5. Duplicate Mapping Handling

If multiple source columns map to the same canonical field:

Example:

first_name + fname both exist

MVP behavior:

Prefer first occurrence (left-to-right)
Do NOT merge values
Do NOT raise error
🧪 TDD REQUIREMENTS (MANDATORY)

You MUST write tests FIRST.

Required Unit Tests
1. Exact match
"first" → "First"
2. Alias match
"fname" → "First"
3. Case-insensitive match
"FNAME" → "First"
4. Unknown column
"random_col" → dropped
5. Missing required field
e.g. no "Last"
should NOT error
simply not present in output
6. Multiple aliases mapping to same field
ensure deterministic selection
7. _source_sheet preservation
must remain untouched
⚙️ Implementation Constraints (MVP Discipline)

DO:

Load mapping.json via existing loader
Build reverse lookup: alias → canonical field
Keep logic simple and deterministic

DO NOT:

Validate data completeness
Add missing columns
Normalize values (T3-2 responsibility)
Inject Client field (T3-3 responsibility)
Over-engineer abstraction layers
🧠 Design Principles (CRITICAL)
1. Mapping is structural, not semantic
It aligns column names, nothing else
2. Mapping must be deterministic
Same input → same output
No randomness or ordering ambiguity
3. Mapping must be loss-aware
Unmapped columns are intentionally dropped
This is expected behavior
🧠 Why This Matters (Explain After Implementation)

Explain briefly:

1. Why mapping is isolated from validation
prevents premature failure
keeps pipeline composable
2. Why alias-driven design is critical
real-world Excel data is inconsistent
enables extensibility without code changes
3. How this stage protects downstream logic
ensures consistent schema before normalization/validation
🚫 DO NOT
Raise errors for missing fields
Assume all canonical fields exist
Modify data values
Combine columns
Add business logic
Reference validation rules
✅ Success Criteria

This ticket is complete when:

All tests pass
Known aliases correctly map
Unmapped columns are dropped
Missing fields are tolerated
Output is deterministic
_source_sheet is preserved

Begin.
```

- **Summary of Response:**
    - Generated a structured Claude prompt for implementing a deterministic column mapping engine (T3-1)  
    - Reinforced strict separation between mapping and validation stages in the pipeline  
    - Defined alias-driven schema normalization with case-insensitive matching rules  
    - Included comprehensive TDD requirements covering mapping correctness and edge cases  

- **Impact:**
    - Established a clean transformation layer between parsing (T2-2) and validation (T4)  
    - Ensured predictable schema normalization for downstream pipeline consistency  
    - Strengthened MVP discipline by preventing premature validation or business logic leakage
---

### Prompt ID: P-024
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA review prompt for column mapping engine correctness and determinism
#### Prompt
```
# 🧠 Claude Code Prompt — Senior QA / Test Review (T3-1 Column Mapping Engine)

You are acting as a **Senior QA Engineer + Lead Data Engineer** performing a deep review of:

> **T3-1 — Column Mapping Engine (transformer.py)**

Your responsibility is to evaluate:

* correctness of mapping logic
* test coverage quality
* determinism and reliability
* alignment with pipeline architecture

---

# 🎯 Review Objective

Determine:

> “Is this mapping engine safe, deterministic, and reliable for real-world messy Excel data?”

This stage is **high-risk for silent data corruption**.

---

# 📌 Context Reminder

### Input (from parser):

* pandas DataFrame
* column names already:

  * lowercase
  * trimmed
* includes `_source_sheet`

### Output (to normalization stage):

* canonical column names (e.g., First, Last, Address1, etc.)
* unmapped columns dropped
* `_source_sheet` preserved

---

# ⚠️ Critical Constraints

This stage must:

* ✅ Map aliases → canonical names
* ✅ Be case-insensitive
* ✅ Be deterministic

This stage must NOT:

* ❌ Validate missing fields
* ❌ Enforce schema completeness
* ❌ Modify data values
* ❌ Inject Client field
* ❌ Perform normalization

---

# ⚠️ Critical Areas to Evaluate

## 1. Alias Mapping Logic (HIGHEST RISK)

Evaluate:

* Is alias matching truly case-insensitive?
* Are aliases normalized before comparison?
* Is mapping.json used correctly as source of truth?

Check for bugs like:

* partial matches instead of exact matches
* whitespace issues
* incorrect alias resolution

---

## 2. Reverse Mapping Construction

Typical pattern:

```id="revmap"
alias → canonical_field

Check:

Is reverse mapping built correctly?
Are duplicate aliases handled safely?
Are conflicts possible?
3. Determinism

Ensure:

Same input always produces same output
No dependency on dictionary ordering (unless controlled)
Column selection is predictable
4. Duplicate Column Handling

Scenario:

first_name + fname both exist

Check:

Which column is chosen?
Is behavior consistent?
Is it documented or implicit?

MVP expectation:

first occurrence wins (left-to-right)
5. Unmapped Columns

Verify:

All unmapped columns are dropped
No leakage into output
6. Missing Canonical Fields

Ensure:

No error raised
No empty columns created
Fields simply absent
7. _source_sheet Preservation

Check:

Column is retained exactly
Not renamed, not dropped
8. Separation of Concerns

Ensure:

No normalization logic present
No validation logic present
No business rules
🧪 Test Suite Review
1. Required Coverage

Ensure tests exist for:

exact match
alias match
case-insensitive match
unknown column dropped
missing required field
duplicate alias scenario
_source_sheet preservation
2. Edge Case Coverage

Look for missing tests:

multiple aliases mapping to same canonical field
alias collisions (if possible)
empty DataFrame
DataFrame with only unmapped columns
mixed mapped + unmapped columns
3. Test Quality

Evaluate:

Are assertions strong (checking column names, not just shape)?
Are tests deterministic?
Are edge cases explicitly verified?
Is behavior clearly validated (not implied)?
4. Fixture Realism

Even without full T7-1:

Are test DataFrames realistic?
Do they reflect actual messy Excel scenarios?
⚠️ Common Failure Patterns

Actively look for:

mapping based on substring instead of exact alias
case sensitivity bugs
inconsistent handling of duplicates
silent dropping of important columns due to bad mapping
accidental transformation of values
🧪 Output Requirements

Provide your review in this structure:

1. ✅ What Was Done Well
Strong design choices
Correct pipeline alignment
Clean mapping logic
2. 🔴 Critical Issues (Must Fix)
Incorrect mapping behavior
Violations of acceptance criteria
Anything that risks data corruption
3. 🟡 Medium Issues (Should Fix Soon)
Edge case gaps
Determinism concerns
Test weaknesses
4. 🟢 Minor Improvements
Code clarity
Small refactors
Logging suggestions (within MVP scope)
5. 🧪 Test Coverage Gaps
Missing edge cases
Weak assertions
Scenarios not tested
6. 🔧 Suggested Fixes
Specific, actionable improvements
Keep strictly within MVP scope
7. 🧠 Final Verdict

Choose one:

✅ Ready to merge
⚠️ Merge with fixes
❌ Not ready

Provide reasoning.

🚫 DO NOT
Rewrite the entire module
Add validation or normalization logic
Introduce new architecture
Expand scope beyond MVP
✅ Success Criteria

A strong review will:

Catch silent mapping bugs
Ensure deterministic behavior
Strengthen test reliability
Protect downstream pipeline stages

Begin review.
```

- **Summary of Response:**
    - Produced a detailed QA review prompt targeting correctness and determinism of the column mapping engine  
    - Emphasized risks of silent data corruption from improper alias resolution and duplicate handling  
    - Defined rigorous test coverage expectations including edge cases and realistic data scenarios  
    - Reinforced strict separation from validation and normalization stages  

- **Impact:**
    - Strengthened reliability of schema transformation layer before validation stage  
    - Reduced risk of incorrect column mappings propagating downstream  
    - Ensured mapping logic is deterministic, testable, and aligned with MVP pipeline architecture
---

### Prompt ID: P-025
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Claude prompt generation for data normalization stage (T3-2)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T3-2 - Data normalization:

# Description
Strip whitespace from all string fields. Title-case First, Last, City. Upper-case State. Cast DonationAmount to float. Parse DonationDate to ISO 8601. Preserve ZIP as string.

# Acceptance criteria
- " john " → "John"
- "new york" → "New York"
- "ny" → "NY"
- Excel date serial correctly parsed
- ZIP "01234" stays "01234" not 1234

# Test plan
Parametrized unit tests for each normalization rule. Dedicated test for ZIP edge case.
```

- **Summary of Response:**
    - Generated a Claude prompt for implementing a data normalization module with strict field-level transformations
    - Defined explicit normalization rules for names, locations, state codes, dates, and numeric casting
    - Emphasized preservation of ZIP codes as strings to prevent data loss
    - Included TDD requirements with parametrized tests for each normalization behavior
- **Impact:**
    - Established a clean normalization layer between mapping (T3-1) and validation (T4)
    - Ensured consistent formatting of critical fields for downstream validation and warehouse ingestion
    - Reduced risk of data integrity issues, especially with date parsing and ZIP code handling
---

### Prompt ID: P-026
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** T3-2 data normalization implementation prompt with strict MVP and TDD constraints
#### Prompt
```
# 🧠 Claude Code Prompt — T3-2 Data Normalization (MVP + TDD + Pipeline Discipline)

You are acting as a **Lead Data Engineer** implementing:

> **T3-2 — Data Normalization**

for the Donor Bureau Excel → CSV ingestion pipeline.

---

# 🎯 Project Context (Critical)

Pipeline flow:

```id="pipeflow"
parse → map → normalize → validate → split → output

You are implementing the normalization stage.

⚠️ Upstream + Downstream Awareness
Input (from T3-1 mapping engine):
pandas DataFrame
columns are canonical:
First, Last, Address1, City, State, Zip, DonationDate, DonationAmount
Some fields MAY be missing
Values may be:
messy
inconsistent
improperly formatted
Output (to T4 validation):
Same DataFrame
values standardized into consistent formats
STILL allowed to be invalid (validation happens next)
🚨 Critical Engineering Constraint

This stage is NOT responsible for validation.

That means:

Invalid values → allowed to pass through
Missing fields → allowed
Do NOT reject rows
Do NOT enforce completeness

👉 Validation happens in T4

🎯 Ticket Goal

Implement:

app/normalizer.py

This module must:

standardize values across all relevant fields
operate only on existing columns
NOT introduce or remove columns
⚙️ Functional Requirements
1. Global String Cleanup

For ALL string fields:

strip leading/trailing whitespace

Example:

" john " → "john"
2. Name + City Formatting

Apply title case:

First → Title Case
Last → Title Case
City → Title Case

Examples:

"john" → "John"
"new york" → "New York"
3. State Formatting
Convert to uppercase

Example:

"ny" → "NY"
4. DonationAmount
Cast to float

Examples:

"100" → 100.0
100 → 100.0

Do NOT:

validate > 0
reject invalid values
5. DonationDate
Parse into ISO 8601 format (YYYY-MM-DD)

Must support:

Excel date serials
standard string formats:
"MM/DD/YYYY"
"YYYY-MM-DD"
"March 16, 2025"

Output format:

2025-03-16
6. ZIP Code Handling (CRITICAL EDGE CASE)
Must remain a string
Must preserve leading zeros

Example:

"01234" → "01234"

Do NOT:

cast to int
drop leading zeros
7. Missing Columns
If a column is missing:
skip it silently
do NOT error
🧪 TDD REQUIREMENTS (MANDATORY)

You MUST write tests FIRST.

Required Unit Tests
1. Whitespace stripping
" john " → "john"
2. Title case normalization
"john" → "John"
"new york" → "New York"
3. State uppercase
"ny" → "NY"
4. DonationAmount casting
"100" → 100.0
5. DonationDate parsing

Test multiple formats:

Excel serial
MM/DD/YYYY
ISO
natural language (e.g. "March 16, 2025")
6. ZIP preservation (CRITICAL TEST)
"01234" → "01234"

Ensure:

remains string
leading zero preserved
7. Missing column handling
Input missing "City"
normalization should NOT fail
⚙️ Implementation Constraints (MVP Discipline)

DO:

Use pandas vectorized operations where possible
Use safe parsing methods for dates (e.g. pandas.to_datetime)

DO NOT:

Drop rows
Raise validation errors
Enforce required fields
Inject new columns
Over-engineer abstraction layers
🧠 Design Principles (CRITICAL)
1. Normalize, don’t validate
Clean data format
Do NOT judge correctness
2. Be tolerant of messy input
Real-world Excel data is inconsistent
System must not break on imperfect values
3. Preserve data integrity
Especially ZIP codes
Avoid destructive transformations
🧠 Why This Matters (Explain After Implementation)

Explain briefly:

1. Why normalization is separate from validation
keeps pipeline flexible
avoids premature rejection
2. Why date parsing is high-risk
many formats
Excel serial quirks
3. Why ZIP handling is critical
leading zeros frequently lost in pipelines
subtle but serious data integrity issue
🚫 DO NOT
Validate data (no rejection logic)
Assume all columns exist
Cast ZIP to numeric
Enforce business rules
Add unnecessary abstraction
✅ Success Criteria

This ticket is complete when:

All tests pass
Strings are trimmed and formatted correctly
Dates are standardized to ISO format
Amounts are floats
ZIP codes preserve leading zeros
Missing columns do not break execution

Begin.
```

- **Summary of Response:**
    - Generated a detailed Claude prompt for implementing the data normalization stage with strict field-level transformations  
    - Enforced separation from validation, ensuring normalization only standardizes formats without rejecting data  
    - Defined handling for complex cases like date parsing and ZIP code preservation  
    - Included comprehensive TDD requirements with parametrized tests for each normalization rule  

- **Impact:**
    - Established a critical formatting layer ensuring consistent data structure before validation  
    - Reduced risk of downstream errors caused by inconsistent date, string, and numeric formats  
    - Preserved data integrity (especially ZIP codes), preventing subtle but high-impact data issues
---

### Prompt ID: P-027
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA review prompt for data normalization correctness and data integrity
#### Prompt
```
# 🧠 Claude Code Prompt — Senior QA / Test Review (T3-2 Data Normalization)

You are acting as a **Senior QA Engineer + Lead Data Engineer** performing a deep review of:

> **T3-2 — Data Normalization (normalizer.py)**

Your responsibility is to evaluate:

* correctness of normalization logic
* test coverage depth and quality
* data safety (no unintended corruption)
* strict adherence to pipeline responsibilities

---

# 🎯 Review Objective

Determine:

> “Does this normalization layer safely standardize messy input data without corrupting or over-processing it?”

This stage is **high risk for subtle data corruption**, especially:

* date parsing
* numeric casting
* ZIP code handling

---

# 📌 Context Reminder

### Input:

* pandas DataFrame
* canonical column names (from mapping stage)
* values may be inconsistent, messy, or malformed
* some columns may be missing

### Output:

* same DataFrame structure
* values normalized into consistent formats
* invalid values still allowed (validation happens in T4)

---

# ⚠️ Critical Constraints

This stage must:

* ✅ Normalize values (formatting only)
* ✅ Be tolerant of messy inputs
* ✅ Preserve data integrity

This stage must NOT:

* ❌ Reject rows
* ❌ Validate correctness (e.g., amount > 0)
* ❌ Add or remove columns
* ❌ Inject business logic

---

# ⚠️ Critical Areas to Evaluate

## 1. Global Whitespace Handling

Check:

* Are all string fields trimmed?
* Are non-string fields safely ignored?

Watch for:

* calling `.strip()` on non-strings (crashes)
* inconsistent application across columns

---

## 2. Title Case Normalization

Fields:

* First
* Last
* City

Evaluate:

* Correct application of `.title()`
* Handles edge cases like:

  * "mcDonald" → (acceptable MVP behavior?)
  * "o'connor"

Focus:

* consistency, not perfection

---

## 3. State Normalization

Check:

* `.upper()` applied correctly
* whitespace removed first

Example:

``` id="q1zvlt"
" ny " → "NY"
4. DonationAmount Casting (HIGH RISK)

Evaluate:

Correct conversion to float
Handles:
strings ("100")
numeric values (100)
empty or malformed values (should NOT crash)

Watch for:

exceptions not handled
unintended coercion to NaN without awareness
5. DonationDate Parsing (HIGHEST RISK)

Evaluate:

Uses robust parsing (e.g., pandas.to_datetime)
Supports:
Excel serial dates
multiple string formats
Outputs ISO format: YYYY-MM-DD

Check for:

timezone issues
incorrect parsing (e.g., day/month swap)
silent failures producing NaT
6. ZIP Code Handling (CRITICAL EDGE CASE)

Verify:

Always remains a string
Leading zeros preserved

Watch for:

accidental casting to int
pandas auto-conversion stripping zeros

Example failure:

"01234" → "1234" ❌
7. Missing Columns Handling

Check:

Code safely skips missing columns
No KeyErrors
No assumptions about column presence
8. Separation of Concerns

Ensure:

No validation logic present
No row rejection
No schema enforcement
No column creation/removal
🧪 Test Suite Review
1. Required Coverage

Ensure tests exist for:

whitespace stripping
title casing
state uppercase
DonationAmount casting
DonationDate parsing (multiple formats)
ZIP preservation
missing column handling
2. Edge Case Coverage

Look for missing tests:

null values in string fields
mixed data types in same column
invalid date formats
invalid numeric values
empty strings vs NaN
ZIP already numeric (should still output string?)
3. Test Quality

Evaluate:

Are assertions strong (value-level, not just type)?
Are tests deterministic?
Are multiple date formats explicitly tested?
Is ZIP behavior explicitly validated?
4. Silent Failure Detection

Look for:

transformations that fail silently (NaT, NaN)
lack of assertions catching these failures
⚠️ Common Failure Patterns

Actively look for:

ZIP codes losing leading zeros
date parsing inconsistencies
.strip() applied to non-string types
numeric casting crashing on bad input
normalization accidentally performing validation
🧪 Output Requirements

Provide your review in this structure:

1. ✅ What Was Done Well
Strong normalization logic
Correct pipeline alignment
Good handling of messy data
2. 🔴 Critical Issues (Must Fix)
Data corruption risks
Violations of acceptance criteria
Crashes or unsafe transformations
3. 🟡 Medium Issues (Should Fix Soon)
Edge case gaps
Weak handling of mixed types
Test coverage gaps
4. 🟢 Minor Improvements
Code clarity
Minor optimizations
Readability improvements
5. 🧪 Test Coverage Gaps
Missing scenarios
Weak assertions
Unchecked edge cases
6. 🔧 Suggested Fixes
Specific, actionable improvements
Stay within MVP scope
7. 🧠 Final Verdict

Choose one:

✅ Ready to merge
⚠️ Merge with fixes
❌ Not ready

Provide reasoning.

🚫 DO NOT
Rewrite the entire module
Introduce validation logic
Add new features
Expand beyond MVP scope
✅ Success Criteria

A strong review will:

Protect against subtle data corruption
Ensure consistent normalization behavior
Strengthen test reliability
Prepare clean handoff to validation stage (T4)

Begin review.
```

- **Summary of Response:**
    - Generated a detailed QA review prompt focused on safeguarding data integrity in normalization logic  
    - Highlighted high-risk areas such as date parsing, numeric casting, and ZIP code preservation  
    - Defined comprehensive test coverage expectations including edge cases and silent failure detection  
    - Reinforced strict separation between normalization and validation responsibilities  

- **Impact:**
    - Strengthened reliability of the normalization layer before validation  
    - Reduced risk of subtle, hard-to-detect data corruption in downstream pipeline stages  
    - Ensured normalization logic is robust, test-driven, and aligned with MVP architecture
---

### Prompt ID: P-028
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude prompt for Client field injection stage (T3-3)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 

T3-3 - Client field injection: 

# Description 
Add a Client column derived from the sheet name for each row. 
Since a single workbook may contain multiple clients (one per sheet), the Client value must be assigned based on the originating sheet of each record. 

# Acceptance Criteria 
- Every row includes a non-null Client value 
- Client value matches the _source_sheet field from the parser 
- Works correctly for multi-sheet workbooks with different client names 
- Sheet names are normalized (e.g., trimmed whitespace) before assignment 
- No row has an empty or whitespace-only Client value 

# Assumptions 
- Each sheet represents a distinct client dataset 
- Sheet names are sufficiently descriptive to act as a client identifier 
- _source_sheet column is reliably populated during parsing 

# Test Plan 
- Unit test: single-sheet workbook → all rows have same Client value 
- Unit test: multi-sheet workbook → rows correctly reflect their respective sheet names 
- Unit test: sheet name with leading/trailing whitespace → correctly normalized 

- Integration test: 
        - mixed multi-sheet file → verify correct client assignment across all rows
```

- **Summary of Response:**
    - Generated a structured Claude prompt defining T3-3 within pipeline context (post-mapping, pre-validation)
    - Emphasized strict reliance on _source_sheet as source of truth for Client field
    - Reinforced normalization rules and non-null guarantees without introducing validation logic
    - Included TDD requirements with unit and integration tests covering multi-sheet scenarios
- **Impact:**
    - Clearly defines responsibility boundaries between parsing and downstream validation
    - Ensures consistent Client attribution across multi-sheet ingestion workflows
    - Prevents premature validation while guaranteeing required field presence for later stages
---

### Prompt ID: P-029
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Generate Claude implementation prompt for T3-3 Client field injection
#### Prompt
```
# 🧠 Claude Code Prompt — T3-3 Client Field Injection (MVP + TDD + Pipeline Discipline)

You are acting as a **Lead Data Engineer** implementing:

> **T3-3 — Client Field Injection**

for the Donor Bureau Excel → CSV ingestion pipeline.

---

# 🎯 Project Context (Critical)

Pipeline flow:

parse → map → normalize → client_injection → validate → split → output

You are implementing the stage responsible for assigning the **Client** field.

---

## ⚠️ Upstream + Downstream Awareness

### Input (from T3-2 normalization):

- pandas DataFrame
- includes `_source_sheet` column (from parser)
- may contain multiple sheets combined into one DataFrame
- values already normalized, but structure not yet validated

### Output (to T4 validation):

- same DataFrame
- now includes a **Client** column

---

## 🚨 Critical Engineering Constraint

This stage is **NOT responsible for validation**.

That means:

- Do NOT reject rows
- Do NOT enforce schema completeness beyond injecting Client
- Do NOT validate client naming quality

👉 Validation happens in **T4**

---

# 🎯 Ticket Goal

Implement:

app/client.py

(or integrate into existing transformer layer if already structured that way)

This module must:

- create a `Client` column
- populate it using `_source_sheet`
- normalize values safely (trim whitespace)
- ensure consistency across all rows

---

# ⚙️ Functional Requirements

## 1. Client Assignment

- For each row:
  - Client = `_source_sheet`

---

## 2. Sheet Name Normalization

- Strip leading/trailing whitespace

Example:
" Alpha Fund " → "Alpha Fund"

---

## 3. Required Behavior

- Every row must have a non-null Client value
- No empty strings
- No whitespace-only values

---

## 4. Multi-Sheet Handling

Must correctly assign different Client values within same DataFrame:

Sheet1 → Client A  
Sheet2 → Client B

---

## 5. _source_sheet Handling

- Must remain unchanged
- Must NOT be dropped or overwritten

---

# 🧪 TDD REQUIREMENTS (MANDATORY)

Write tests FIRST.

## Required Unit Tests

1. Single-sheet input
- all rows same Client value
- matches sheet name

2. Multi-sheet input
- correct client per row
- multiple clients present

3. Sheet name normalization
- trims whitespace correctly

4. No empty Client values
- no null / "" / whitespace-only

---

## Integration Test

- multi-sheet DataFrame simulation
- verify:
  - correct Client assignment
  - no data loss
  - _source_sheet consistency

---

# ⚙️ Implementation Constraints (MVP Discipline)

DO:
- use pandas vectorized operations
- rely ONLY on `_source_sheet`
- keep logic minimal and deterministic

DO NOT:
- validate client names
- drop rows
- modify unrelated columns
- add metadata logic
- over-engineer abstractions

---

# 🧠 Design Principles (CRITICAL)

1. Client is derived, not sourced from data cells
2. Deterministic transformation only
3. Normalize, do not validate

---

# 🚫 DO NOT

- read Client from Excel content
- validate client names
- modify _source_sheet
- introduce business logic

---

# ✅ Success Criteria

Complete when:
- all tests pass
- every row has valid Client
- correct mapping from _source_sheet
- deterministic multi-sheet handling

---

Begin.
```

- **Summary of Response:**
    - Structured a full MVP + TDD implementation prompt for Claude defining Client field injection logic
    - Reinforced strict dependency on _source_sheet as sole source of truth for Client assignment
    - Explicitly separated concerns between ingestion, transformation, and downstream validation
    - Included deterministic behavior rules and multi-sheet handling requirements
- **Impact:**
    - Locks in consistent client attribution across all pipeline data before validation stage
    - Prevents leakage of business logic into transformation layer
    - Ensures downstream analytics can reliably segment data by client without ambiguity
---

### Prompt ID: P-030
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Generate QA review prompt for T3-3 Client field injection validation
#### Prompt
```
# 🧠 Claude Code Prompt — Senior QA / Test Review (T3-3 Client Field Injection)

You are acting as a **Senior QA Engineer + Lead Data Engineer** performing a deep review of:

> T3-3 — Client Field Injection

Your responsibility is to evaluate:

- correctness of Client assignment logic
- data integrity across multi-sheet ingestion
- test coverage quality
- adherence to strict MVP pipeline boundaries

---

# 🎯 Review Objective

Determine:

> “Is the Client field correctly and reliably derived from sheet metadata without introducing inconsistencies or data corruption?”

This is a **high-trust field** used for downstream segmentation and analytics.

---

# 📌 Context Reminder

Input:
- pandas DataFrame
- includes `_source_sheet` column (from parser stage)
- may contain multiple sheets combined
- sheet names may contain whitespace inconsistencies

Output:
- same DataFrame
- new `Client` column
- derived ONLY from `_source_sheet`

---

# ⚠️ Critical Constraints

This stage must:
- derive Client strictly from `_source_sheet`
- normalize sheet names (trim whitespace only)
- be deterministic across all rows

This stage must NOT:
- read client values from Excel cells
- validate client names
- modify other columns
- drop or filter rows
- depend on external mapping/config

---

# ⚠️ Critical Areas to Evaluate

## 1. Source of Truth Enforcement (HIGHEST PRIORITY)
Check:
- Is `_source_sheet` the ONLY source used?
- Is any fallback logic present?
- Are in-cell “Client” values ever used?

---

## 2. Sheet Name Normalization
Verify:
- whitespace trimming applied correctly
- no over-normalization (no unintended lowercasing)
- consistent behavior across all rows

Example:
" Alpha Fund " → "Alpha Fund"

---

## 3. Multi-Sheet Integrity
Check:
- correct Client values per sheet
- no cross-sheet contamination
- no row misassignment across sheets

---

## 4. Determinism
Ensure:
- same input → same output
- no row-order dependency
- no groupby/order side effects

---

## 5. Empty / Invalid Values Handling
Verify:
- no null Client values
- no empty strings
- no whitespace-only values

---

## 6. Column Integrity
Ensure:
- `_source_sheet` unchanged
- `Client` correctly added
- no overwrites of existing columns

---

## 7. Separation of Concerns
Confirm:
- no validation logic (T4 responsibility)
- no mapping logic (T3-1 responsibility)
- no normalization logic beyond trimming

---

# 🧪 Test Suite Review

## Required Coverage
- single-sheet case
- multi-sheet case
- whitespace in sheet names
- multiple distinct clients
- no empty Client values

---

## Edge Case Coverage
- empty `_source_sheet`
- malformed sheet names
- duplicate sheet names
- single-row DataFrame
- large dataset consistency

---

## Test Quality
- value-based assertions
- explicit multi-sheet validation
- clear failure diagnostics

---

## Integration Confidence
- compatibility with T2-2 parser output
- compatibility with T3-2 normalization
- safe handoff to T4 validation

---

# ⚠️ Common Failure Patterns
- using Excel cell “Client” instead of sheet name
- inconsistent whitespace handling
- cross-sheet contamination
- silent null Client values
- accidental mutation of `_source_sheet`

---

# 🧪 Output Requirements

## 1. What Was Done Well
## 2. Critical Issues (Must Fix)
## 3. Medium Issues
## 4. Minor Improvements
## 5. Test Coverage Gaps
## 6. Suggested Fixes
## 7. Final Verdict

---

# 🚫 DO NOT
- rewrite implementation
- add validation logic
- introduce new pipeline stages
- expand scope beyond MVP

---

# ✅ Success Criteria

Ensure:
- deterministic Client derivation
- no cross-sheet contamination
- safe integration into T4 stage
- strong test coverage for multi-sheet behavior

---

Begin review.
```

- **Summary of Response:**
     - Produced a structured QA review prompt for T3-3 focusing on Client derivation correctness and multi-sheet integrity
     - Reinforced strict reliance on _source_sheet as sole source of truth
     - Defined detailed test coverage expectations and edge case analysis
     - Maintained strict MVP boundaries and separation from validation logic
- **Impact:**
     - Strengthens data integrity guarantees for downstream analytics and segmentation
     - Reduces risk of cross-sheet contamination in multi-client datasets
     - Ensures consistent, deterministic behavior before entering validation stage (T4)
---

### Prompt ID: P-031
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for pipeline orchestrator (T3-4)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T3-4 - Pipeline orchestrator:

# Description
Central function that executes pipeline in order:
parse → map → normalize → validate → split → enforce schema → output

# Acceptance criteria
- single run_pipeline(df, config) function exists
- each stage receives the output of the previous
- any stage raising an exception halts the pipeline and bubbles up a structured error
- the function returns a dict with clean_df, rejected_df, and summary.

# Test plan
- unit test with a mocked happy path (all stages pass)
- unit test where validation stage raises — confirm pipeline halts and error propagates correctly
- integration test using a real fixture end-to-end.
```

- **Summary of Response:**
    - Generated a structured Claude prompt defining T3-4 pipeline orchestrator as a deterministic execution layer
    - Specified strict stage ordering: parse → map → normalize → validate → split → enforce schema → output
    - Defined failure propagation rules ensuring any stage error halts execution and returns structured output
    - Included unit and integration test requirements covering both happy path and failure scenarios
- **Impact:**
    - Establishes a single control point for pipeline execution and stage coordination
    - Ensures consistent data flow across all transformation stages with strict ordering guarantees
    - Improves reliability by enforcing fail-fast behavior and structured error handling
    - Enables end-to-end testability of the full ingestion pipeline prior to production scaling
---

### Prompt ID: P-032
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Generate Claude implementation prompt for T3-4 pipeline orchestrator (execution layer)
#### Prompt
```
# 🧠 Claude Code Prompt — T3-4 Pipeline Orchestrator (MVP TDD Execution Layer)

You are acting as a **Lead Data Engineer** implementing:

> T3-4 — Pipeline Orchestrator

for the Donor Bureau Excel → CSV ingestion system.

---

# 🎯 Role of This Component (Critical Context)

This is the **central execution layer** of the entire pipeline.

It is NOT responsible for data transformation logic.

It is ONLY responsible for:

> Coordinating execution order + passing outputs between stages safely.

---

# ⚙️ Pipeline Flow (STRICT ORDER)

You MUST implement the following deterministic flow:

parse → map → normalize → client_injection → validate → split → enforce_schema → output

Each stage:

- receives output from previous stage
- returns output to next stage
- must remain independent and testable

---

# 📌 Core Function Requirement

Implement:

```python
run_pipeline(df, config)
📥 Input
df: raw parsed DataFrame (from parser stage)
config: loaded configuration object (mapping.json + settings)
📤 Output

Function MUST return:

{
"clean_df": DataFrame,
"rejected_df": DataFrame,
"summary": {
"total_rows": int,
"clean_rows": int,
"rejected_rows": int
}
}

⚠️ Critical Design Constraints
1. No Business Logic Allowed

This orchestrator MUST NOT:

normalize data
validate fields
map columns
infer schema rules

It only coordinates.

2. Deterministic Execution
Same input → same output
No randomness
No hidden side effects
No external state dependency
3. Strict Stage Boundaries

Each stage must be called explicitly:

df1 = parse(df, config)
df2 = map_columns(df1, config)
df3 = normalize(df2)
df4 = inject_client(df3)
df5 = validate(df4)
clean_df, rejected_df = split(df5)
final_df = enforce_schema(clean_df)

🚨 Error Handling Requirements (CRITICAL)
1. Fail Fast Behavior

If ANY stage raises an exception:

pipeline MUST stop immediately
exception MUST NOT be swallowed
error MUST bubble up to caller
2. Structured Error Contract

If an error occurs, wrap it in:

{
"error_stage": "<stage_name>",
"error_type": "<exception_type>",
"error_message": "<message>"
}

3. No Partial Output on Failure

If pipeline fails:

do NOT return partial clean/rejected data
raise structured exception instead
🧪 TESTING REQUIREMENTS (TDD-FIRST)
1. Happy Path Unit Test (Mocked Stages)

Mock all stages:

parse
map
normalize
client_injection
validate
split
enforce_schema

Verify:

correct execution order
correct data passing between stages
correct return structure
2. Failure Propagation Test (Validation Stage)

Simulate:

validate() raises exception

Verify:

pipeline halts immediately
exception propagates
no further stages executed
3. Integration Test (Real Fixture)

Verify:

clean_df output correct
rejected_df output correct
summary counts correct
deterministic behavior
🧠 Observability Requirements (MVP LIGHTWEIGHT)
log stage start
log stage completion
log stage failure

No heavy observability systems.

🚫 DO NOT
implement transformation logic
mutate DataFrames beyond passing through
merge pipeline stages
swallow exceptions
introduce async/concurrency
✅ SUCCESS CRITERIA
run_pipeline is single entry point
strict execution order enforced
failure halts pipeline immediately
full test coverage for:
happy path
failure propagation
integration flow
🧠 FINAL NOTE

This orchestrator is the backbone of the system.

If it fails or becomes ambiguous:

downstream debugging becomes impossible.

Begin implementation.
```

- **Summary of Response:**
    - Generated a deterministic orchestration-layer prompt defining `run_pipeline(df, config)` as the central pipeline execution function
    - Enforced strict stage ordering with no embedded business logic in orchestrator layer
    - Defined fail-fast error handling with structured error propagation contract
    - Included TDD requirements covering mocked unit tests, failure propagation, and full integration testing
- **Impact:**
    - Establishes a single source of truth for pipeline execution sequencing and coordination
    - Ensures strong separation of concerns between orchestration and transformation logic
    - Prevents partial execution failures and silent error swallowing in production workflows
    - Enables full end-to-end testability of the entire ingestion pipeline with deterministic behavior
---

### Prompt ID: P-033
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Senior QA / Lead Data Engineer Review Prompt for T3-4 Pipeline Orchestrator
#### Prompt:
```
# 🧠 Claude Code Prompt — Senior QA / Lead Tester Review (T3-4 Pipeline Orchestrator)

You are acting as a **Senior QA Engineer + Lead Data Engineer** reviewing:

> **T3-4 — Pipeline Orchestrator (run_pipeline)**

This is the **central execution layer** of the Donor Bureau ingestion pipeline.

Your goal is to validate:

> “Does this orchestrator correctly coordinate the pipeline without hiding failures or corrupting flow integrity?”

---

# 🎯 Context Reminder

Pipeline order MUST be:

```text
parse → map → normalize → client_injection → validate → split → enforce_schema → output

This component does NOT transform data.

It ONLY orchestrates execution.

⚠️ CRITICAL REVIEW OBJECTIVE

You are looking for:

broken execution order
hidden failure handling
incorrect stage wiring
partial or inconsistent outputs
silent data corruption introduced by orchestration
🚨 MOST IMPORTANT FAILURE MODE (WATCH CLOSELY)
Silent Failure Masking

Check if ANY of the following exist:

try/except blocks that swallow exceptions
returning partial DataFrames on failure
converting errors into empty DataFrames
logging errors but continuing execution

👉 These are critical bugs in a data pipeline

⚙️ Required Function Behavior

Verify existence and correctness of:

run_pipeline(df, config)

Must:

execute all stages in correct order
pass output of one stage into next
return structured output dict
fail fast on error
📤 Expected Output Structure

Ensure return format is EXACT:

{
    "clean_df": DataFrame,
    "rejected_df": DataFrame,
    "summary": {
        "total_rows": int,
        "clean_rows": int,
        "rejected_rows": int
    }
}
🧪 TEST REVIEW REQUIREMENTS
1. Happy Path Test (Mocked Stages)

Verify:

all stages are mocked correctly
execution order is enforced
each stage receives correct input
final output structure is validated

🚨 Watch for weak tests that only check “function called”

2. Failure Propagation Test (CRITICAL)

Simulate:

validate() raises an exception

Verify:

pipeline stops immediately
exception is NOT swallowed
no downstream stages execute
error propagates to caller
3. Integration Test (Real Fixture)

Verify:

full pipeline executes end-to-end
correct clean_df and rejected_df outputs
summary counts are accurate
deterministic results across runs
4. Edge Case Coverage

Check for missing tests:

empty DataFrame input
validation failure mid-pipeline
malformed config input
single-row dataset
large dataset consistency
⚙️ EXECUTION FLOW VALIDATION

Confirm:

each stage is called EXACTLY once per run
no stage is skipped
no stage is duplicated
output chaining is correct

Example expectation:

parse(df)
  ↓
map()
  ↓
normalize()
  ↓
inject_client()
  ↓
validate()
  ↓
split()
  ↓
enforce_schema()
  ↓
return
🧠 ARCHITECTURE REVIEW

Check for:

1. Separation of Concerns
orchestrator does NOT transform data
stages remain independent
no business logic leaks into orchestrator
2. Determinism
same input always produces same output
no hidden state or caching
no random or time-based behavior
3. Error Handling Design

Ensure:

failures are immediately raised
structured error context exists if implemented
no partial result return on failure
⚠️ COMMON BUGS TO LOOK FOR
stages executed in wrong order
validate step bypassed accidentally
enforce_schema applied before split (wrong order)
clean/rejected swap bugs
summary counts mismatched
DataFrame mutation across stages (shared reference issues)
🧪 OUTPUT FORMAT

Return your review using:

1. ✅ What Works Well
correct orchestration structure
strong separation of concerns
good test design
2. 🔴 Critical Issues (Must Fix)
ordering violations
hidden failure handling
incorrect outputs
missing failure propagation
3. 🟡 Medium Issues (Should Fix)
weak test assertions
incomplete edge case coverage
unclear stage interfaces
4. 🟢 Minor Improvements
readability improvements
logging clarity
naming improvements
5. 🧪 Test Coverage Gaps
missing integration cases
insufficient failure simulation
weak mocking strategy
6. 🔧 Suggested Fixes
actionable improvements only
do NOT redesign pipeline architecture
stay within MVP scope
7. 🧠 Final Verdict

Choose one:

✅ Ready to merge
⚠️ Merge with fixes
❌ Not ready

Provide justification.

🚫 DO NOT
rewrite the orchestrator
add new pipeline stages
introduce async/concurrency
modify business logic
expand scope beyond MVP
🎯 SUCCESS CRITERIA

This review passes if:

pipeline execution is deterministic
failures are correctly propagated
stage order is strictly enforced
no silent failure paths exist
tests provide real confidence in orchestration correctness

Begin review.
```

- **Summary of Response:**
    - Produced a structured senior QA review prompt for the T3-4 pipeline orchestrator
    - Emphasized strict enforcement of execution order: parse → map → normalize → client_injection → validate → split → enforce_schema → output
    - Focused heavily on detecting silent failure masking, which is the highest-risk failure mode in orchestration layers
    - Defined detailed requirements for unit, failure propagation, and integration testing
    - Reinforced strict separation of concerns and deterministic execution without side effects
- **Impact:**
    - Ensures the orchestrator is evaluated as a deterministic control plane rather than a transformation layer
    - Prevents hidden failure paths that could silently corrupt downstream data workflows
    - Strengthens confidence in end-to-end pipeline reliability before scaling or production use
---

### Prompt ID: P-034
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** E3 Checkpoint Review — End-to-End QA & Data Engineering Audit

#### Prompt:
```
ok now that we've completed up to E3 - Data Processing please generate a prompt to Claude to do a checkpoint review of all the code as it stands and also take into consideration the input_contract, fixtures, testing, MVP as a lead senior QA / Data Engineer
```

- **Summary of Response:**
    - Generated a comprehensive E3 checkpoint review prompt covering the entire pipeline from config through orchestration
    - Integrated input_contract, fixture realism, TDD rigor, and MVP discipline into a unified QA evaluation framework
    - Emphasized high-risk areas including parser reliability, mapping determinism, normalization safety, and orchestrator    - fail-fast behavior
    - Defined a structured audit output including executive summary, issue severity tiers, test coverage assessment, and readiness verdict

- **Impact:**
    - Provides a critical quality gate before entering T4 (validation), reducing risk of compounding downstream errors
    - Surfaces hidden data integrity issues early across the full pipeline lifecycle
    - Ensures alignment between implementation, contract expectations, and real-world data variability
    - Strengthens confidence that the system is production-viable and not just test-passing
---

### Prompt ID: P-035
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** E3 System Checkpoint Audit — Contract Compliance & Pipeline Readiness Assessment
#### Prompt
```
# 🧠 Claude Code Prompt — E3 Checkpoint System Review (Senior QA + Lead Data Engineer)

You are acting as a **Senior Lead QA Engineer + Principal Data Engineer** performing a **full system checkpoint review** of the Donor Bureau Excel → CSV ingestion pipeline at milestone:

> **E3 — Data Processing Complete (T2–T3 implemented)**

---

# 🎯 Purpose of This Review

This is NOT a file-by-file review.

This is a **system-level audit** to determine:

> “Is this pipeline correct, testable, and aligned with the Input Contract and MVP architecture before moving into validation (T4) and output hardening (T5)?”

---

# 📌 Primary Sources of Truth (NON-NEGOTIABLE)

You must evaluate ALL code against:

## 1. Input Contract (STRICT AUTHORITY)

* `/docs/input_contract.md`

This defines:

* sheet structure
* header detection rules
* column aliases
* metadata handling rules
* assumptions about real-world data

---

## 2. Fixture Library (GROUND TRUTH FOR BEHAVIOR)

* `/tests/fixtures/` (T7-1 expected coverage)

You must assume:

> If a behavior is not represented in fixtures, it is NOT validated.

---

## 3. Architecture Intent (MVP PIPELINE DESIGN)

Pipeline must follow:

text id="pipeline_e3"
parse → map → normalize → client_injection → validate → split → enforce_schema → output

---

# ⚠️ CRITICAL REVIEW OBJECTIVES

You are verifying:

## 1. Contract Compliance

Does the system strictly obey `input_contract.md`?

Look for:

* incorrect header detection assumptions
* metadata rows misinterpreted as data
* incorrect alias mapping
* invalid client derivation logic
* broken multi-sheet handling

---

## 2. Pipeline Integrity (T2–T3)

Verify each stage:

* parser (multi-sheet correctness)
* mapper (alias correctness, no validation leakage)
* normalizer (no schema enforcement, only transformation)
* client injection (pure derivation from `_source_sheet`)
* orchestrator (correct sequencing, no logic leakage)

---

## 3. Separation of Concerns (CRITICAL)

Check for violations:

* validation logic inside T3 stages ❌
* transformation logic inside orchestrator ❌
* schema enforcement before validation ❌
* client logic in parser or mapper ❌

---

## 4. Data Integrity Risks (HIGH PRIORITY)

Actively search for:

* ZIP code corruption (leading zero loss)
* date parsing inconsistencies (Excel serial + string mix)
* numeric coercion errors (DonationAmount)
* silent NaT / NaN propagation
* sheet mixing across multi-sheet ingestion
* client misassignment across sheets

---

## 5. Error Handling Strategy

Verify:

* fail-fast behavior in orchestrator
* structured error propagation
* no silent swallowing of exceptions
* validation errors separated from system errors

---

## 6. Test Coverage vs Real Behavior

Cross-check:

### Required test categories:

* single-sheet ingestion
* multi-sheet ingestion
* header offset detection
* metadata row skipping
* alias mapping coverage
* normalization correctness (dates, ZIP, amounts)
* validation rejection logic
* orchestrator failure propagation
* full integration test

---

# ⚠️ MAJOR GAP ANALYSIS (CRITICAL TASK)

Identify:

## 1. What is NOT tested but SHOULD be

Based on input contract + fixtures

## 2. What is tested but NOT representative of real-world input

## 3. Any mismatch between:

* fixtures vs contract
* contract vs implementation
* implementation vs tests

---

# 🧪 SYSTEM INTEGRATION REVIEW

Simulate mentally:

> “If I upload a real messy Excel file from a donor organization, will this pipeline behave correctly end-to-end?”

Check:

* correct sheet parsing
* correct header detection
* correct alias resolution
* correct normalization
* correct client assignment
* correct validation split
* correct output schema

---

# 📊 OUTPUT REQUIREMENTS

Provide a structured report:

---

## 1. 🧠 Executive Summary

* Is system MVP-ready for T4?
* Major risks blocking progression?

---

## 2. ✅ What Is Strong

* architecture alignment
* correct separation of concerns
* strong TDD adherence
* good pipeline modularity

---

## 3. 🔴 Critical Issues (BLOCKERS)

Must include:

* contract violations
* data corruption risks
* pipeline ordering issues
* test coverage gaps affecting correctness

---

## 4. 🟡 Medium Risks

* edge cases not fully handled
* weak fixture coverage alignment
* brittle parsing assumptions

---

## 5. 🟢 Minor Issues

* readability improvements
* logging improvements
* minor refactors

---

## 6. 🧪 Test Coverage Audit

* What is well-covered
* What is missing
* What is misleading or insufficient

---

## 7. 📉 Contract vs Code Drift Analysis

Explicitly list:

* Input contract expectation → implementation mismatch
* Fixture expectation → missing coverage
* Implementation assumption → not validated

---

## 8. 🔧 Recommendations (MVP-SAFE ONLY)

* fixes must NOT introduce new architecture
* no feature expansion
* no refactoring beyond necessity

---

## 9. 🧠 Final Verdict

Choose one:

* ✅ READY FOR T4 (Validation Layer)
* ⚠️ READY WITH MINOR FIXES
* ❌ NOT READY — MUST FIX BEFORE PROCEEDING

---

# 🚫 STRICT PROHIBITIONS

Do NOT:

* redesign pipeline
* add new stages
* introduce new frameworks
* expand scope beyond MVP
* ignore input_contract.md

---

# 🎯 SUCCESS CRITERIA

This review passes only if:

* pipeline is contract-compliant
* T2–T3 stages are cleanly separated
* data integrity is guaranteed
* test coverage is meaningful (not superficial)
* system is safe to proceed to validation layer (T4)

---

Begin full system audit.

```

- **Summary of Response:**
    - Constructed a comprehensive system-level QA audit prompt for evaluating the Donor Bureau pipeline at E3 completion
    - Positioned the review around three core authorities: input_contract.md, fixture library, and MVP pipeline architecture
    - Emphasized critical risk areas including header detection, alias mapping, normalization safety, client assignment, and orchestrator integrity
    - Introduced a structured gap analysis to identify mismatches between contract, fixtures, tests, and implementation
    - Defined rigorous output expectations including executive summary, issue severity tiers, contract drift analysis, and final readiness verdict
    - Reinforced strict MVP boundaries and prohibited scope expansion or architectural redesign during review
- **Impact:**
    - Establishes a high-signal checkpoint ensuring the pipeline is safe, contract-compliant, and test-validated before entering T4 (validation layer)
    - Surfaces hidden inconsistencies between design intent and implementation early, reducing downstream rework
    - Strengthens confidence in end-to-end pipeline reliability under real-world messy Excel inputs
    - Provides a clear decision gate for whether the system can safely progress or requires remediation
---

### Prompt ID: P-036
- **Author:** Mark / Claude
- **Target:** ChatGPT
- **Purpose:** E3 Audit Remediation — Apply QA-Identified Fixes and Align Contract, Fixtures, and Pipeline Stubs
#### Prompt
```
Fed the codebase to Claude and it did a checkpoint review on it:
Good — I can now see the actual code in your repo. This matches what we built together. Here is the E3 system audit against the real codebase.

1. 🧠 Executive Summary
⚠️ READY WITH MINOR FIXES
The pipeline is architecturally sound and ready for T4. Two items need attention before proceeding: an alias drift between input_contract.md and mapping.json, and a missing real-world format fixture in the pipeline integration test. Neither requires code changes to the pipeline stages.

2. ✅ What Is Strong
Pipeline stage boundaries are clean. Every module has a single responsibility. No transformation logic in the orchestrator, no validation in the normalizer, no mapping in the parser. The docstring contracts at the top of each file are accurate and enforced.
Header detection is contract-compliant. _detect_header_row() scans first N rows from config, stops at first match with ≥ 2 aliases, uses header_scan_rows from mapping.json. The confirmed Alpha Fund metadata pattern is covered in test_parser.py.
ZIP preservation is correct. zfill(5) handles both string and integer inputs. pd.isna() early return prevents crashes on null values.
Read-only worksheet double-iteration bug was caught and fixed. Rows are materialized once per sheet via list(sheet.iter_rows(...)) before any processing.
PipelineError is well-structured. stage, error_type, and error_message as named attributes makes T4-4 API error responses straightforward to implement.
df.copy() used consistently across all stages — no shared reference mutation between pipeline stages.
_run_stage() wrapper ensures no exception can be swallowed — every failure wraps to PipelineError and re-raises immediately.

3. 🔴 Critical Issues
Alias drift between input_contract.md and mapping.json.
The contract (section 3.1) and mapping.json do not match:
FieldContract aliasesmapping.json aliasesDriftDonationAmountdonationamount, amount, gift_amount, donationamount, donationamount, donation_amount, gift_amountdonation missing from config; donation_amount undocumentedDonationDatedonationdate, giftdate, date, gift_dategiftdate, gift_date, donationdate, donation_date, datedonation_date undocumented in contractStatestate, stst, state, state_codestate_code undocumented in contract
The fix is to update input_contract.md section 3.1 to include the additional aliases in mapping.json. The config has more aliases than the contract documents — the contract should reflect reality. This is a documentation fix only, no code changes needed.

4. 🟡 Medium Risks
Pipeline integration test uses header-in-row-1 fixture only. test_pipeline_integration_full_flow in test_pipeline.py uses a simple fixture with no metadata rows. The confirmed real-world Alpha Fund format (rows 1–3 metadata, row 4 header) is tested in test_parser.py in isolation but never end-to-end through the full pipeline. Add a second fixture variant to the integration test with metadata rows before the header.
validator.py stub uses iterrows() — the slowest pandas iteration pattern, O(n) Python loop. Acceptable for MVP stub but must be replaced with vectorized operations in T4-1. Add a # TODO T4-1: replace with vectorized validation comment so it's not accidentally left in production.
schema.py stub silently drops missing columns rather than failing. When T5-6 replaces it, the real implementation must fail loudly if required columns are absent. Document this gap with a comment in the stub.

5. 🟢 Minor Issues
from typing import Any in pipeline.py is imported but only used in _run_stage's return annotation. Python 3.12 handles this without the import — minor cleanup.
test_placeholder.py still exists and serves no purpose now. Safe to remove once T4 is complete.
__init__.py in app/processing/ is empty — correct, no changes needed.

6. 🧪 Test Coverage Audit
Well covered:

Single and multi-sheet parsing — header row 1, offset row 3, offset row 5
Metadata row handling — confirmed Alpha Fund pattern tested explicitly
Alias mapping — exact, alias, case-insensitive, duplicates, missing fields
All normalization rules — dates (4 formats + Excel serial), ZIP, amounts, strings
Client injection — multi-sheet, whitespace, null edge cases
Pipeline orchestration — execution order, stage chaining, failure propagation at every stage
Upload endpoint — extension, MIME type, empty file, path traversal

Missing:

Pipeline integration test with metadata rows before header (real-world format)
Pipeline integration test with multi-sheet workbook (two clients)
Any test for donation alias (in contract, absent from mapping.json)
End-to-end test confirming Instructions-style non-data sheet excluded through full pipeline

Misleading:

test_pipeline_integration_full_flow passes with a simple header-in-row-1 fixture — gives confidence about pipeline wiring but not about real-world file handling


7. 📉 Contract vs Code Drift
ItemContractCodeStatusdonation alias for DonationAmountDocumentedMissing from mapping.json❌donation_amount aliasNot documentedIn mapping.json⚠️donation_date aliasNot documentedIn mapping.json⚠️state_code aliasNot documentedIn mapping.json⚠️Header scan N rows from config✅✅✅Threshold ≥ 2 alias matches✅✅✅Client from sheet tab name only✅✅✅Metadata rows skipped✅✅✅ZIP as string, leading zeros preserved✅✅✅

8. 🔧 Recommendations
Fix 1 — Update input_contract.md section 3.1 to document all aliases currently in mapping.json. Add donation_amount, donation_date, state_code. Either add donation to mapping.json or remove it from the contract. Documentation fix only.
Fix 2 — Add metadata-row fixture to test_pipeline_integration_full_flow — a second workbook using the Alpha Fund format (3 metadata rows before header) run through the full pipeline. Confirms the real-world format works end-to-end, not just in the parser.
Fix 3 — Add # TODO T4-1: replace iterrows() with vectorized validation to validator.py stub.
Fix 4 — Add # TODO T5-6: full implementation must fail loudly if required columns absent to schema.py stub.

9. 🧠 Final Verdict
⚠️ READY WITH MINOR FIXES
Fix 1 (contract sync) and Fix 2 (integration test fixture) should be done before T4 begins. Both are 15-minute tasks. Fixes 3 and 4 are one-line comments that protect against future mistakes when stubs are replaced. None of these require any changes to the pipeline stage implementations themselves. The core system is correct and ready.
please generate a prompt to instruct it to fix the flagged issues as a senior data engineer / lead projecgt manager
```

- **Summary of Response:**
    - Generated a targeted remediation prompt instructing ChatGPT to address all issues identified in the E3 checkpoint audit while maintaining strict MVP and pipeline integrity constraints
    - Focused on resolving alias drift between input_contract.md and mapping.json by synchronizing documentation with implemented configuration
    - Requested addition of a realistic metadata-row integration test fixture to ensure end-to-end pipeline coverage of real-world Excel formats
    - Instructed addition of explicit TODO markers in validator and schema stubs to prevent accidental architectural drift in future T4/T5 implementation phases
    - Reinforced that no pipeline logic changes are required, only alignment, documentation correction, and test coverage improvements
- **Impact:**
    - Ensures consistency between system contract, configuration, and real implementation behavior before entering validation stage (T4)
    - Reduces risk of production mismatch caused by undocumented or drifted alias definitions
    - Improves test realism by enforcing full end-to-end coverage of metadata-heavy Excel ingestion patterns
    - Strengthens maintainability by clearly marking future implementation boundaries in stubbed components
    - Preserves architectural integrity while closing critical QA-identified gaps without disrupting MVP pipeline structure
---

### Prompt ID: P-037
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** E3 checkpoint stabilization and contract alignment fixes for pipeline integrity
#### Prompt
```
# 🧠 Claude Code Prompt — E3 Checkpoint Fixes (Senior Data Engineer + Lead PM)

You are acting as a **Senior Data Engineer + Lead Project Manager**.

You are responsible for applying **ONLY the fixes identified in the E3 checkpoint review**.

This is a **stability + alignment pass**, not a redesign.

---

# 🎯 Objective

Bring the codebase into:

> ✅ full alignment between input_contract.md, mapping.json, and test fixtures
> ✅ improved integration test realism
> ✅ future-safe MVP stubs for T4/T5 stages

---

# ⚠️ STRICT CONSTRAINTS

You MUST:

* ❌ NOT refactor pipeline architecture
* ❌ NOT change stage ordering
* ❌ NOT modify business logic behavior
* ❌ NOT add new features
* ❌ NOT expand scope beyond fixes listed below

You MAY:

* update documentation
* update test fixtures
* add missing test coverage
* add TODO comments for future stages
* make minimal config corrections

---

# 🔴 FIX #1 — CONTRACT ↔ CONFIG ALIGNMENT (CRITICAL)

## Problem

Mismatch between:

* `/docs/input_contract.md`
* `app/config/mapping.json`

## Required Action

You must reconcile alias definitions so they are **fully consistent and single-source-of-truth aligned**.

---

## Steps:

### 1. Update `input_contract.md` section 3.1

Ensure it includes ALL aliases currently in `mapping.json`, including:

* donation_amount
* donation_date
* state_code
* any other discovered aliases

OR (if cleaner):

* remove unused aliases from mapping.json instead

👉 Choose ONE source of truth direction:

* Contract drives config OR
* Config drives contract (preferred if config is more complete)

---

## Acceptance Criteria

* No alias exists in config that is not documented in contract
* No alias exists in contract that is not used in config (unless explicitly deprecated)
* Both files match exactly after update

---

# 🟡 FIX #2 — REALISTIC INTEGRATION TEST COVERAGE

## Problem

Integration test does NOT include real-world metadata pattern.

---

## Required Action

Add a **new fixture + test path** that includes:

### Fixture Requirements:

* 3 metadata rows before header
* header not in row 1
* same Alpha Fund pattern already used in parser tests
* full end-to-end pipeline execution

---

## Test Requirements:

Update:

text
test_pipeline_integration_full_flow

to include:

* metadata-offset workbook
* full pipeline execution (not parser-only)
* validation of:

  * clean_df correctness
  * rejected_df correctness
  * summary accuracy

---

## Acceptance Criteria

* integration test covers real-world metadata header offset
* pipeline passes without parser-only assumptions
* counts remain deterministic

---

# 🟡 FIX #3 — FUTURE SAFETY COMMENT (T4-1)

## File:

`validator.py`

Add:

python
# TODO T4-1: replace iterrows() with vectorized validation

---

## Rule

* DO NOT change implementation
* DO NOT optimize now
* This is purely a forward-looking safeguard

---

# 🟡 FIX #4 — FUTURE SAFETY COMMENT (T5-6)

## File:

`schema.py`

Add:

python
# TODO T5-6: enforce strict schema validation (fail if required columns missing)

---

## Rule

* DO NOT change behavior (dropping columns stays for now)
* ONLY add comment documenting future enforcement requirement

---

# 🧪 VALIDATION REQUIREMENTS

After fixes, ensure:

## 1. Test Suite Must Pass

* all unit tests pass
* all integration tests pass
* no snapshot changes unless intentional and justified

---

## 2. No Behavioral Changes

Confirm:

* pipeline output unchanged (except improved coverage)
* no stage reordering
* no logic modifications in T2–T3 stages

---

## 3. Contract Alignment Achieved

* input_contract.md and mapping.json are consistent
* no hidden alias mismatches remain

---

# 🧠 ENGINEERING PRINCIPLE

This is a:

> “stability + alignment + realism pass”

NOT a refactor.

---

# 🚫 DO NOT

* redesign pipeline
* optimize pandas usage
* modify normalization logic
* change parsing logic
* introduce new abstractions
* expand scope beyond listed fixes

---

# ✅ SUCCESS CRITERIA

This task is complete when:

* contract and mapping.json are fully aligned
* integration test includes real metadata header scenario
* future TODO markers exist in validator and schema modules
* full test suite passes deterministically
* pipeline behavior is unchanged and stable

---

# 🧠 FINAL NOTE

This step ensures:

> your system is not just correct in isolation, but correct under real-world Excel ingestion conditions.

---

Begin implementation.

```

- **Summary of Response:**
    - Generated a tightly scoped E3 checkpoint fix prompt instructing Claude to reconcile contract/config drift, improve    integration test realism with metadata-offset fixtures, and add future-safe TODO annotations for T4/T5 while explicitly preventing any architectural or behavioral changes.

- **Impact:**
    - Restores single source of truth alignment between contract and configuration
    - Improves end-to-end test realism for real-world Excel ingestion patterns
    - Strengthens forward compatibility for upcoming validation and schema stages
    - Ensures system stability without introducing regression or scope creep
---

### Prompt ID: P-038
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate MVP TDD implementation prompt for T4-1 null/missing field validator
#### Prompt
```
ok now let's move into this Epic: 
T4-1 - Null / missing field validator 
T4-2 - Type and value validators 
T4-3 - Row splitter (clean / rejected) 
T4-4 - System-level error handling 

in our first ticket: 

T4-1 - Null / missing field validator 
Description 
validator.py checks every required field for null, empty string, or whitespace-only. 
Rows failing any check added to rejected df with error reason column. 

Acceptance criteria 
Row missing First → rejected with "Missing: First, Last" 
Row with all fields → passes through 
Multiple missing fields → single row, combined reason 

Test plan 
Unit tests: 
all fields present, one missing, multiple missing, whitespace-only field. 

From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:
```

- **Summary of Response:**
    - Generated a strict MVP-focused T4-1 validator prompt defining missing-field detection logic, clean vs rejected dataframe splitting, deterministic error message construction, and mandatory TDD coverage for null, whitespace, and multi-field failure scenarios.
- **Impact:**
    - Establishes first concrete validation layer in pipeline (structural integrity enforcement)
    - Ensures consistent rejection logic for incomplete records before type/value validation (T4-2)
    - Prevents silent data quality issues from propagating downstream
    - Reinforces strict separation between validation, transformation, and orchestration layers
---

### Prompt ID: P-039
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Implement T4-1 missing-field validator enforcing row-level completeness checks in MVP pipeline
#### Prompt
```
# 🧠 Claude Code Prompt — T4-1 Missing Field Validator (Lead Data Engineer + MVP TDD)

You are acting as a **Lead Data Engineer** implementing:

> **T4-1 — Null / Missing Field Validator**

for the Donor Bureau Excel ingestion pipeline.

---

# 🎯 Role of This Component (CRITICAL CONTEXT)

This is the **first true enforcement layer** in the pipeline.

Pipeline context:

text id="t4flow"
parse → map → normalize → client_injection → validate → split → enforce_schema → output

This stage is responsible for:

> Identifying incomplete or invalid rows and routing them into a rejected dataset.

---

# ⚠️ CRITICAL CONSTRAINTS

This module MUST:

* ❌ NOT transform data
* ❌ NOT normalize data
* ❌ NOT map columns
* ❌ NOT enforce schema
* ❌ NOT modify values

It ONLY:

* detects missing values
* classifies row validity
* attaches rejection reasons

---

# 🎯 FUNCTIONAL REQUIREMENT

Implement a validation function in:

python id="validator_file"
validator.py

Example signature:

python id="validate_fn"
validate_required_fields(df) -> (clean_df, rejected_df)

(or equivalent consistent with your existing pipeline interface)

---

# 📌 REQUIRED VALIDATION RULES

A row is INVALID if ANY required field is:

* null (NaN)
* empty string ""
* whitespace-only string "   "

---

# 📋 REQUIRED FIELDS

The validator must enforce presence of:

* First
* Last
* Address1
* City
* State
* Zip
* DonationDate
* DonationAmount
* Client

---

# 🚨 REJECTION LOGIC

## 1. Single Missing Field

Example:

First = missing

Rejection reason:

"Missing: First"

---

## 2. Multiple Missing Fields

Example:

First = missing
Last = missing

Rejection reason:

"Missing: First, Last"

---

## 3. Whitespace Handling

Treat as missing:

* ""
* "   "

---

## 4. Valid Row

If ALL required fields are present and non-empty:

* row goes to clean_df
* no rejection reason

---

# 📤 OUTPUT CONTRACT

Return:

python id="output_contract"
clean_df
rejected_df


Where:

## clean_df

* only valid rows
* no missing required fields

## rejected_df

* invalid rows
* includes extra column:

text id="reason_col"
rejection_reason

---

# 🧪 TEST-DRIVEN DEVELOPMENT REQUIREMENTS

You MUST write tests FIRST or in parallel.

---

## 1. Unit Test — All Fields Present

Input:

* complete row

Expected:

* appears in clean_df
* not in rejected_df

---

## 2. Unit Test — Single Missing Field

Input:

* missing "First"

Expected:

* rejected_df contains row
* rejection_reason = "Missing: First"

---

## 3. Unit Test — Multiple Missing Fields

Input:

* missing First + Last

Expected:

* rejection_reason = "Missing: First, Last"
* correct comma-separated ordering

---

## 4. Unit Test — Whitespace Handling

Input:

* "   " treated as missing

Expected:

* rejected correctly flagged

---

## 5. Unit Test — Mixed Dataset

Input:

* mix of valid + invalid rows

Expected:

* clean + rejected counts sum to input size

---

# ⚙️ IMPLEMENTATION REQUIREMENTS (MVP DISCIPLINE)

DO:

* use vectorized pandas operations where possible
* keep logic simple and explicit
* ensure deterministic behavior

---

DO NOT:

* modify values (no normalization here)
* change schema structure
* drop columns other than classification split
* introduce business logic
* depend on upstream assumptions beyond required fields

---

# 🧠 DESIGN PRINCIPLE

This stage is:

> “Row classification only — not transformation, not interpretation.”

---

# ⚠️ COMMON FAILURE MODES TO AVOID

* treating NaN inconsistently across string/numeric fields
* forgetting whitespace-only cases
* incorrect concatenation of rejection reasons
* modifying input DataFrame instead of copying
* leaking invalid rows into clean_df

---

# 🧪 EDGE CASES TO CONSIDER

* completely empty row
* row with all whitespace values
* mixture of NaN and empty strings
* single-column missing vs multi-column missing
* large dataset performance (vectorization preferred)

---

# 📊 OUTPUT VALIDATION REQUIREMENTS

Ensure:

* clean_df + rejected_df row counts = input row count
* no row appears in both outputs
* rejection_reason always present in rejected_df
* clean_df has ZERO nulls in required fields

---

# 🚫 DO NOT

* perform type validation (T4-2 responsibility)
* perform schema enforcement (T5-6 responsibility)
* modify or enrich data values
* introduce pipeline orchestration logic

---

# ✅ SUCCESS CRITERIA

This ticket is complete when:

* all required field null/empty detection works correctly
* rejection reasons are accurate and deterministic
* all unit tests pass
* no clean rows contain missing required fields
* pipeline remains stable and unchanged upstream/downstream

---

# 🧠 FINAL NOTE

This validator is the **first enforcement gate** in your system.

Its correctness ensures:

> downstream analytics are not polluted by incomplete donor records.

---

Begin implementation.

```

- **Summary of Response:**
    - Generated a strict MVP-aligned T4-1 missing-field validator prompt defining row-level completeness checks, deterministic rejection reasoning, and clean vs rejected dataframe splitting, with mandatory TDD coverage and strict separation from type validation and schema enforcement stages.
- **Impact:**
    - Establishes first data quality enforcement gate in the pipeline
    - Prevents incomplete records from propagating into downstream validation and analytics stages
    - Ensures deterministic, test-driven classification logic for missing fields
    - Reinforces strict separation between validation, transformation, and schema enforcement responsibilities
---

### Prompt ID: P-040
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Production-grade QA review of T4-1 missing-field validator for data integrity and pipeline safety
#### Prompt
```
# 🧠 Claude Code Prompt — T4-1 QA / Senior Test Engineer Review

You are acting as a **Senior QA Engineer + Lead Data Engineer reviewer**.

Your task is to perform a **strict, production-style code review** of the implementation for:

> **T4-1 — Null / Missing Field Validator**

This is a **critical data quality gate** in the Donor Bureau pipeline.

---

# 🎯 PRIMARY OBJECTIVE

Verify that the implementation correctly:

* identifies missing required fields
* correctly classifies rows into clean vs rejected
* produces deterministic rejection reasons
* preserves data integrity (no accidental mutation or leakage)

---

# 📌 WHAT YOU ARE REVIEWING

You are reviewing the code in:

text id="validator_location"
validator.py

and its associated tests.

---

# ⚠️ REVIEW PHILOSOPHY

This is NOT a style review.

This is a:

> “Would this break production data integrity in a real donor ingestion system?”

review.

---

# 🧪 CORE FUNCTIONAL REQUIREMENTS CHECK

You MUST verify:

## 1. Missing Field Detection

Confirm correct handling of:

* null / NaN values
* empty strings ""
* whitespace-only strings "   "

✔ These must ALL be treated as missing

---

## 2. Required Fields Enforcement

Ensure validator checks ALL required fields:

* First
* Last
* Address1
* City
* State
* Zip
* DonationDate
* DonationAmount
* Client

---

## 3. Rejection Logic Correctness

Verify:

### Single missing field:

* `"Missing: First"`

### Multiple missing fields:

* `"Missing: First, Last"`

✔ Ensure:

* comma separation is correct
* ordering is deterministic (IMPORTANT)
* no extra spaces or formatting drift

---

## 4. Data Integrity Guarantees

Confirm:

* clean_df contains ONLY valid rows
* rejected_df contains ONLY invalid rows
* NO row appears in both outputs
* NO row is silently dropped

---

## 5. Rejection Column Integrity

Ensure:

* rejected_df includes `rejection_reason`
* field is always populated (never null/empty)

---

## 6. Pandas Safety Review

Check for common issues:

* mutation of input DataFrame
* chained assignment warnings
* accidental view vs copy bugs
* inconsistent handling of NaN vs empty string
* row-wise iteration where vectorization should be used

---

# 🧪 TEST COVERAGE REVIEW

You MUST evaluate test completeness:

## Required tests:

### ✔ All valid row

* goes to clean_df

### ✔ Single missing field

* correct rejection reason

### ✔ Multiple missing fields

* combined deterministic message

### ✔ Whitespace-only fields

* treated as missing

### ✔ Mixed dataset

* row counts match input exactly

---

# 🚨 RED FLAGS (FAIL REVIEW IF PRESENT)

Immediately flag if you see:

* missing whitespace handling
* inconsistent NaN handling
* non-deterministic rejection reason ordering
* use of iterrows for core logic without justification
* mutation of input df
* dropped rows without explicit classification
* silent failures

---

# 📊 INTEGRATION EXPECTATIONS

Ensure alignment with pipeline:

text id="pipeline_context"
parse → map → normalize → validate (T4-1) → split → enforce_schema → output

T4-1 must NOT:

* normalize
* transform
* cast types
* enforce schema rules

---

# 🧠 SYSTEM THINKING CHECK

Evaluate whether this validator correctly serves as:

> the first enforcement gate for data completeness

Ask:

* Would bad donor records slip through?
* Would good records be incorrectly rejected?
* Is behavior deterministic across runs?

---

# 🧪 EDGE CASE VALIDATION

Confirm handling of:

* completely empty rows
* partially filled rows
* numeric vs string null inconsistencies
* mixed whitespace + NaN columns
* very large datasets (performance considerations)

---

# 📋 OUTPUT FORMAT

Return your review in this structure:

## 1. Executive Summary

* PASS / FAIL / PASS WITH RISKS

## 2. Critical Issues (if any)

* must-fix correctness problems

## 3. Data Integrity Risks

* subtle pipeline risks

## 4. Test Coverage Gaps

* missing or weak tests

## 5. Edge Case Findings

* unhandled scenarios

## 6. Final Verdict

* ready for T4-2 OR blocked

---

# 🧠 FINAL INSTRUCTION

This is a **data correctness gate**, not a code style review.

If this validator is wrong:

> every downstream analytics system becomes unreliable.

Be strict.
Be deterministic.
Be production-minded.

---

Begin review.

```

- **Summary of Response:**
    - Generated a strict production-grade QA review prompt for T4-1 missing-field validator focusing on data integrity, deterministic rejection logic, and safe classification of clean vs rejected rows, with emphasis on real-world ingestion reliability and edge-case handling.
- **Impact:**
    - Ensures validator correctness before advancing to downstream T4 stages
    - Protects pipeline integrity by enforcing strict data classification rules
    - Catches subtle production risks like NaN/whitespace misclassification and row leakage
    - Reinforces deterministic, test-driven validation behavior in early enforcement layer
---

### Prompt ID: P-041
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for strict data validation (TDD MVP ticket)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 

T4-2 - Type and value validators: 
Description 
DonationAmount must be numeric and > 0. 
DonationDate must be a valid date. 
State must be valid 2-letter US abbreviation. 
ZIP must be 5 digits. 

Acceptance criteria 
Trim BEFORE validation 
Amount = 0 → rejected 
Amount = "abc" → rejected 
State = "XX" → rejected 
ZIP = "1234" → rejected 
Valid date string parses correctly 

Test plan 
Parametrized tests for each rule, boundary cases (0 vs 0.01, 4-digit vs 5-digit ZIP).
```

- **Summary of Response:**
    - Produced a structured implementation prompt for Claude focused on strict TDD-driven     - validation logic
    - Defined explicit data validation rules for donation ingestion (amount, date, state, ZIP)
    - Emphasized preprocessing requirement (trim before validation) and clear reject conditions
    - Outlined parametrized test strategy with boundary cases for robust coverage
- **Impact:**
    - Formalized core data quality gate for ingestion pipeline
    - Established strict validation contract to prevent bad warehouse data
    - Reinforced test-driven development approach as a required implementation standard
---

### Prompt ID: P-042
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** T4-2 validation layer implementation (type + domain rules with TDD)
#### Prompt
```
# 🧠 Claude Code Prompt — T4-2 Type & Value Validators (Lead Data Engineer + MVP TDD)

You are acting as a **Lead Data Engineer** implementing:

> **T4-2 — Type and Value Validation Layer**

for the Donor Bureau Excel ingestion pipeline.

---

# 🎯 ROLE OF THIS STAGE (CRITICAL CONTEXT)

This is the **second enforcement gate** after T4-1 (null/missing validation).

Pipeline context:

text id="pipeline_flow"
parse → map → normalize → client_injection → T4-1 → T4-2 → T4-3 → enforce_schema → output

---

# ⚠️ STRICT CONSTRAINTS

This stage MUST:

* ❌ NOT handle missing field detection (T4-1 responsibility)
* ❌ NOT perform mapping
* ❌ NOT perform normalization (except trimming required for validation safety)
* ❌ NOT enforce schema structure
* ❌ NOT mutate business logic outside validation classification

It ONLY:

* validates type correctness
* validates domain rules
* classifies valid vs invalid rows
* appends rejection reasons

---

# 🎯 OBJECTIVE

Implement `validator.py` enhancements (or a dedicated function/module) that validates:

* DonationAmount
* DonationDate
* State
* Zip

and routes invalid rows into `rejected_df` with deterministic rejection reasons.

---

# 📋 INPUT EXPECTATIONS

You are receiving a DataFrame that has:

* already passed T4-1 (no null/empty required fields)
* already been mapped (canonical schema)
* already been normalized (basic casing/format rules applied)

---

# 🧪 VALIDATION RULES

## 1. DonationAmount

### Rules:

* must be numeric
* must be > 0

### Invalid cases:

* `"abc"` → reject
* `0` → reject
* negative values → reject

### Valid:

* `0.01`, `1`, `100.5`

---

## 2. DonationDate

### Rules:

* must be parseable into a valid date (pandas datetime or equivalent)
* must NOT be null (already enforced in T4-1, but still validate parseability)

### Valid formats:

* `MM/DD/YYYY`
* `YYYY-MM-DD`
* `March 16, 2025`
* Excel serial dates

### Invalid:

* `"not a date"`
* `"32/32/2025"`

---

## 3. State

### Rules:

* must be exactly 2-letter US state abbreviation
* must be uppercase after validation

### Invalid:

* `"XX"`
* `"NEW YORK"`
* `"Cali"`

---

## 4. ZIP

### Rules:

* must be a string of exactly 5 digits
* leading zeros MUST be preserved

### Invalid:

* `"1234"`
* `"123456"`
* `"12A45"`

---

# ⚠️ PRE-CONDITION: TRIMMING

Before validation:

* strip whitespace from all string inputs used in validation checks

Example:

* `" NY "` → `"NY"`

---

# 📤 OUTPUT CONTRACT

Return:

python id="output_contract"
clean_df
rejected_df

---

## rejected_df MUST include:

* rejection_reason column
* original row data intact
* no partial modification of valid fields

---

# 📌 REJECTION RULES

Each row may accumulate multiple errors.

### Format:

text id="error_format"
"Invalid Amount, Invalid State"

---

### Required messages:

| Field          | Message          |
| -------------- | ---------------- |
| DonationAmount | "Invalid Amount" |
| DonationDate   | "Invalid Date"   |
| State          | "Invalid State"  |
| Zip            | "Invalid Zip"    |

---

# 🧪 TEST-DRIVEN REQUIREMENTS

You MUST implement unit tests.

---

## 1. Amount Tests

* `"abc"` → rejected
* `0` → rejected
* `0.01` → accepted

---

## 2. Date Tests

* valid formats → accepted
* invalid strings → rejected

---

## 3. State Tests

* `"NY"` → valid
* `"XX"` → invalid

---

## 4. ZIP Tests

* `"12345"` → valid
* `"1234"` → invalid
* `"123456"` → invalid

---

## 5. Edge Case Tests

* boundary values
* mixed valid + invalid rows
* malformed numeric strings

---

# ⚙️ IMPLEMENTATION GUIDELINES

DO:

* use pandas-safe vectorized operations where possible
* ensure deterministic outputs
* avoid row-by-row loops unless absolutely necessary
* preserve input immutability

---

DO NOT:

* perform null checking (T4-1 responsibility)
* modify schema structure
* normalize casing beyond validation requirements
* change upstream transformations

---

# 🧠 SYSTEM ROLE CLARITY

This stage is:

> “data correctness enforcement (type + domain rules)”

NOT transformation.

---

# 🚨 COMMON PITFALLS

Avoid:

* treating empty strings again (already handled in T4-1)
* inconsistent date parsing behavior across formats
* ZIP coercion to int (DESTROYS leading zeros)
* state validation against non-normalized casing
* silent coercion of invalid values

---

# 📊 SUCCESS CRITERIA

This ticket is complete when:

* all invalid values correctly routed to rejected_df
* clean_df contains only valid records
* rejection reasons are deterministic and consistent
* all tests pass
* no mutation of input data occurs

---

# 🧠 FINAL NOTE

This layer ensures:

> downstream analytics only receive structurally valid and semantically meaningful donation records.

It is a **data quality enforcement gate**, not a transformation layer.

---

Begin implementation.

```

- **Summary of Response:**
    - Designed a strict T4-2 validation module separating clean vs rejected records
    - Implemented type + domain validation for DonationAmount, DonationDate, State, and ZIP using pandas-safe operations
    - Built deterministic rejection aggregation logic with standardized error messages
    - Added unit tests covering valid, invalid, and edge-case scenarios per field requirements
- **Impact:**
    - Established a robust data quality enforcement layer between normalization and schema enforcement
    - Ensured only validated, warehouse-safe donation records proceed downstream
    - Reinforced TDD-driven structure for future pipeline validation stages
---

### Prompt ID: P-043
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Production-grade QA review of T4-2 data validation layer
#### Prompt
```
# 🧠 Claude Code Prompt — T4-2 QA / Senior Test Engineer Review

You are acting as a **Senior QA Engineer + Lead Data Engineer reviewer**.

Your task is to perform a **strict production-grade review** of the implementation for:

> **T4-2 — Type and Value Validators**

This is a **critical data quality enforcement layer** in the Donor Bureau pipeline.

---

# 🎯 PRIMARY OBJECTIVE

Validate that the implementation correctly enforces:

* numeric + > 0 constraint for DonationAmount
* robust date parsing for DonationDate
* strict 2-letter US state validation
* strict 5-digit ZIP validation (with leading zero preservation)
* correct routing into clean_df vs rejected_df

---

# ⚠️ REVIEW CONTEXT

Pipeline stage:

text id="pipeline_flow"
parse → map → normalize → T4-1 → T4-2 → T4-3 → enforce_schema → output

You are reviewing a system that has already passed:

* mapping
* normalization
* null/empty validation (T4-1)

So **DO NOT expect missing-field handling here**.

---

# 🧪 CORE VALIDATION CHECKS

## 1. DonationAmount

Verify:

* numeric validation is correct
* rejects `"abc"`
* rejects `0`
* rejects negative values
* accepts `0.01`, `1`, `100.5`

🚨 Watch for:

* accidental string coercion
* pandas silent conversion to NaN
* float comparison errors

---

## 2. DonationDate

Verify:

* robust parsing across formats:

  * MM/DD/YYYY
  * YYYY-MM-DD
  * natural language dates
  * Excel serial dates

* invalid dates properly rejected

🚨 Watch for:

* inconsistent datetime parsing across rows
* silent coercion to NaT without capture
* timezone artifacts (if present)

---

## 3. State Validation

Verify:

* only valid 2-letter US state codes accepted
* must be uppercase comparison-safe

Reject:

* `"XX"`
* `"New York"`
* `"california"`

🚨 Watch for:

* missing normalization assumption (should already be normalized upstream)
* accidental partial matches

---

## 4. ZIP Validation

Verify:

* exactly 5 digits
* must remain string
* leading zeros preserved

Reject:

* `"1234"`
* `"123456"`
* `"12A45"`

🚨 CRITICAL FAILURE MODE:

* ZIP converted to int → destroys leading zeros

---

# 📤 OUTPUT INTEGRITY CHECK

Ensure:

* clean_df contains ONLY valid rows
* rejected_df contains ONLY invalid rows
* NO row appears in both
* NO row is dropped silently

---

# 📌 REJECTION LOGIC REVIEW

Check:

* rejection_reason exists in rejected_df
* reasons are deterministic and consistent

Expected format:

text id="reason_format"
"Invalid Amount, Invalid State"

Verify:

* ordering is stable
* duplicates are not repeated
* formatting is consistent

---

# 🧪 TEST COVERAGE REVIEW

Confirm existence of:

## Amount tests

* "abc" → reject
* 0 → reject
* 0.01 → accept

## Date tests

* valid formats → accept
* invalid formats → reject

## State tests

* "NY" → accept
* "XX" → reject

## ZIP tests

* "12345" → accept
* "1234" → reject
* "123456" → reject

## Edge cases

* mixed valid/invalid rows
* boundary numeric values
* malformed numeric strings

---

# 🚨 RED FLAGS (FAIL REVIEW IF PRESENT)

Immediately fail or flag if:

* ZIP cast to int anywhere
* date parsing inconsistencies between rows
* silent NaT or NaN propagation without explicit handling
* inconsistent rejection_reason formatting
* row mutation instead of classification
* missing vectorization where required
* reuse of T4-1 logic incorrectly (duplicate validation layers)

---

# 📊 PERFORMANCE & SAFETY REVIEW

Check:

* unnecessary row-wise iteration (iterrows)
* pandas inefficiency on large datasets
* accidental DataFrame mutation across stages
* correct use of copies vs views

---

# 🧠 SYSTEM INTEGRITY CHECK

Evaluate:

* Can invalid data still slip through into clean_df?
* Are valid rows ever incorrectly rejected?
* Is behavior deterministic across runs?

---

# 📋 OUTPUT FORMAT

Return:

## 1. Executive Summary

PASS / FAIL / PASS WITH RISKS

## 2. Critical Issues

* correctness-breaking bugs

## 3. Data Integrity Risks

* subtle pipeline risks

## 4. Test Coverage Gaps

* missing or weak tests

## 5. Edge Cases Missed

* unhandled real-world scenarios

## 6. Final Verdict

* READY FOR T4-3 OR BLOCKED

---

# 🧠 FINAL INSTRUCTION

This is a **data correctness enforcement review**, not a style review.

If this layer is wrong:

> downstream analytics will silently ingest invalid financial donation data.

Be strict.
Be deterministic.
Be production-focused.

---

Begin review.

```

- **Summary of Response:**
    - Defined a strict QA review prompt for validating T4-2 data validation logic in a    - production-style pipeline
    - Focused on correctness of numeric, date, state, and ZIP validation rules
    - Included explicit failure conditions, edge cases, and data integrity checks
    - Required structured QA output with PASS/FAIL decisioning and risk analysis
- **Impact:**
    - Established a rigorous QA gate for data quality enforcement before downstream processing
    - Ensures validation layer reliability for financial donation ingestion pipeline
    - Sets standard for production-grade reviewer prompts used in multi-stage ETL system testing
---

### Prompt ID: P-044
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for row splitting logic
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T4-3 - Row splitter (clean / rejected):

Description
After all validation rules run, split df into clean_df and rejected_df. Rejected df includes original data + rejection_reason column.

Acceptance criteria
clean_df has zero null values in any schema field
clean_df + rejected_df row count = original row count
rejected_df.rejection_reason is never empty
Test plan
Integration test: mixed input file, verify counts and no leakage between dfs.
```


- **Summary of Response:**

- **Impact:**

### Prompt ID: P-045
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Row splitting logic for clean vs rejected datasets
#### Prompt
```
# 🧠 Claude Code Prompt — T4-3 Row Splitter (Clean / Rejected)

## Lead Data Engineer + MVP Test-Driven Implementation (Final)

You are acting as a **Lead Data Engineer** implementing:

> **T4-3 — Row Splitter (Clean vs Rejected Separation)**

for the Donor Bureau Excel ingestion pipeline.

---

# 🎯 ROLE IN PIPELINE (CRITICAL CONTEXT)

This is the **final stage of the validation layer**.

Pipeline:

parse → map → normalize → T4-1 → T4-2 → T4-3 → enforce_schema → output

At this point:

* all validation logic has already run
* rows already contain `rejection_reason` if invalid

Your job is to:

> deterministically partition rows into clean_df and rejected_df

---

# ⚠️ STRICT CONSTRAINTS (NON-NEGOTIABLE)

You MUST NOT:

* ❌ perform any validation logic
* ❌ recompute rejection_reason
* ❌ modify row values
* ❌ alter schema columns
* ❌ drop rows

You MUST ONLY:

* split rows based on existing validation results
* preserve data integrity 100%

---

# 🎯 CORE OBJECTIVE

Implement a function (e.g. in `validator.py` or `splitter.py`):

def split_rows(df):
    return clean_df, rejected_df

---

# 📌 SPLITTING LOGIC (SOURCE OF TRUTH)

## A row is:

### ✅ CLEAN IF:

* `rejection_reason` is:

  * NaN OR
  * empty string "" OR
  * whitespace-only

---

### ❌ REJECTED IF:

* `rejection_reason` contains ANY non-empty value

---

# ⚠️ IMPORTANT DETAIL

You MUST treat:

NaN == empty == whitespace-only

as **clean condition**

and anything else as rejected.

---

# 📤 OUTPUT CONTRACT

## clean_df

* contains ONLY valid rows
* MUST NOT include `rejection_reason` column (drop it explicitly)
* MUST have zero nulls in required schema fields

---

## rejected_df

* contains ONLY invalid rows
* MUST include `rejection_reason`
* MUST preserve all original columns

---

# 📋 ACCEPTANCE CRITERIA (STRICT)

## 1. Row Conservation (MANDATORY)

python
len(clean_df) + len(rejected_df) == len(df)

🚨 FAIL if violated

---

## 2. No Leakage

* no row appears in both outputs
* no row is lost

---

## 3. Clean Data Guarantee

* clean_df has:

  * NO null values in required fields
  * NO rejection_reason column

---

## 4. Rejected Data Guarantee

* rejected_df:

  * ALWAYS has rejection_reason
  * rejection_reason is never null/empty

---

# 🧪 TEST-DRIVEN REQUIREMENTS

You MUST implement integration tests.

---

## 1. Mixed Dataset (PRIMARY TEST)

Input:

* some valid rows
* some rejected rows

Expected:

* correct split
* correct counts
* no overlap

---

## 2. All Clean Dataset

Expected:

* rejected_df empty
* clean_df == input (minus rejection_reason)

---

## 3. All Rejected Dataset

Expected:

* clean_df empty
* rejected_df == input

---

## 4. Edge Case — Single Row

* correctly classified
* no indexing issues

---

## 5. Edge Case — Whitespace rejection_reason

* treated as CLEAN

---

# ⚙️ IMPLEMENTATION GUIDELINES

DO:

* use vectorized pandas filtering
* use boolean masks
* explicitly call `.copy()` when splitting
* explicitly drop rejection_reason from clean_df

---

DO NOT:

* use iterrows
* mutate input DataFrame
* rely on implicit pandas behavior
* perform string operations without null safety

---

# 🚨 COMMON FAILURE MODES TO AVOID

* treating "" differently than NaN
* forgetting whitespace-only case
* using `.isna()` without `.str.strip()` check
* accidental overlap between clean/rejected
* missing `.copy()` → downstream mutation bugs
* leaking rejection_reason into clean_df

---

# 🧠 DESIGN PRINCIPLE

This stage enforces:

> “Every row is accounted for — either usable or explicitly rejected.”

---

# 📊 VALIDATION CHECKS (MANDATORY BEFORE COMPLETE)

You MUST confirm:

* total rows preserved exactly
* no overlap between outputs
* rejected_df.rejection_reason fully populated
* clean_df contains only valid rows

---

# 🚫 DO NOT

* re-run validation rules
* modify T4-1 or T4-2 outputs
* enforce schema (T5 responsibility)
* introduce new business logic

---

# 🧠 SUCCESS CRITERIA

This ticket is complete when:

* split logic is deterministic and correct
* all integration tests pass
* zero row leakage exists
* pipeline behavior remains stable

---

# 🧠 FINAL NOTE

This is a **data integrity boundary**.

If implemented incorrectly:

> rows will be lost, duplicated, or misclassified — breaking trust in the system.

---

Begin implementation.

```

- **Summary of Response:**
    - Defined strict separation logic based solely on rejection_reason
    - Enforced non-mutating, deterministic data partitioning using pandas
    - Introduced comprehensive integration test coverage including edge cases
    - Emphasized data integrity guarantees (no loss, no overlap, full accountability)
- **Impact:**
    - Established a critical pipeline boundary ensuring trust in downstream data
    - Eliminated ambiguity in how valid vs invalid rows are handled
    - Provided a testable, production-safe contract for dataset splitting
    - Reduced risk of silent data corruption or leakage in ingestion pipeline
---

### Prompt ID: P-046
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA audit for row splitting logic (clean vs rejected datasets)
#### Prompt
```
# 🧠 Claude Code Prompt — T4-3 QA / Senior Test Engineer Review (Final)

You are acting as a **Senior QA Engineer + Lead Data Engineer reviewer**.

Your task is to perform a **strict, production-level audit** of:

> **T4-3 — Row Splitter (Clean vs Rejected Separation)**

This is a **data integrity boundary** in the Donor Bureau pipeline.

---

# 🎯 PRIMARY OBJECTIVE

Ensure the implementation:

* correctly partitions rows into clean_df and rejected_df
* preserves ALL input rows (no loss, no duplication)
* interprets `rejection_reason` deterministically
* does NOT mutate input data
* enforces strict separation with zero leakage

---

# ⚠️ PIPELINE CONTEXT

parse → map → normalize → T4-1 → T4-2 → T4-3 → enforce_schema → output

At this stage:

* validation has already been completed
* `rejection_reason` already exists (if row is invalid)

This stage MUST ONLY split — nothing else.

---

# 🧪 CORE VALIDATION CHECKS

## 1. Row Conservation (CRITICAL)

You MUST verify:

len(clean_df) + len(rejected_df) == len(input_df)

🚨 If this fails → **FAIL REVIEW IMMEDIATELY**

---

## 2. No Row Leakage

Confirm:

* no row appears in BOTH outputs
* no row is missing from BOTH outputs

Check:

* index overlap
* duplicated rows
* incorrect boolean masks

---

## 3. Clean Data Integrity

Verify:

* clean_df contains ONLY rows where:

  * `rejection_reason` is null, empty, or whitespace-only

* clean_df:

  * has NO nulls in required fields
  * does NOT include `rejection_reason` column

🚨 Watch for:

* whitespace `"   "` slipping through incorrectly
* rejection_reason not dropped

---

## 4. Rejected Data Integrity

Verify:

* rejected_df contains ALL invalid rows
* rejected_df includes `rejection_reason`
* rejection_reason is NEVER:

  * null
  * empty
  * whitespace-only

---

## 5. Deterministic Behavior

Ensure:

* same input → same outputs every run
* no randomness or ordering dependency
* boolean masks are stable and explicit

---

# ⚠️ CRITICAL EDGE CASES

You MUST confirm correct handling of:

## Whitespace Case

rejection_reason = "   "

→ MUST be treated as CLEAN

---

## NaN Case

rejection_reason = NaN

→ MUST be treated as CLEAN

---

## Mixed Case

* mix of valid + invalid rows
* counts must match exactly

---

## Single Row Dataset

* correctly classified
* no indexing issues

---

# 🚨 COMMON FAILURE MODES (HIGH PRIORITY)

Flag immediately if present:

* using `.isna()` without handling empty string
* using `.str.strip()` without null safety
* treating empty string differently than NaN
* forgetting `.copy()` → mutation side effects
* incorrect boolean masks causing overlap
* rejection_reason leaking into clean_df
* dropping rows instead of splitting

---

# 🧪 TEST COVERAGE REVIEW

Ensure tests exist for:

## 1. Mixed Dataset (REQUIRED)

* both clean and rejected rows
* verify counts + no leakage

## 2. All Clean Dataset

* rejected_df empty
* clean_df == full dataset

## 3. All Rejected Dataset

* clean_df empty
* rejected_df == full dataset

## 4. Whitespace Edge Case

* `"   "` treated as CLEAN

## 5. Single Row Case

* no indexing issues

---

# 📊 DATA INTEGRITY AUDIT

Verify:

* total rows preserved exactly
* no duplicates introduced
* no rows silently dropped
* no mutation of original DataFrame

---

# 🧠 SYSTEM ROLE VALIDATION

Confirm this module behaves strictly as:

> “deterministic partitioning layer”

NOT:

* validation logic
* transformation logic
* enrichment logic

---

# 🚫 FAIL CONDITIONS

Immediately FAIL review if:

* row count mismatch
* any overlap between clean/rejected
* rejection_reason incorrectly interpreted
* mutation of input data
* missing `.copy()` safeguards
* inconsistent filtering logic

---

# 📋 OUTPUT FORMAT

Return:

## 1. Executive Summary

PASS / FAIL / PASS WITH RISKS

## 2. Critical Issues

(data integrity or correctness bugs)

## 3. Data Integrity Risks

(subtle pipeline risks)

## 4. Test Coverage Gaps

(missing or weak tests)

## 5. Edge Cases Missed

(real-world failure scenarios)

## 6. Final Verdict

READY FOR T4-4 OR BLOCKED

---

# 🧠 FINAL INSTRUCTION

This is NOT a style review.

This is a **data integrity audit**.

If this layer is wrong:

> rows will be lost, duplicated, or misclassified — breaking trust in the entire system.

Be strict.
Be deterministic.
Think like production.

---

Begin review.

```

- **Summary of Response:**
    - Enforced a strict QA audit framework focused on row conservation, deterministic splitting, and zero data leakage
    - Defined critical validation checks, edge cases (NaN, whitespace), and failure conditions
    - Required comprehensive test coverage across mixed, clean-only, rejected-only, and edge scenarios
    - Positioned T4-3 as a pure partitioning layer with no transformation or validation responsibilities
- **Impact:**
    - Elevated T4-3 to a high-risk data integrity checkpoint with explicit pass/fail criteria
    - Established rigorous QA standards that prevent silent data loss or misclassification
    - Provided a reusable audit template for validating downstream pipeline stages
---

### Prompt ID: P-047
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude prompt for system-level error handling implementation
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T4-4 - System-level error handling:

Description
Implement centralized error handling for non-row-level failures across the pipeline. Capture and handle exceptions during file upload, parsing, sheet processing, and configuration loading.

Ensure the system:

Fails gracefully for invalid inputs or system issues
Returns structured API error responses
Clearly distinguishes between:
System errors (fail request)
Validation failures (return 200 with rejected rows)

Acceptance Criteria
Corrupted or unreadable .xlsx file → 400 response with descriptive error message
Unsupported file type or malformed structure → 400 response with clear reason
Missing or invalid mapping.json → application fails at startup with explicit error
Unexpected/unhandled exceptions → 500 response with generic error message (no stack trace exposed)
Validation failures (row-level issues) DO NOT trigger 400/500:
Request returns 200
Rejected rows are included in output as designed
All system-level errors are logged with:
file name (if available)
pipeline stage (upload, parse, transform, etc.)
error type/message

Assumptions
All pipeline components (parser, transformer, validator) raise structured exceptions
Central handler (e.g., FastAPI exception middleware) is used to intercept errors
Console logging is sufficient for MVP
No sensitive data masking required for MVP

Test Plan
Unit test: corrupted file input → assert 400 response with structured error
Unit test: invalid/missing mapping config → assert startup failure
Integration test: force parser failure → assert 400 response and correct error structure
Integration test: validation failures only → assert 200 response with rejected_rows > 0
Manual test: upload malformed Excel file → verify error message clarity and log output
```

- **Summary of Response:**
    - Generated a structured Claude prompt aligning with MVP and TDD principles
    - Emphasized centralized error handling via middleware (e.g., FastAPI)
    - Clearly defined separation between system-level errors and row-level validation failures
    - Incorporated detailed acceptance criteria and test cases into implementation instructions
- **Impact:**
    - Standardized how errors are handled across the entire pipeline
    - Prevented incorrect failure states for validation-only issues
    - Improved system reliability and debuggability through structured logging and responses
    - Provided clear implementation guidance for consistent backend behavior
---

### Prompt ID: P-048
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** System-level error handling implementation
#### Prompt
```
# 🧠 Claude Code Prompt — T4-4 System-Level Error Handling

## Lead Data Engineer Implementation (MVP, Test-Driven, Production-Oriented)

You are acting as a **Lead Data Engineer** implementing:

> **T4-4 — System-Level Error Handling**

for the Donor Bureau Excel ingestion pipeline.

This is a **production-critical layer** that defines how the system behaves under failure.

---

# 🎯 PRIMARY OBJECTIVE

Implement **centralized, deterministic error handling** that:

* gracefully handles system-level failures
* returns structured API responses
* distinguishes clearly between:

  * ✅ **Validation failures (row-level)** → HTTP 200
  * ❌ **System failures (pipeline/runtime)** → HTTP 400 / 500

---

# ⚠️ CORE PRINCIPLE (NON-NEGOTIABLE)

> **Row-level failures are NOT system failures.**

| Scenario                   | Response                 |
| -------------------------- | ------------------------ |
| Invalid rows               | 200 (with rejected_rows) |
| Bad file / broken pipeline | 400 or 500               |

---

# 🧠 ERROR CATEGORIES (SOURCE OF TRUTH)

You MUST classify errors into:

---

## 1. Client Errors → HTTP 400

These are **bad inputs**:

* corrupted / unreadable `.xlsx`
* invalid file type
* malformed workbook structure
* parser cannot process file

---

## 2. System Errors → HTTP 500

These are **unexpected failures**:

* unhandled exceptions
* code bugs
* runtime failures in pipeline stages

---

## 3. Validation Outcomes → HTTP 200

These are **expected pipeline results**:

* rows fail validation (T4-1 / T4-2)
* rejected rows returned in output

🚨 MUST NOT raise exceptions

---

# 🏗️ REQUIRED ARCHITECTURE

## 1. Central Exception Type (REQUIRED)

You already have `PipelineError`.

Ensure it includes:

class PipelineError(Exception):
    def __init__(self, stage: str, error_type: str, message: str):
        self.stage = stage
        self.error_type = error_type
        self.message = message

---

## 2. Exception Raising (Pipeline Layer)

Each stage MUST raise:

raise PipelineError(
    stage="parse",
    error_type="InvalidFile",
    message="Unable to read Excel file"
)

🚨 NO raw exceptions should escape pipeline

---

## 3. FastAPI Exception Handler (REQUIRED)

Implement centralized handler:

@app.exception_handler(PipelineError)
async def pipeline_error_handler(request, exc):

---

## 4. Generic Exception Handler (REQUIRED)

Catch all unexpected failures:

@app.exception_handler(Exception)

---

# 📤 API RESPONSE CONTRACT

## 400 Response (Client Error)

{
  "error": {
    "type": "InvalidFile",
    "stage": "parse",
    "message": "Unable to read Excel file"
  }
}

---

## 500 Response (System Error)

{
  "error": {
    "type": "InternalServerError",
    "stage": "unknown",
    "message": "An unexpected error occurred"
  }
}

🚨 DO NOT expose stack traces

---

## 200 Response (Validation Outcome)

{
  "total_rows": 100,
  "clean_rows": 80,
  "rejected_rows": 20,
  "clean_file": "...",
  "rejected_file": "..."
}

---

# 🧪 TEST-DRIVEN REQUIREMENTS

---

## 1. Corrupted File Test (REQUIRED)

* upload broken `.xlsx`
* expect:

  * HTTP 400
  * structured error response
  * correct stage = "parse"

---

## 2. Invalid File Type Test

* upload `.csv`
* expect:

  * HTTP 400
  * descriptive error

---

## 3. Mapping Config Failure Test

* simulate missing or invalid `mapping.json`
* expect:

  * app fails at startup
  * clear error message

---

## 4. Forced Parser Failure (Integration)

* mock parser to raise PipelineError
* expect:

  * HTTP 400
  * correct structure

---

## 5. Unexpected Exception Test

* raise generic Exception inside pipeline
* expect:

  * HTTP 500
  * safe message (no stack trace)

---

## 6. Validation-Only Failure Test

* valid file, invalid rows
* expect:

  * HTTP 200
  * rejected_rows > 0
  * no exception raised

---

# 📊 LOGGING REQUIREMENTS (MVP)

You MUST log:

* file name (if available)
* pipeline stage
* error_type
* message

Example:

[ERROR] file=donations.xlsx stage=parse type=InvalidFile msg="Unable to read Excel file"

---

# ⚙️ IMPLEMENTATION GUIDELINES

DO:

* use structured exceptions everywhere
* wrap external library errors (openpyxl, pandas)
* use FastAPI exception middleware
* keep responses consistent

---

DO NOT:

* leak stack traces
* mix validation logic into error handling
* return raw Python exceptions
* silently swallow errors

---

# 🚨 CRITICAL FAILURE MODES

Immediately FAIL if:

* validation errors return 400/500
* stack traces appear in API response
* exceptions bypass handler
* inconsistent response schemas
* missing stage/error_type in response

---

# 🧠 DESIGN PRINCIPLE

This layer ensures:

> “Every failure is understandable, traceable, and correctly classified.”

---

# 📋 COMPLETION CHECKLIST

Before finishing, confirm:

* PipelineError used consistently
* FastAPI handlers implemented
* All error scenarios tested
* Logging present and readable
* No stack traces exposed
* Validation vs system errors clearly separated

---

# 🧠 FINAL NOTE

This is what makes your pipeline:

* **debuggable**
* **trustworthy**
* **production-ready**

Without this layer:

> failures become invisible, confusing, and dangerous.

---

Begin implementation.

```

- **Summary of Response:**
    - Defined centralized error handling using a custom PipelineError class across all pipeline stages
    - Implemented FastAPI exception handlers for both controlled (400) and unexpected (500) errors
    - Established strict API response schemas separating validation outcomes (200) from system failures
    - Introduced comprehensive test coverage and logging requirements for all failure scenarios
- **Impact:**
    - Standardized how all failures are classified, surfaced, and logged across the pipeline
    - Prevented misclassification of validation errors as system failures, preserving API contract integrity
    - Improved debuggability and production readiness through structured responses and logging
    - Created a clear foundation for reliable error handling in downstream features and future scaling
---

### Prompt ID: P-049
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** System-level error handling QA audit (T4-4)
#### Prompt
```
# 🧠 Claude Code Prompt — T4-4 QA / Senior Test Engineer Review

## System-Level Error Handling (Production Audit)

You are acting as a **Senior QA Engineer + Lead Data Engineer reviewer**.

Your task is to perform a **strict, production-grade audit** of:

> **T4-4 — System-Level Error Handling**

This is a **critical reliability layer** that determines how the system behaves under failure.

---

# 🎯 PRIMARY OBJECTIVE

Verify that the system:

* correctly classifies errors (400 vs 500 vs 200)
* returns **consistent, structured API responses**
* does NOT leak internal implementation details
* cleanly separates **validation outcomes vs system failures**
* logs all failures with actionable context

---

# ⚠️ PIPELINE CONTEXT

upload → parse → map → normalize → validate → split → output

At this layer:

* failures are **non-row-level only**
* row-level validation MUST NOT raise exceptions

---

# 🧠 CORE RULE (NON-NEGOTIABLE)

> Validation failures → HTTP 200
> System failures → HTTP 400 / 500

🚨 If violated → FAIL immediately

---

# 🧪 CRITICAL VALIDATION CHECKS

---

## 1. Error Classification (HIGH PRIORITY)

Verify correct mapping:

| Scenario             | Expected        |
| -------------------- | --------------- |
| Corrupted `.xlsx`    | 400             |
| Invalid file type    | 400             |
| Parser failure       | 400             |
| Missing mapping.json | startup failure |
| Unexpected exception | 500             |
| Validation failures  | 200             |

🚨 FAIL if any misclassified

---

## 2. API Response Structure

### 400 / 500 responses MUST follow:

{
  "error": {
    "type": "...",
    "stage": "...",
    "message": "..."
  }
}

Verify:

* `type` present and meaningful
* `stage` present and accurate
* `message` clear and user-safe

---

## 3. NO STACK TRACE LEAKAGE (CRITICAL)

Confirm:

* no Python tracebacks in API responses
* no internal file paths exposed
* no raw exception strings returned

🚨 Any leakage → FAIL

---

## 4. Validation vs System Separation

Verify:

* validation failures (bad rows):

  * DO NOT raise exceptions
  * return 200
  * produce rejected rows

* system failures:

  * DO raise exceptions
  * handled centrally

---

## 5. PipelineError Usage

Confirm:

* all expected failures use PipelineError
* structure includes:

  * stage
  * error_type
  * message

Verify no raw exceptions escape pipeline layers.

---

## 6. FastAPI Exception Handlers

Ensure:

### a. PipelineError handler exists

* returns 400
* structured response
* correct mapping of fields

---

### b. Generic Exception handler exists

* returns 500
* safe message
* no internal details

---

## 7. Logging Audit (MVP)

Verify logs include:

* file name (if available)
* stage
* error_type
* message

Example:

[ERROR] file=donations.xlsx stage=parse type=InvalidFile msg="Unable to read Excel file"

🚨 Missing logging → HIGH RISK

---

# ⚠️ EDGE CASE TESTING

Ensure tests cover:

---

## 1. Corrupted File

* unreadable Excel
* expect 400 + structured error

---

## 2. Invalid File Type

* `.csv` upload
* expect 400

---

## 3. Forced Parser Failure

* simulate PipelineError
* verify:

  * 400 response
  * correct stage

---

## 4. Unexpected Exception

* force generic Exception
* expect:

  * 500
  * safe message

---

## 5. Validation-Only Failure

* bad rows
* expect:

  * 200
  * rejected_rows > 0
  * NO exception

---

## 6. Missing Config (Startup)

* mapping.json missing/invalid
* expect:

  * app fails to start
  * explicit error

---

# 🚨 COMMON FAILURE MODES

Flag immediately if present:

* validation errors returning 400/500
* raw exceptions leaking
* inconsistent response schema
* missing stage in error
* missing error_type
* logging absent or incomplete
* exception bypassing handler
* mixing validation logic into error handling

---

# 📊 INTEGRATION BEHAVIOR

Verify:

* upload endpoint properly surfaces pipeline errors
* pipeline errors propagate cleanly
* no silent failures
* consistent responses across all endpoints

---

# 🧠 DESIGN VALIDATION

Confirm this layer enforces:

> “All failures are visible, classified, and actionable.”

NOT:

* hidden
* ambiguous
* inconsistent

---

# 🚫 FAIL CONDITIONS

Immediately FAIL if:

* stack trace appears in API response
* incorrect HTTP status codes
* validation failures treated as system errors
* missing structured error response
* unhandled exceptions crash server

---

# 📋 OUTPUT FORMAT

Return:

## 1. Executive Summary

PASS / FAIL / PASS WITH RISKS

## 2. Critical Issues

(break correctness or safety)

## 3. Reliability Risks

(logging gaps, edge-case failures)

## 4. Test Coverage Gaps

## 5. Edge Cases Missed

## 6. Final Verdict

READY FOR T5 OR BLOCKED

---

# 🧠 FINAL INSTRUCTION

This is NOT a style review.

This is a **production reliability audit**.

If this layer fails:

> debugging becomes impossible and user trust collapses.

Be strict.
Be skeptical.
Think like production.

---

Begin review.

```

- **Summary of Response:**
    - Defines a strict QA audit framework for system-level error handling across the pipeline
    - Enforces clear separation between validation errors (200) and system failures (400/500)
    - Establishes standardized API error response schema and PipelineError usage
    - Introduces comprehensive edge case testing and logging requirements for production reliability
- **Impact:**
    - Formalizes error handling as a critical production reliability layer
    - Sets non-negotiable standards for API consistency, safety, and observability
    - Ensures downstream debugging and user trust through structured failure handling
    - Acts as a gatekeeper before progressing to T5, preventing fragile system behavior
---

### Prompt ID: P-050
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate QA checkpoint review prompt for Claude
#### Prompt
```
ok now that we've completed up to E4 - Validation Engine-  
please generate a prompt to Claude to do a checkpoint review of all the code as it stands, 
and also take into consideration the input_contract, fixtures, testing, MVP 
as a lead senior QA / Data Engineer
```

- **Summary of Response:**
    - Generated a structured prompt directing Claude to act as a senior QA / Data Engineer
    - Emphasized review of validation logic, input contracts, fixtures, and test coverage
    - Included focus on MVP alignment and production readiness
    - Encouraged identification of gaps, edge cases, and improvement recommendations
- **Impact:**
    - Enabled a formal quality checkpoint before proceeding further in development
    - Helped ensure alignment between implementation and defined data contracts/testing strategy
    - Increased confidence in system reliability and readiness for next build phase
---

### Prompt ID: P-051
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Full MVP pipeline checkpoint audit (E1–E4)
#### Prompt
```
# 🧠 Claude Code Prompt — E4 Checkpoint Review

## Senior QA Engineer + Lead Data Engineer System Audit (MVP Gate)

You are acting as a **Senior QA Engineer + Lead Data Engineer** performing a **full checkpoint audit** of the Donor Bureau pipeline after completion of:

> ✅ E1 — Ingestion (Upload)
> ✅ E2 — File Processing (Parser)
> ✅ E3 — Data Transformation (Mapping, Normalization, Client Injection, Orchestration)
> ✅ E4 — Validation Engine (T4-1 → T4-4)

---

# 🎯 PRIMARY OBJECTIVE

Determine whether the system is:

> **Production-ready at MVP level OR blocked by critical risks**

You must evaluate the **entire codebase holistically**, not just individual modules.

---

# 🧠 SYSTEM CONTEXT

### Pipeline:

upload → parse → map → normalize → client → validate (T4-1, T4-2) → split → error handling → (T5 next)

### Output Goal:

A **clean, deterministic CSV** + **rejected rows CSV**

---

# ⚠️ REVIEW SCOPE (MANDATORY)

You MUST evaluate:

---

## 1. 🧱 Architecture Integrity

* Are stage boundaries clean and enforced?
* Any leakage of responsibilities?

  * validation in parser?
  * transformation in validator?
  * logic inside orchestrator?
* Is pipeline orchestration deterministic and strict?

---

## 2. 📄 Input Contract Alignment

Cross-check **code vs `input_contract.md`**:

* Header detection logic matches contract?
* Alias mapping matches documented aliases?
* Metadata row behavior correct?
* Sheet → Client derivation enforced?
* Any drift between contract and implementation?

🚨 Flag ANY contract/code mismatch

---

## 3. 🧪 Fixture Strategy & Readiness

Evaluate against:

* `fixture_validation.md`
* T7-1 expectations

Determine:

* Are we violating the rule:

  > “No T2–T4 logic before fixture validation”?

* Are current tests:

  * synthetic only?
  * or representative of real-world formats?

🚨 Identify:

* Missing fixture coverage
* False confidence risks

---

## 4. 🧪 Test Coverage (CRITICAL)

Audit all tests:

### Required Coverage Areas

#### Ingestion

* file type validation
* empty file handling

#### Parser

* multi-sheet handling
* header offset detection
* metadata rows
* no-header sheets
* Instructions/non-data sheets

#### Mapping

* alias coverage
* case insensitivity
* missing fields behavior

#### Normalization

* date parsing (multiple formats + Excel serial)
* ZIP preservation
* whitespace handling

#### Client Injection

* multi-sheet correctness
* whitespace trimming

#### Validation (T4)

* null/missing fields
* type/value validation
* edge cases (ZIP, state, amount, date)
* row splitting integrity

#### Error Handling

* 400 vs 500 vs 200 separation
* structured API responses
* no stack trace leakage

---

## 5. 📊 Data Integrity Guarantees

You MUST verify:

* No row loss across pipeline
* No duplication introduced
* Deterministic outputs (same input → same output)
* Clean/rejected split correctness

🚨 This is the highest priority

---

## 6. ⚠️ Validation Engine Audit (E4)

Deeply evaluate:

### T4-1 / T4-2

* vectorized vs row-wise logic
* correctness of rules
* trimming BEFORE validation
* combined rejection_reason logic

### T4-3

* row conservation
* no leakage
* whitespace/null handling correctness

### T4-4

* correct HTTP classification
* structured responses
* logging completeness
* no stack traces

---

## 7. 🔥 Error Handling & Observability

* Are all errors:

  * classified?
  * logged?
  * traceable?

* Can a developer debug failures easily?

* Any silent failures?

---

## 8. ⚙️ MVP Scope Discipline

You MUST assess:

* Is anything over-engineered?
* Is anything missing that blocks MVP?

MVP definition:

> Upload Excel → get clean CSV + rejected CSV reliably

---

## 9. 📉 Risks & Technical Debt

Identify:

### 🔴 Critical Risks

* break correctness or data integrity

### 🟡 Medium Risks

* scalability, performance, maintainability

### 🟢 Minor Issues

* cleanup, polish

---

## 10. 🔗 Stage Integration

Verify:

* stages connect correctly
* data contracts between stages are respected
* no schema drift between stages

---

# 🚨 SPECIAL FOCUS AREAS

You MUST explicitly check:

* alias drift (mapping.json vs contract)
* metadata-row handling end-to-end
* multi-sheet + multi-client behavior
* Instructions/non-data sheet exclusion
* validation vs system error separation

---

# 📋 OUTPUT FORMAT (STRICT)

Return:

---

## 1. 🧠 Executive Summary

PASS / FAIL / PASS WITH RISKS

---

## 2. 🔴 Critical Issues

(must fix before T5)

---

## 3. 🟡 Medium Risks

(should fix soon)

---

## 4. 🟢 Minor Issues

(cleanup)

---

## 5. 🧪 Test Coverage Gaps

---

## 6. 📄 Contract vs Code Drift

---

## 7. ⚙️ MVP Readiness Assessment

Is system ready for:

> T5 — Output Generation (CSV writing + download)?

---

## 8. 🧠 Final Verdict

One of:

* ✅ READY FOR T5
* ⚠️ READY WITH MINOR FIXES
* ❌ BLOCKED

---

# 🧠 FINAL INSTRUCTION

This is NOT a casual review.

This is a **production checkpoint audit**.

Think like:

* a data engineer responsible for data correctness
* a QA engineer responsible for failure detection
* a hiring manager reviewing this project

---

If this system fails:

> data trust is broken, and the pipeline is not usable.

Be strict.
Be skeptical.
Think in edge cases.

---

Begin full system audit.

```

- **Summary of Response:**
    - Defined a comprehensive QA audit framework covering architecture, validation, contracts, and data integrity
    - Enforced strict MVP readiness criteria with PASS/FAIL gating and risk classification
    - Introduced deep validation of test coverage, fixture realism, and contract/code alignment
    - Emphasized deterministic outputs and zero data loss as top priorities
- **Impact:**
    - Established a formal production checkpoint before proceeding to T5 (CSV output)
    - Elevated quality bar from feature completion to system reliability and trustworthiness
    - Identified audit structure that can be reused for future pipeline stages and reviews
---

### Prompt ID: P-052
- **Author:** Mark
- **Target:** Claude
- **Purpose:** Generate QA checkpoint review report documentation
#### Prompt
```
ok now please as a senior level project manager / QA 
generate a report on the approach and results of the checkpoint review in .md format 
to be included in the docs/checkpoints/*.md of the repo
```

- **Summary of Response:**
    - Produced a structured markdown report for checkpoint review documentation
    - Included sections for review scope, methodology, findings, and results
    - Summarized validation of implemented features against acceptance criteria
    - Highlighted any gaps, risks, or areas needing improvement
- **Impact:**
    - Established a standardized QA reporting format for project checkpoints
    - Improved visibility into progress and quality across development phases
    - Enabled consistent documentation for stakeholder and repo-level review
---

### Prompt ID: P-053
- **Author:** Mark
- **Target:** Claude
- **Purpose:** Validate completion and alignment of sample file validation ticket
#### Prompt
```
ok so in our project board we still have this ticket under the in progress column:

T0-3 - Sample file validation

Description
Validate all test fixture Excel files against the defined input contract and assumptions. Ensure the pipeline design can handle multiple templates within a single workbook, variable header row positions, and sheet-level client segmentation. Identify mismatches early and either update assumptions or adjust fixtures accordingly.
Acceptance Criteria
* All fixture files reviewed against input contract and assumptions checklist
* At least one fixture workbook includes:
   * Multiple sheets
   * Each sheet representing a different client (via sheet name)
   * Different column naming conventions (template variations)
   * Different header row positions (not always row 1)
   * Header row location is validated for each sheet (correct row identified or failure expected)
* Any violations are:
   * Documented
   * Resolved via contract update OR fixture exclusion
* Confirmed that pipeline design can handle:
   * Multi-sheet ingestion
   * Mixed templates within a single workbook
   * Header detection across sheets
* No “unknown” or undefined formats remain in accepted fixture set
Assumptions
* Fixture set represents real-world variability, including:
   * Multiple templates within one workbook
   * Header rows appearing within the first N rows (not guaranteed row 1)
   * Each sheet corresponds to a distinct client (sheet name used as Client field)
* File sizes remain under 10MB
* All relevant edge cases are captured within fixture library
Test Plan
* Manually validate each fixture file against:
   * Input contract
   * Assumptions checklist
* For each sheet in each fixture:
   * Identify expected header row location
   * Identify expected client value (sheet name)
   * Confirm template variation coverage
* Document pass/fail for:
   * Header detection viability
   * Mapping compatibility
   * Structural assumptions
* Record and resolve all discrepancies before development proceeds

now that we are at the E4 -> E5 junction please review this ticket to make sure we haven't drifted and also is it completed? if not what needs to be done to complete it?
```

- **Summary of Response:**
    - Determined ticket is likely incomplete without explicit validation artifacts (checklist, documentation, pass/fail records)
    - Identified missing outputs: fixture audit log, header row mappings, and documented violations/resolutions
    - Emphasized need for confirmed coverage of all edge cases (multi-sheet, template variation, header detection)
    - Recommended final validation report to formally close ticket
- **Impact:**
    - Clarified definition of “done” for fixture validation phase
    - Prevented premature progression to E5 without verified input reliability
    - Established need for documented validation artifacts to support pipeline robustness
---

### Prompt ID: P-054
- **Author:** Mark / Claude
- **Target:** ChatGPT
- **Purpose:** Final schema enforcement layer for clean_df prior to CSV generation
#### Prompt
```
ok after talking with Claude: 
< 
ok we are at the E4 -> E5 junction: 
what I'd like to do at this point is feed you all of our source code (via cat?) so that you have a fresh view of everything before we move into the next phase: 
T5 - Output generation: 
T5-1 - clean_donations.csv writer 
T5-2 - rejected_rows.csv writer 
T5-3 - Download response + summary 
T5-4 - Deterministic file naming 
T5-5 - Basic logging 
T5-6 - Final schema enforcement layer 

9:28 AM Good idea. 
Let me read everything fresh from the actual repo. 
Ran 4 commands Ran 4 commands 
Good. I now have a complete fresh picture of the entire codebase. 
Here's what I know going into E5: 
Current pipeline output from run_pipeline(): 

python { "clean_df": DataFrame, # canonical columns, schema-ordered, internal cols removed "rejected_df": DataFrame, # original columns + rejection_reason "summary": {"total_rows": int, "clean_rows": int, "rejected_rows": int} } 

enforce_schema() stub current behavior: selects only columns present in OUTPUT_SCHEMA in order — silently drops missing ones. T5-6 replaces this. 
main.py current response: returns only {"summary": ..., "filename": ...} — no CSV content, no download links. 
T5 builds on top of this. 
OUTPUT_SCHEMA: 
python ["First", "Last", "Address1", "City", "State", "Zip", "DonationDate", "DonationAmount", "Client"] rejected_df columns: all canonical fields + rejection_reason. 
My read on T5 ticket ordering and dependencies: 
T5-6 first — before writing CSV writers, enforce_schema needs to be strict. 
If a required column is missing from clean_df due to an upstream gap, the CSV writer should not silently write a partial file. 
T5-6 gives us a hard gate. 
Every other T5 ticket depends on clean_df being schema-correct. 
T5-1 and T5-2 next — clean CSV writer and rejected CSV writer. 
Both are straightforward pandas to_csv() wrappers with deterministic settings (encoding, index=False, quoting). T5-4 alongside T5-1/T5-2 — deterministic file naming (derived from original filename + timestamp or batch ID). 
Naming logic belongs with the writers, not with the endpoint. 
T5-3 after writers — download response. Once files are written and named, the endpoint can return them as file downloads or as paths/URLs depending on how far we want to go for MVP. 
T5-5 last — basic logging pass across E5. 
Once the full output flow is working, audit the log statements and make sure the right things are being logged at the right levels. 
Ready to begin when you are — want to start with T5-6 to replace the schema stub, or take the tickets in order T5-1 through T5-6? 
> 

From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 

T5-6 - Final schema enforcement layer 

Description 
Ensure final clean_df strictly conforms to required schema (columns + order + completeness). 

Acceptance Criteria 
Output contains EXACTLY: First, Last, Address1, City, State, Zip, DonationDate, DonationAmount, Client 
No extra columns 
No missing columns 
Column order enforced before CSV write
```

- **Summary of Response:**
    - Defined strict schema enforcement logic as a hard gate before CSV generation
    - Required validation of column presence, completeness, and exact ordering
    - Clarified that missing or extra columns should cause failure rather than silent drop
    - Positioned this step as a dependency blocker for all downstream T5 output tasks
- **Impact:**
    - Established final “schema gate” ensuring data integrity before any file output
    - Prevented silent data loss by enforcing strict column validation rules
    - Locked in deterministic structure required for all CSV writers and downstream pipeline stages
---

### Prompt ID: P-055
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Implement strict schema enforcement layer in data pipeline
#### Prompt
```
# 🧠 Claude Code Prompt — T5-6 Final Schema Enforcement

## Lead Data Engineer Implementation (MVP Gatekeeper Layer)

You are acting as a **Lead Data Engineer** implementing:

> **T5-6 — Final Schema Enforcement Layer**

This is a **hard gate** between the pipeline and output generation.

---

# 🎯 PRIMARY OBJECTIVE

Ensure that:

> **clean_df EXACTLY matches the required warehouse ingestion schema**

Before ANY CSV is written.

---

# ⚠️ CRITICAL CONTEXT

Current state:

* `clean_df` is produced after:

  * parsing
  * mapping
  * normalization
  * validation
  * row splitting

* `enforce_schema()` currently:
  ❌ silently drops missing columns
  ❌ allows incomplete datasets

This is **NOT acceptable for production ingestion**

---

# 🚨 CORE PRINCIPLE (NON-NEGOTIABLE)

> If the schema is wrong → FAIL LOUDLY

DO NOT:

* silently fix
* infer missing columns
* allow partial outputs

---

# 📊 REQUIRED OUTPUT SCHEMA (SOURCE OF TRUTH)

OUTPUT_SCHEMA = [
    "First",
    "Last",
    "Address1",
    "City",
    "State",
    "Zip",
    "DonationDate",
    "DonationAmount",
    "Client",
]

---

# 📌 ACCEPTANCE CRITERIA (STRICT)

## 1. Exact Column Match

* clean_df MUST contain:

  * ALL columns in OUTPUT_SCHEMA
  * NO extra columns

---

## 2. Missing Column → HARD FAILURE

If ANY column is missing:

raise PipelineError(
    stage="schema",
    error_type="MissingColumn",
    message="Missing required column: Address1"
)

🚨 Do NOT attempt recovery

---

## 3. Extra Column → REMOVE

* Any column NOT in schema:

  * MUST be dropped
  * MUST NOT appear in output

---

## 4. Column Order Enforcement

Final DataFrame MUST be:

df = df[OUTPUT_SCHEMA]

🚨 Order matters for downstream systems

---

## 5. No Mutation Side Effects

* MUST operate on a `.copy()`
* MUST NOT mutate upstream data

---

# 🏗️ IMPLEMENTATION REQUIREMENTS

Implement in:

app/processing/schema.py

Function signature:

def enforce_schema(clean_df: pd.DataFrame) -> pd.DataFrame:

---

# ⚠️ ERROR HANDLING INTEGRATION

* Use existing `PipelineError`
* stage MUST be `"schema"`
* error_type MUST be descriptive:

  * `"MissingColumn"`
  * `"SchemaViolation"`

---

# 🧪 TEST-DRIVEN REQUIREMENTS

You MUST write unit tests.

---

## 1. Happy Path (REQUIRED)

Input:

* DataFrame with all required columns (unordered)

Expected:

* output columns EXACT match
* correct order enforced

---

## 2. Missing Column (CRITICAL)

Input:

* DataFrame missing `Address1`

Expected:

* raises PipelineError
* correct message

---

## 3. Extra Columns Present

Input:

* DataFrame includes `_source_sheet`, `random_col`

Expected:

* output drops extras
* only schema columns remain

---

## 4. Empty DataFrame

Input:

* empty df with correct columns

Expected:

* passes (structure is valid)

---

## 5. Column Case Sensitivity

Input:

* incorrect casing (`first`, `last`)

Expected:

* FAIL (mapping stage should have handled this)

🚨 Do NOT normalize here

---

# 🚨 COMMON FAILURE MODES

Flag immediately if present:

* silently filling missing columns with nulls
* allowing partial schema
* mutating original DataFrame
* not enforcing order
* swallowing errors instead of raising
* using try/except to hide issues

---

# 🧠 DESIGN PRINCIPLE

This layer enforces:

> “Only warehouse-ready data leaves the pipeline.”

---

# 🔗 PIPELINE INTEGRATION

This function MUST:

* be called AFTER T4-3 (row split)
* be applied ONLY to clean_df
* run BEFORE CSV writing (T5-1)

---

# 📋 COMPLETION CHECKLIST

Before finishing, confirm:

* strict schema enforcement implemented
* PipelineError raised correctly
* column order enforced
* extra columns removed
* full unit test coverage
* no silent failures

---

# 🧠 FINAL NOTE

This is the **last line of defense** before data leaves your system.

If this layer is weak:

> bad data reaches the warehouse → downstream systems break → trust is lost

---

Be strict.
Be unforgiving.
Fail loudly.

---

Begin implementation.

```

- **Summary of Response:**
    - Defined a strict schema enforcement function as a hard gate before data export
    - Introduced fail-fast behavior requiring exact column matching, ordering, and removal of extraneous fields
    - Specified integration point in pipeline and enforced unit testing requirements for multiple edge cases
- **Impact:**
    - Strengthened data integrity by ensuring only warehouse-valid datasets can proceed to export
    - Shifted pipeline design toward fail-fast, production-grade reliability
    - Established testing expectations and reduced risk of silent schema corruption
---

### Prompt ID: P-056
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Final schema enforcement QA audit prompt for production data pipeline validation
#### Prompt
```
# 🧠 Claude Code Prompt — T5-6 QA / Senior Test Engineer Review

## Final Schema Enforcement (Production Gate Audit)

You are acting as a **Senior QA Engineer + Lead Data Engineer reviewer**.

Your task is to perform a **strict, production-level audit** of:

> **T5-6 — Final Schema Enforcement Layer**

This is the **last line of defense before data leaves the pipeline**.

---

# 🎯 PRIMARY OBJECTIVE

Verify that:

* `clean_df` STRICTLY conforms to the required schema
* invalid schema conditions **fail loudly** (no silent corruption)
* output is **warehouse-ready and deterministic**

---

# ⚠️ CORE PRINCIPLE (NON-NEGOTIABLE)

> If schema is incorrect → PIPELINE MUST FAIL

🚨 Any silent success with bad schema = **FAIL**

---

# 📊 REQUIRED SCHEMA (SOURCE OF TRUTH)

OUTPUT_SCHEMA = [
    "First",
    "Last",
    "Address1",
    "City",
    "State",
    "Zip",
    "DonationDate",
    "DonationAmount",
    "Client",
]

---

# 🧪 CRITICAL VALIDATION CHECKS

---

## 1. Exact Column Match (HIGH PRIORITY)

Verify:

* ALL required columns present
* NO extra columns remain

🚨 FAIL if:

* any required column missing
* any unexpected column present in final output

---

## 2. Missing Column Handling (CRITICAL)

Confirm:

* missing column triggers:

PipelineError(stage="schema", error_type="MissingColumn", ...)

Verify:

* correct stage = `"schema"`
* error_type is meaningful
* error message identifies missing column

🚨 FAIL if:

* missing column is silently ignored
* missing column is filled with nulls
* generic exception used instead

---

## 3. Extra Column Handling

Verify:

* extra columns are dropped BEFORE output
* no internal columns leak:

  * `_source_sheet`
  * intermediate fields
  * debug columns

---

## 4. Column Order Enforcement (CRITICAL)

Confirm final DataFrame:

df = df[OUTPUT_SCHEMA]

Verify:

* EXACT order matches schema
* no reliance on existing order

🚨 FAIL if order is incorrect

---

## 5. No Mutation Side Effects

Ensure:

* `.copy()` used before transformation
* original DataFrame not modified

Test:

* pass df into function
* confirm original remains unchanged

---

## 6. Deterministic Behavior

Verify:

* same input → identical output
* no randomness
* no reliance on column ordering from upstream

---

# ⚠️ EDGE CASE VALIDATION

---

## 1. Empty DataFrame

* correct schema, zero rows
* MUST pass

---

## 2. Missing Column Case

* missing `Address1`
* MUST raise PipelineError

---

## 3. Extra Columns Case

* includes `_source_sheet`, `random_col`
* MUST drop extras

---

## 4. Incorrect Column Casing

Input:

first, last

Expected:

* FAIL (schema enforcement does NOT normalize)

---

## 5. Duplicate Columns (Rare but Critical)

* confirm behavior is deterministic
* no silent overwriting

---

# 🚨 COMMON FAILURE MODES

Flag immediately if present:

* silent column dropping without validation
* silent addition of missing columns
* mutation of input DataFrame
* incorrect column order
* reliance on upstream correctness
* try/except masking schema issues

---

# 🧪 TEST COVERAGE AUDIT

Ensure tests exist for:

* happy path (unordered columns → ordered output)
* missing column → failure
* extra columns → dropped
* empty DataFrame
* incorrect casing → failure

🚨 Missing any of these → TEST GAP

---

# 🔗 PIPELINE INTEGRATION CHECK

Verify:

* function is called AFTER row splitting (T4-3)
* applied ONLY to `clean_df`
* executed BEFORE CSV writing

---

# 📊 DATA INTEGRITY IMPACT

Confirm:

* no data lost during column selection
* no data reshaped incorrectly
* row count unchanged

---

# 🚫 FAIL CONDITIONS

Immediately FAIL if:

* schema violations pass silently
* incorrect column order
* missing PipelineError usage
* mutation of input data
* extra columns leak into output

---

# 📋 OUTPUT FORMAT

Return:

---

## 1. 🧠 Executive Summary

PASS / FAIL / PASS WITH RISKS

---

## 2. 🔴 Critical Issues

(schema correctness failures)

---

## 3. 🟡 Data Integrity Risks

---

## 4. 🧪 Test Coverage Gaps

---

## 5. ⚠️ Edge Cases Missed

---

## 6. 🧠 Final Verdict

* ✅ READY FOR T5-1 / T5-2
* ⚠️ READY WITH MINOR FIXES
* ❌ BLOCKED

---

# 🧠 FINAL INSTRUCTION

This is NOT a formatting review.

This is a **data contract enforcement audit**.

If this layer fails:

> invalid data reaches the warehouse → downstream systems break → trust is lost

Be strict.
Be unforgiving.
Think like production.

---

Begin review.

```

- **Summary of Response:**
    - Performed strict QA audit instruction design for schema enforcement layer
    - Defined hard fail conditions for any schema violation in clean_df
    - Specified required column contract, ordering rules, and mutation safety constraints
    - Included edge case handling and required test coverage expectations
    - Enforced pipeline placement rules (post-split, pre-export)
- **Impact:**
    - Established final “production gate” validation layer for data warehouse integrity
    - Ensures schema violations fail loudly instead of silently corrupting downstream systems
    - Strengthens test coverage expectations and prevents structural data drift in pipeline
---

### Prompt ID: P-057
- **Author:** Mark / Claude
- **Target:** ChatGPT
- **Purpose:** Generate implementation prompt for deterministic file naming (T5-4)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T5-4 - Deterministic file naming:

Description
Generate clear, unique filenames for output files (clean and rejected CSVs) using a timestamp and the original input filename. The goal is to prevent collisions while keeping naming simple and human-readable. Determinism is enforced at the data level (CSV content), not the filename.

Acceptance criteria
Filenames follow a consistent pattern:

{timestamp}_{input_filename}_clean.csv
{timestamp}_{input_filename}_rejected.csv
Multiple uploads do not overwrite existing files
Filenames are safe for filesystem and URL usage (no spaces, special characters sanitized)
Clean and rejected files from the same upload share the same base identifier (timestamp + filename)
Assumptions
Timestamp granularity (e.g., seconds or milliseconds) is sufficient to avoid collisions in MVP usage
Input filenames may contain unsafe characters and must be sanitized
Files are stored locally in a temporary/output directory
Test plan
Unit test: filename is correctly formatted given an input filename
Unit test: unsafe characters in filename are sanitized properly
Integration test: multiple uploads generate distinct filenames
Integration test: clean and rejected files from same upload share matching base name

(explanation of why we need to build in the order:

T6 -> T4 -> T1 -> T2 -> T3 -> T5:

T5-6 first — schema enforcement is a hard gate. No point writing CSV writers until we know exactly what shape the data will be in. Done.
T5-4 next — file naming logic (how output files get named) needs to be defined before T5-1 and T5-2 write anything to disk. The writers need to know what to call the files they're creating.
T5-1 and T5-2 together — once naming is settled, both CSV writers are nearly identical (to_csv() wrappers with deterministic settings). Clean writer and rejected writer can be implemented in the same pass.
T5-3 after writers — the download response endpoint can only be wired up once there are actual files to serve. It depends on T5-1, T5-2, and T5-4 all being complete.
T5-5 last — logging is a pass over the finished output flow rather than a blocker for anything else. Once the full E5 pipeline is working end-to-end, audit the log statements and fill in any gaps.)
```

- **Summary of Response:**
    - Generated a structured implementation prompt directing Claude to build deterministic filename logic
    - Emphasized sanitization, timestamp-based uniqueness, and shared base identifiers
    - Incorporated test-driven requirements (unit + integration tests)
    - Reinforced dependency order within T5 to ensure correct build sequencing
- **Impact:**
    - Clarified that file naming is a prerequisite for all CSV output logic
    - Enabled consistent, collision-safe file handling across pipeline runs
    - Aligned implementation with TDD approach and overall E5 pipeline sequencing
---

### Prompt ID: P-058
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Deterministic file naming utility for output pipeline
#### Prompt
```
# 🧠 Claude Code Prompt — T5-4 Deterministic File Naming

## Lead Data Engineer Implementation (MVP, Test-Driven, Output Layer Foundation)

You are acting as a **Lead Data Engineer** implementing:

> **T5-4 — Deterministic File Naming**

This is a **foundational dependency** for all output generation (T5-1, T5-2, T5-3).

---

# 🎯 PRIMARY OBJECTIVE

Create a **reliable, deterministic, collision-safe file naming system** for:

* clean output CSV
* rejected rows CSV

---

# ⚠️ CONTEXT (CRITICAL TO GET RIGHT)

You are building this **BEFORE** CSV writers.

Why:

* T5-1 / T5-2 depend on filenames
* T5-3 (download endpoint) depends on filenames
* naming must be consistent and reusable

---

# 🧠 CORE DESIGN PRINCIPLES

### 1. Human-readable

* filenames should be understandable

### 2. Collision-safe

* multiple uploads MUST NOT overwrite files

### 3. Paired outputs

* clean + rejected files MUST share same base identifier

### 4. Safe for filesystem + URLs

* no spaces
* no special characters

---

# 📌 REQUIRED FILENAME FORMAT

{timestamp}_{sanitized_input_filename}_clean.csv
{timestamp}_{sanitized_input_filename}_rejected.csv

---

# 🧩 COMPONENTS

## 1. Timestamp

* MUST be included
* MUST ensure uniqueness
* format recommendation:

YYYYMMDD_HHMMSS

Example:

20260412_143205

---

## 2. Input Filename (Sanitized)

Input:

"My Donations (Final).xlsx"

Output:

my_donations_final

### Rules:

* lowercase
* replace spaces → `_`
* remove special characters
* strip extension (.xlsx)
* allow only:

  * letters
  * numbers
  * underscores

---

## 3. Suffix

* `_clean.csv`
* `_rejected.csv`

---

# 🏗️ IMPLEMENTATION REQUIREMENTS

Create utility module:

app/utils/file_naming.py

---

## Required Functions

### 1. sanitize_filename()

def sanitize_filename(filename: str) -> str:

---

### 2. generate_output_filenames()

def generate_output_filenames(input_filename: str) -> dict:
    return {
        "clean": "...",
        "rejected": "...",
        "base": "..."
    }

---

# 📤 OUTPUT CONTRACT

Example:

{
    "base": "20260412_143205_my_donations",
    "clean": "20260412_143205_my_donations_clean.csv",
    "rejected": "20260412_143205_my_donations_rejected.csv"
}

---

# 📁 STORAGE ASSUMPTION

* files saved to:

/tmp/ or /output/

* filenames MUST be safe for:

  * filesystem
  * URL paths

---

# 🧪 TEST-DRIVEN REQUIREMENTS

---

## 1. Filename Format Test (REQUIRED)

Input:

"donations.xlsx"

Expected:

* matches pattern
* contains timestamp
* correct suffixes

---

## 2. Sanitization Test

Input:

"My Donations (Final).xlsx"

Expected:

my_donations_final

---

## 3. Unsafe Characters Test

Input:

"client@data#2024!.xlsx"

Expected:

clientdata2024

---

## 4. Matching Base Name Test

Ensure:

clean.startswith(base)
rejected.startswith(base)

---

## 5. Multiple Uploads (CRITICAL)

Simulate:

* two calls within short time

Expected:

* filenames differ (timestamp uniqueness)

---

# ⚠️ IMPLEMENTATION RULES

DO:

* use `datetime.utcnow()` or equivalent
* use regex for sanitization
* keep logic deterministic
* isolate logic in utility module

---

DO NOT:

* hardcode filenames
* include original extension (.xlsx)
* allow spaces or special characters
* generate filenames inside endpoint logic

---

# 🚨 COMMON FAILURE MODES

Flag immediately if present:

* filenames with spaces
* unsafe characters not removed
* inconsistent naming between clean/rejected
* timestamp missing or incorrect
* collision risk (same filename generated twice)
* extension duplication (e.g., .xlsx.csv)

---

# 🔗 PIPELINE INTEGRATION

This module will be used by:

* T5-1 (clean writer)
* T5-2 (rejected writer)
* T5-3 (download endpoint)

---

# 📋 COMPLETION CHECKLIST

Before finishing, confirm:

* filenames follow exact format
* sanitization works for all edge cases
* timestamp ensures uniqueness
* clean + rejected share base identifier
* full unit test coverage exists

---

# 🧠 FINAL NOTE

This may look simple — it is NOT.

If this fails:

* files overwrite each other
* downloads break
* debugging becomes impossible

This is **infrastructure-level correctness**.

---

Be precise.
Be consistent.
Be deterministic.

---

Begin implementation.
```

- **Summary of Response:**
    - Implemented utility module for filename sanitization and deterministic generation
    - Used timestamp + sanitized base name to create paired clean/rejected filenames
    - Applied regex-based cleaning to enforce filesystem-safe naming rules
    - Developed comprehensive unit tests covering format, uniqueness, and edge cases
- **Impact:**
    - Established a reliable naming convention used across all output layers (T5-1, T5-2, T5-3)
    - Eliminated risk of file overwrites and inconsistent output references
    - Enabled downstream features (file writing, downloads) to depend on a stable contract
---

### Prompt ID: P-059
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA review for deterministic file naming system
#### Prompt
```
🧠 Claude Code Prompt — T5-4 QA / Senior Test Engineer Review

You are acting as a Senior QA Engineer + Lead Data Engineer reviewer.

Your task is to perform a strict, production-grade code review of the implementation for:

T5-4 — Deterministic File Naming

This is a critical infrastructure layer that ensures:

No file collisions
Predictable output handling
Safe filesystem + URL compatibility

This logic directly impacts:

CSV writers (T5-1, T5-2)
Download endpoints (T5-3)
Observability and debugging
🎯 Review Objectives

Evaluate the implementation for:

1. Correctness (Primary)

Ensure all acceptance criteria are fully satisfied:

Filenames follow exact pattern:

{timestamp}_{input_filename}_clean.csv
{timestamp}_{input_filename}_rejected.csv
Clean + rejected files:
Share identical base identifier
Differ only by suffix (_clean, _rejected)
Multiple uploads:
NEVER overwrite existing files
Always produce unique filenames
2. Determinism vs Uniqueness (Subtle but Critical)

Validate correct balance:

✅ File contents are deterministic
✅ Filenames are unique per run
❌ No hidden randomness that breaks traceability
❌ No reuse of timestamps that risks collisions

Check:

Timestamp resolution (seconds vs ms)
Whether collisions are realistically possible
3. Filename Safety (High Risk Area)

Verify robust sanitization of input filenames:

Must handle:

Spaces → replaced or removed
Special characters (@#$%^&*())
Path traversal attempts (../../file.xlsx)
Unicode edge cases (if present)

Ensure:

Output filenames are safe for:
Filesystem
URLs (used in T5-3)
No unsafe characters remain
4. Separation of Concerns

Ensure naming logic is:

Encapsulated (e.g., file_naming.py or utility function)
NOT embedded inside:
FastAPI route
CSV writer functions
Reusable across:
clean writer
rejected writer
5. Integration Readiness

Validate compatibility with downstream tickets:

T5-1 / T5-2:
Writers can consume filenames cleanly
T5-3:
Filenames are URL-safe without additional transformation
6. Test Coverage (Critical)

Evaluate unit + integration tests:

Required Unit Tests
Correct filename format
Sanitization behavior
Matching base identifier for clean/rejected
Edge cases:
filenames with spaces
filenames with symbols
empty or malformed names
Required Integration Tests
Multiple uploads → unique filenames
Same upload twice → different filenames
Clean + rejected share base name
7. Edge Case Handling

Explicitly verify behavior for:

Input filename with no extension
Very long filenames
Duplicate uploads within same second
Empty filename or missing metadata
8. Code Quality

Evaluate:

Function naming clarity
Simplicity (no over-engineering)
Readability and maintainability
Type hints
Docstrings explaining:
naming strategy
sanitization rules
🔍 Output Format

Provide your review in this exact structure:

1. Executive Summary
Is this production-ready for MVP?
Any blockers?
2. ✅ What Is Strong
List well-implemented aspects
3. 🔴 Critical Issues (Must Fix Before Merge)
Anything that risks:
collisions
unsafe filenames
broken downstream integration
4. 🟡 Medium Risks
Non-breaking but important improvements
5. 🟢 Minor Issues
Style, clarity, minor cleanup
6. 🧪 Test Coverage Gaps
Missing tests
Weak assertions
Edge cases not covered
7. 🔧 Required Fixes
Concrete, actionable steps
8. 🧠 Final Verdict

Choose one:

✅ READY
⚠️ READY WITH MINOR FIXES
❌ NOT READY
⚠️ Important Context
This is MVP, but:
File naming is not a place to cut corners
Bugs here cascade into multiple downstream systems
Assume:
Local filesystem storage
No cloud storage yet
No async processing yet
🚫 Do NOT
Do NOT rewrite the code
Do NOT suggest future enhancements outside MVP scope
Focus strictly on correctness, safety, and testability

This review should be strict, practical, and production-minded.
```

- **Summary of Response:**
    - Structured a rigorous QA review framework focused on correctness, determinism, and filename safety
    - Emphasized collision avoidance, sanitization, and separation of concerns as critical evaluation areas
    - Defined explicit unit and integration test requirements, including edge cases
    - Standardized output format for consistent, production-grade code reviews
- **Impact:**
    - Established a high-quality QA standard for infrastructure-level components
    - Reduced risk of downstream failures in file handling and API layers
    - Ensured consistency and thoroughness in future code reviews for the project
---

### Prompt ID: P-060
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for deterministic CSV writer
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 

T5-1 - clean_donations.csv writer: 

Description 
Write clean_df to CSV in exact schema column order. 
UTF-8, no BOM. 
No index column. 
Deterministic column ordering enforced. 

Acceptance criteria 
Column order matches spec exactly 
Same input always produces identical output 
No pandas index column in output 
Rows sorted deterministically (e.g., by original order or stable index) 

Test plan 
Unit test: 
read output CSV and assert columns match schema list exactly. 
Run twice, diff outputs.
```

- **Summary of Response:**
    - Generated a structured implementation prompt for Claude aligned to MVP and TDD approach
    - Emphasized deterministic output (column order, row order, encoding, no index)
    - Included explicit acceptance criteria mapping to test assertions
    - Reinforced repeatability via idempotent output and diff-based validation
- **Impact:**
    - Enabled consistent and testable CSV output generation step
    - Locked down schema enforcement and reproducibility requirements
    - Provided clear implementation guidance for downstream data pipeline reliability
---

### Prompt ID: P-061
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Implement deterministic clean CSV writer module
#### Prompt
```
🧠 Claude Code Prompt — T5-1 Implementation (Clean CSV Writer)

You are acting as a Lead Data Engineer working within a test-driven, MVP-focused data pipeline.

Your task is to implement:

T5-1 — clean_donations.csv writer

This is part of the Output Generation (T5) layer and depends on:

✅ T5-6 (schema enforcement — already implemented)
✅ T5-4 (deterministic file naming — already implemented)
🎯 Objective

Write the clean_df DataFrame to a CSV file that is:

Schema-perfect
Deterministic
Warehouse-ready

This file is the primary deliverable of the entire pipeline.

⚠️ Critical Context (Do NOT Violate)
clean_df has already passed:
validation (T4)
schema enforcement (T5-6)

👉 This writer must NOT transform data — only serialize it.

Any schema issues here = upstream bug
This layer must act as a pure output boundary
📦 Implementation Requirements
1. Create a Dedicated Module

Create:

app/output/writer.py

Include a function like:

def write_clean_csv(clean_df: pd.DataFrame, output_path: Path) -> Path:
2. Enforce Deterministic Output

You MUST ensure:

✅ Column Order
EXACTLY matches:
[
    "First",
    "Last",
    "Address1",
    "City",
    "State",
    "Zip",
    "DonationDate",
    "DonationAmount",
    "Client",
]
Do NOT rely on DataFrame order implicitly
Explicitly reindex columns before writing
✅ Row Order (Deterministic)
Preserve original row order from pipeline
OR enforce stable ordering (if needed)

⚠️ Do NOT introduce randomness or sorting unless explicitly required

✅ Encoding + Format
Encoding: "utf-8" (NO BOM)
index=False
No extra whitespace or formatting artifacts
3. Integrate File Naming (T5-4)
The function should accept a fully resolved output_path
DO NOT generate filenames here
DO NOT embed timestamp logic here

👉 Separation of concerns is critical

4. Output Behavior
File must be written to disk
Function returns the Path to the written file
Overwriting should NOT occur (handled upstream via naming)
🧪 Test-Driven Development (MANDATORY)

Create tests in:

app/tests/test_writer.py
Unit Test 1 — Column Order Enforcement
Create DataFrame with shuffled column order
Write CSV
Read it back
Assert:
list(df.columns) == EXPECTED_SCHEMA
Unit Test 2 — No Index Column
Write CSV
Open raw file
Assert:
No extra unnamed index column
First column is "First"
Unit Test 3 — Deterministic Output
Write same DataFrame twice to two files
Compare file contents (string or bytes)
Assert they are identical
Unit Test 4 — Encoding
Write file
Read raw bytes
Confirm:
UTF-8 encoding
No BOM (\ufeff should NOT exist)
Unit Test 5 — Empty DataFrame (Edge Case)
Input: valid schema, zero rows
Output:
CSV exists
Only header row present
🚫 Explicit Non-Goals

Do NOT:

Validate schema (handled in T5-6)
Modify data values
Add logging (T5-5)
Handle rejected_df (T5-2)
Generate filenames (T5-4)
Return HTTP responses (T5-3)
🧠 Design Principles
Pure function mindset → input DataFrame → output file
Determinism > convenience
Strict schema adherence
Minimal logic, maximum reliability
✅ Acceptance Criteria Checklist

Before finishing, confirm:

 Column order EXACT match
 No index column in output
 UTF-8 encoding, no BOM
 Deterministic output across runs
 Function returns file path
 Tests pass via uv run pytest
🧠 Final Instruction

Implement this cleanly, minimally, and test-first.

This file is the contract boundary with the data warehouse — treat it as production-critical even at MVP.
```

- **Summary of Response:**
    - Defined a dedicated writer module with a pure function for CSV serialization
    - Enforced strict column ordering and UTF-8 (no BOM) output requirements
    - Implemented comprehensive unit tests covering determinism, encoding, and edge cases
    - Maintained strict separation of concerns with no transformation or naming logic
- **Impact:**
    - Established a reliable, deterministic output boundary for warehouse ingestion
    - Reduced risk of downstream data issues by enforcing schema consistency at write time
    - trengthened TDD discipline with clearly defined validation of output behavior
---

### Prompt ID: P-062
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Production-grade QA review of CSV writer layer (clean + rejected outputs)
#### Prompt
```
🧠 Claude Code Prompt — T5-1 + T5-2 QA / Senior Test Engineer Review

You are acting as a Senior QA Engineer + Lead Data Engineer reviewer.

Your task is to perform a strict production-grade code review of the implementation for:

T5-1 — clean_donations.csv writer
T5-2 — rejected_rows.csv writer (already implemented)

These are critical output layer components in the Donor Bureau pipeline. They represent the final data contract with downstream systems (warehouse + download API).

🎯 Review Objectives

You must evaluate BOTH writers for:

Correctness
Determinism
Schema integrity
Edge case handling
Production safety (MVP standard, but strict)
🧩 Context You Must Assume

The pipeline guarantees:

clean_df is already:
validated (T4)
schema-enforced (T5-6)
fully normalized
rejected_df contains:
original fields
rejection_reason column (ALWAYS present)

👉 These writers MUST NOT:

validate data
transform data
fix schema issues
perform business logic

They are pure serialization layers

📦 T5-1 Review Scope (clean_donations.csv writer)

Validate:

1. Schema Enforcement
EXACT column order:
First, Last, Address1, City, State, Zip, DonationDate, DonationAmount, Client
No missing columns
No extra columns
2. Deterministic Output
Same input → identical CSV output
No randomness
Stable ordering preserved
3. CSV Integrity
UTF-8 encoding (NO BOM)
index=False
No pandas index leakage
No formatting artifacts
4. Separation of Concerns
Writer does NOT:
rename columns
validate data
modify DataFrame
Only serializes
5. Edge Cases
Empty DataFrame:
header still written
no crash
6. Test Coverage Expectations

Verify presence of:

Column order test
Deterministic output test
Encoding test (no BOM)
Empty dataframe test
📦 T5-2 Review Scope (rejected_rows.csv writer)

Validate:

1. Schema Integrity
Must include ALL original columns
Must append:
rejection_reason
Column must ALWAYS exist
2. Empty Rejection Handling
If no rejected rows:
file STILL created
header STILL present
valid CSV structure
3. Data Preservation
Original row data must remain unchanged
rejection_reason must NOT be overwritten or dropped
4. Determinism
Same rejected input → identical output
Stable ordering preserved
5. CSV Output Rules
UTF-8 encoding (NO BOM)
No index column
No mutation of source DataFrame
6. Edge Cases
0 rejected rows
all rows rejected
mixed valid/invalid dataset
7. Test Coverage Expectations

Verify presence of:

empty rejection file test
multi-reason rejection test
schema integrity test
deterministic output test
🔍 Cross-Cutting Review (T5-1 vs T5-2)

You MUST compare both implementations for:

1. Architectural Consistency
Are both writers implemented using the same pattern?
Are responsibilities consistent?
Is shared logic duplicated incorrectly?
2. File Handling Consistency
Same encoding rules
Same index=False behavior
Same output directory strategy
Same naming integration assumptions (T5-4)
3. Integration Readiness (T5-3 dependency)

Ensure outputs are:

safe for download endpoints
deterministic in filename pairing
compatible with file naming layer
🚨 Critical Failure Conditions (Must Flag)

Immediately flag if ANY of the following exist:

Column order is not strictly enforced in T5-1
rejection_reason is optional or missing in T5-2
index column appears in output
nondeterministic file output across runs
silent schema mutation in writer layer
encoding issues (BOM present)
empty rejection file not handled correctly
🧪 Test Quality Review

Evaluate whether tests are:

deterministic
isolated
not relying on real filesystem state
covering edge cases explicitly
asserting file contents (not just function calls)
📊 Output Format

Return review in this structure:

1. Executive Summary
Is this production-ready for MVP?
2. ✅ What Is Strong
Key strengths in implementation
3. 🔴 Critical Issues (Must Fix Before Merge)
Data loss risks
schema violations
nondeterminism
missing rejection handling
4. 🟡 Medium Risks
structural improvements
maintainability concerns
5. 🟢 Minor Issues
naming, style, clarity
6. 🧪 Test Coverage Gaps
missing or weak tests
edge cases not covered
7. 🔧 Required Fixes
actionable fixes
8. 🧠 Final Verdict

Choose one:

✅ READY
⚠️ READY WITH MINOR FIXES
❌ NOT READY
⚠️ Important Context
This is MVP, but:
Output layer correctness is non-negotiable
These files are the final truth before warehouse ingestion
🚫 Do NOT
Do NOT rewrite code
Do NOT redesign architecture
Do NOT suggest future enhancements beyond MVP scope
Focus only on correctness, determinism, and safety
```

- **Summary of Response:**
    - Defined a strict senior QA / lead data engineering review prompt for validating CSV writer components in a donor ingestion pipeline
    - Established detailed evaluation criteria for correctness, determinism, schema integrity, and edge-case handling across clean and rejected outputs
    - Introduced explicit cross-cutting consistency checks between output writers and enforced MVP-level production safety constraints
- **Impact:**
    - Standardized QA expectations for final-layer data export components before warehouse ingestion
    - Strengthened enforcement of deterministic, schema-safe output behavior across pipeline writers
    - Created a reusable production-grade review template for validating data export logic in similar ingestion systems
---

### Prompt ID: P-063
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate implementation prompt for synchronous file upload/download API design
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T5-3 - Download response + summary:

Description
POST /upload processes the file synchronously and returns a JSON response containing summary statistics and download URLs for generated CSV files. Processing completes before the response is returned.

Response structure:
{
  "total_rows": int,
  "clean_rows": int,
  "rejected_rows": int,
  "clean_file": "/download/{clean_filename}",
  "rejected_file": "/download/{rejected_filename}"
}
A separate GET /download/{filename} endpoint serves generated CSV files from the temp/output directory.

Acceptance criteria
POST /upload returns 200 only after processing completes
Response JSON strictly matches defined schema
total_rows = clean_rows + rejected_rows
Download URLs are valid and return correct files
GET /download/{filename} returns correct file with 200
GET /download/{invalid_filename} returns 404
Files returned match contents generated during processing
Assumptions
Processing is synchronous for MVP (no background jobs)
Files are stored temporarily on local disk
Filenames are unique per upload (no collisions)
Files persist long enough for user to download (no immediate cleanup)
Test plan
Integration test: upload valid Excel → assert 200 response → validate JSON schema and counts
Integration test: download clean_file → verify schema + row count
Integration test: download rejected_file → verify rejection_reason column
Integration test: invalid filename → expect 404
Integration test: repeated identical upload → consistent counts and outputs
```

- **Summary of Response:**
    - Generated a structured Claude implementation prompt defining a synchronous file upload pipeline with explicit API contracts
    - Specified required endpoints for /upload and /download/{filename} with strict response schema enforcement
    - Included acceptance criteria and integration test scenarios covering validation, file integrity, and error handling
- **Impact:**
    - Locked in a synchronous MVP architecture for file processing and delivery
    - Defined strict API response contract for downstream consistency
    - Established a comprehensive integration testing strategy for upload/download lifecycle validation
---

### Prompt ID: P-064
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** FastAPI orchestration layer for pipeline output + secure download endpoint with TDD
#### Prompt
```
🧠 Claude Code Prompt — T5-3 Implementation (Download API + Summary Response)

You are acting as a Lead Data Engineer implementing a production-grade (MVP scope) API layer for the Donor Bureau pipeline.

Your task is to implement:

T5-3 — Download response + summary

This ticket connects the processing pipeline (T1–T4) with the output layer (T5-1, T5-2, T5-4) and exposes results to the user via FastAPI.

🎯 Objective

Extend the existing /upload endpoint to:

Run the full pipeline synchronously
Write output CSV files (already implemented in T5-1 and T5-2)
Return a structured JSON response containing:
processing summary
download links for generated files

Also implement:

GET /download/{filename}

to serve generated CSV files.

⚠️ Critical Context (DO NOT VIOLATE)

You MUST assume:

Pipeline already exists:
run_pipeline(df, config) returns:
clean_df
rejected_df
summary
Output writers already exist:
T5-1 → clean CSV writer
T5-2 → rejected CSV writer
T5-4 → deterministic file naming

👉 This ticket ONLY orchestrates and exposes results.

📦 Implementation Requirements
1. Update /upload Endpoint
Must now:
Accept .xlsx upload (already implemented in T2-1)
Run full pipeline synchronously
Generate output files using:
clean writer (T5-1)
rejected writer (T5-2)
naming utility (T5-4)
Return Response MUST match EXACT schema:
{
  "total_rows": int,
  "clean_rows": int,
  "rejected_rows": int,
  "clean_file": "/download/{clean_filename}",
  "rejected_file": "/download/{rejected_filename}"
}
Hard Rules:
total_rows = clean_rows + rejected_rows MUST hold
Response is returned ONLY after full processing completes
No async/background processing (MVP constraint)
No extra metadata fields allowed
2. Implement File Serving Endpoint

Create:

GET /download/{filename}
Requirements:
Serves files from local output directory
Returns:
200 with file content if exists
404 if file does not exist
Security constraints:
Prevent path traversal (../)
Only allow safe filenames
Validate filename strictly before file access
3. File Storage Assumptions
Files stored locally in a temporary output directory
Filenames are guaranteed unique (T5-4 handles this)
No cloud storage or persistence layer required
🧪 Test-Driven Development (MANDATORY)

Create or extend tests using httpx + pytest.

1. Upload Integration Test (Happy Path)
Upload valid .xlsx
Assert:
HTTP 200
JSON schema matches exactly
total_rows = clean + rejected
2. Download Clean File Test
Use returned clean_file path
Assert:
HTTP 200
CSV schema matches expected
Row count correct
3. Download Rejected File Test
Assert:
rejection_reason column exists
rows preserved correctly
4. Invalid File Test
Upload .csv or malformed file
Assert:
HTTP 400
meaningful error message
5. Invalid Download Test

Call:

GET /download/does_not_exist.csv
Assert:
HTTP 404
6. Repeat Upload Determinism Test
Upload same file twice
Assert:
different filenames (T5-4 behavior)
identical row counts and outputs
🧠 Design Requirements
Separation of Concerns

Ensure clear layering:

Layer	Responsibility
API	request/response only
Pipeline	data processing
Writers	file output
Naming	file naming
Download endpoint	file retrieval
Error Handling
Pipeline errors → return structured 400
System errors → 500
Validation errors handled upstream (T4)
Security Requirements
No arbitrary file access
Sanitize filename input
Prevent directory traversal attacks
🚨 Critical Acceptance Criteria Checklist

Before completion, ensure:

 /upload returns correct schema ONLY
 Processing is fully synchronous
 Clean + rejected files are written correctly
 /download/{filename} works securely
 404 returned for invalid files
 total_rows = clean + rejected always holds
 No schema drift in API response
🧪 MVP Constraints
No background jobs
No message queues
No cloud storage
No auth layer
Local filesystem only
🚫 Do NOT
Do NOT modify pipeline logic (T1–T4)
Do NOT redesign writers (T5-1 / T5-2)
Do NOT introduce async processing
Do NOT add extra response fields
Do NOT introduce external storage systems
🧠 Final Instruction

This ticket is the first user-facing product surface of the system.

It must be:

predictable
deterministic
secure
test-covered
minimal but production-safe

Build it exactly to spec, with strong TDD discipline.
```

- **Summary of Response:**
    - Implemented FastAPI orchestration layer updating /upload to run synchronous pipeline execution and return strict JSON schema with clean/rejected file links
    - Added secure /download/{filename} endpoint with filename validation, path traversal protection, and 404 handling
    - Created/extended pytest + httpx test suite covering upload flow, download validation, error cases, and deterministic re-upload behavior
- **Impact:**
    - Established first user-facing API surface for the Donor Bureau ingestion system
    - Enforced strict separation of concerns between pipeline, writers, naming, and API layers
    - Introduced secure file serving + end-to-end test coverage as production gate for MVP readiness
---

### Prompt ID: P-065
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Senior QA / Lead Data Engineer review of FastAPI upload/download API (T5-3 integration layer)
#### Prompt
```
🧠 Claude Code Prompt — T5-3 QA / Senior Test Engineer Review

You are acting as a Senior QA Engineer + Lead Data Engineer reviewer.

Your task is to perform a strict, production-grade code review of the implementation for:

T5-3 — Download response + summary (FastAPI upload + download endpoints)

This is the first user-facing API surface of the Donor Bureau system and connects:

ingestion (T2)
processing pipeline (T1–T4)
output generation (T5-1, T5-2, T5-4)
🎯 Review Objectives

Evaluate the implementation for:

API correctness
contract fidelity
determinism
file safety/security
integration correctness
test coverage completeness

This is a critical integration boundary layer.

📦 Functional Scope Under Review
1. POST /upload

Must:

Accept .xlsx
Run full pipeline synchronously
Generate:
clean CSV (T5-1)
rejected CSV (T5-2)
deterministic filenames (T5-4)
Return strict JSON response:
{
  "total_rows": int,
  "clean_rows": int,
  "rejected_rows": int,
  "clean_file": "/download/{clean_filename}",
  "rejected_file": "/download/{rejected_filename}"
}
2. GET /download/{filename}

Must:

Serve files from local output directory
Return:
200 → file exists
404 → file missing

Must enforce:

path traversal protection
filename sanitization safety
no arbitrary file access
🔍 Review Areas
1. API Contract Correctness (CRITICAL)

Verify:

Response schema matches EXACT structure
No extra fields added
No missing fields
No type inconsistencies
total_rows = clean_rows + rejected_rows always enforced
2. Pipeline Integration Correctness

Ensure:

/upload correctly calls full pipeline
clean_df and rejected_df are correctly passed to writers
T5-1 / T5-2 outputs are actually persisted
T5-4 naming is used correctly (no duplication or reimplementation)
3. Determinism & Consistency

Check:

Same input → same:
counts
outputs
Repeated uploads:
produce different filenames (T5-4)
identical data outputs
No hidden randomness in API layer
4. File Handling Safety (HIGH RISK)

For /download/{filename} verify:

No directory traversal vulnerability (../, /etc/passwd, etc.)
Only allowed files served
Files restricted to output directory
Proper 404 handling for missing files
5. Error Handling (SYSTEM vs VALIDATION)

Verify strict separation:

System Errors (must return HTTP 400/500)
corrupted file
unreadable Excel
pipeline crash
missing dependencies
Validation Errors
MUST still return 200
rejected rows included in response/output

Ensure this separation is correctly implemented.

6. File Output Integrity

Confirm:

clean CSV uses correct schema (T5-6 enforcement)
rejected CSV includes rejection_reason always
UTF-8 encoding preserved
no pandas index leakage
files exist at expected paths after upload
7. Test Coverage Review (CRITICAL)

Verify existence and quality of tests:

Required Integration Tests
valid upload → correct response schema
download clean file → correct schema + row counts
download rejected file → rejection_reason validated
invalid file upload → 400 response
invalid filename download → 404 response
repeated upload → deterministic behavior
Test Quality Checks
Uses real FastAPI test client (httpx)
No mocking of core pipeline (except necessary boundaries)
Assertions validate file contents (not just status codes)
Deterministic and repeatable
8. Architecture Review

Ensure proper separation:

Layer	Responsibility
FastAPI routes	orchestration only
pipeline	data processing
writers	CSV output
naming utility	filename generation
download endpoint	file serving

Flag any leakage of responsibilities.

🚨 Critical Failure Conditions

Immediately FAIL review if:

API response schema is not exact
file paths are insecure or unsanitized
clean/rejected counts are incorrect
pipeline logic is embedded in API layer
download endpoint allows arbitrary file access
missing integration test coverage for full flow
🧪 Output Format

Return review in:

1. Executive Summary
Is this MVP production-ready?
2. ✅ What Is Strong
Positive implementation qualities
3. 🔴 Critical Issues (Must Fix Before Merge)
Security issues
schema violations
incorrect integration
broken determinism
4. 🟡 Medium Risks
maintainability concerns
structural improvements
5. 🟢 Minor Issues
naming, style, clarity
6. 🧪 Test Coverage Gaps
missing tests
weak assertions
missing edge cases
7. 🔧 Required Fixes
actionable fixes only
8. 🧠 Final Verdict

Choose one:

✅ READY
⚠️ READY WITH MINOR FIXES
❌ NOT READY
⚠️ Important Context
This is MVP, but:
This is the first real user-facing API contract
correctness > performance
security > convenience
🚫 Do NOT
Do NOT rewrite code
Do NOT redesign architecture
Do NOT add new features
Focus strictly on correctness, safety, and test coverage

This review should be strict, adversarial, and production-minded.
```

- **Summary of Response:**
    - Defines a strict QA + senior data engineering review framework for the T5-3 FastAPI upload/download endpoints
    - Enforces API contract validation, determinism, file safety, and correct pipeline integration
    - Specifies required test coverage and separation of concerns across API, pipeline, and file layers
    - Provides structured review output format and explicit failure conditions for production readiness gate
- **Impact:**
    - Establishes a hard production-quality gate for the first user-facing API layer in the Donor Bureau system
    - Ensures security, correctness, and deterministic behavior are enforced before merge
    - Standardizes QA expectations for integration testing and FastAPI contract compliance
---

### Prompt ID: P-066
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for pipeline logging instrumentation task
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan:

T5-5 - Basic logging:

Description
Implement lightweight logging within the processing pipeline to capture key execution metrics. Log file name, total rows processed, clean row count, rejected row count, and total processing time. Logs should be emitted to the console for MVP simplicity.

Acceptance criteria
Logs include file name for each upload
Logs include total_rows, clean_rows, rejected_rows
Processing time (in seconds or ms) is logged
Log output is readable and structured (consistent format per run)
Assumptions
Console logging is sufficient for MVP (no external logging system required)
Processing is synchronous, so total runtime can be measured within request lifecycle
Test plan
Unit test: mock logger and verify expected log fields are emitted
Integration test: run full pipeline and assert logs contain row counts and processing time
Manual test: upload file and visually confirm log output format and values
```

- **Summary of Response:**
    
    - Generated a structured implementation prompt for Claude focused on adding console-based logging to a data processing pipeline
    
    - Emphasized capture of key execution metrics including file name, row counts, and processing time
    
    - Reinforced MVP constraints (no external logging system, synchronous processing)
    
    - Included explicit test expectations across unit, integration, and manual validation layers
- **Impact:**
    
    - Defined a clear logging instrumentation requirement for the pipeline MVP, ensuring observability of ingestion metrics while maintaining simplicity. Established a test-driven validation approach for verifying logging correctness and consistency across execution runs.
---

### Prompt ID: P-067
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Implement MVP observability logging layer for donation ingestion pipeline
#### Prompt
```
🧠 Claude Code Prompt — T5-5 Implementation (Basic Logging Layer)

You are acting as a Lead Data Engineer implementing observability for the Donor Bureau pipeline.

Your task is to implement:

T5-5 — Basic Logging

This is a cross-cutting observability layer that spans:

upload endpoint (T5-3)
pipeline execution (T1–T4)
output generation (T5-1, T5-2)

It is not business logic — it is instrumentation only.

🎯 Objective

Implement lightweight, structured console logging that captures key execution metrics for every upload request.

This is the MVP observability layer for the system.

⚠️ Critical Constraints (DO NOT VIOLATE)
Logging must NOT affect:
pipeline behavior
data transformation
validation logic
Must be:
lightweight
synchronous
console-only (no external systems)
Must NOT introduce side effects
📦 Logging Requirements
1. Required Metrics (MUST LOG EVERY RUN)

For every /upload request, log:

Input file name
total_rows
clean_rows
rejected_rows
processing_time_ms (or seconds)
2. Log Format (STRICT REQUIREMENT)

Logs must be:

consistent across runs
human-readable
structured (key-value style preferred)
Example format:
[PIPELINE_METRICS] file=donations.xlsx total_rows=120 clean_rows=100 rejected_rows=20 processing_time_ms=342
3. Placement Rules

Logging should occur:

AFTER pipeline execution completes
BEFORE API response is returned
Inside FastAPI upload orchestration layer OR dedicated logging utility
4. Timing Requirements

You MUST measure:

full end-to-end pipeline execution time
includes:
parsing
mapping
validation
writing outputs
Constraint:
Use synchronous timing only (e.g., time.perf_counter())
5. Implementation Strategy
Create one of the following:

Preferred:

app/logging/logger.py

OR inline utility inside pipeline orchestration layer if minimal.

Logging function example shape:
def log_pipeline_metrics(file_name, total_rows, clean_rows, rejected_rows, start_time, end_time):
🧪 Test-Driven Development (MANDATORY)
1. Unit Test — Logger Output Capture
Mock logger (or capsys)
Run logging function
Assert log contains:
file name
total_rows
clean_rows
rejected_rows
processing time
2. Integration Test — Full Pipeline Logging
Upload fixture via /upload
Capture stdout
Assert log line exists and contains:
correct row counts
processing time > 0
correct file name
3. Manual Verification Test
Run full upload manually
Confirm:
log appears in console
format is readable and consistent
values match API response
🧠 Design Requirements
Separation of Concerns

Ensure:

Logging does NOT live inside:
validators
transformers
writers

It should be:

triggered by orchestration layer OR pipeline wrapper
Determinism

Logging must:

never change pipeline output
never affect performance meaningfully
always reflect actual computed values
MVP Simplicity Rule
No:
ELK stack
external log collectors
async logging systems
structured logging frameworks unless trivial
Yes:
Python standard logging OR print-based structured logs
🚨 Acceptance Criteria Checklist

Before completion, ensure:

 Logs include file name
 Logs include total_rows, clean_rows, rejected_rows
 Logs include processing time
 Output format is consistent
 Logs are emitted per upload
 No pipeline behavior is affected
 Unit + integration tests exist
🧪 Edge Cases to Consider
Empty file upload
All rows rejected
Very large file (10k+ rows)
Pipeline exception (ensure logging does not break failure flow)
🚫 Do NOT
Do NOT introduce external logging services
Do NOT modify pipeline logic
Do NOT change API response structure
Do NOT add async logging
Do NOT over-engineer observability
🧠 Final Instruction

This is a minimal but production-relevant observability layer.

Your goal is:

“We should be able to understand what happened in any upload from a single log line.”

Keep it simple, consistent, and testable.
```

- **Summary of Response:**
    - Implemented a lightweight console logging utility for pipeline metrics using synchronous timing
    - Added structured log output capturing file name, row counts, and processing duration
    - Integrated logging at orchestration layer without modifying validation or transformation logic
    - Included unit and integration tests validating stdout log capture and correctness of metrics
- **Impact:**
    - Established MVP observability layer enabling end-to-end upload traceability
    - Improved debuggability of pipeline executions without introducing external dependencies
    - Created a foundation for future production-grade monitoring and instrumentation
---

### Prompt ID: P-068
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** QA review prompt for pipeline logging implementation
#### Prompt
```
🧪 Claude Code Review Prompt — T5-5 Basic Logging (Senior QA / Lead Tester)

You are acting as a Senior QA Engineer + Lead Data Engineer reviewer for the Donor Bureau Excel Pipeline.

Your task is to perform a strict production-level code review of the recently implemented:

T5-5 — Basic Logging (Pipeline Observability Layer)

This logging layer is part of a test-driven MVP data pipeline that processes Excel workbooks into clean/rejected CSV outputs.

🧠 Context You Must Consider

You are reviewing this within a fully implemented pipeline that already includes:

Pipeline Stages (must not be broken by logging)
parse → map → normalize → validate → split → enforce schema → output
Existing Output Contract

Each upload produces:

clean_df (schema-enforced, valid records only)
rejected_df (original data + rejection_reason)
summary:
total_rows
clean_rows
rejected_rows
T5-1 → T5-4 Already Implemented
clean CSV writer
rejected CSV writer
deterministic file naming
download endpoints (/download/{filename})
Critical Constraint

Logging MUST be:

non-intrusive
non-breaking
non-mutating to pipeline outputs
non-reliant on external systems (MVP = console only)
🎯 Your Task

Perform a full QA + architecture review of the logging implementation and determine:

1. Correctness
Are all required log fields present?
filename
total_rows
clean_rows
rejected_rows
processing time
Are values accurate and derived from the correct pipeline stage outputs?
2. Non-Intrusiveness (Critical)
Does logging mutate or leak into:
clean_df
rejected_df
summary
Does it interfere with determinism of output files?
3. Placement in Pipeline
Is logging executed:
at correct lifecycle point (end of pipeline run OR orchestrator level)
NOT inside transformation logic (parser/validator/normalizer)
4. Performance Impact
Any unnecessary:
dataframe copies
row-level logging inside loops
repeated string formatting per row

Flag anything that violates MVP simplicity.

5. Logging Format Quality
Is output:
structured and consistent per run
readable in console
useful for debugging pipeline runs

Recommend improvements if logs are noisy or inconsistent.

6. Test Coverage Review

Verify test coverage includes:

Required tests
mock logger assertion (unit test)
full pipeline run with log inspection (integration test)
timing validation (processing duration captured)

Flag missing or weak assertions.

🚨 Red Line Rules (Must Fail Review If Broken)

Fail the implementation if ANY of the following occur:

Logging alters DataFrames or pipeline outputs
Logging occurs inside row-level loops in validators or transformers
Missing any required metric field
No clear timing mechanism for full pipeline execution
Logging tightly coupled to business logic instead of orchestrator layer
🧪 MVP Philosophy Reminder

This is a lightweight MVP system, not enterprise observability.

✔ Acceptable:

print/log to console
simple structured string logs
basic timing via time.perf_counter()

❌ Not acceptable:

ELK stack integration
external logging services
async log pipelines
per-row logging noise
📦 Output Format

Return your review in this structure:

1. Executive Summary

(pass / pass with minor fixes / fail)

2. Critical Issues (blocking)
list any blocking issues
3. Non-Critical Issues
improvements or refactors
4. Test Coverage Gaps
missing or weak tests
5. Architecture Feedback
placement, separation of concerns, MVP alignment
6. Final Recommendation
ready / needs fixes / rollback required

If anything is ambiguous, assume strict MVP correctness and testability over convenience.
```

- **Summary of Response:**
    - Defined strict QA code review framework for pipeline logging layer (T5-5)
    - Enforced non-intrusive MVP logging constraints and placement rules
    - Specified required metrics, performance checks, and test coverage expectations
    - Introduced red-line failure conditions for pipeline safety and determinism
- **Impact:**
    - Established a production-grade review gate for observability features in the ETL pipeline
    - Ensured logging cannot interfere with core data transformation or outputs
    - Standardized QA expectations for future pipeline instrumentation work
---

### Prompt ID: P-069
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Comprehensive QA checkpoint review prompt for completed pipeline (T5 Output Generation)
#### Prompt
```
Ok now that we've completed up to T5 - Output generation
- please generate a prompt to Claude to do a checkpoint review of all the code as it stands and also take into consideration the input_contract, fixtures, testing, MVP as a lead senior QA / Data Engineer
```

- **Summary of Response:**
    - Generated a structured prompt for Claude requesting a full checkpoint review of the existing codebase up to T5 Output Generation
    - Focused the review on input_contract compliance, test fixtures, and existing test coverage
    - Framed the request from a senior QA / Data Engineering perspective aligned with MVP constraints and production readiness
- **Impact:**
    - Established a formal QA checkpoint gate in the workflow
    - Reinforced adherence to input contracts and testing standards
    - Improved alignment of implementation with MVP requirements and production-grade expectations
---

### Prompt ID: P-070
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Senior QA checkpoint audit prompt for full Donor Bureau pipeline review
#### Prompt
```
🧪 Claude Code Review Prompt — E5 Checkpoint Review (Senior QA / Lead Data Engineer)

You are acting as a Senior QA Engineer + Lead Data Engineer reviewer performing a full system checkpoint audit of the Donor Bureau Excel Pipeline.

This review occurs after completion of:

E1 → E5 (T0–T5) full pipeline implementation

The system now includes:

ingestion (FastAPI upload endpoint)
multi-sheet parsing
mapping + normalization
validation engine
row splitting (clean vs rejected)
schema enforcement
CSV output generation
deterministic file naming
download endpoints
logging layer
full test suite with fixtures
🧠 Your Objective

Perform a production-grade checkpoint review of the entire codebase as a cohesive system.

You are NOT reviewing individual tickets.

You are validating whether the system is:

✅ Correct
✅ Deterministic
✅ Test-driven compliant
✅ Aligned with input_contract.md
✅ Safe for MVP production use

📚 REQUIRED CONTEXT TO EVALUATE AGAINST

You MUST evaluate the code against these system artifacts:

1. Input Contract (Source of Truth)
/docs/input_contract.md

Key expectations:

multi-sheet workbook ingestion
metadata row skipping before headers
header detection within first N rows
alias-based column mapping
client derived from sheet name only
strict final schema enforcement
2. Fixture Validation System (Critical Gate)
/docs/fixture_validation.md
backend/tests/fixtures/

You must verify:

fixture coverage matches real-world patterns
metadata-before-header cases are tested end-to-end
multi-sheet + mixed template workbooks are covered
invalid header / missing header cases are tested
donation formats and ZIP edge cases are tested

⚠️ If fixtures do NOT fully validate input contract assumptions, this is a BLOCKER.

3. MVP Product Constraints

This is a strict MVP system:

✔ Allowed:

pandas
FastAPI
openpyxl
synchronous processing
local file output
console logging

❌ Not allowed:

distributed systems
async job queues
external storage
enterprise observability stacks
4. Pipeline Architecture (Must Be Preserved)

Final pipeline must remain:

parse → map → normalize → validate → split → enforce schema → output

With strict separation:

parsing = structure detection
mapping = alias resolution
normalization = formatting only
validation = business rules only
split = clean vs rejected
schema enforcement = final contract gate
output = file writing only
🎯 REVIEW TASKS
1. Contract Compliance Audit (CRITICAL)

Verify:

Does every rule in input_contract.md exist in code?
Are there any implementation shortcuts that violate the contract?
Are metadata rows handled correctly end-to-end?
Is header detection consistent with contract definition?
Is client assignment strictly from sheet name only?
2. End-to-End Pipeline Correctness

Check:

parse → map → normalize → validate → split → enforce → output integrity
No stage leaks responsibilities into another
No silent data loss or mutation bugs
No inconsistent DataFrame states across stages
3. Determinism Audit (VERY IMPORTANT)

Verify:

identical input → identical output CSVs
stable ordering in clean_df
no randomness in header detection
no timestamp-dependent data leakage into dataset
4. Output Layer Validation

Check:

clean_donations.csv:
exact schema
correct ordering
no index column
rejected_rows.csv:
rejection_reason always present
includes original columns + reason
download endpoints:
correct file mapping
no path traversal risk
5. Validation Engine Integrity

Ensure:

null validation works correctly
type validation is strict but correct
rejection reasons are consistent and human-readable
no row leaks between clean/rejected sets
clean_df has zero invalid values
6. Fixture Coverage Audit (BLOCKING CHECK)

Verify:

Multi-sheet workbooks tested end-to-end
Metadata-before-header real-world pattern tested in full pipeline
Header offset logic validated via fixtures
Mixed valid/invalid row datasets included
Instructions/non-data sheet exclusion tested
DonationDate format variety covered
ZIP edge case (leading zeros) covered

⚠️ If ANY are missing → BLOCK RELEASE

7. System-Level Error Handling Review

Verify:

corrupted file → 400
invalid file type → 400
missing mapping.json → startup failure
unexpected exceptions → 500 safe response
validation failures → 200 with rejected rows

Ensure:

no stack traces leak to API responses
error messages are structured and consistent
8. Logging Review (MVP OBSERVABILITY)

Check:

logs include:
filename
total_rows
clean_rows
rejected_rows
processing time
logging does NOT:
mutate data
affect determinism
slow pipeline significantly
🚨 RED FLAGS (AUTO-FAIL CONDITIONS)

Fail the system if ANY occur:

Input contract mismatch not explicitly resolved
Fixtures do not validate real-world metadata/header behavior
Any stage leaks responsibilities (e.g., validation in parser)
Non-deterministic outputs
Silent row loss or corruption
Clean/rejected counts do not reconcile with input
Schema enforcement is not strict at final stage
📦 OUTPUT FORMAT

Return review in:

1. Executive Summary

(pass / pass with risks / fail)

2. Contract Compliance Findings
alignment gaps
violations
3. Pipeline Architecture Review
stage correctness
separation of concerns
4. Data Integrity & Determinism
correctness of outputs
reproducibility
5. Fixture Coverage Audit
what is covered
what is missing (BLOCKING)
6. Test Suite Quality Review
unit tests
integration tests
missing scenarios
7. System Risk Assessment
production readiness risks
8. Final Recommendation
READY FOR E6 / BLOCKED / NEEDS FIXES
🧠 Final Instruction

Be strict.

This is a data pipeline correctness gate, not a feature review.

Prioritize:

correctness over convenience
determinism over flexibility
contract fidelity over implementation shortcuts
```

- **Summary of Response:**
    - Defined a strict senior-level QA gate prompt for full system review of the Donor Bureau pipeline (E1–E5)
    - Established evaluation criteria across contract compliance, determinism, fixtures, architecture, and output integrity
    - Introduced blocking conditions and production-readiness gatekeeping rules for E6 progression
- **Impact:**
    - Formalized a hard QA checkpoint for production readiness validation
    - Enforced strict contract-first, deterministic design principles across the pipeline
    - Created a go/no-go decision framework that governs advancement to next development phase
---

### Prompt ID: P-071
- **Author:** Mark / Claude
- **Target:** ChatGPT
- **Purpose:** Generate QA review prompt for frontend scaffold proposal
#### Prompt
```
I gave this prompt to Claude and it generated the proposal, please digest this and give a prompt to claude to review the proposal as a senior lead project manager / QA / engineer for best next steps:

now please generate a proposal as a lead engineer on this ticket to the senior project manager / QA for review on strategy and adherence to MVP

5:59 PM
Here's my proposal for T6-0 frontend scaffold before we proceed.

T6-0 — Frontend Scaffold: Lead Engineer Proposal
To: Senior Project Manager / QA From: Lead Engineer Re: React + Vite frontend scaffold strategy before T6-1 lands

What this ticket is and isn't
T6-0 is not a feature ticket. It's infrastructure — the minimal scaffolding required so that T6-1 (drag-and-drop component) and T6-2 (API integration) have a place to live. It should be invisible to the end user and produce no visible UI on its own.

What we're scaffolding and why
React + Vite via npm create vite@latest . -- --template react. Vite is the standard dev toolchain for React MVPs in 2026 — fast HMR, zero config, and the same stack referenced in the original project plan. No TypeScript for now — the original ticket spec says React only, and adding TypeScript at this stage adds friction without adding value at MVP scale.

react-dropzone installed alongside base dependencies since T6-1 depends on it and it makes no sense to scaffold without it.

No UI framework. The original T6-1 ticket explicitly says "No UI frameworks required — keep styling minimal." Tailwind, MUI, and Chakra are all off the table for MVP. Inline styles or a small CSS file only.

No test framework scaffolded. T6-1 is manually tested per the ticket spec. We don't add Jest or Vitest until there's a reason to — that's post-MVP scope.

Dev container approach
The current dev container is Python-only. We're updating it to install Node 20 inside the same container via NodeSource, so the full stack (backend + frontend) is available in one environment. This is the correct MVP approach — running two containers or requiring devs to exit the container for frontend work adds unnecessary friction.

The postCreateCommand will run both uv sync --dev (backend) and npm install (frontend) on container creation so the environment is ready with no manual steps.

What gets committed in T6-0
frontend/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.jsx
│   ├── App.jsx          ← minimal shell, no real UI yet
│   └── components/      ← empty, ready for T6-1
.devcontainer/
└── devcontainer.json    ← updated with Node 20 + npm install
Dockerfile               ← updated with Node 20 install
Boilerplate removed: App.css, assets/react.svg, public/vite.svg — none of it is relevant to this project.

App.jsx at T6-0 will be a two-line shell:

jsx
export default function App() {
  return <main style={{ maxWidth: 640, margin: "3rem auto", padding: "0 1.5rem" }} />
}
No content. T6-1 drops UploadDropzone into it.

MVP adherence check
Concern	Position
Are we over-building?	No — Vite scaffold is the minimum viable starting point
Does this affect the backend?	No — purely additive, no backend files touched
Does this affect CI?	Potentially — CI currently only runs uv run pytest. We should confirm the GitHub Actions workflow doesn't break on the new frontend/ directory. No frontend CI step is being added at this stage.
Is this reversible?	Yes — the entire frontend/ directory can be deleted with no backend impact
Does this block anything?	Yes — T6-1 and T6-2 cannot proceed without it
One open question for PM/QA review
Should npm run dev (frontend) run automatically when the dev container starts, or should it be a manual step?

My recommendation: manual for now. The postCreateCommand installs deps but doesn't start the dev server. Devs run npm run dev themselves when they need it. Auto-starting both uvicorn and Vite on container launch adds noise and port conflicts during backend-only work. This can be revisited in T6-2 when both servers need to run together.

Proposed commit
chore: scaffold React + Vite frontend, add Node 20 to dev container (T6-0)
Awaiting sign-off before rebuilding the container and merging.
```

- **Summary of Response:**
    - Generated a structured meta-prompt instructing Claude to review the proposal from PM/QA/engineering perspectives
    - Emphasized validating MVP adherence, scope control, and avoidance of over-engineering
    - Directed focus toward risks, CI impact, dev container setup, and dependency decisions
    - Included requirement to provide clear approval, requested changes, and next-step actions
- **Impact:**
    - Introduced a formal QA review layer before implementation
    - Helped enforce discipline around MVP boundaries and architectural decisions
    - Reduced risk of unnecessary complexity in frontend setup
    - Established a repeatable pattern for proposal → review → approval workflow
---

### Prompt ID: P-072
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Frontend scaffold proposal audit for MVP alignment
#### Prompt
```
🧠 Claude Review Prompt — T6-0 Frontend Scaffold Proposal Audit

You are acting as a Senior Project Manager + Lead QA Engineer + Senior Data Engineer reviewer.

Your task is to perform a critical review of the T6-0 Frontend Scaffold Proposal that was just generated.

This is NOT an implementation task.

This is a strategy, scope, and MVP alignment review before any code is written or merged.

🎯 Objective

Determine whether the proposed approach for:

T6-0 — Frontend Scaffold (React + Vite + Dev Container Updates)

is:

aligned with MVP goals
consistent with the existing backend-first architecture
not introducing unnecessary complexity or risk
the correct foundation for T6-1 and T6-2
🧠 Context You MUST Consider
Current System State (CRITICAL)

The backend pipeline is fully built and validated through T5:

ingestion (FastAPI)
parsing (multi-sheet, header detection)
mapping + normalization
validation engine
clean/rejected split
strict schema enforcement
CSV output + download endpoints
deterministic file naming
logging
full test suite + fixtures

👉 This system is the core product.
👉 The frontend is a thin UX layer, NOT the product.

MVP Philosophy (NON-NEGOTIABLE)

This project prioritizes:

simplicity over completeness
correctness over convenience
minimal surface area over flexibility

Frontend must be:

lightweight
low-risk
easily removable
not coupled to backend logic
🔍 Review Tasks
1. Scope Validation (CRITICAL)

Evaluate whether T6-0 is correctly scoped as:

infrastructure only (no user-facing functionality)
minimal setup required for T6-1

Answer:

Is anything unnecessary being introduced?
Is anything missing that will block T6-1?
2. Technology Choices

Evaluate the decision to use:

React + Vite
no TypeScript
no UI framework
no test framework
React Dropzone pre-installed

For each:

Is this correct for MVP?
Is anything over-engineered?
Is anything under-prepared?
3. Dev Container Strategy (HIGH RISK AREA)

Critically evaluate:

Adding Node 20 into the existing Python dev container

Answer:

Is this the correct approach for MVP?
Are there risks (bloat, rebuild time, environment complexity)?
Should frontend and backend be separated instead?
Does this violate simplicity or improve developer experience?

👉 This is the MOST important part of the review.

4. CI/CD Impact

Evaluate:

current GitHub Actions only runs uv run pytest
proposal does NOT add frontend CI

Answer:

Is this acceptable for MVP?
Are there any hidden risks (e.g., failing builds due to frontend folder)?
Should anything minimal be added now?
5. File Structure Review

Evaluate proposed structure:

frontend/
  src/
    App.jsx
    components/

Answer:

Is this minimal and sufficient?
Any unnecessary files?
Any missing structure needed for T6-1 or T6-2?
6. Dependency Timing

Evaluate:

Installing React Dropzone during T6-0

Answer:

Correct to install early?
Or should it be introduced in T6-1?
7. Dev Workflow Decision

Evaluate the open question:

Should npm run dev auto-start in container?

Answer:

Which is better for MVP:
manual start
automatic start
Consider:
developer experience
noise
backend-first workflow
8. Risk Assessment

Identify any:

architectural risks
coupling risks
future friction
unnecessary complexity
🚨 Red Flags (Call Out If Present)
frontend over-engineered relative to backend
unnecessary tooling introduced
container complexity increases significantly
frontend tightly coupled to backend
premature optimization
📦 Output Format

Return your review in this structure:

1. Executive Summary

(pass / pass with modifications / reject)

2. What Is Correct
list strong decisions
3. Issues / Risks
list concerns
clearly label severity (high / medium / low)
4. Required Changes Before Approval
concrete changes that MUST be made
5. Optional Improvements (Post-MVP)
things to defer
6. Final Decision
APPROVE / APPROVE WITH CHANGES / REJECT
🧠 Final Instruction

Be strict.

This is a guardrail checkpoint before introducing frontend complexity into a clean backend system.

If something feels even slightly overbuilt for MVP → challenge it.
```

- **Summary of Response:**
    - Enforced strict MVP alignment, emphasizing frontend as a thin, decoupled layer over a completed backend
    - Identified dev container (Node + Python) as primary risk area and evaluated tradeoffs
    - Challenged early dependency installation (React Dropzone) and unnecessary tooling
    - Recommended minimal structure and deferred enhancements to post-MVP
- **Impact:**
    - Prevented premature frontend complexity from contaminating a stable backend system
    - Drove decision-making toward minimal, low-risk frontend scaffolding
    - Established a formal review gate before introducing new architectural layers
---

### Prompt ID: P-073
- **Author:** Mark / Claude
- **Target:** ChatGPT
- **Purpose:** Frontend scaffold implementation instructions based on audit review
#### Prompt
```
please take this review and give instructions as the lead senior project manager to the senior engineer to implement this proposal according to the review's suggestions:

T6-0 Frontend Scaffold Proposal — Audit Review
Reviewer: Senior Project Manager / Lead QA / Senior Data Engineer
Subject: T6-0 strategy review before any code is written or merged

1. Executive Summary
⚠️ APPROVE WITH CHANGES
The proposal is directionally correct — React + Vite is the right minimal choice, the scope is genuinely infrastructure-only, and the decision to skip TypeScript and a test framework is sound MVP discipline. One issue requires a change before approval: Node 20 should not be installed inside the Python backend container. Everything else is either correct or acceptable at MVP scale.

2. What Is Correct
React + Vite is the right call. Zero config, fast, standard, no lock-in. Exactly what a thin UX layer over a backend pipeline should use.
No TypeScript. Correct for MVP. TypeScript adds toolchain complexity (tsconfig, type definitions for external packages, IDE setup) that has no payoff at this scale. The component surface area for T6-1 and T6-2 is small enough that untyped JavaScript is the right call.
No UI framework. The original T6-1 ticket spec says "No UI frameworks required — keep styling minimal." Respecting that constraint is correct. Introducing Tailwind, MUI, or any other framework during scaffold would be scope creep.
No test framework scaffolded. T6-1 is manually tested per spec. Adding Jest or Vitest now adds toolchain config with nothing to run against. Defer until there's a reason.
react-dropzone pre-installed at T6-0. This is correct. T6-1 has a hard dependency on it. Installing a known T6-1 dependency during scaffold is not over-building — it's avoiding a mid-ticket npm install that would need its own commit and review.
Boilerplate removal (App.css, react.svg, vite.svg) is correct. Leaving Vite boilerplate in the repo creates noise and implies the project uses things it doesn't.
npm run dev as manual start. Correct. Developers are primarily working on the backend. Auto-starting Vite on container launch adds port noise and slows startup for backend-only work sessions. Manual is the right MVP default.
No frontend CI step added. Acceptable for MVP. There's nothing to test yet. The risk of a broken frontend build blocking backend CI doesn't exist if frontend has no CI step. Revisit in T6-2 when there's actually something to lint or build.

3. Issues / Risks
🔴 HIGH — Node 20 installed inside the Python backend container.
This is the most significant concern in the proposal. The current container is a focused Python/uv environment. Installing Node 20 via NodeSource into it increases container size substantially (Node 20 + npm adds ~200-400MB to the image), increases rebuild time, and introduces a second runtime ecosystem into what should be a single-purpose build environment.
The correct approach for a full-stack project with two separate codebases is two separate containers orchestrated via docker-compose.yml — one for the backend (Python/uv) and one for the frontend (Node). This is already partially implemented: the original docker-compose.yml from T1-1 already has a frontend service using node:20-slim behind a profiles: [frontend] flag. The proposal ignores this and instead stuffs Node into the backend container, which is the wrong direction.
Merging Node into the Python container also means every future docker build for the backend — including CI — installs Node. That's unnecessary weight on a backend-only CI pipeline.
🟡 MEDIUM — postCreateCommand runs npm install unconditionally.
If the frontend/ directory is scaffolded but package.json doesn't exist yet at the time the container is created (e.g., on a fresh clone before T6-0 is merged), the npm install step will fail loudly and break container creation. The command needs a guard:
bashcd /workspace/backend && uv sync --dev && [ -f /workspace/frontend/package.json ] && cd /workspace/frontend && npm install || true
Or better: keep the backend and frontend container setup entirely separate.
🟡 MEDIUM — Dockerfile change scope.
The proposal updates the Dockerfile that builds the backend service. Adding Node to the backend Dockerfile couples the frontend toolchain to the backend image permanently. Any time the backend image is built (CI, production, deployment), Node is included for no reason. This is a maintainability and security surface area increase that should not be accepted at MVP.
🟢 LOW — ESLint and Prettier VS Code extensions added to devcontainer.json.
These are reasonable additions given frontend work is starting, but they're mildly premature — there's no ESLint or Prettier config in the repo yet. Adding the extensions without the config means VS Code will show warnings about missing config files. Either add minimal configs alongside the extensions, or defer the extensions to T6-1 when they'll actually be used.

4. Required Changes Before Approval
Change 1 (required) — Do not modify the backend Dockerfile to install Node.
The frontend service in docker-compose.yml already exists using node:20-slim. Remove the profiles flag and let it run alongside the backend. The VS Code dev container attaches to the backend service; the frontend dev server runs in its own container. Developers access it at localhost:5173 the same way they access the backend at localhost:8000.
The updated docker-compose.yml frontend service:
yamlfrontend:
  image: node:20-slim
  volumes:
    - .:/workspace
  working_dir: /workspace/frontend
  ports:
    - "5173:5173"
  command: sh -c "npm install && npm run dev -- --host"
Remove the profiles: [frontend] line so it starts automatically with docker compose up.
Change 2 (required) — Revert the Dockerfile to its current state.
No Node in the backend image. The backend Dockerfile should remain Python-only.
Change 3 (required) — Update postCreateCommand to backend-only.
json"postCreateCommand": "cd /workspace/backend && uv sync --dev"
Frontend deps are handled by the frontend container on startup. No npm install in the backend container's postCreate.

5. Optional Improvements (Post-MVP)
Proxy config in vite.config.js. In T6-2 when the frontend calls POST /upload, it will need to proxy API requests to localhost:8000 to avoid CORS issues during local development. Adding this to vite.config.js is a one-liner but belongs in T6-2 when the API integration is actually wired up, not T6-0.
.eslintrc and .prettierrc. Correct tooling configs belong in the repo eventually, but they're a T6-1 concern when there's actual code to lint.
Frontend CI. A npm run build step in GitHub Actions is the right eventual addition — it catches broken JSX before merge. Belongs in T6-2 or its own chore ticket, not here.

6. Final Decision
✅ APPROVE WITH CHANGES
Three required changes, all structural:

Remove Node from the backend Dockerfile
Remove profiles from the frontend docker-compose service so it runs alongside the backend
Revert postCreateCommand to backend-only

Once those three changes are made, T6-0 is correctly scoped, minimal, and a clean foundation for T6-1. The technology choices (React + Vite, no TypeScript, no UI framework, react-dropzone pre-installed) are all sound MVP decisions and do not require changes.
```

- **Summary of Response:**
    - Translated audit review into clear implementation directives for senior engineer
    - Emphasized separation of backend (Python) and frontend (Node) via Docker Compose
    - Identified three required structural fixes (Dockerfile, docker-compose, postCreateCommand)
    - Reinforced MVP discipline (no TypeScript, no UI framework, no premature tooling)
- **Impact:**
    - Prevented improper container architecture and long-term technical debt
    - Established clean separation of concerns between frontend and backend environments
    - Ensured scalable, maintainable dev setup aligned with production practices
    - Unblocked T6-0 approval and enabled progression to frontend implementation tickets
---

### Prompt ID: P-074
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** Enforce frontend architecture separation and scaffold implementation (T6-0)
#### Prompt
```
🧭 T6-0 Implementation Directive — Senior PM → Senior Engineer

We are approved to proceed with T6-0, but only under strict adherence to the architectural corrections identified in the review.

This is a course-correction, not a redesign.

🎯 Objective

Deliver a clean, minimal frontend scaffold that:

enables T6-1 and T6-2
introduces zero unnecessary backend coupling
preserves the integrity of our Python-first pipeline architecture
🚨 Non-Negotiable Changes (Must Be Implemented)
1. ❌ Do NOT install Node in the backend container

Explicit directive:

Remove ALL Node installation steps from:
Dockerfile
.devcontainer/devcontainer.json
any shell scripts

Reason:

Backend container must remain:

Python + uv only

No dual-runtime containers. No exceptions.

2. ✅ Use existing frontend container (docker-compose)

We are standardizing on a multi-container setup.

Required change:

Update docker-compose.yml:

REMOVE:
profiles:
  - frontend
KEEP / ENSURE:
frontend:
  image: node:20-slim
  volumes:
    - .:/workspace
  working_dir: /workspace/frontend
  ports:
    - "5173:5173"
  command: sh -c "npm install && npm run dev -- --host"
Outcome:
Frontend runs alongside backend automatically
No manual profile activation required
Clean separation of concerns maintained
3. 🔁 Revert backend Dockerfile

The backend Dockerfile must remain:

Python-only
unchanged from T1

👉 If Node appears anywhere → remove it

4. 🔁 Fix devcontainer postCreateCommand

Replace with:

"postCreateCommand": "cd /workspace/backend && uv sync --dev"
DO NOT:
run npm install here
reference frontend at all

👉 Frontend dependencies are handled inside the frontend container

🧱 Frontend Scaffold (Approved Scope)

Proceed with scaffold exactly as proposed, with no expansion:

frontend/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   └── components/
Implementation Constraints
✅ Include:
React + Vite scaffold
react-dropzone installed
minimal App.jsx shell
❌ Do NOT include:
TypeScript
Tailwind / MUI / Chakra
test frameworks
API logic
state management libraries
App.jsx (MVP shell)

Keep exactly minimal:

export default function App() {
  return (
    <main style={{ maxWidth: 640, margin: "3rem auto", padding: "0 1.5rem" }} />
  )
}
⚙️ Dev Workflow (Final Decision)
Frontend dev server:
runs automatically via docker-compose

accessible at:

http://localhost:5173
Backend:

runs at:

http://localhost:8000
Devcontainer:
attaches to backend container only
frontend runs independently

👉 This separation is intentional and correct

🧪 Acceptance Criteria (T6-0)

Before marking complete, verify:

Environment
docker compose up starts:
backend (8000)
frontend (5173)
Frontend
Vite app loads at localhost:5173
No errors in console
App renders empty shell
Backend
unaffected
tests still pass (uv run pytest)
⚠️ Guardrails

If any of the following occur, STOP and fix:

Node appears in backend container
Dockerfile modified beyond Python scope
devcontainer references frontend setup
frontend cannot run independently
backend CI impacted
📦 Commit
chore: scaffold React + Vite frontend with separate container (T6-0)
🧠 Final Direction

This is about protecting the architecture you’ve built.

You now have:

a production-quality data pipeline
and you're layering a thin UI on top

We are not turning this into a full-stack monolith.

✅ Next Step

Once complete and verified:

→ Move directly to T6-1 (Drag & Drop Upload Component)

If anything feels like “this might be easier if we just…”
→ that’s usually where architecture starts degrading.

Stay disciplined.
```

- **Summary of Response:**
    - Enforced strict separation between backend (Python-only) and frontend (Node container)
    - Defined exact docker-compose, devcontainer, and Dockerfile corrections
    - Scoped minimal React + Vite scaffold with no additional complexity
    - Established clear acceptance criteria and architectural guardrails
- **Impact:**
    - Prevented architectural drift into a monolithic or dual-runtime backend
    - Standardized multi-container development workflow
    - Enabled safe progression to frontend features (T6-1, T6-2)
    - Reinforced long-term maintainability and separation of concerns
---

### Prompt ID: P-075
- **Author:** Mark
- **Target:** ChatGPT
- **Purpose:** Generate Claude implementation prompt for React drag-and-drop upload component (T6-1)
#### Prompt
```
From the role of a senior lead project manager, please generate a prompt for Claude to implement this ticket as a lead data engineer while sticking tightly to our MVP test driven product plan: 
in this epic: 
T6 - Frontend Upload Interface: 
we have these tickets: 
T6-1 - Drag-drop upload component 
T6-2 - Processing state + results display 
let's start with T6-1: 
Description 
React component with drag-drop zone (React Dropzone). 
Validates .xlsx extension client-side. 
Shows file name and size after selection. 

Acceptance criteria 
Non-xlsx files rejected with UI message 
Submit button disabled until a valid .xlsx file is selected 
File name and size visible after selection 

Test plan 
Manual: drag valid xlsx — confirm name and size display and submit enables 
Drag csv — confirm rejection message. 
Attempt submit with no file selected — confirm button remains disabled.
```

- **Summary of Response:**
    - Generated a structured “Claude prompt” instructing implementation of a React drag-and-drop upload component using React Dropzone
    - Emphasized MVP-first, test-driven development approach aligned with the project plan
    - Included explicit acceptance criteria translation into implementation requirements (file validation, UI states, disabled submit behavior)
    - Reinforced separation of concerns between UI state handling and validation logic
- **Impact:**
    - Converted a high-level ticket into an execution-ready developer prompt for Claude
    - Established clear frontend behavior rules for file ingestion UX
    - Created a reusable pattern for future T6 epic frontend implementation tickets
---

### Prompt ID: P-076
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** 
#### Prompt
```
🧠 Claude Code Prompt — T6-1 Drag & Drop Upload Component
You are acting as a Lead Frontend Engineer working under a Senior Data Engineer + QA-driven MVP process.
Your task is to implement:
T6-1 — Drag & Drop Upload Component
This is the first user-facing surface of the Donor Bureau pipeline. It must be minimal, deterministic, and strictly scoped to MVP.
🎯 Context
The backend pipeline is complete through E5 (output generation).
* POST /upload exists and processes .xlsx
* Returns:

{
  "total_rows": int,
  "clean_rows": int,
  "rejected_rows": int,
  "clean_file": "/download/{filename}",
  "rejected_file": "/download/{filename}"
}
Frontend scaffold (T6-0) is complete:
*  React + Vite 
*  No TypeScript 
*  No UI framework 
* react-dropzone installed 
*  Minimal App.jsx shell exists 
⚠️ MVP Constraints (STRICT)
You MUST adhere to these:
DO:
*  Use react-dropzone 
*  Use plain React (JS only) 
*  Use minimal inline styles or a small CSS file 
*  Keep component fully self-contained 
*  Focus ONLY on file selection + validation + display 
DO NOT:
*  Add API calls (belongs to T6-2) 
*  Add global state management 
*  Add UI frameworks (Tailwind, MUI, etc.) 
*  Add test frameworks 
*  Add routing 
*  Add over-engineered abstractions 
🧩 Implementation Requirements
Component
Create:

frontend/src/components/UploadDropzone.jsx
Behavior
1. Drag & Drop + Click Upload
Use react-dropzone to support:
*  Drag & drop file 
*  Click to select file 
2. File Validation (Client-side)
Accept ONLY:
* .xlsx files 
Reject:
* .csv 
* .txt 
*  any other extension 
Validation rules:
*  Check file extension (.xlsx) 
*  Case-insensitive 
3. UI States
You must support these states:
A. No file selected
*  Show dropzone area 
*  Submit button is disabled 
B. Invalid file selected
*  Show error message: 
   * "Only .xlsx files are supported" 
*  Clear selected file 
*  Submit remains disabled 
C. Valid file selected
*  Display: 
   *  File name 
   *  File size (KB or MB, formatted) 
*  Enable Submit button 
4. Submit Button
*  Label: "Upload" 
*  Disabled until valid .xlsx is selected 
*  On click: 
   *  For now → console.log(file) 
   *  (NO API call yet — T6-2) 
UI Expectations (Minimal)
*  Centered container (reuse App.jsx layout) 
*  Simple dashed border dropzone 
*  Basic hover/active styling 
*  Clean, readable layout 
No design system. No polish beyond usability.
App Integration
Update:

frontend/src/App.jsx
To render:

<UploadDropzone />
📁 Expected File Structure

frontend/src/
  App.jsx
  main.jsx
  components/
    UploadDropzone.jsx
Optional:

frontend/src/styles.css
🧪 Manual Test Plan (Must Pass)
You MUST verify:
✅ Valid file
*  Drag .xlsx 
*  File name + size appear 
*  Submit button enables 
❌ Invalid file
*  Drag .csv 
*  Error message appears 
*  No file retained 
*  Submit disabled 
❌ No file
*  Click submit 
*  Button remains disabled 
⚠️ QA / Engineering Standards
*  No unused state 
*  No console spam except submit action 
*  Clean, readable component 
*  No unnecessary abstractions 
*  No coupling to backend yet 
🚫 Common Failure Modes (Avoid These)
*  Accepting files based on MIME only (must check extension) 
*  Keeping invalid file in state 
*  Enabling submit prematurely 
*  Overcomplicating styling 
*  Adding API logic early 
📦 Deliverables
1. UploadDropzone.jsx 
2.  Updated App.jsx 
3.  (Optional) minimal CSS file 
4.  Brief explanation of: 
   *  State management approach 
   *  Validation logic 
   *  How it satisfies acceptance criteria 
🧠 Guiding Principle
This is not a UI project.
This is a thin control surface for a data pipeline.
Build the smallest, cleanest, most deterministic component possible.
```

- **Summary of Response:**

- **Impact:**
---

### Prompt ID: P-077
- **Author:** ChatGPT
- **Target:** Claude
- **Purpose:** 
#### Prompt
```
🧠 Claude Code Prompt — T6-1 QA / Senior Test Engineer Review

You are acting as a Senior QA Engineer + Frontend Test Lead + Data Pipeline Reviewer.

Your task is to perform a strict, production-style code review of the implementation for:

T6-1 — Drag & Drop Upload Component

🎯 Review Objectives

This is the first user-facing component in a data pipeline system.

Your job is to evaluate:

Correctness (does it meet the spec exactly?)
Robustness (does it break under edge cases?)
MVP discipline (is anything overbuilt?)
UX clarity (does the user understand what’s happening?)
Readiness for T6-2 (API integration)
📦 Scope of Review

You are reviewing:

UploadDropzone.jsx
App.jsx integration
Any CSS files (if present)
📋 Acceptance Criteria (Must Be Enforced Strictly)
File Validation
Only .xlsx files are accepted
Validation is case-insensitive
.csv and all other types are rejected
UI Behavior
Invalid file:
Error message shown
File NOT retained in state
Valid file:
File name displayed
File size displayed (human-readable)
No file:
Submit button disabled
Submit Behavior
Button disabled until valid file selected
Clicking submit:
Does NOT call API
Only logs file (for now)
🔍 What You Must Evaluate
1. Validation Logic (CRITICAL)
Is validation based on file extension, not just MIME?
Is .XLSX (uppercase) handled correctly?
Are edge cases handled:
File with no extension
File named file.xlsx.exe
Is invalid file cleared from state?
2. State Management
Is state minimal and clean?
Any unnecessary state variables?
Is error state properly reset when a valid file is selected?
Any stale state bugs?
3. Dropzone Implementation
Is react-dropzone used correctly?
Are accepted file types configured properly?
Any reliance on browser MIME that could fail?
4. UI / UX Behavior
Is the UI state clearly communicated?
Is the error message visible and unambiguous?
Is the submit button behavior correct in all states?
Any confusing transitions?
5. Edge Cases

Explicitly test mentally:

Drag invalid → then valid
Drag valid → then invalid
Rapid file changes
Same file uploaded twice
Empty file (0 bytes)
6. Code Quality
Any overengineering?
Any unnecessary abstractions?
Is the component readable and maintainable?
Any console logs left behind (besides submit)?
7. MVP Discipline
Did the engineer:
❌ Add API calls prematurely?
❌ Add styling frameworks?
❌ Add unnecessary complexity?
Or:
✅ Keep it minimal and scoped?
8. Integration Readiness (T6-2)
Can this component easily:
Send file via FormData?
Is the file object preserved correctly?
Any blockers for API integration?
🧪 Required Output Format

You MUST respond with:

1. 🧠 Executive Summary
✅ READY
⚠️ READY WITH FIXES
❌ NOT READY
2. 🔴 Critical Issues (Must Fix Before Merge)
Bugs
Spec violations
Broken edge cases
3. 🟡 Medium Risks
UX confusion
Fragile logic
Future integration risks
4. 🟢 Minor Issues
Cleanup
Readability
Small improvements
5. 🧪 Test Coverage Gaps
What is NOT testable manually but risky?
6. 🔧 Recommended Fixes

Concrete, actionable changes (not vague advice)

7. 🧠 Final Verdict

Clear go/no-go decision for merge

⚠️ Review Standards
Be strict
Be specific
Do NOT assume correctness
Treat this like production code entering a real system
🧠 Guiding Principle

This component is the entry point into a data validation pipeline.

If it accepts bad input, everything downstream is compromised.
```

- **Summary of Response:**

- **Impact:**