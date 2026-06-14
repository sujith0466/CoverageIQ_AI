import json
from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.function import Function
from app.repositories.function import function as function_repo

class RiskIntelligenceService:
    BUSINESS_KEYWORDS = [
        "auth", "login", "logout", "password", "token", "session", "user", "admin",
        "payment", "refund", "invoice", "tax", "billing"
    ]
    
    @staticmethod
    def _detect_business_criticality(func: Function) -> bool:
        target_text = f"{func.name} {func.docstring or ''}".lower()
        for kw in RiskIntelligenceService.BUSINESS_KEYWORDS:
            if kw in target_text:
                return True
        return False

    @staticmethod
    def calculate_risk(func: Function) -> Tuple[float, str, List[str]]:
        score = 0.0
        reasons = []

        # 1. Coverage Risk
        coverage = func.coverage_percent
        if coverage is not None:
            if coverage == 0:
                score += 40
                reasons.append("0% coverage")
            elif 1 <= coverage <= 25:
                score += 30
                reasons.append("1-25% coverage")
            elif 26 <= coverage <= 50:
                score += 20
                reasons.append("26-50% coverage")
            elif 51 <= coverage <= 75:
                score += 10
                reasons.append("51-75% coverage")
            elif 76 <= coverage <= 99:
                pass
            elif coverage == 100:
                score -= 10
                # Don't add a reason for a bonus

        # 2. Complexity Risk
        if func.start_line is not None and func.end_line is not None:
            lines = func.end_line - func.start_line
            if lines > 100:
                score += 20
                reasons.append("Function > 100 lines")
            elif lines > 50:
                score += 10
                reasons.append("Function > 50 lines")

        param_count = len(func.parameters) if func.parameters else 0
        if param_count > 10:
            score += 20
            reasons.append("More than 10 parameters")
        elif param_count > 5:
            score += 10
            reasons.append("More than 5 parameters")

        # 3. Dependency Risk
        called_funcs = len(func.called_functions) if func.called_functions else 0
        if called_funcs >= 10:
            score += 20
            reasons.append("10+ called functions")
        elif called_funcs >= 5:
            score += 10
            reasons.append("5+ called functions")

        # 4. Domain Risk
        target_text = f"{func.name} {func.docstring or ''}".lower()
        called_list = func.called_functions or []
        called_names = " ".join([cf if isinstance(cf, str) else cf.get("name", "") for cf in called_list]).lower()
        full_text = target_text + " " + called_names
        
        has_auth = any(kw in full_text for kw in ["auth", "login", "logout", "password", "token", "session"])
        if has_auth:
            score += 20
            reasons.append("Authentication logic detected")
            
        has_payment = any(kw in full_text for kw in ["payment", "refund", "invoice", "tax", "billing"])
        if has_payment:
            score += 25
            reasons.append("Payment logic detected")
            
        has_db = any(kw in full_text for kw in ["db", "query", "session", "commit", "execute"])
        if has_db:
            score += 15
            reasons.append("Database operations detected")
            
        has_api = any(kw in full_text for kw in ["requests", "api", "http", "fetch", "post", "get"])
        if has_api:
            score += 15
            reasons.append("External API calls detected")

        # Bound score between 0 and 100
        score = max(0.0, min(100.0, score))
        
        # Risk Levels
        if score <= 30:
            level = "LOW"
        elif score <= 70:
            level = "MEDIUM"
        else:
            level = "HIGH"
            
        return score, level, reasons

    @staticmethod
    async def analyze_project_risks(db: AsyncSession, report_id: str) -> Dict[str, Any]:
        functions = await function_repo.get_by_report(db, report_id=report_id)
        if not functions:
            return {
                "success": False,
                "message": "No functions found for this report.",
                "project_risk_score": 0,
                "summary": {"high_risk": 0, "medium_risk": 0, "low_risk": 0},
                "functions": []
            }
            
        updated_functions = []
        for func in functions:
            score, level, reasons = RiskIntelligenceService.calculate_risk(func)
            func.risk_score = score
            func.risk_level = level
            func.risk_reasons = reasons
            updated_functions.append(func)
            
        # Sort to assign priority rank
        updated_functions.sort(key=lambda x: x.risk_score, reverse=True)
        
        high_risk = 0
        medium_risk = 0
        low_risk = 0
        
        for idx, func in enumerate(updated_functions):
            func.risk_priority_rank = idx + 1
            if func.risk_level == "HIGH":
                high_risk += 1
            elif func.risk_level == "MEDIUM":
                medium_risk += 1
            else:
                low_risk += 1
                
            db.add(func)
            
        await db.commit()
        
        # Project risk score = avg of top 20
        top_20 = updated_functions[:20]
        project_risk_score = sum(f.risk_score for f in top_20) / len(top_20) if top_20 else 0
        
        return {
            "success": True,
            "project_risk_score": round(project_risk_score, 2),
            "summary": {
                "high_risk": high_risk,
                "medium_risk": medium_risk,
                "low_risk": low_risk
            },
            "functions": [f for f in updated_functions]
        }
