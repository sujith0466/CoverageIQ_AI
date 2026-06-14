import requests
import json
import sys

def test_api():
    try:
        response = requests.get('http://localhost:8000/api/audit/report/0b5721cf-9ad6-4ee1-9380-187a39bb5745')
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
