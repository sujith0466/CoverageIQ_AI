from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import CRUDBase
from app.models.generated_test import GeneratedTest
from app.schemas.generated_test import GeneratedTestCreate, GeneratedTestUpdate

class CRUDGeneratedTest(CRUDBase[GeneratedTest, GeneratedTestCreate, GeneratedTestUpdate]):
    async def get_by_function(self, db: AsyncSession, *, function_id: str) -> List[GeneratedTest]:
        result = await db.execute(select(GeneratedTest).where(GeneratedTest.function_id == function_id))
        return result.scalars().all()

generated_test = CRUDGeneratedTest(GeneratedTest)
