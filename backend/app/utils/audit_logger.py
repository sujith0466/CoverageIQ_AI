import logging
import json
import sys
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

# Configure stdout logger for structured enterprise logging
logger = logging.getLogger("CoverageIQ_Audit")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

async def log_event(
    db: AsyncSession,
    event_type: str,
    report_id: str = None,
    entity_type: str = None,
    entity_id: str = None,
    details: Dict[str, Any] = None
):
    """
    Safely creates an audit log entry in the database and emits a structured stdout log.
    If the database insert fails, the error is caught and printed, ensuring existing workflows do not break.
    """
    # 1. Emit structured stdout log
    msg = f"[AUDIT] {event_type}"
    log_data = {"report_id": report_id, "entity_type": entity_type, "entity_id": entity_id, "details": details}
    # Filter out None values for cleaner logs
    clean_data = {k: v for k, v in log_data.items() if v is not None}
    if clean_data:
        msg += f" {json.dumps(clean_data)}"
    logger.info(msg)

    # 2. Persist to database
    try:
        audit_log = AuditLog(
            event_type=event_type,
            report_id=report_id or "SYSTEM",
            entity_type=entity_type,
            entity_id=entity_id,
            details_json=details
        )
        db.add(audit_log)
        await db.commit()
    except Exception as e:
        # Rollback the session so subsequent DB operations in the same transaction aren't poisoned
        await db.rollback()
        logger.error(f"Failed to persist audit log to database: {str(e)}")
