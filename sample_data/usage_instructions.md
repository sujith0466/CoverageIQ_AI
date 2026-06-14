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
   - **IMPORTANT**: The AST engine needs to read the actual `.py` files. You must point this to the `sample_projects/banking` directory in your cloned repository.
   - Example Windows: `D:/CoverageIQ-AI/sample_projects/banking`
   - Example Mac/Linux: `/Users/username/CoverageIQ-AI/sample_projects/banking`
4. Click **Analyze**.

## Expected Outputs
The system will dynamically parse the `banking` Python files, reconcile them against the XML gaps, and generate `pytest` code targeting the missing branches. You should see a "Medium/High" risk score for `transfer_funds`.
