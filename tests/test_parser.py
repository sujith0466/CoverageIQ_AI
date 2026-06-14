import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app.services.parser import CoverageParserService

XML_TEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xml_tests'))

def get_xml_path(filename: str) -> str:
    return os.path.join(XML_TEST_DIR, filename)

def test_valid_cobertura_parses_successfully():
    result = CoverageParserService.parse_cobertura_xml(get_xml_path('valid_cobertura.xml'))
    assert result["success"] is True
    assert result["coverage_percent"] == 75.0
    assert result["total_files"] == 1

def test_namespace_cobertura_parses_successfully():
    result = CoverageParserService.parse_cobertura_xml(get_xml_path('valid_coveragepy.xml'))
    assert result["success"] is True
    assert result["coverage_percent"] == 75.0

def test_generic_xml_is_rejected_correctly():
    result = CoverageParserService.parse_cobertura_xml(get_xml_path('generic_catalog.xml'))
    assert result["success"] is False
    assert "Expected root tag <coverage>" in result["message"]
    assert "found <catalog>" in result["message"]

def test_jacoco_xml_is_rejected_correctly():
    result = CoverageParserService.parse_cobertura_xml(get_xml_path('valid_jacoco.xml'))
    assert result["success"] is False
    assert "found <report>" in result["message"]

def test_broken_syntax_xml_is_rejected():
    result = CoverageParserService.parse_cobertura_xml(get_xml_path('broken_syntax.xml'))
    assert result["success"] is False
    assert "Failed to parse XML file" in result["message"]
