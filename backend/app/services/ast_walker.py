import os
import ast
from typing import List, Dict, Any

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)

class ASTWalkerService:
    IGNORE_DIRS = {'venv', 'node_modules', '__pycache__', '.git', '.env'}

    @classmethod
    def scan_directory(cls, directory_path: str, report_id: str) -> Dict[str, Any]:
        print("=" * 50)
        print("STEP 2: ASTWalkerService.scan_directory HIT")
        print(f"RAW DIRECTORY_PATH: {repr(directory_path)}")
        
        # FIX: Strip whitespace and quotes that users might accidentally paste
        cleaned_path = directory_path.strip(' "\'\n\r')
        print(f"CLEANED PATH: {repr(cleaned_path)}")
        
        exists = os.path.exists(cleaned_path)
        isdir = os.path.isdir(cleaned_path)
        print(f"os.path.exists({repr(cleaned_path)}): {exists}")
        print(f"os.path.isdir({repr(cleaned_path)}): {isdir}")
        print("=" * 50)
        
        if not exists or not isdir:
            return {
                "success": False, 
                "message": "Invalid directory path.\n\nIf running with Docker Compose, use a mounted container path such as:\n/workspace/sample_projects/banking\n\nSee sample_data/usage_instructions.md for examples."
            }
            
        functions = []
        for root, dirs, files in os.walk(cleaned_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in cls.IGNORE_DIRS]
            
            for file in files:
                if not file.endswith('.py'):
                    continue
                    
                file_path = os.path.join(root, file)
                funcs = cls._parse_file(file_path, report_id)
                functions.extend(funcs)
                    
        return {"success": True, "functions": functions, "total": len(functions)}

    @classmethod
    def _parse_file(cls, file_path: str, report_id: str) -> List[Dict[str, Any]]:
        functions = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_data = cls._extract_function_data(node, file_path, report_id)
                    functions.append(func_data)
        except SyntaxError:
            pass # Skip files with syntax errors
        except Exception:
            pass
        return functions

    @classmethod
    def _extract_function_data(cls, node, file_path: str, report_id: str) -> Dict[str, Any]:
        is_async = isinstance(node, ast.AsyncFunctionDef)
        
        params = []
        for arg in node.args.args:
            params.append(arg.arg)
        for arg in node.args.posonlyargs:
            params.append(arg.arg)
        for arg in node.args.kwonlyargs:
            params.append(arg.arg)
        if getattr(node.args, 'vararg', None):
            params.append(f"*{node.args.vararg.arg}")
        if getattr(node.args, 'kwarg', None):
            params.append(f"**{node.args.kwarg.arg}")
            
        function_type = 'method' if (params and params[0] in ('self', 'cls')) else 'function'
            
        docstring = ast.get_docstring(node)
        
        decorators = []
        for dec in node.decorator_list:
            try:
                decorators.append(ast.unparse(dec))
            except Exception:
                pass
                
        return_type = None
        if node.returns:
            try:
                return_type = ast.unparse(node.returns)
            except Exception:
                pass

        visitor = FunctionCallVisitor()
        visitor.visit(node)
        called_functions = list(set(visitor.calls))
        
        from app.utils.path_utils import normalize_path
        normalized_path = normalize_path(file_path)
        
        return {
            "report_id": report_id,
            "name": node.name,
            "file_path": normalized_path,
            "start_line": getattr(node, 'lineno', None),
            "end_line": getattr(node, 'end_lineno', None),
            "parameters": params,
            "docstring": docstring,
            "function_type": function_type,
            "is_async": is_async,
            "return_type": return_type,
            "decorators": decorators,
            "called_functions": called_functions
        }
