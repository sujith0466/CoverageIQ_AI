import os
from pathlib import Path

def normalize_path(path: str) -> str:
    """
    Normalize any filesystem path to a standard forward-slash format.
    Ensures that AST paths and XML paths can be compared consistently
    regardless of the OS they were generated on.
    """
    if not path:
        return ""
    # Convert to POSIX format (forward slashes)
    return Path(path).as_posix()

def match_paths(ast_path: str, xml_path: str) -> bool:
    """
    Multi-strategy path matching between an AST function path and an XML coverage path.
    """
    ast_norm = normalize_path(ast_path)
    xml_norm = normalize_path(xml_path)
    
    # Strategy 1: Exact match
    if ast_norm == xml_norm:
        return True
        
    # Strategy 2: Suffix containment
    if ast_norm.endswith(xml_norm) or xml_norm.endswith(ast_norm):
        return True
        
    # Strategy 3: Component-based longest common suffix
    ast_parts = Path(ast_norm).parts
    xml_parts = Path(xml_norm).parts
    
    score = 0
    for ap, xp in zip(reversed(ast_parts), reversed(xml_parts)):
        if ap == xp:
            score += 1
        else:
            break
            
    # At minimum, the filename must match
    ast_basename = Path(ast_norm).name
    xml_basename = Path(xml_norm).name
    
    if score >= 1 and ast_basename == xml_basename:
        return True
        
    return False
