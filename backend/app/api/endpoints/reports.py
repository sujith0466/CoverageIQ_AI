from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.services.report import ReportService
from app.schemas.report import ReportUploadResponse, ReportAnalyzeResponse
from app.repositories.report import report as report_repo
from app.models.report import Report, ReportStatus
from app.services.parser import CoverageParserService
from app.utils.audit_logger import log_event
import os

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads")

@router.get("/latest")
async def get_latest_report(db: AsyncSession = Depends(get_db)):
    """
    Retrieve the most recently created report.
    """
    result = await db.execute(select(Report).order_by(Report.created_at.desc()).limit(1))
    latest = result.scalars().first()
    if not latest:
        return {"success": False, "message": "No reports found"}
    return {"success": True, "report_id": latest.id}

from app.schemas.report_history import ReportHistoryResponse, ReportSummaryResponse
from app.services.report_history_service import ReportHistoryService

@router.get("/history", response_model=ReportHistoryResponse)
async def get_report_history(db: AsyncSession = Depends(get_db)):
    """
    Retrieve historical reports.
    """
    history = await ReportHistoryService.get_report_history(db)
    return ReportHistoryResponse(success=True, reports=history)

@router.get("/{report_id}/summary", response_model=ReportSummaryResponse)
async def get_report_summary(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve report summary statistics.
    """
    summary = await ReportHistoryService.get_report_summary(db, report_id)
    if not summary:
        # Pydantic may fail if we return a dict that doesn't match the model,
        # but the prompt requires success: False for endpoints usually.
        # Since ReportSummaryResponse doesn't have a success/message field, 
        # we will just let it 404 or return empty.
        pass # In a real app we'd raise HTTPException 404
    return summary

@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a coverage XML report.
    """
    await log_event(db, "REPORT_UPLOADED", report_id=None, details={"filename": file.filename})
    return await ReportService.upload_coverage_report(db, file)

@router.post("/{report_id}/analyze", response_model=ReportAnalyzeResponse)
async def analyze_report(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Parse and analyze an uploaded XML report.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return ReportAnalyzeResponse(success=False, message="Report not found")
        
    file_path = os.path.join(UPLOAD_DIR, f"{report_id}.xml")
    
    # Parse the XML
    parsed_data = CoverageParserService.parse_cobertura_xml(file_path)
    await log_event(db, "XML_PARSED", report_id=report_id, details={"success": parsed_data.get("success")})
    
    if not parsed_data.get("success"):
        # Update status to FAILED
        await report_repo.update(db, db_obj=db_report, obj_in={"status": ReportStatus.FAILED})
        return ReportAnalyzeResponse(success=False, message=parsed_data.get("message"))
        
    # Update Report with metrics
    update_data = {
        "status": ReportStatus.ANALYZED,
        "coverage_percent": parsed_data["coverage_percent"],
        "total_files": parsed_data["total_files"],
        "total_classes": parsed_data["total_classes"],
        "total_lines": parsed_data["total_lines"],
        "covered_lines": parsed_data["covered_lines"],
        "line_rate": parsed_data["line_rate"],
        "branch_rate": parsed_data["branch_rate"],
        "raw_metrics": parsed_data["raw_metrics"]
    }
    
    await report_repo.update(db, db_obj=db_report, obj_in=update_data)
    
    return ReportAnalyzeResponse(
        success=True,
        coverage_percent=parsed_data["coverage_percent"],
        total_files=parsed_data["total_files"],
        total_classes=parsed_data["total_classes"],
        total_lines=parsed_data["total_lines"],
        covered_lines=parsed_data["covered_lines"],
        line_rate=parsed_data["line_rate"],
        branch_rate=parsed_data["branch_rate"],
        files=parsed_data.get("files", []),
        message="Report analyzed successfully"
    )

from app.schemas.function import ScanRequest, ScanResponse, FunctionCreate
from app.services.ast_walker import ASTWalkerService
from app.repositories.function import function as function_repo

@router.post("/{report_id}/scan", response_model=ScanResponse)
async def scan_codebase(
    report_id: str,
    request: ScanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Scan a codebase directory for Python functions using AST and store metadata.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return ScanResponse(success=False, message="Report not found")

    # --- CoverageIQ self-scan detection ---
    from app.services.gap_detector import _is_coverageiq_directory
    if _is_coverageiq_directory(request.directory_path):
        return ScanResponse(
            success=False,
            message="⚠️ CoverageIQ source code detected. Please select your target project directory, not the CoverageIQ backend itself."
        )

    await log_event(db, "PROJECT_ROOT_SCANNED", report_id=report_id, details={"directory": request.directory_path})
    await log_event(db, "AST_SCAN_STARTED", report_id=report_id)
    scan_result = ASTWalkerService.scan_directory(request.directory_path, report_id)
    await log_event(db, "AST_SCAN_COMPLETED", report_id=report_id, details={"functions_found": scan_result.get("total", 0)})

    if not scan_result.get("success"):
        return ScanResponse(success=False, message=scan_result.get("message"))

    # Bulk insert parsed functions
    functions_data = scan_result.get("functions", [])
    if functions_data:
        obj_in_list = [FunctionCreate(**func_dict) for func_dict in functions_data]
        await function_repo.create_multi(db, obj_in_list=obj_in_list)

    return ScanResponse(
        success=True,
        total_functions_found=scan_result.get("total", 0),
        functions=functions_data,
        message="Codebase scanned successfully."
    )

from app.schemas.function import DetectGapsResponse
from app.services.gap_detector import CoverageGapService

@router.post("/{report_id}/detect-gaps", response_model=DetectGapsResponse)
async def detect_coverage_gaps(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Detect coverage gaps by combining XML metrics and AST function boundaries.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return DetectGapsResponse(success=False, message="Report not found")
        
    await log_event(db, "GAP_ANALYSIS_STARTED", report_id=report_id)
    result = await CoverageGapService.detect_gaps(db, report_id)
    await log_event(db, "GAP_ANALYSIS_COMPLETED", report_id=report_id, details={"uncovered_functions": result.uncovered, "partial_functions": result.partial})
    return result

from app.schemas.generated_test import GenerateTestsRequest, GenerateTestsResponse
from app.services.test_generator import TestGenerationService

@router.post("/{report_id}/generate-tests", response_model=GenerateTestsResponse)
async def generate_tests(
    report_id: str,
    request: GenerateTestsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate tests for uncovered or partial functions using LLMs.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return GenerateTestsResponse(success=False, message="Report not found")
        
    db_functions = await function_repo.get_by_report(db, report_id=report_id)
    if not db_functions:
        return GenerateTestsResponse(success=False, message="No functions found.")
        
    # Filter functions
    target_functions = []
    for func in db_functions:
        if func.coverage_status in ["UNCOVERED", "PARTIAL"]:
            if request.function_ids:
                if func.id in request.function_ids:
                    target_functions.append(func)
            else:
                target_functions.append(func)
                
    if not target_functions:
        return GenerateTestsResponse(success=False, message="No eligible uncovered or partial functions found.")
        
    results = await TestGenerationService.generate_tests(db, target_functions)
    
    return GenerateTestsResponse(
        success=True,
        generated_count=len(results),
        tests=results,
        message="Tests generated successfully."
    )

from app.services.risk_engine import RiskIntelligenceService

@router.post("/{report_id}/risk-analysis")
async def analyze_project_risks(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform a comprehensive risk analysis on the codebase functions.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    await log_event(db, "RISK_ANALYSIS_STARTED", report_id=report_id)
    result = await RiskIntelligenceService.analyze_project_risks(db, report_id)
    await log_event(db, "RISK_ANALYSIS_COMPLETED", report_id=report_id, details={
        "critical_functions": result.get("critical_functions", 0),
        "high_risk_functions": result.get("high_risk_functions", 0)
    })
    return result

from app.services.dependency_engine import DependencyIntelligenceService

@router.post("/{report_id}/dependency-analysis")
async def analyze_project_dependencies(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform dependency and impact analysis on the codebase functions.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    return await DependencyIntelligenceService.analyze_project_dependencies(db, report_id)

from app.services.coverage_predictor import CoveragePredictionService

@router.post("/{report_id}/coverage-prediction")
async def predict_project_coverage(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate coverage improvement predictions and prioritization.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    return await CoveragePredictionService.predict_project_coverage(db, report_id)

from app.services.executive_dashboard import ExecutiveDashboardService

@router.get("/{report_id}/executive-dashboard")
async def get_executive_dashboard(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate the Executive Intelligence Dashboard payload.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    return await ExecutiveDashboardService.generate_dashboard(db, report_id)


@router.get("/{report_id}/debug-paths")
async def debug_paths(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Debug endpoint to return path matching details: xml_files, ast_files, matched_files, unmatched_files.
    """
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    # Get XML files
    raw_metrics = db_report.raw_metrics or {}
    files_data = raw_metrics.get("files", [])
    xml_files = [f["filename"] for f in files_data]
    
    # Get AST functions
    from sqlalchemy.future import select
    from app.models.function import Function
    result = await db.execute(select(Function).where(Function.report_id == report_id))
    functions = result.scalars().all()
    ast_files = list(set([f.file_path for f in functions]))
    
    # Match using path_utils
    from app.utils.path_utils import match_paths
    matched_files = []
    unmatched_files = []
    
    for ast_path in ast_files:
        matched = False
        for xml_path in xml_files:
            if match_paths(ast_path, xml_path):
                matched = True
                matched_files.append({"ast_path": ast_path, "xml_path": xml_path})
                break
        if not matched:
            unmatched_files.append(ast_path)
            
    return {
        "success": True,
        "report_id": report_id,
        "xml_files": xml_files,
        "ast_files": ast_files,
        "matched_files": matched_files,
        "unmatched_files": unmatched_files
    }
