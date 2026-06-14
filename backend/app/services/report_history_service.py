from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from app.models.report import Report
from app.models.function import Function
from app.models.generated_test import GeneratedTest
from app.models.audit_log import AuditLog
from app.schemas.report_history import ReportHistoryItem, ReportSummaryResponse

class ReportHistoryService:
    @classmethod
    async def get_report_history(cls, db: AsyncSession) -> List[ReportHistoryItem]:
        query = select(Report).order_by(Report.created_at.desc())
        result = await db.execute(query)
        reports = result.scalars().all()
        
        history = []
        for r in reports:
            # Functions found
            func_query = select(func.count(Function.id)).where(Function.report_id == r.id)
            funcs_count = (await db.execute(func_query)).scalar() or 0
            
            # Tests generated
            test_query = select(func.count(GeneratedTest.id)).join(Function).where(Function.report_id == r.id)
            tests_count = (await db.execute(test_query)).scalar() or 0
            
            # Latest audit status
            audit_query = select(AuditLog.event_type).where(AuditLog.report_id == r.id).order_by(AuditLog.created_at.desc()).limit(1)
            latest_status = (await db.execute(audit_query)).scalar()
            
            history.append(ReportHistoryItem(
                report_id=r.id,
                uploaded_at=r.created_at,
                coverage_percent=r.coverage_percent,
                files_analyzed=r.total_files or 0,
                functions_found=funcs_count,
                tests_generated=tests_count,
                latest_status=latest_status
            ))
            
        return history

    @classmethod
    async def get_report_summary(cls, db: AsyncSession, report_id: str) -> Optional[ReportSummaryResponse]:
        query = select(Report).where(Report.id == report_id)
        result = await db.execute(query)
        report = result.scalar_one_or_none()
        
        if not report:
            return None
            
        # Function stats
        funcs_query = select(Function.coverage_status, func.count(Function.id)).where(Function.report_id == report_id).group_by(Function.coverage_status)
        funcs_result = await db.execute(funcs_query)
        func_stats = dict(funcs_result.all())
        
        covered = func_stats.get("COVERED", 0)
        partial = func_stats.get("PARTIAL", 0)
        uncovered = func_stats.get("UNCOVERED", 0)
        functions_found = covered + partial + uncovered
        
        # Tests generated
        test_query = select(func.count(GeneratedTest.id)).join(Function).where(Function.report_id == report_id)
        tests_generated = (await db.execute(test_query)).scalar() or 0
        
        # Health score (simplistic aggregation from functions or just calculation)
        health_query = select(func.avg(Function.risk_score)).where(Function.report_id == report_id)
        avg_risk = (await db.execute(health_query)).scalar() or 0.0
        health_score = max(0.0, 100.0 - avg_risk)
        
        # Previous coverage trend
        prev_query = select(Report.coverage_percent).where(Report.created_at < report.created_at).order_by(Report.created_at.desc()).limit(1)
        prev_coverage = (await db.execute(prev_query)).scalar()
        
        coverage_change = None
        if prev_coverage is not None and report.coverage_percent is not None:
            coverage_change = round(report.coverage_percent - prev_coverage, 2)
            
        return ReportSummaryResponse(
            report_id=report_id,
            coverage_percent=report.coverage_percent,
            files_analyzed=report.total_files or 0,
            functions_found=functions_found,
            covered_functions=covered,
            partial_functions=partial,
            uncovered_functions=uncovered,
            generated_tests=tests_generated,
            health_score=round(health_score, 2),
            previous_coverage=prev_coverage,
            current_coverage=report.coverage_percent,
            coverage_change=coverage_change
        )
