import requests
import json

API_URL = 'http://localhost:8000/api/reports'
xml_file = 'sample_projects/dragon_bank/coverage.xml'
src_dir = '/workspace/sample_projects/dragon_bank'

print("Uploading Dragon Bank...")
with open(xml_file, 'rb') as f:
    res = requests.post(f'{API_URL}/upload', files={'file': f})
    
data = res.json()
report_id = data.get('report_id')
print(f"Report ID: {report_id}")

print("Analyzing...")
res = requests.post(f'{API_URL}/{report_id}/analyze')
print(res.json())

print("Scanning AST...")
res = requests.post(f'{API_URL}/{report_id}/scan', json={"directory_path": src_dir})
print(res.json())

print("Detecting Gaps...")
res = requests.post(f'{API_URL}/{report_id}/detect-gaps')
print(res.json())

print("\n=== DEBUG ENDPOINT ===")
res = requests.get(f'{API_URL}/{report_id}/debug-paths')
debug_data = res.json()
print(json.dumps(debug_data, indent=2))
