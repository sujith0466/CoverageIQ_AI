# AI Usage Note

CoverageIQ AI demonstrates applied AI engineering in its feature set and its development lifecycle.

## 1. Product AI Features
The platform relies on autonomous Large Language Models to evaluate missing software tests and write syntactic replacements.

- **Engine Primary**: Groq (Llama 3 70b)
- **Engine Secondary**: Google Gemini (1.5 Pro)
- **Context Supplying**: The Python `ast` syntax tree is heavily analyzed, converted to structural hints, and injected into the LLM system prompt to ground the AI with exact line numbers, parameters, and variable states.
- **Explainability**: We explicitly prompt the AI to define *why* it is recommending a specific test. This outputs to the Governance Traceability view to ensure humans can audit AI behavior.

## 2. Development AI Tooling
During the engineering lifecycle of this repository, AI Assistants (specifically, Google Gemini) were utilized for:
- Refactoring `React` state managers and components.
- Designing the database migration strategy (Alembic).
- Auditing the repository for XXE (XML External Entity) vulnerabilities and replacing standard libraries with `defusedxml`.
- Writing boilerplate structural documentation.
