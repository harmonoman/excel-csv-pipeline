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