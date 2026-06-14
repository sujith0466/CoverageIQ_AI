import os
import sys
import defusedxml.ElementTree as ET

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app.services.parser import CoverageParserService

test_files = [
    "valid_cobertura.xml",
    "valid_jacoco.xml",
    "valid_coveragepy.xml",
    "generic_catalog.xml",
    "broken_syntax.xml"
]

def analyze_xml_file(filepath):
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    print(f"--- Analyzing: {filename} ---")
    print(f"Size: {size} bytes")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(200)
    print(f"Preview: {content!r}...")
    
    # Simulate parser.py logic
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        root_tag = root.tag
        
        print(f"Root tag extracted: {root_tag}")
        
        if '}' in root_tag:
            namespace, tag = root_tag.split('}', 1)
            namespace = namespace.strip('{')
            print(f"Namespace detected: {namespace}")
            print(f"Tag without namespace: {tag}")
        else:
            print("Namespace detected: None")
            tag = root_tag
            
        print(f"Is recognised as coverage root tag by strict check? {root_tag == 'coverage'}")
        
        # Test actual parser
        result = CoverageParserService.parse_cobertura_xml(filepath)
        print(f"Parser Result: {result}")
        
    except ET.ParseError as e:
        print(f"XML Parsing Failed: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    print("\n")

if __name__ == "__main__":
    for f in test_files:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xml_tests', f))
        if os.path.exists(path):
            analyze_xml_file(path)
        else:
            print(f"File not found: {path}")
