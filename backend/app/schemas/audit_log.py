from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class AuditLogBase(BaseModel):
    event_type: str
    report_id: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    details_json: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogListResponse(BaseModel):
    success: bool
    audit_logs: List[AuditLogResponse]
    message: Optional[str] = None
