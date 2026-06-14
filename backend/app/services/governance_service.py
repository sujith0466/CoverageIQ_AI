from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.report import Report
from app.models.function import Function
from app.models.generated_test import GeneratedTest
from app.schemas.governance import GovernanceOverviewResponse

class GovernanceService:
    @classmethod
    async def get_overview(cls, db: AsyncSession) -> GovernanceOverviewResponse:
        reports_query = select(func.count(Report.id))
        reports_analyzed = (await db.execute(reports_query)).scalar() or 0
        
        funcs_query = select(func.count(Function.id))
        functions_scanned = (await db.execute(funcs_query)).scalar() or 0
        
        gaps_query = select(func.count(Function.id)).where(Function.coverage_status.in_(["UNCOVERED", "PARTIAL"]))
        coverage_gaps_found = (await db.execute(gaps_query)).scalar() or 0
        
        tests_query = select(func.count(GeneratedTest.id))
        tests_generated = (await db.execute(tests_query)).scalar() or 0
        
        avg_cov_query = select(func.avg(Report.coverage_percent))
        average_coverage = (await db.execute(avg_cov_query)).scalar() or 0.0
        
        avg_risk_query = select(func.avg(Function.risk_score))
        average_risk = (await db.execute(avg_risk_query)).scalar() or 0.0
        average_health_score = max(0.0, 100.0 - average_risk)
        
        return GovernanceOverviewResponse(
            success=True,
            reports_analyzed=reports_analyzed,
            functions_scanned=functions_scanned,
            coverage_gaps_found=coverage_gaps_found,
            tests_generated=tests_generated,
            average_coverage=round(average_coverage, 2),
            average_health_score=round(average_health_score, 2)
        )
