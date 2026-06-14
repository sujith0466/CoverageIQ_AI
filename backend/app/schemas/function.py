from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FunctionBase(BaseModel):
    report_id: str
    name: str
    file_path: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    parameters: Optional[list] = None
    docstring: Optional[str] = None
    function_type: Optional[str] = None
    is_async: Optional[bool] = False
    return_type: Optional[str] = None
    decorators: Optional[list] = None
    called_functions: Optional[list] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    risk_reasons: Optional[list] = None
    risk_priority_rank: Optional[int] = None
    dependency_count: Optional[int] = 0
    impact_radius: Optional[int] = 0
    critical_dependency_score: Optional[float] = None
    dependency_level: Optional[str] = None
    
    potential_coverage_gain: Optional[float] = None
    test_priority_score: Optional[float] = None
    recommended_test_order: Optional[int] = None
    recommendation_category: Optional[str] = None
    
    coverage_status: Optional[str] = None
    coverage_percent: Optional[float] = None
    executable_lines: Optional[int] = None
    covered_lines: Optional[int] = None
    coverage_details: Optional[dict] = None

class ScanRequest(BaseModel):
    directory_path: str

class ScanResponse(BaseModel):
    success: bool
    total_functions_found: Optional[int] = 0
    functions: Optional[list] = []
    message: Optional[str] = None

class DetectGapsResponse(BaseModel):
    success: bool
    total_functions: Optional[int] = 0
    covered: Optional[int] = 0
    partial: Optional[int] = 0
    uncovered: Optional[int] = 0
    functions: Optional[list] = []
    message: Optional[str] = None

class FunctionCreate(FunctionBase):
    pass

class FunctionUpdate(FunctionBase):
    pass

class FunctionInDBBase(FunctionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class Function(FunctionInDBBase):
    pass
