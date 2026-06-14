# API Reference

All endpoints operate under the `/api` prefix.

## 1. System Health
- **`GET /api/health`**
  - **Returns**: `{"status": "ok", "database": "connected"}`
  - **Checks**: FastAPI responsiveness and asynchronous connection to the PostgreSQL database.

## 2. Report Management
- **`POST /api/reports/upload`**
  - **Payload**: Multipart file payload containing `coverage.xml`.
  - **Action**: Safely parses using `defusedxml` and writes to storage. Returns a unique `report_id`.
- **`GET /api/reports/history`**
  - **Returns**: Array of all previously processed reports, including global health scores and upload timestamps.

## 3. Analysis Pipeline
- **`POST /api/reports/{report_id}/analyze`**
  - Aggregates XML statistics.
- **`POST /api/reports/{report_id}/scan`**
  - **Payload**: `{"directory_path": "..."}`
  - **Action**: Scans the AST to index function definitions.
- **`POST /api/reports/{report_id}/detect-gaps`**
  - Correlates AST coverage definitions to flag exact untested logic blocks.
- **`POST /api/reports/{report_id}/risk-analysis`**
  - Invokes the Risk Engine to quantify exposure of untested code.

## 4. Artificial Intelligence
- **`POST /api/reports/{report_id}/generate-tests`**
  - **Action**: Orchestrates the LLM to write synthetic `pytest` assertions.

## 5. Governance
- **`GET /api/explainability/report/{report_id}`**
  - **Returns**: Audit details mapping *why* the LLM was dispatched for a function (e.g., "High Risk Heuristic", "Critical Path Flag").
- **`GET /api/audit`**
  - **Returns**: Immutable append-only system events (Uploads, Generation, Rejections).
