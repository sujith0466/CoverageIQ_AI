from typing import List, Dict, Any, Tuple, Set
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.function import Function
from app.repositories.function import function as function_repo

class DependencyIntelligenceService:
    
    @staticmethod
    def _build_graph(functions: List[Function]) -> Dict[str, List[str]]:
        """Build a graph mapping function_name -> list of called function_names that exist in the DB."""
        valid_names = {f.name for f in functions}
        graph = {}
        for func in functions:
            called_list = func.called_functions or []
            valid_called = []
            for cf in called_list:
                name = cf if isinstance(cf, str) else cf.get("name", "")
                if name in valid_names:
                    valid_called.append(name)
            graph[func.name] = valid_called
            func.dependency_count = len(valid_called)
        return graph

    @staticmethod
    def _calculate_impact(graph: Dict[str, List[str]]) -> Tuple[Dict[str, int], Dict[str, int]]:
        """Calculate impact radius (unique downstream nodes) and max depth for each node."""
        impact_radius = {}
        max_depth = {}
        
        # Memoization for radius and depth
        memo_descendants = {}
        
        def dfs(node: str, visited: Set[str]) -> Set[str]:
            if node in memo_descendants:
                return memo_descendants[node]
            
            visited.add(node)
            descendants = set()
            for child in graph.get(node, []):
                if child not in visited:  # Cycle detection
                    descendants.add(child)
                    descendants.update(dfs(child, visited))
            
            visited.remove(node)
            memo_descendants[node] = descendants
            return descendants
            
        def dfs_depth(node: str, visited: Set[str]) -> int:
            visited.add(node)
            depth = 0
            for child in graph.get(node, []):
                if child not in visited:
                    depth = max(depth, 1 + dfs_depth(child, visited))
            visited.remove(node)
            return depth

        for node in graph:
            descendants = dfs(node, set())
            impact_radius[node] = len(descendants)
            max_depth[node] = dfs_depth(node, set())
            
        return impact_radius, max_depth

    @staticmethod
    def _calculate_score(func: Function, impact_radius: int, depth: int, total_functions: int) -> float:
        # Impact Radius = 40%
        # Risk Score = 35%
        # Coverage Status = 15%
        # Dependency Depth = 10%
        
        radius_score = (impact_radius / max(1, total_functions)) * 100.0 * 0.40
        
        risk = func.risk_score or 0.0
        risk_score = risk * 0.35
        
        status_val = 0
        if func.coverage_status == "UNCOVERED":
            status_val = 100
        elif func.coverage_status == "PARTIAL":
            status_val = 50
        coverage_score = status_val * 0.15
        
        depth_score = (depth / max(1, total_functions)) * 100.0 * 0.10
        
        total_score = radius_score + risk_score + coverage_score + depth_score
        return min(100.0, max(0.0, total_score))

    @staticmethod
    def _get_level(score: float) -> str:
        if score > 90:
            return "CRITICAL DEPENDENCY"
        elif score > 70:
            return "HIGH"
        elif score > 30:
            return "MEDIUM"
        return "LOW"
        
    @staticmethod
    def _generate_recommendation(func: Function, impact_radius: int) -> str:
        if func.coverage_status in ["UNCOVERED", "PARTIAL"] and impact_radius >= 2:
            return f"Test this function first because it impacts {impact_radius} downstream functions."
        if func.dependency_level == "CRITICAL DEPENDENCY":
            return "Immediate refactor or testing required due to high downstream impact."
        if func.coverage_status == "COVERED":
            return "Well tested. Safe to modify."
        return "Standard testing priority."

    @staticmethod
    async def analyze_project_dependencies(db: AsyncSession, report_id: str) -> Dict[str, Any]:
        functions = await function_repo.get_by_report(db, report_id=report_id)
        if not functions:
            return {
                "success": False,
                "message": "No functions found.",
            }
            
        total_funcs = len(functions)
        graph = DependencyIntelligenceService._build_graph(functions)
        impact_radius_map, max_depth_map = DependencyIntelligenceService._calculate_impact(graph)
        
        updated_functions = []
        for func in functions:
            radius = impact_radius_map.get(func.name, 0)
            depth = max_depth_map.get(func.name, 0)
            
            func.impact_radius = radius
            score = DependencyIntelligenceService._calculate_score(func, radius, depth, total_funcs)
            func.critical_dependency_score = round(score, 2)
            func.dependency_level = DependencyIntelligenceService._get_level(score)
            
            db.add(func)
            updated_functions.append({
                **func.__dict__,
                "recommendation": DependencyIntelligenceService._generate_recommendation(func, radius)
            })
            
        await db.commit()
        
        # Calculate summary
        critical = sum(1 for f in updated_functions if f["dependency_level"] == "CRITICAL DEPENDENCY")
        high = sum(1 for f in updated_functions if f["dependency_level"] == "HIGH")
        medium = sum(1 for f in updated_functions if f["dependency_level"] == "MEDIUM")
        low = sum(1 for f in updated_functions if f["dependency_level"] == "LOW")
        
        largest_impact_func = max(updated_functions, key=lambda f: f["impact_radius"], default=None)
        
        # Clean up SQLAlchemy state from dicts
        for f in updated_functions:
            f.pop("_sa_instance_state", None)
        
        return {
            "success": True,
            "summary": {
                "critical_dependencies": critical,
                "high_dependencies": high,
                "medium_dependencies": medium,
                "low_dependencies": low
            },
            "largest_impact_function": largest_impact_func["name"] if largest_impact_func else "None",
            "largest_impact_radius": largest_impact_func["impact_radius"] if largest_impact_func else 0,
            "functions": updated_functions,
            "graph": graph  # We return graph dynamically instead of saving to DB
        }
