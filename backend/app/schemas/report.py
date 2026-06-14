from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.report import ReportStatus

class ReportBase(BaseModel):
    filename: str
    coverage_percent: Optional[float] = None
    total_files: Optional[int] = None
    total_classes: Optional[int] = None
    total_lines: Optional[int] = None
    covered_lines: Optional[int] = None
    line_rate: Optional[float] = None
    branch_rate: Optional[float] = None
    raw_metrics: Optional[Dict[str, Any]] = None
    status: ReportStatus = ReportStatus.UPLOADED

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class ReportInDBBase(ReportBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class Report(ReportInDBBase):
    pass

class ReportUploadResponse(BaseModel):
    success: bool
    report_id: Optional[str] = None
    filename: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

from typing import Optional, Dict, Any, List

class FileCoverage(BaseModel):
    filename: str
    lines_valid: int
    lines_covered: int
    coverage_percent: float

class ReportAnalyzeResponse(BaseModel):
    success: bool
    coverage_percent: Optional[float] = None
    total_files: Optional[int] = None
    total_classes: Optional[int] = None
    total_lines: Optional[int] = None
    covered_lines: Optional[int] = None
    line_rate: Optional[float] = None
    branch_rate: Optional[float] = None
    files: Optional[List[FileCoverage]] = []
    message: Optional[str] = None
