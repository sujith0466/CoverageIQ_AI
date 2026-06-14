import requests
import time
import json
import os

API_URL = 'http://localhost:8000/api/reports'

# 1. Upload
print('1. Uploading...')
res = requests.post(f'{API_URL}/upload', files={'file': open('sample_data.xml', 'rb')})
report_id = res.json().get('report_id')
print(f'Report ID: {report_id}')

# 2. Analyze
print('2. Analyze...')
res = requests.post(f'{API_URL}/{report_id}/analyze')
print(res.json().get('success'))

# 3. AST Scan (assuming directory_path is .)
print('3. AST Scan...')
res = requests.post(f'{API_URL}/{report_id}/scan', json={'directory_path': '.'})
print(res.json().get('success'))

# 4. Detect Gaps
print('4. Detect Gaps...')
res = requests.post(f'{API_URL}/{report_id}/detect-gaps')
print(res.json().get('success'))

# 5. Risk Analysis
print('5. Risk Analysis...')
res = requests.post(f'{API_URL}/{report_id}/risk-analysis')
print(res.json().get('success'))

# 6. Dependency
print('6. Dependency...')
res = requests.post(f'{API_URL}/{report_id}/dependency-analysis')
print(res.json().get('success'))

# 7. Prediction
print('7. Prediction...')
res = requests.post(f'{API_URL}/{report_id}/coverage-prediction')
print(res.json().get('success'))

# 8. Generate Tests
print('8. Generate Tests...')
res = requests.post(f'{API_URL}/{report_id}/generate-tests', json={'function_ids': []})
data = res.json()
print(f"Success: {data.get('success')}, Count: {data.get('generated_count')}")
if data.get('tests'):
    print("Sample generated test:")
    print(json.dumps(data['tests'][0], indent=2))
