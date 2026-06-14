# CoverageIQ Pipeline Workflow

This document traces the exact data flow through the CoverageIQ system from the moment a user uploads a project to the moment AI-generated tests are rendered on the screen.

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API (FastAPI)
    participant Parser
    participant AST_Walker
    participant Risk_Engine
    participant LLM_Generator

    User->>Frontend: Upload coverage.xml + Zip Source
    Frontend->>API: POST /api/reports/upload (multipart/form-data)
    API->>Parser: Parse securely (defusedxml)
    Parser-->>API: Extracted lines/branches
    API-->>Frontend: { report_id }
    
    Frontend->>API: POST /api/reports/{id}/scan
    API->>AST_Walker: Crawl project directory tree
    AST_Walker-->>API: List of defined functions
    API-->>Frontend: Scan Success
    
    Frontend->>API: POST /api/reports/{id}/detect-gaps
    API->>API: Reconcile XML with AST definitions
    API-->>Frontend: Function Coverage Statuses
    
    Frontend->>API: POST /api/reports/{id}/risk-analysis
    API->>Risk_Engine: Evaluate uncovered functions (complexity, deps, length)
    Risk_Engine-->>API: Assign CRITICAL/HIGH/MED/LOW labels
    API-->>Frontend: Risk Output
    
    Frontend->>API: POST /api/reports/{id}/generate-tests
    API->>LLM_Generator: Dispatch High-Risk untested functions
    LLM_Generator->>LLM_Generator: Prompt Engineering (Groq/Gemini)
    LLM_Generator-->>API: Pytest Assertions & Explainability Reasons
    API-->>Frontend: Render Code Modals
```
