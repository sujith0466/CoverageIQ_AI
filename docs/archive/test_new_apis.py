import requests
import json

def test_new_apis():
    print("Testing new APIs...\n")
    
    # 1. Test Governance Overview
    print("--- Governance Overview ---")
    res = requests.get('http://localhost:8000/api/governance/overview')
    print(json.dumps(res.json(), indent=2))
    
    # 2. Test Report History
    print("\n--- Report History ---")
    res = requests.get('http://localhost:8000/api/reports/history')
    history_data = res.json()
    print(f"Success: {history_data.get('success')}, count: {len(history_data.get('reports', []))}")
    
    if history_data.get('reports'):
        first_report_id = history_data['reports'][0]['report_id']
        
        # 3. Test Report Summary
        print(f"\n--- Report Summary for {first_report_id} ---")
        res = requests.get(f'http://localhost:8000/api/reports/{first_report_id}/summary')
        print(json.dumps(res.json(), indent=2))
        
        # 4. Test Explainability
        print(f"\n--- Explainability for {first_report_id} ---")
        res = requests.get(f'http://localhost:8000/api/explainability/report/{first_report_id}')
        print(json.dumps(res.json(), indent=2)[:500] + " ... (truncated)")

if __name__ == "__main__":
    test_new_apis()
