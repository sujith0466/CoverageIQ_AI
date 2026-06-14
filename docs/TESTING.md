# Testing & Validation

CoverageIQ includes automated suites designed to stress-test the upload parsing, the LLM integration layer, and the asynchronous database operations.

## 1. Running the Validation Matrix

The core test bed is `scripts/validate_all.py`. This script performs an end-to-end traversal of the 5 included sample projects.

```bash
cd scripts
python validate_all.py
```

**What it tests:**
- End-to-end multipart `/upload` integration.
- `defusedxml` protection against malformed parsing.
- AST parsing logic accuracy.
- Execution speed of the LLM generator.
- Database writing performance under load.

## 2. Testing Constraints & Upload Hardening

You can manually verify the system's defenses by running the boundary test suite:
```bash
python scripts/test_upload.py
```

This verifies that:
- Files exceeding 10MB (XML) are rejected with a 400 status.
- Spoofed MIME types are rejected.
- Non-XML/ZIP extensions are barred entirely.
