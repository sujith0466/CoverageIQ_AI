import requests

def test_upload():
    # Test valid XML
    with open("sample_projects/banking/banking_coverage.xml", "rb") as f:
        res = requests.post("http://localhost:8000/api/reports/upload", files={"file": ("coverage.xml", f, "text/xml")})
        print("Valid XML upload:", res.json())
        
    # Test invalid extension
    with open("sample_projects/banking/banking_coverage.xml", "rb") as f:
        res = requests.post("http://localhost:8000/api/reports/upload", files={"file": ("coverage.txt", f, "text/plain")})
        print("Invalid extension upload:", res.json())
        
    # Test invalid content type for XML
    with open("sample_projects/banking/banking_coverage.xml", "rb") as f:
        res = requests.post("http://localhost:8000/api/reports/upload", files={"file": ("coverage.xml", f, "application/json")})
        print("Invalid content type XML upload:", res.json())

    # Test valid ZIP
    with open("sample_projects/banking/banking_coverage.xml", "rb") as f: # Just mocking a file
        res = requests.post("http://localhost:8000/api/reports/upload", files={"file": ("project.zip", f, "application/zip")})
        print("Valid ZIP upload:", res.json())
        
if __name__ == "__main__":
    test_upload()
