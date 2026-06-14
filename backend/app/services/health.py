from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class HealthService:
    @staticmethod
    async def check_db_health(db: AsyncSession) -> bool:
        try:
            await db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
