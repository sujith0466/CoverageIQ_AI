from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.function import Function
from app.models.generated_test import GeneratedTest
from app.schemas.explainability import ExplainabilityResponse, ExplainabilityItem

class ExplainabilityService:
    @classmethod
    async def get_report_explainability(cls, db: AsyncSession, report_id: str) -> Optional[ExplainabilityResponse]:
        # Fetch all generated tests for this report
        query = select(GeneratedTest, Function).join(Function).where(Function.report_id == report_id)
        result = await db.execute(query)
        rows = result.all()
        
        explanations = []
        for test, func in rows:
            reasons = []
            if func.coverage_status == "UNCOVERED":
                reasons.append("Uncovered function")
            elif func.coverage_status == "PARTIAL":
                reasons.append("Partially covered function")
                
            if func.risk_level in ["CRITICAL", "HIGH"]:
                reasons.append(f"High risk profile ({func.risk_level})")
                
            if func.dependency_count > 3:
                reasons.append("High dependency count")
                
            if func.test_priority_score and func.test_priority_score >= 80:
                reasons.append("Top priority for test generation")
                
            if not reasons:
                reasons.append("Selected by baseline criteria")
                
            explanations.append(ExplainabilityItem(
                function=func.name,
                coverage=func.coverage_percent or 0.0,
                risk=func.risk_level or "LOW",
                reason=reasons,
                generated_test_id=test.id
            ))
            
        return ExplainabilityResponse(
            success=True,
            report_id=report_id,
            explanations=explanations
        )
