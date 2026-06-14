import requests
import json
import asyncio
from app.db.session import AsyncSessionLocal
from app.models.function import Function
from app.models.report import Report
from sqlalchemy.future import select

API_URL = 'http://localhost:8000/api/reports'

async def main():
    res = requests.get(f'{API_URL}/latest')
    report_id = res.json().get('report_id')

    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Function).where(Function.report_id == report_id).limit(2))
        funcs = res.scalars().all()
        for f in funcs:
            f.coverage_status = 'UNCOVERED'
            f.risk_level = 'HIGH'
            f.test_priority_score = 95.0
            print(f"Mocking function: {f.name}")
        await db.commit()
    
    print("Generating tests...")
    res = requests.post(f'{API_URL}/{report_id}/generate-tests', json={'function_ids': []})
    data = res.json()
    print(f"Success: {data.get('success')}, Count: {data.get('generated_count')}")
    if data.get('tests'):
        print(json.dumps(data['tests'][0], indent=2))

if __name__ == '__main__':
    asyncio.run(main())
