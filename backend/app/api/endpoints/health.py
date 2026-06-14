from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.health import HealthService

router = APIRouter()

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        is_healthy = await HealthService.check_db_health(db)
        if not is_healthy:
            raise HTTPException(status_code=503, detail="Database connection failed")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")
