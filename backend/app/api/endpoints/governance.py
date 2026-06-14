from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.governance import GovernanceOverviewResponse
from app.services.governance_service import GovernanceService

router = APIRouter()

@router.get("/overview", response_model=GovernanceOverviewResponse)
async def get_governance_overview(
    db: AsyncSession = Depends(get_db)
):
    """
    Get system-wide governance metrics.
    """
    return await GovernanceService.get_overview(db)
