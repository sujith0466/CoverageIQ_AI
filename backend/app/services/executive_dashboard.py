from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.function import Function
from app.models.generated_test import GeneratedTest
from app.repositories.function import function as function_repo
from app.repositories.report import report as report_repo
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

class ExecutiveDashboardService:

    @staticmethod
    async def generate_dashboard(db: AsyncSession, report_id: str) -> Dict[str, Any]:
        report = await report_repo.get(db, id=report_id)
        if not report:
            return {"success": False, "message": "Report not found"}

        # Fetch Functions
        functions = await function_repo.get_by_report(db, report_id=report_id)
        
        total_functions = len(functions)
        if total_functions == 0:
            return {"success": False, "message": "No functions found to analyze."}
            
        function_ids = [f.id for f in functions]
        
        # Fetch Test Cases
        test_cases = []
        if function_ids:
            result = await db.execute(select(GeneratedTest).where(GeneratedTest.function_id.in_(function_ids)))
            test_cases = result.scalars().all()

        # 1. Coverage Metrics
        total_exe_lines = sum(f.executable_lines or 0 for f in functions)
        total_cov_lines = sum(f.covered_lines or 0 for f in functions)
        current_coverage = round((total_cov_lines / total_exe_lines * 100) if total_exe_lines > 0 else 0, 2)
        
        potential_cov_gain = sum(f.potential_coverage_gain or 0.0 for f in functions if f.coverage_status in ["UNCOVERED", "PARTIAL"])
        potential_coverage = round(min(100.0, current_coverage + potential_cov_gain), 2)
        improvement_potential = round(potential_coverage - current_coverage, 2)
        
        coverage_health_score = current_coverage

        # 2. Risk Metrics
        avg_risk_score = sum(f.risk_score or 0.0 for f in functions) / total_functions
        high_risk_funcs = [f for f in functions if f.risk_level == "HIGH"]
        med_risk_funcs = [f for f in functions if f.risk_level == "MEDIUM"]
        low_risk_funcs = [f for f in functions if f.risk_level == "LOW"]
        
        risk_health_score = round(max(0.0, 100.0 - avg_risk_score), 2)
        
        highest_risk_func = max(functions, key=lambda f: f.risk_score or 0.0, default=None)

        # 3. Dependency Metrics
        critical_deps = [f for f in functions if f.dependency_level == "CRITICAL DEPENDENCY"]
        high_deps = [f for f in functions if f.dependency_level == "HIGH"]
        med_deps = [f for f in functions if f.dependency_level == "MEDIUM"]
        
        dep_penalty = (len(critical_deps) * 20) + (len(high_deps) * 10) + (len(med_deps) * 5)
        dependency_health_score = round(max(0.0, 100.0 - dep_penalty), 2)
        
        largest_impact_func = max(functions, key=lambda f: f.impact_radius or 0, default=None)

        # 4. Testing Intelligence
        total_generated = len(test_cases)
        successful_gen = len([t for t in test_cases if t.generation_status == "SUCCESS"])
        failed_gen = total_generated - successful_gen
        
        uncovered_funcs = [f for f in functions if f.coverage_status in ["UNCOVERED", "PARTIAL"]]
        testing_readiness_score = 100.0
        if uncovered_funcs:
            ratio = (successful_gen / len(uncovered_funcs)) * 100.0
            testing_readiness_score = round(min(100.0, ratio), 2)
            
        top_priorities = sorted([f for f in functions if f.recommended_test_order], key=lambda f: f.recommended_test_order)
        top_5_priorities = top_priorities[:5]
        top_priority_func = top_priorities[0] if top_priorities else None

        # 5. Health Score Calculation
        # Coverage Health = 35%
        # Risk Health = 30%
        # Dependency Health = 20%
        # Testing Readiness = 15%
        project_health_score = round(
            (coverage_health_score * 0.35) +
            (risk_health_score * 0.30) +
            (dependency_health_score * 0.20) +
            (testing_readiness_score * 0.15),
            2
        )
        
        # Status Thresholds
        if project_health_score >= 90:
            status = "EXCELLENT"
        elif project_health_score >= 75:
            status = "GOOD"
        elif project_health_score >= 50:
            status = "NEEDS ATTENTION"
        else:
            status = "CRITICAL"
            
        # 6. Executive Summary (Rule-based)
        summary = (
            f"CoverageIQ analyzed {total_functions} functions.\n"
            f"Current Coverage: {current_coverage}%.\n"
            f"{len(high_risk_funcs)} High Risk Functions detected.\n"
            f"{len(critical_deps)} Critical Dependencies identified.\n"
            f"Potential Coverage Improvement: +{improvement_potential}%.\n"
        )
        if top_priorities:
            priority_names = " \u2192 ".join([f.name for f in top_priorities[:3]])
            summary += f"\nRecommended Priority:\n{priority_names}."

        # 7. Executive Recommendations
        recommendations = []
        if improvement_potential > 10:
            recommendations.append("Increase coverage in untested modules to realize potential gains.")
        if len(critical_deps) > 0:
            recommendations.append("Review critical dependency chains immediately to prevent cascading failures.")
        if len(high_risk_funcs) > 0:
            recommendations.append("Address high-risk business-critical functions before deploying.")
        if len(uncovered_funcs) > total_generated:
            recommendations.append("Generate tests for uncovered functions using AI Test Generation.")
        if current_coverage < 80:
            recommendations.append("Coverage is below industry standard. Prioritize writing missing tests.")

        # Prepare Response
        return {
            "success": True,
            "project_health_score": project_health_score,
            "status": status,
            "coverage": {
                "health_score": coverage_health_score,
                "current_coverage": current_coverage,
                "potential_coverage": potential_coverage,
                "improvement_potential": improvement_potential
            },
            "risk": {
                "health_score": risk_health_score,
                "project_risk_score": round(avg_risk_score, 2),
                "high_risk_functions": len(high_risk_funcs),
                "medium_risk_functions": len(med_risk_funcs),
                "low_risk_functions": len(low_risk_funcs)
            },
            "dependencies": {
                "health_score": dependency_health_score,
                "critical_dependencies": len(critical_deps),
                "largest_impact_function": largest_impact_func.name if largest_impact_func else "None",
                "largest_impact_radius": largest_impact_func.impact_radius if largest_impact_func else 0
            },
            "testing": {
                "health_score": testing_readiness_score,
                "generated_tests": total_generated,
                "successful_generations": successful_gen,
                "failed_generations": failed_gen,
                "recommended_tests": len(uncovered_funcs),
                "top_5_functions": [{"name": f.name, "score": f.test_priority_score} for f in top_5_priorities]
            },
            "recommendations": recommendations,
            "executive_summary": summary,
            "top_priority_function": top_priority_func.name if top_priority_func else "None",
            "highest_risk_function": highest_risk_func.name if highest_risk_func else "None",
            "largest_impact_function": largest_impact_func.name if largest_impact_func else "None"
        }
