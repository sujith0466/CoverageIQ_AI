import logging
import json
import sys
from typing import Any, Dict

logger = logging.getLogger("CoverageIQ")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

def log_event(event_name: str, metadata: Dict[str, Any] = None):
    """
    Log a structured enterprise event.
    """
    msg = f"[{event_name}]"
    if metadata:
        msg += f" {json.dumps(metadata)}"
    logger.info(msg)
