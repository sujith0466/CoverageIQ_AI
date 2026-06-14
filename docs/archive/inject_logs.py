import os

reports_path = 'frontend/../backend/app/api/endpoints/reports.py'
with open(reports_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Inject logger import
if 'from app.utils.logger import log_event' not in content:
    content = content.replace('from app.services.parser import CoverageParserService', 'from app.services.parser import CoverageParserService\nfrom app.utils.logger import log_event')

# Inject logs
# 1. upload_report
if 'UPLOAD_RECEIVED' not in content:
    content = content.replace(
        '    """\n    Upload a coverage XML report.\n    """',
        '    """\n    Upload a coverage XML report.\n    """\n    log_event("UPLOAD_RECEIVED", {"filename": file.filename})'
    )

# 2. analyze_report
if 'XML_PARSED' not in content:
    content = content.replace(
        '    # Parse the XML\n    parsed_data = CoverageParserService.parse_cobertura_xml(file_path)',
        '    # Parse the XML\n    parsed_data = CoverageParserService.parse_cobertura_xml(file_path)\n    log_event("XML_PARSED", {"report_id": report_id, "success": parsed_data.get("success")})'
    )

# 3. scan_codebase
if 'PROJECT_ROOT_SCANNED' not in content:
    content = content.replace(
        '    scan_result = ASTWalkerService.scan_directory(request.directory_path, report_id)',
        '    log_event("PROJECT_ROOT_SCANNED", {"report_id": report_id, "directory": request.directory_path})\n    log_event("AST_SCAN_STARTED", {"report_id": report_id})\n    scan_result = ASTWalkerService.scan_directory(request.directory_path, report_id)\n    log_event("AST_SCAN_COMPLETED", {"report_id": report_id, "functions_found": scan_result.get("total", 0)})'
    )

with open(reports_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Logs injected to reports.py")
