from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.explainability import ExplainabilityResponse
from app.services.explainability_service import ExplainabilityService

router = APIRouter()

@router.get("/report/{report_id}", response_model=ExplainabilityResponse)
async def get_report_explainability(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get explainability trail for generated tests.
    """
    result = await ExplainabilityService.get_report_explainability(db, report_id)
    if not result:
        return ExplainabilityResponse(success=False, report_id=report_id, explanations=[])
    return result
