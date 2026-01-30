"""Content and progress file loading with robust error handling."""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Ensure data directory exists
DATA.mkdir(parents=True, exist_ok=True)

DEFAULT_PROGRESS = {
    "module_index": 0,
    "history": [],
    "terminal_unlocked": {"commands": ["help", "status"]}
}


def load_course() -> Dict[str, Any]:
    """
    Load course definition from course.json.
    
    Returns:
        Course data dictionary
        
    Raises:
        FileNotFoundError: If course.json doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    p = DATA / "course.json"
    try:
        if not p.exists():
            logger.error(f"Course file not found: {p}")
            raise FileNotFoundError(f"Course file not found: {p}")
        
        course_data = json.loads(p.read_text(encoding="utf-8-sig"))
        logger.info("Successfully loaded course data")
        return course_data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in course.json: {e}")
        raise json.JSONDecodeError("Invalid JSON in course.json", e.doc, e.pos)
    except (IOError, OSError) as e:
        logger.error(f"Error reading course.json: {e}")
        raise


def load_progress() -> Dict[str, Any]:
    """
    Load user progress from progress.json.
    
    Returns:
        Progress data dictionary, or default if file missing/invalid
    """
    p = DATA / "progress.json"
    try:
        if not p.exists():
            logger.info("Progress file not found, using defaults")
            return DEFAULT_PROGRESS.copy()
        
        progress_data = json.loads(p.read_text(encoding="utf-8-sig"))
        logger.info("Successfully loaded progress data")
        return progress_data
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in progress.json, using defaults: {e}")
        return DEFAULT_PROGRESS.copy()
    except (IOError, OSError) as e:
        logger.warning(f"Error reading progress.json, using defaults: {e}")
        return DEFAULT_PROGRESS.copy()


def save_progress(progress: Dict[str, Any]) -> None:
    """
    Save user progress to progress.json.
    
    Args:
        progress: Progress data to save
        
    Raises:
        IOError: If file cannot be written
    """
    if not isinstance(progress, dict):
        logger.error(f"Invalid progress data type: {type(progress)}")
        raise ValueError("Progress must be a dictionary")
    
    try:
        p = DATA / "progress.json"
        p.write_text(json.dumps(progress, indent=2), encoding="utf-8")
        logger.info("Successfully saved progress data")
    except (IOError, OSError) as e:
        logger.error(f"Error writing progress.json: {e}")
        raise IOError(f"Cannot save progress: {e}")