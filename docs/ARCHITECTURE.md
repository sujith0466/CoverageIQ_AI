# Architecture Overview

CoverageIQ AI is built as a highly decoupled, modern web application prioritizing scalability, intelligence, and type safety.

## 1. System Components

### Frontend (Client Tier)
- **Framework**: React 18 with TypeScript via Vite.
- **Styling**: Vanilla CSS, relying on a unified Design System (glassmorphism, interactive layouts, dark mode native).
- **Communication**: Uses Axios wrapped in strongly-typed models to interact with the backend API.
- **Core Views**: Upload, Dashboard, File Explorer, AI Modal, Governance/Audit Trail.

### Backend (API & Analysis Tier)
- **Framework**: FastAPI (Python 3.11+).
- **Architecture Pattern**: Repository-Service-Controller model.
  - **Controllers**: Thin API routing (`endpoints/reports.py`, `endpoints/audit.py`).
  - **Services**: Heavy lifting and orchestration (`report.py`, `test_generator.py`).
  - **Repositories**: Database abstractions (`repositories/report.py`).
- **Core Engines**:
  - `parser.py`: Extracts raw XML data safely using `defusedxml`.
  - `ast_walker.py`: Statistically crawls local source trees to map function nodes.
  - `gap_detector.py`: Reconciles XML hits vs. AST definitions.
  - `risk_engine.py`: Computes algorithmic risk indices for uncovered code.
  - `test_generator.py`: Brokers LLM connections (Groq/Gemini) for dynamic assertions.
  - `governance_service.py`: Explainability logic for LLM actions.

### Database (Data Tier)
- **Engine**: PostgreSQL hosted on Neon (Serverless).
- **ORM**: SQLAlchemy 2.0 with `asyncpg`.
- **Migrations**: Alembic.
- **Data Models**: Relational structures for `Report`, `FunctionCoverage`, `GeneratedTest`, and `AuditLog`.

### AI Integration
- **LLM Pipeline**: Abstracted `LangChain` connections. Fallback logic prioritizes Groq for speed, with Gemini as a secondary heuristic generator.

## 2. Infrastructure
- **Containerization**: Dual Docker containers managed by `docker-compose.yml` (`frontend`, `backend`).
- **Networking**: Frontend `5173` routes dynamically to Backend `8000`. Wait-for-it healthchecks assure dependency resolution on boot.
