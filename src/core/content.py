# -*- coding: utf-8 -*-
"""Content loading utilities with error handling and validation."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def load_lesson(path: str) -> str:
    """
    Load lesson content from a file.
    
    Args:
        path: File path to lesson content
        
    Returns:
        Lesson content as string
        
    Raises:
        FileNotFoundError: If lesson file doesn't exist
        IOError: If file cannot be read
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            logger.error(f"Lesson file not found: {path}")
            raise FileNotFoundError(f"Lesson file not found: {path}")
        
        content = file_path.read_text(encoding="utf-8-sig")
        logger.info(f"Successfully loaded lesson from {path}")
        return content
    except (IOError, OSError) as e:
        logger.error(f"Error reading lesson file {path}: {e}")
        raise IOError(f"Cannot read lesson file {path}: {e}")


def load_problem(problem_id: str, base_dir: str = "src/data/problems") -> Dict[str, Any]:
    """
    Load problem definition from JSON file.
    
    Args:
        problem_id: Problem identifier (e.g., 'm1_ps1')
        base_dir: Base directory containing problem files
        
    Returns:
        Problem definition as dictionary
        
    Raises:
        FileNotFoundError: If problem file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
        ValueError: If problem_id is invalid
    """
    if not problem_id or not isinstance(problem_id, str):
        logger.error(f"Invalid problem_id: {problem_id}")
        raise ValueError(f"Invalid problem_id: {problem_id}")
    
    try:
        p = Path(base_dir) / f"{problem_id}.json"
        if not p.exists():
            logger.error(f"Problem file not found: {p}")
            raise FileNotFoundError(f"Problem file not found: {p}")
        
        content = p.read_text(encoding="utf-8-sig")
        problem_data = json.loads(content)
        logger.info(f"Successfully loaded problem {problem_id}")
        return problem_data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in problem file {problem_id}: {e}")
        raise json.JSONDecodeError(f"Invalid JSON in problem {problem_id}", e.doc, e.pos)
    except (IOError, OSError) as e:
        logger.error(f"Error reading problem file {problem_id}: {e}")
        raise IOError(f"Cannot read problem file {problem_id}: {e}")

