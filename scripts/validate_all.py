import requests
import json

API_URL = 'http://localhost:8000/api/reports'
PROJECTS = [
    ('Banking', 'sample_projects/banking/banking_coverage.xml', '/workspace/sample_projects/banking'),
    ('E-Commerce', 'sample_projects/ecommerce/ecommerce_coverage.xml', '/workspace/sample_projects/ecommerce'),
    ('Auth', 'sample_projects/auth/auth_coverage.xml', '/workspace/sample_projects/auth'),
    ('Inventory', 'sample_projects/inventory/inventory_coverage.xml', '/workspace/sample_projects/inventory'),
    ('Legacy System', 'sample_projects/legacy_system/legacy_coverage.xml', '/workspace/sample_projects/legacy_system'),
]

RESULTS = []

for name, xml_file, src_dir in PROJECTS:
    print(f'\n{"="*50}')
    print(f'PROJECT: {name}')
    print('='*50)
    
    try:
        # 1. Upload
        with open(xml_file, 'rb') as f:
            res = requests.post(f'{API_URL}/upload', files={'file': (xml_file.split('/')[-1], f, 'text/xml')})
        report_id = res.json().get('report_id')
        print(f'[1] Upload: {res.json().get("success")} | report_id={report_id}')
        
        if not report_id:
            RESULTS.append({'project': name, 'status': 'FAIL', 'error': 'Upload failed'})
            continue
        
        # 2. Analyze
        res = requests.post(f'{API_URL}/{report_id}/analyze')
        print(f'[2] Analyze: {res.json().get("success")} | coverage={res.json().get("coverage_percent")}%')
        
        # 3. AST Scan
        res = requests.post(f'{API_URL}/{report_id}/scan', json={'directory_path': src_dir})
        scan_data = res.json()
        print(f'[3] AST Scan: {scan_data.get("success")} | functions={scan_data.get("total_functions_found")}')
        
        if not scan_data.get('success'):
            RESULTS.append({'project': name, 'status': 'FAIL', 'error': scan_data.get('message')})
            continue
        
        # 4. Detect Gaps
        res = requests.post(f'{API_URL}/{report_id}/detect-gaps')
        gap = res.json()
        covered = gap.get('covered', 0)
        partial = gap.get('partial', 0)
        uncovered = gap.get('uncovered', 0)
        total = gap.get('total_functions', 0)
        print(f'[4] Gaps: covered={covered} partial={partial} uncovered={uncovered} total={total}')
        
        # Check for UNKNOWN
        funcs = gap.get('functions', [])
        unknowns = [f for f in funcs if f.get('coverage_status') == 'UNKNOWN']
        print(f'    UNKNOWN statuses: {len(unknowns)}')
        
        # 5. Risk Analysis
        res = requests.post(f'{API_URL}/{report_id}/risk-analysis')
        risk = res.json()
        print(f'[5] Risk: success={risk.get("success")} high={risk.get("summary", {}).get("high_risk")} med={risk.get("summary", {}).get("medium_risk")} low={risk.get("summary", {}).get("low_risk")}')
        
        # 6. Dependency
        res = requests.post(f'{API_URL}/{report_id}/dependency-analysis')
        dep = res.json()
        print(f'[6] Deps: success={dep.get("success")} critical={dep.get("summary", {}).get("critical_dependencies")}')
        
        # 7. Prediction
        res = requests.post(f'{API_URL}/{report_id}/coverage-prediction')
        pred = res.json()
        print(f'[7] Prediction: success={pred.get("success")} current={pred.get("current_coverage")} potential={pred.get("potential_coverage")}')
        
        # 8. Executive Dashboard
        res = requests.get(f'{API_URL}/{report_id}/executive-dashboard')
        dash = res.json()
        print(f'[8] Dashboard: success={dash.get("success")} health={dash.get("project_health_score")} status={dash.get("status")}')
        
        # 9. Generate Tests
        res = requests.post(f'{API_URL}/{report_id}/generate-tests', json={'function_ids': []})
        tests = res.json()
        print(f'[9] Tests: success={tests.get("success")} count={tests.get("generated_count")}')
        
        result = {
            'project': name,
            'status': 'PASS' if (covered + partial + uncovered == total and len(unknowns) == 0) else 'PARTIAL',
            'covered': covered,
            'partial': partial,
            'uncovered': uncovered,
            'unknown': len(unknowns),
            'total': total,
            'health_score': dash.get('project_health_score'),
            'health_status': dash.get('status'),
            'tests_generated': tests.get('generated_count', 0)
        }
        RESULTS.append(result)
        
    except Exception as e:
        print(f'ERROR: {e}')
        RESULTS.append({'project': name, 'status': 'ERROR', 'error': str(e)})

print('\n\n' + '='*60)
print('VALIDATION MATRIX')
print('='*60)
for r in RESULTS:
    print(json.dumps(r, indent=2))
