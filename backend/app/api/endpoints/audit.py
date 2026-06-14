from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogListResponse, AuditLogResponse

router = APIRouter()

@router.get("/report/{report_id}", response_model=AuditLogListResponse)
async def get_report_audit_logs(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve audit logs for a specific report, ordered by creation date descending.
    """
    query = select(AuditLog).where(AuditLog.report_id == report_id).order_by(AuditLog.created_at.desc())
    result = await db.execute(query)
    logs = result.scalars().all()
    
    return AuditLogListResponse(
        success=True,
        audit_logs=[AuditLogResponse.model_validate(log) for log in logs],
        message=f"Found {len(logs)} audit logs"
    )
