# LLM Prompts & Engineering

This document outlines the templated prompts utilized by the AI services within CoverageIQ to extract structured intelligence and generate code.

## 1. Test Generation Prompt

**Service Module:** `TestGeneratorService`
**Purpose:** Autonomously generate `pytest` assertion blocks for high-risk uncovered code logic.

```text
You are an expert Python test engineer.
Write a comprehensive pytest unit test for the following function.
The test should cover the most critical execution path and any obvious edge cases.

Function Name: {function_name}

Code:
{function_code}

Requirements:
1. ONLY return valid, executable Python code.
2. DO NOT include markdown formatting like ```python.
3. Include necessary standard library imports.
4. Assume the function can be imported via `from module import {function_name}`.
5. Use `pytest` for assertions.
```

## 2. Expected Structured Outputs

When parsing, the `TestGeneratorService` expects raw, clean string output from the LLM containing only Python code. Any Markdown wrappers (like \`\`\`python) are dynamically stripped by the application backend prior to saving to the PostgreSQL database.

**Sample Output Structure:**
```python
import pytest
from module import process_loan

def test_process_loan_denied_low_score():
    assert process_loan(50000, 550) == False

def test_process_loan_approved():
    assert process_loan(50000, 750) == True
```

## 3. Assumptions and Limitations

* **Assumptions**: 
  * The LLM understands standard `pytest` syntax implicitly.
  * The provided `function_code` snippet contains enough context (without the full file) for the LLM to deduce the expected inputs and outputs.
* **Limitations**: 
  * Because the LLM does not have execution access to the database or the live application state, generated tests utilizing complex ORM objects or mocked API calls may require human adjustment.
