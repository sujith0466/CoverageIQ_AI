from pydantic import BaseModel
from typing import List, Optional

class ExplainabilityItem(BaseModel):
    function: str
    coverage: Optional[float] = 0.0
    risk: str
    reason: List[str]
    generated_test_id: Optional[str] = None

class ExplainabilityResponse(BaseModel):
    success: bool
    report_id: str
    explanations: List[ExplainabilityItem]
