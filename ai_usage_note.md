# AI Usage Note

CoverageIQ AI operates natively as an artificial intelligence evaluation platform. This document outlines how AI models are utilized during runtime to power its core features.

## Purpose of AI in CoverageIQ
The core objective of CoverageIQ AI is to move beyond simple static coverage parsing and leverage LLMs to autonomously write executable unit tests for complex, untested functions. The system analyzes raw `coverage.xml` reports, maps gaps to the Abstract Syntax Tree (AST), and queries the AI to write `pytest` assertions that secure the application's most vulnerable logic.

## Models Utilized
* **Primary AI Engine**: Groq Cloud (specifically `Llama-3` variants, dynamically determined via the LangChain environment setup) for ultra-low-latency code generation.
* **Fallback AI Engine**: Google Gemini for secondary evaluation logic if required.

## How AI is used for Test Generation
1. The **Parser Engine** detects untested logic gaps from coverage files.
2. The **AST Walker** retrieves the raw Python code function string.
3. The **Risk Engine** assigns a priority risk score.
4. The **Test Generator Service** intercepts high-risk missing functions and submits a strict templated prompt to the LLM containing the target function code, asking it to output syntactically valid `pytest` strings.

## What AI Helped With
* Writing missing unit tests autonomously.
* Analyzing heuristic risk vectors.
* (During development) Generating the foundational structural logic for the `TestGeneratorService` module.

## AI Limitations & Validation Strategy
* **Hallucinations**: Generative models may hallucinate libraries or internal methods that do not exist.
* **Validation Strategy**: Generated tests are currently stored as strings and displayed in the Executive Dashboard for human review. In future iterations, tests will be executed in a sandboxed CI runner, and traceback errors will be iteratively fed back to the LLM for self-healing and correction.

## Fallback Mechanisms
If the primary LLM (Groq) is unavailable or encounters a rate limit, the system gracefully falls back to static string notifications indicating that test generation failed, returning standard heuristic analytics without crashing the dashboard.

## Best Prompts Used
The full suite of engineered prompts can be found in `prompts.md`. The core successful heuristic utilized strict output framing:
`ONLY return valid, executable Python code. DO NOT include markdown formatting. Assume the function can be imported via 'from module import {function_name}'.`

## What AI Got Wrong & Lessons Learned
* **JSON Formatting**: Early iterations attempted to force the LLM to return complex JSON objects containing the test code, risk rationale, and metadata. The LLM frequently hallucinated broken JSON syntax or escaped characters incorrectly. 
* **Lesson Learned**: We pivoted to requesting pure strings of Python code, using the backend (FastAPI) to structurally construct the JSON API response around the raw LLM output.
* **Context Windows**: Passing the entire source file to the LLM to generate one missing test was too slow and expensive. We utilized Python's native `ast` library to statically chunk only the specific untested function, drastically reducing token usage and hallucination radius.

## AI-Assisted Debugging Example
During development, the AI was highly utilized to debug a critical XML parsing issue. A valid `coverage.xml` was being rejected by the backend. The AI was prompted to write a multi-file tracing script (`tests/audit.py`), which discovered that the `ElementTree` parser was prepending XML namespaces to the root tag (e.g., `{http://cobertura.sourceforge.net/xml/}coverage`), causing strict string comparison to fail. The AI subsequently generated the namespace-stripping logic currently active in `parser.py`.
