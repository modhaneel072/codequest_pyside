# -*- coding: utf-8 -*-
"""File I/O utilities with error handling and validation."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def read_text_utf8(path: str) -> str:
    """
    Read text file with UTF-8 encoding.
    
    Args:
        path: File path
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            logger.error(f"File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}")
        
        content = file_path.read_text(encoding="utf-8-sig")
        logger.debug(f"Successfully read file: {path}")
        return content
    except (IOError, OSError) as e:
        logger.error(f"Error reading file {path}: {e}")
        raise IOError(f"Cannot read file {path}: {e}")


def load_json(path: str) -> Dict[str, Any]:
    """
    Load JSON file with error handling.
    
    Args:
        path: Path to JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    try:
        content = read_text_utf8(path)
        data = json.loads(content)
        logger.info(f"Successfully loaded JSON from {path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path}: {e}")
        raise json.JSONDecodeError(f"Invalid JSON in {path}", e.doc, e.pos)


def write_json(path: str, data: Dict[str, Any]) -> None:
    """
    Write data to JSON file with error handling.
    
    Args:
        path: Path to JSON file
        data: Dictionary to write
        
    Raises:
        IOError: If file cannot be written
        ValueError: If data is not a dictionary
    """
    if not isinstance(data, dict):
        logger.error(f"Invalid data type for JSON: {type(data)}")
        raise ValueError("Data must be a dictionary")
    
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info(f"Successfully wrote JSON to {path}")
    except (IOError, OSError) as e:
        logger.error(f"Error writing JSON to {path}: {e}")
        raise IOError(f"Cannot write JSON to {path}: {e}")
