import os

file_path = 'frontend/../backend/app/api/endpoints/reports.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

debug_endpoint = """
@router.get("/{report_id}/debug-paths")
async def debug_paths(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Debug endpoint to return path matching details: xml_files, ast_files, matched_files, unmatched_files.
    \"\"\"
    db_report = await report_repo.get(db, id=report_id)
    if not db_report:
        return {"success": False, "message": "Report not found"}
        
    # Get XML files
    raw_metrics = db_report.raw_metrics or {}
    files_data = raw_metrics.get("files", [])
    xml_files = [f["filename"] for f in files_data]
    
    # Get AST functions
    from sqlalchemy.future import select
    from app.models.function import Function
    result = await db.execute(select(Function).where(Function.report_id == report_id))
    functions = result.scalars().all()
    ast_files = list(set([f.file_path for f in functions]))
    
    # Match using path_utils
    from app.utils.path_utils import match_paths
    matched_files = []
    unmatched_files = []
    
    for ast_path in ast_files:
        matched = False
        for xml_path in xml_files:
            if match_paths(ast_path, xml_path):
                matched = True
                matched_files.append({"ast_path": ast_path, "xml_path": xml_path})
                break
        if not matched:
            unmatched_files.append(ast_path)
            
    return {
        "success": True,
        "report_id": report_id,
        "xml_files": xml_files,
        "ast_files": ast_files,
        "matched_files": matched_files,
        "unmatched_files": unmatched_files
    }
"""

if 'def debug_paths' not in content:
    content += '\n' + debug_endpoint
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Debug endpoint injected successfully.")
else:
    print("Debug endpoint already exists.")
