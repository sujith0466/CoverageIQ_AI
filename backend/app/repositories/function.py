from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.function import Function
from app.schemas.function import FunctionCreate, FunctionUpdate

class CRUDFunction(CRUDBase[Function, FunctionCreate, FunctionUpdate]):
    async def create_multi(self, db: AsyncSession, *, obj_in_list: List[FunctionCreate]) -> List[Function]:
        db_objs = [Function(**obj_in.model_dump()) for obj_in in obj_in_list]
        db.add_all(db_objs)
        await db.commit()
        return db_objs

    async def get_by_report(self, db: AsyncSession, *, report_id: str) -> List[Function]:
        from sqlalchemy.future import select
        result = await db.execute(select(Function).where(Function.report_id == report_id))
        return result.scalars().all()

function = CRUDFunction(Function)
