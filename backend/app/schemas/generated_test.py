from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeneratedTestBase(BaseModel):
    function_id: str
    test_code: str
    confidence_score: Optional[float] = None
    test_quality_score: Optional[float] = None
    model_used: Optional[str] = None
    generation_status: Optional[str] = "PENDING"
    prompt_version: Optional[str] = None
    generated_at: Optional[datetime] = None

class GenerateTestsRequest(BaseModel):
    function_ids: Optional[list[str]] = None

class GenerateTestsResponse(BaseModel):
    success: bool
    generated_count: Optional[int] = 0
    tests: Optional[list] = []
    message: Optional[str] = None

class GeneratedTestCreate(GeneratedTestBase):
    pass

class GeneratedTestUpdate(GeneratedTestBase):
    pass

class GeneratedTestInDBBase(GeneratedTestBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class GeneratedTest(GeneratedTestInDBBase):
    pass
