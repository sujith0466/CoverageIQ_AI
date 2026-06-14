import requests
import json
import time

API_URL = "http://localhost:8000/api"

# 1. Upload
print("Uploading coverage.xml...")
with open("coverage.xml", "rb") as f:
    res = requests.post(f"{API_URL}/reports/upload", files={"file": f})
report_id = res.json()["report_id"]
print(f"Report ID: {report_id}")

# 2. Analyze
print("Analyzing report...")
res = requests.post(f"{API_URL}/reports/{report_id}/analyze")
print("Analyze Response:", res.json()["success"])

# 3. AST Scan
print("Running AST Scan on /workspace/sample_project...")
res = requests.post(
    f"{API_URL}/reports/{report_id}/scan",
    json={"directory_path": "/workspace/sample_project"}
)
scan_data = res.json()
print(f"AST Scan Response Success: {scan_data['success']}")
print(f"Total Functions Found: {scan_data['total_functions_found']}")
for func in scan_data.get('functions', []):
    print(f"  - {func['name']} ({func['file_path']})")

# 4. Detect Gaps
print("Detecting Coverage Gaps...")
res = requests.post(f"{API_URL}/reports/{report_id}/detect-gaps")
gap_data = res.json()
print("Gap Detection Results:")
print(f"  Covered: {gap_data.get('covered', 0)}")
print(f"  Partial: {gap_data.get('partial', 0)}")
print(f"  Uncovered: {gap_data.get('uncovered', 0)}")

# 5. Risk Analysis
print("Analyzing Risks...")
res = requests.post(f"{API_URL}/reports/{report_id}/risk-analysis")
risk_data = res.json()
print(f"Risk Analysis Success: {risk_data.get('success')}")
print(f"Project Risk Score: {risk_data.get('project_risk_score')}")

# 6. Dependency Analysis
print("Analyzing Dependencies...")
res = requests.post(f"{API_URL}/reports/{report_id}/dependency-analysis")
dep_data = res.json()
print(f"Dependency Analysis Success: {dep_data.get('success')}")
print(f"Largest Impact: {dep_data.get('largest_impact_function')} (Radius: {dep_data.get('largest_impact_radius')})")
print(f"Dependency Summary: {dep_data.get('summary')}")

# 7. Coverage Prediction
print("Predicting Coverage Optimization...")
res = requests.post(f"{API_URL}/reports/{report_id}/coverage-prediction")
pred_data = res.json()
print(f"Coverage Prediction Success: {pred_data.get('success')}")
print(f"Current Coverage: {pred_data.get('current_coverage')}%")
print(f"Potential Coverage: {pred_data.get('potential_coverage')}%")
# 8. Executive Dashboard
print("Generating Executive Dashboard...")
res = requests.get(f"{API_URL}/reports/{report_id}/executive-dashboard")
dash_data = res.json()
print(f"Dashboard Generation Success: {dash_data.get('success')}")
print(f"Project Health Score: {dash_data.get('project_health_score')} ({dash_data.get('status')})")
print(f"Testing Readiness Score: {dash_data.get('testing', {}).get('health_score')}%")

with open("ast_test_output.json", "w") as f:
    json.dump({"scan": scan_data, "gaps": gap_data, "risks": risk_data, "deps": dep_data, "prediction": pred_data, "dashboard": dash_data}, f, indent=2)
