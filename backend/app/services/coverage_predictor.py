from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.function import Function
from app.repositories.function import function as function_repo
from app.repositories.report import report as report_repo

class CoveragePredictionService:
    
    @staticmethod
    def _calculate_potential_gain(func: Function, total_executable_lines: int) -> float:
        if total_executable_lines == 0:
            return 0.0
        # Uncovered Executable Lines = executable_lines - covered_lines
        exe = func.executable_lines or 0
        cov = func.covered_lines or 0
        uncov = max(0, exe - cov)
        
        gain = (uncov / total_executable_lines) * 100.0
        return round(gain, 2)

    @staticmethod
    def _calculate_priority_score(
        func: Function, 
        max_gain: float, 
        max_radius: int
    ) -> float:
        # Coverage Gain = 40%
        # Risk Score = 25%
        # Critical Dependency Score = 25%
        # Impact Radius = 10%
        
        gain = func.potential_coverage_gain or 0.0
        gain_score = (gain / max_gain * 100.0 * 0.40) if max_gain > 0 else 0.0
        
        risk = func.risk_score or 0.0
        risk_score = risk * 0.25
        
        dep = func.critical_dependency_score or 0.0
        dep_score = dep * 0.25
        
        radius = func.impact_radius or 0
        radius_score = (radius / max_radius * 100.0 * 0.10) if max_radius > 0 else 0.0
        
        total = gain_score + risk_score + dep_score + radius_score
        return min(100.0, max(0.0, round(total, 2)))

    @staticmethod
    def _get_recommendation_category(score: float) -> str:
        if score >= 90:
            return "TEST IMMEDIATELY"
        elif score >= 70:
            return "HIGH VALUE"
        elif score >= 40:
            return "MEDIUM VALUE"
        return "LOW VALUE"
        
    @staticmethod
    def _generate_recommendation(func: Function) -> str:
        if getattr(func, "is_highest_gain", False):
            return "Testing this function provides the highest projected coverage increase."
        if func.recommendation_category == "TEST IMMEDIATELY":
            return "Critical risk and dependency impact. Must be tested immediately."
        if func.potential_coverage_gain and func.potential_coverage_gain > 5:
            return f"Significant coverage bump of +{func.potential_coverage_gain}%."
        if func.coverage_status == "COVERED":
            return "Already fully covered. Maintain existing tests."
        return "Standard testing priority."

    @staticmethod
    async def predict_project_coverage(db: AsyncSession, report_id: str) -> Dict[str, Any]:
        report = await report_repo.get(db, id=report_id)
        functions = await function_repo.get_by_report(db, report_id=report_id)
        
        if not functions or not report:
            return {"success": False, "message": "No functions or report found."}
            
        total_exe_lines = sum(f.executable_lines or 0 for f in functions)
        total_cov_lines = sum(f.covered_lines or 0 for f in functions)
        current_coverage = round((total_cov_lines / total_exe_lines * 100) if total_exe_lines > 0 else 0, 2)
        
        # 1. Calculate Coverage Gain
        for func in functions:
            func.potential_coverage_gain = CoveragePredictionService._calculate_potential_gain(func, total_exe_lines)
            
        # 2. Find maximums for normalization
        max_gain = max((f.potential_coverage_gain or 0.0 for f in functions), default=0.0)
        max_radius = max((f.impact_radius or 0 for f in functions), default=0)
        
        # Identify highest gain function
        highest_gain_func = max(functions, key=lambda f: f.potential_coverage_gain or 0.0, default=None)
        if highest_gain_func:
            highest_gain_func.is_highest_gain = True

        # 3. Calculate Scores & Categories
        for func in functions:
            func.test_priority_score = CoveragePredictionService._calculate_priority_score(func, max_gain, max_radius)
            func.recommendation_category = CoveragePredictionService._get_recommendation_category(func.test_priority_score)
            
        # 4. Sort and assign order
        # We only want to recommend functions that are not COVERED (or those that have gain > 0)
        # Actually, let's sort all, but the uncovered ones naturally bubble to the top due to score.
        functions.sort(key=lambda f: f.test_priority_score or 0.0, reverse=True)
        
        uncovered_funcs_in_recommendations = 0
        for idx, func in enumerate(functions):
            func.recommended_test_order = idx + 1
            if func.coverage_status in ["UNCOVERED", "PARTIAL"]:
                exe = func.executable_lines or 0
                cov = func.covered_lines or 0
                uncovered_funcs_in_recommendations += max(0, exe - cov)
                
            db.add(func)
            
        await db.commit()

        # Potential Coverage Formula:
        # Current Covered Lines + All Uncovered Executable Lines from recommended functions
        potential_covered_lines = total_cov_lines + uncovered_funcs_in_recommendations
        potential_coverage = round(min(100.0, (potential_covered_lines / total_exe_lines * 100) if total_exe_lines > 0 else 0), 2)
        improvement_potential = round(potential_coverage - current_coverage, 2)

        # Prepare response
        response_funcs = []
        for f in functions:
            f_dict = {**f.__dict__}
            f_dict.pop("_sa_instance_state", None)
            f_dict.pop("is_highest_gain", None)
            f_dict["recommendation"] = CoveragePredictionService._generate_recommendation(f)
            response_funcs.append(f_dict)
            
        return {
            "success": True,
            "current_coverage": current_coverage,
            "potential_coverage": potential_coverage,
            "improvement_potential": improvement_potential,
            "highest_gain_function": highest_gain_func.name if highest_gain_func else "None",
            "highest_gain": highest_gain_func.potential_coverage_gain if highest_gain_func else 0.0,
            "recommendations": response_funcs
        }
