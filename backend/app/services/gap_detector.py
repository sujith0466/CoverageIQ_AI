import os
import xml.etree.ElementTree as ET
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.function import function as function_repo
from app.schemas.function import DetectGapsResponse

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")

# CoverageIQ's own directories — warn the user if they scan these
COVERAGEIQ_MARKERS = [
    "app/api", "app/services", "app/models", "app/repositories",
    "app/schemas", "app/db", "app/core", "alembic/versions",
    "app/main.py"
]


def _is_coverageiq_directory(directory_path: str) -> bool:
    """Detect if the user is trying to scan CoverageIQ's own source code."""
    norm = directory_path.replace("\\", "/").rstrip("/")
    # Check for typical CoverageIQ internal paths
    for marker in COVERAGEIQ_MARKERS:
        full_marker = f"/{marker}"
        if norm.endswith(full_marker) or norm == marker:
            return True
    # Check if the directory contains known CoverageIQ files
    try:
        for root, dirs, files in os.walk(directory_path):
            for f in files:
                rel = os.path.join(root, f).replace("\\", "/")
                for marker in COVERAGEIQ_MARKERS:
                    if marker in rel:
                        return True
            break  # only check the top level
    except Exception:
        pass
    return False


from app.utils.path_utils import normalize_path, match_paths

def _match_coverage_file(func_path_posix: str, coverage_map: dict) -> dict:
    """
    Find lines for the matched file using path_utils.
    """
    for xml_path, lines in coverage_map.items():
        if match_paths(func_path_posix, xml_path):
            return lines
    return {}


class CoverageGapService:
    @staticmethod
    async def detect_gaps(db: AsyncSession, report_id: str) -> DetectGapsResponse:
        file_path = os.path.join(UPLOAD_DIR, f"{report_id}.xml")
        if not os.path.exists(file_path):
            return DetectGapsResponse(success=False, message="Coverage XML file not found.")

        # 1. Parse XML and build Coverage Map
        coverage_map = {}  # posix_filename -> {line_number: hits}
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for package in root.findall('.//package'):
                for cls in package.findall('.//class'):
                    filename = cls.attrib.get('filename')
                    if not filename:
                        continue

                    # Normalize path using pathlib — always forward slashes
                    norm_filename = Path(filename).as_posix()
                    if norm_filename not in coverage_map:
                        coverage_map[norm_filename] = {}

                    for line in cls.findall('.//line'):
                        num = int(line.attrib.get('number', 0))
                        hits = int(line.attrib.get('hits', 0))
                        coverage_map[norm_filename][num] = hits
        except Exception as e:
            return DetectGapsResponse(success=False, message=f"Failed to parse XML: {str(e)}")

        # 2. Fetch Functions and Compute Gaps
        db_functions = await function_repo.get_by_report(db, report_id=report_id)
        if not db_functions:
            return DetectGapsResponse(success=False, message="No AST functions found for this report.")

        covered_count = 0
        partial_count = 0
        uncovered_count = 0
        updated_funcs = []

        for func in db_functions:
            if not func.start_line or not func.end_line:
                continue

            norm_func_path = Path(func.file_path).as_posix()

            # Use multi-strategy path matching
            matched_file_lines = _match_coverage_file(norm_func_path, coverage_map)

            executable_lines = 0
            covered_lines = 0
            covered_list = []
            uncovered_list = []

            for line_num in range(func.start_line, func.end_line + 1):
                if line_num in matched_file_lines:
                    executable_lines += 1
                    hits = matched_file_lines[line_num]
                    if hits > 0:
                        covered_lines += 1
                        covered_list.append(line_num)
                    else:
                        uncovered_list.append(line_num)

            if executable_lines == 0:
                # No coverage data found for this function — treat as UNCOVERED (0%)
                # This is correct: if no XML data exists for the function's lines,
                # it means no test ran those lines = uncovered.
                coverage_percent = 0.0
                status = "UNCOVERED"
                uncovered_count += 1
            else:
                coverage_percent = round((covered_lines / executable_lines) * 100, 2)
                if coverage_percent >= 90.0:
                    status = "COVERED"
                    covered_count += 1
                elif coverage_percent == 0.0:
                    status = "UNCOVERED"
                    uncovered_count += 1
                else:
                    status = "PARTIAL"
                    partial_count += 1

            coverage_details = {
                "covered": covered_list,
                "uncovered": uncovered_list
            }

            update_data = {
                "coverage_percent": coverage_percent,
                "executable_lines": executable_lines,
                "covered_lines": covered_lines,
                "coverage_status": status,
                "coverage_details": coverage_details
            }

            await function_repo.update(db, db_obj=func, obj_in=update_data)

            updated_funcs.append({
                "id": func.id,
                "name": func.name,
                "file_path": func.file_path,
                "start_line": func.start_line,
                "end_line": func.end_line,
                "function_type": func.function_type,
                "is_async": func.is_async,
                "coverage_percent": coverage_percent,
                "coverage_status": status,
                "executable_lines": executable_lines,
                "covered_lines": covered_lines
            })

        return DetectGapsResponse(
            success=True,
            total_functions=len(db_functions),
            covered=covered_count,
            partial=partial_count,
            uncovered=uncovered_count,
            functions=updated_funcs,
            message="Coverage gaps detected successfully."
        )
