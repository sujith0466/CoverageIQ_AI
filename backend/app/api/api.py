from fastapi import APIRouter
from app.api.endpoints import health, version, reports, audit, explainability, governance

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(version.router, prefix="/version", tags=["version"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(explainability.router, prefix="/explainability", tags=["explainability"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
