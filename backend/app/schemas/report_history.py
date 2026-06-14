from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReportHistoryItem(BaseModel):
    report_id: str
    uploaded_at: datetime
    coverage_percent: Optional[float] = None
    files_analyzed: int
    functions_found: int
    tests_generated: int
    latest_status: Optional[str] = None

class ReportHistoryResponse(BaseModel):
    success: bool
    reports: List[ReportHistoryItem]

class ReportSummaryResponse(BaseModel):
    report_id: str
    coverage_percent: Optional[float] = None
    files_analyzed: int
    functions_found: int
    covered_functions: int
    partial_functions: int
    uncovered_functions: int
    generated_tests: int
    health_score: float
    previous_coverage: Optional[float] = None
    current_coverage: Optional[float] = None
    coverage_change: Optional[float] = None
