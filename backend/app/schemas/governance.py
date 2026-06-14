from pydantic import BaseModel
from typing import Optional

class GovernanceOverviewResponse(BaseModel):
    success: bool
    reports_analyzed: int
    functions_scanned: int
    coverage_gaps_found: int
    tests_generated: int
    average_coverage: float
    average_health_score: float
