import pytest
import os
import sys

# Ensure backend path is loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.services.parser import CoverageParserService

def test_xml_parsing_succeeds():
    # Load the sample XML
    xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sample_data/banking_coverage.xml'))
    
    result = CoverageParserService.parse_cobertura_xml(xml_path)
    
    assert result is not None
    assert result.get("success") is True
    assert result.get("total_classes") > 0
    assert result.get("files") is not None
    assert len(result.get("files")) > 0
    assert result.get("line_rate") is not None
