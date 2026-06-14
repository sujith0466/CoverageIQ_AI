# CoverageIQ Sample Data Instructions

This folder contains pre-configured XML files to help you evaluate CoverageIQ's analysis engine without needing to generate your own `coverage.xml` reports.

## Available Sample XMLs
1. **`banking_coverage.xml`**: A realistic banking module containing uncovered, high-risk financial transaction functions (`transfer_funds`, `process_loan`).
2. **`ecommerce_coverage.xml`**: A shopping cart implementation with missing logic tests.
3. **`inventory_coverage.xml`**: An inventory tracking system with various coverage metrics.

## Testing Workflow (For Reviewers)

To fully experience the AST-mapping and AI generation loop, follow these exact steps:

1. In the **CoverageIQ Dashboard**, click **Upload Report**.
2. Select **`banking_coverage.xml`** from this `sample_data/` directory.
3. The system will prompt you for the **Source Directory Absolute Path**. 
   - **IMPORTANT**: The AST engine needs to read the actual `.py` files. Because the backend runs inside a Docker container, you must provide the Docker container path.
   - Example Docker Paths:
     `/workspace/sample_projects/banking`
     `/workspace/sample_projects/auth`
     `/workspace/sample_projects/ecommerce`

## Recommended Demo Workflow

1. Upload `banking_coverage.xml`
2. Enter: `/workspace/sample_projects/banking`
3. Click Scan AST
4. Review Coverage Intelligence
5. Generate AI Tests

## Expected Outputs
The system will dynamically parse the `banking` Python files, reconcile them against the XML gaps, and generate `pytest` code targeting the missing branches. You should see a "Medium/High" risk score for `transfer_funds`.
