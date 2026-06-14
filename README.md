# CoverageIQ AI

CoverageIQ AI is a next-generation code coverage analysis and intelligent test generation platform. It moves beyond static percentage tracking by integrating AST-based static code analysis with Generative AI (Groq & Gemini) to identify untested code, quantify risk, and autonomously write test suites.

## Problem Statement
Traditional test coverage tools offer blind percentages (e.g., "75% covered") without providing context on **what** is uncovered or **why** it matters. Engineering teams lack visibility into whether critical business logic is missing tests, and they spend significant manual effort writing boilerplate tests to fill gaps.

CoverageIQ AI solves this by translating raw `coverage.xml` artifacts into actionable, function-level intelligence, and autonomously generating the missing test code.

## Features
- **Intelligent XML Parsing**: Securely parses Cobertura `coverage.xml` reports to extract module and class-level hit data.
- **AST Code Walking**: Statically analyzes the uploaded project source tree using Python's `ast` to discover all defined functions.
- **Coverage Gap Detection**: Reconciles AST functions against the XML report to pinpoint exactly which functions are covered, partially covered, or uncovered.
- **Risk Engine Analysis**: Assigns an automated Risk Score (CRITICAL, HIGH, MEDIUM, LOW) to uncovered functions based on cyclomatic complexity, dependency count, and code length.
- **Executive Dashboard**: Provides a unified view of the system's "Health Score", grading the project's testing resilience and highlighting the most vulnerable functions.
- **Generative AI Test Writing**: Utilizes LLMs to automatically write functional `pytest` unit tests for the most at-risk, uncovered functions.
- **Dependency & Traceability**: Identifies upstream dependencies to determine cascading risks.
- **Governance & Explainability Trail**: Maintains an immutable audit log of all system actions and provides transparent explanations for *why* an AI generated a specific test.

## AI Capability Demonstrated
CoverageIQ AI leverages Large Language Models (LLMs) to perform **Autonomous Code Generation & Intelligence Structuring**:
- **Test Generation**: The `TestGeneratorService` prompts LLMs with the precise abstract syntax tree and source code of an untested function to generate syntactically correct `pytest` tests.
- **Risk Scoring**: The system dynamically evaluates whether an LLM or static heuristic is best suited to determine risk thresholds.
- **Zero-Shot Understanding**: Operates across arbitrary Python codebases without prior training data.

## Architecture Overview
The system follows a modern decoupled architecture:
- **Frontend**: React + TypeScript + Vite. Provides a responsive, dynamic dashboard and file exploration interface.
- **Backend**: FastAPI + Python. Houses the core analysis engines (`Parser`, `AST Walker`, `Gap Detector`, `Risk Engine`, `Test Generator`).
- **Database**: PostgreSQL (via Neon Serverless) + SQLAlchemy async ORM. Stores parsed functions, generated tests, and audit trails.
- **AI Providers**: Groq (Llama 3) and Google Gemini via LangChain-compatible integrations.
- **Containerization**: Fully orchestrated via Docker Compose with strict healthcheck probing.

*For more details, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).*

## Setup Instructions

### 1. Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)
- PostgreSQL Database URL (Neon or local)

### 2. Environment Variables
You must configure your API keys and secrets before starting the system.

Copy the example file to create your local environment file:
```bash
cp .env.example .env
```

**Required Environment Variables**
* `GROQ_API_KEY` (or `GEMINI_API_KEY`)
* `DATABASE_URL`
* `SECRET_KEY`

*(Note: Never commit your `.env` file or expose your `SECRET_KEY`. Keep them strictly local.)*

## Run Instructions

### Running via Docker (Recommended)
```bash
docker-compose up -d --build
```
- Frontend will be available at: `http://localhost:5173`
- Backend API will be available at: `http://localhost:8000`

### Running Locally (Without Docker)
**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Sample Input
To test the application, you can use the provided sample projects in the `sample_projects/` directory.

Example flow:
1. Navigate to the CoverageIQ Dashboard.
2. Upload `sample_projects/banking/banking_coverage.xml`.
3. The system will prompt you for the absolute path of the source directory. Provide the path to `sample_projects/banking`.

## Sample Output
Upon successful analysis, the dashboard will render:
- **Coverage %**: 51.4%
- **Functions Found**: 7
- **Gaps Detected**: 2 Uncovered, 2 Partially Covered
- **Risk Assessment**: 2 Medium Risk, 5 Low Risk
- **AI Generated Tests**: The system will automatically present `pytest` assertions for the uncovered `transfer_funds` and `process_loan` functions.

## Test Generation Example
**Input (Untested Code):**
```python
def process_loan(amount, score):
    if score < 600: return False
    if amount > 100000 and score < 700: return False
    return True
```

**Output (Generated Test):**
```python
import pytest
from banking import process_loan

def test_process_loan_low_score():
    assert process_loan(50000, 550) == False

def test_process_loan_high_amount_mid_score():
    assert process_loan(150000, 650) == False

def test_process_loan_approved():
    assert process_loan(50000, 750) == True
```

## Governance Features
- **Immutable Audit Trail**: Every upload, scan, and generation event is recorded in the `AuditLog` table.
- **Explainability**: AI decisions are transparent. The system explicitly provides a "Why Selected?" rationale for every generated test, detailing the risk heuristics that triggered the LLM.

## Assumptions
- Target codebases are written in Python.
- Coverage reports are provided in standard `Cobertura XML` format.
- The backend has local read access to the target codebase's directory structure for AST traversal.

## Limitations
- Cross-language AST parsing (e.g., JavaScript/TypeScript) is not yet supported.
- LLM-generated tests require manual human review; the system does not automatically execute the tests it writes to verify them against the application state.

## Future Enhancements
- Integration with GitHub Actions / CI/CD pipelines to automatically comment generated tests on Pull Requests.
- Support for JavaScript/TypeScript (LCOV) formats.
- Automated sandbox execution to auto-verify generated tests.

## Demo Video
*(Link to Demo Video Placeholder)*

## AI Usage Note
This project heavily utilizes AI assistance (via Google Gemini) for rapid prototyping, architecture planning, and feature implementation. See [docs/AI_USAGE_NOTE.md](docs/AI_USAGE_NOTE.md) for full disclosure of AI tooling used during development.
