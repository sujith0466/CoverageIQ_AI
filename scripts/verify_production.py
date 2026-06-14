import requests
import json
import time

LIVE_API_URL = "https://coverageiq-ai.onrender.com"
FRONTEND_ORIGIN = "https://coverage-iq-ai.vercel.app"

def print_step(title):
    print(f"\n[{title}]")
    print("-" * 40)

def test_health():
    print_step("1. Health Check")
    res = requests.get(f"{LIVE_API_URL}/api/health")
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code == 200

def test_cors():
    print_step("2. CORS Preflight Check")
    headers = {
        "Origin": FRONTEND_ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    res = requests.options(f"{LIVE_API_URL}/api/reports/upload", headers=headers)
    print(f"Status Code: {res.status_code}")
    print(f"Access-Control-Allow-Origin: {res.headers.get('Access-Control-Allow-Origin')}")
    assert res.status_code in [200, 204]
    assert res.headers.get("Access-Control-Allow-Origin") == FRONTEND_ORIGIN

def test_workflow():
    print_step("3. CoverageIQ Workflow (Banking)")
    
    # 3.1 Upload
    with open("sample_projects/banking/banking_coverage.xml", "rb") as f:
        files = {"file": ("banking_coverage.xml", f, "text/xml")}
        res = requests.post(f"{LIVE_API_URL}/api/reports/upload", files=files)
    
    upload_data = res.json()
    print(f"Upload Response: {upload_data}")
    assert upload_data["success"] is True
    report_id = upload_data["report_id"]
    
    # 3.2 Analyze
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/analyze")
    print(f"Analyze Coverage: {res.json().get('coverage_percent')}%")
    
    # 3.3 Scan (AST)
    data = {"directory_path": "../sample_projects/banking"}
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/scan", json=data)
    scan_data = res.json()
    print(f"AST Scan Functions Found: {scan_data.get('functions_found')}")
    
    # 3.4 Detect Gaps
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/detect-gaps")
    gaps = res.json()
    print(f"Gaps -> Covered: {gaps.get('covered')} Partial: {gaps.get('partial')} Uncovered: {gaps.get('uncovered')}")
    
    # 3.5 Risk Engine
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/risk-analysis")
    print(f"Risk Engines -> High: {res.json().get('high_risk_functions')}")
    
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/dependency-analysis")
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/coverage-prediction")
    
    # 3.6 Test Generation
    print("Generating Tests (waiting for LLM...)")
    res = requests.post(f"{LIVE_API_URL}/api/reports/{report_id}/generate-tests")
    tests = res.json()
    print(f"Tests Generated: {tests.get('generated_count')}")

def test_governance():
    print_step("4. Governance Layer")
    res = requests.get(f"{LIVE_API_URL}/api/governance/overview")
    print(f"Overview Status: {res.status_code}")
    print(f"Total Reports: {res.json().get('total_reports')}")
    
    res = requests.get(f"{LIVE_API_URL}/api/reports/history")
    print(f"History Entries: {len(res.json().get('reports', []))}")

if __name__ == "__main__":
    try:
        test_health()
        test_cors()
        test_workflow()
        test_governance()
        print("\n=> ALL AUDIT CHECKS PASSED <= ")
    except Exception as e:
        print(f"\n=> AUDIT FAILED: {e}")
