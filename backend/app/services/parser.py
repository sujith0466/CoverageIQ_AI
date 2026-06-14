import os
import defusedxml.ElementTree as ET
from typing import Dict, Any

class CoverageParserService:
    @staticmethod
    def parse_cobertura_xml(file_path: str) -> Dict[str, Any]:
        """
        Parses a Cobertura XML coverage report and extracts key metrics and file-level coverage.
        Supports fallback calculations if root attributes are missing.
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": "Coverage file not found."}
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            import logging
            logger = logging.getLogger(__name__)
            
            tag_name = root.tag.split('}')[-1] if '}' in root.tag else root.tag
            
            logger.info(f"Original Root Tag: {root.tag}")
            logger.info(f"Parsed Tag Name: {tag_name}")
            
            if tag_name != 'coverage':
                return {"success": False, "message": f"XML is valid, but this is not a coverage report XML. Expected root tag <coverage>, found <{tag_name}>."}
            
            # Helper to safely parse floats/ints
            def parse_float(val):
                try: return float(val) if val is not None else 0.0
                except ValueError: return 0.0
                
            def parse_int(val):
                try: return int(float(val)) if val is not None else 0
                except ValueError: return 0

            # Extract or calculate root metrics
            total_lines = parse_int(root.attrib.get('lines-valid'))
            covered_lines = parse_int(root.attrib.get('lines-covered'))
            line_rate = parse_float(root.attrib.get('line-rate'))
            branch_rate = parse_float(root.attrib.get('branch-rate'))
            
            classes = root.findall('.//class')
            total_classes = len(classes)
            
            files_data = []
            calc_total_lines = 0
            calc_covered_lines = 0
            
            unique_files = {}  # filename -> FileCoverage dict
            
            for cls in classes:
                filename = cls.attrib.get('filename')
                if not filename:
                    continue
                    
                lines = cls.findall('.//line')
                file_valid = len(lines)
                file_covered = sum(1 for line in lines if parse_int(line.attrib.get('hits', 0)) > 0)
                
                # If XML provides class-level stats, use them, else use calc
                cls_valid = parse_int(cls.attrib.get('lines-valid')) or file_valid
                cls_covered = parse_int(cls.attrib.get('lines-covered')) or file_covered
                
                if filename not in unique_files:
                    unique_files[filename] = {
                        "filename": filename,
                        "lines_valid": 0,
                        "lines_covered": 0
                    }
                    
                unique_files[filename]["lines_valid"] += cls_valid
                unique_files[filename]["lines_covered"] += cls_covered
                
                calc_total_lines += cls_valid
                calc_covered_lines += cls_covered

            total_files = len(unique_files)
            
            # Fallback if root attributes were missing
            if total_lines == 0 and calc_total_lines > 0:
                total_lines = calc_total_lines
            if covered_lines == 0 and calc_covered_lines > 0:
                covered_lines = calc_covered_lines
            if line_rate == 0.0 and total_lines > 0:
                line_rate = covered_lines / total_lines
                
            coverage_percent = line_rate * 100
            
            # Build files list
            for fname, fdata in unique_files.items():
                v = fdata["lines_valid"]
                c = fdata["lines_covered"]
                pct = round((c / v * 100) if v > 0 else 0.0, 2)
                files_data.append({
                    "filename": fname,
                    "lines_valid": v,
                    "lines_covered": c,
                    "coverage_percent": pct
                })
            
            # Sort files by lowest coverage first
            files_data.sort(key=lambda x: (x["coverage_percent"], x["filename"]))

            raw_metrics = {
                "version": root.attrib.get("version"),
                "timestamp": root.attrib.get("timestamp"),
                "complexity": root.attrib.get("complexity"),
                "files": files_data  # Store file-level metrics here
            }
            
            return {
                "success": True,
                "coverage_percent": round(coverage_percent, 2),
                "total_files": total_files,
                "total_classes": total_classes,
                "total_lines": total_lines,
                "covered_lines": covered_lines,
                "line_rate": line_rate,
                "branch_rate": branch_rate,
                "raw_metrics": raw_metrics,
                "files": files_data
            }
            
        except ET.ParseError:
            return {"success": False, "message": "Failed to parse XML file. File might be corrupted."}
        except Exception as e:
            return {"success": False, "message": f"An error occurred during parsing: {str(e)}"}
