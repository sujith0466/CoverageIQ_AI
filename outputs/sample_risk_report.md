# Risk Analysis Report
**Project Name**: Banking Core
**Scan Date**: 2026-06-14

## Executive Summary
Total Functions: 7
Uncovered Functions: 2
Partially Covered Functions: 2

## High Risk Gaps
1. `transfer_funds`
   * **Risk Score**: HIGH (85)
   * **Reasoning**: Cyclomatic complexity > 3, dependency length is critical. Core transactional logic.
   * **Lines**: 11-19
   * **Test Generation**: Completed.

2. `process_loan`
   * **Risk Score**: MEDIUM (60)
   * **Reasoning**: Branching complexity = 3. Contains nested IF blocks.
   * **Lines**: 23-28
   * **Test Generation**: Completed.

## Recommendations
Ensure the AI-generated tests for `transfer_funds` are integrated into the main `pytest` suite before deploying.
