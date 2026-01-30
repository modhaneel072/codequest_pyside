# -*- coding: utf-8 -*-
"""Configuration management for CodeQuest."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "title": "CodeQuest",
        "version": "1.0.0",
        "window_width": 1200,
        "window_height": 760,
    },
    "code_execution": {
        "timeout_seconds": 2.0,
        "max_output_length": 5000,
    },
    "grading": {
        "passing_score": 90,
        "mcq_points": 40,
        "total_points": 100,
    },
    "data": {
        "lessons_dir": "src/data/lessons",
        "problems_dir": "src/data/problems",
        "quizzes_dir": "src/data/quizzes",
        "debugs_dir": "src/data/debugs",
    },
    "logging": {
        "level": "INFO",
        "enable_file_logging": True,
        "log_file": "logs/codequest.log",
    }
}


class Config:
    """Application configuration manager."""
    
    _instance: Optional['Config'] = None
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to config.json file (optional)
        """
        self._config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        
        if config_file:
            self._load_config_file(config_file)
        else:
            # Try to load from default location
            default_path = Path(__file__).resolve().parent.parent.parent / "config.json"
            if default_path.exists():
                self._load_config_file(str(default_path))
    
    def _load_config_file(self, config_file: str) -> None:
        """Load configuration from JSON file."""
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                logger.warning(f"Config file not found: {config_file}")
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            
            # Deep merge with defaults
            self._merge_config(self._config, file_config)
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Error loading config from {config_file}: {e}")
    
    @staticmethod
    def _merge_config(target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Deep merge source config into target config."""
        for key, value in source.items():
            if isinstance(value, dict) and isinstance(target.get(key), dict):
                Config._merge_config(target[key], value)
            else:
                target[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Config key (e.g., 'app.title' or 'grading.passing_score')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Config key (e.g., 'app.title')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Set config {key} = {value}")
    
    def save(self, config_file: str) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            config_file: Path to save config to
        """
        try:
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            
            logger.info(f"Saved configuration to {config_file}")
        except Exception as e:
            logger.error(f"Error saving config to {config_file}: {e}")
    
    @classmethod
    def get_instance(cls, config_file: Optional[str] = None) -> 'Config':
        """Get singleton instance of Config."""
        if cls._instance is None:
            cls._instance = cls(config_file)
        return cls._instance


# Module-level convenience function
def get_config(config_file: Optional[str] = None) -> Config:
    """Get the global config instance."""
    return Config.get_instance(config_file)
