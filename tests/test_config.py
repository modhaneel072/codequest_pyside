# -*- coding: utf-8 -*-
"""Tests for configuration system."""

import unittest
import tempfile
from pathlib import Path
from src.core.config import Config, get_config, DEFAULT_CONFIG


class TestConfig(unittest.TestCase):
    """Test suite for configuration system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a fresh config instance for each test
        Config._instance = None
    
    def test_default_values(self):
        """Test that default configuration values are set."""
        config = Config()
        
        self.assertEqual(config.get('app.title'), 'CodeQuest')
        self.assertEqual(config.get('grading.passing_score'), 90)
        self.assertEqual(config.get('code_execution.timeout_seconds'), 2.0)
    
    def test_get_with_default(self):
        """Test get() method with default value."""
        config = Config()
        
        # Non-existent key returns default
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')
        self.assertIsNone(config.get('nonexistent.key'))
    
    def test_set_value(self):
        """Test set() method."""
        config = Config()
        
        config.set('app.title', 'New Title')
        self.assertEqual(config.get('app.title'), 'New Title')
        
        # Test nested key creation
        config.set('custom.nested.value', 42)
        self.assertEqual(config.get('custom.nested.value'), 42)
    
    def test_load_from_file(self):
        """Test loading configuration from JSON file."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write('{"app": {"title": "Test Title"}}')
            temp_path = f.name
        
        try:
            config = Config(temp_path)
            self.assertEqual(config.get('app.title'), 'Test Title')
        finally:
            Path(temp_path).unlink()
    
    def test_save_to_file(self):
        """Test saving configuration to JSON file."""
        config = Config()
        config.set('app.title', 'Saved Title')
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            temp_path = f.name
        
        try:
            config.save(temp_path)
            
            # Load saved config
            config2 = Config(temp_path)
            self.assertEqual(config2.get('app.title'), 'Saved Title')
        finally:
            Path(temp_path).unlink()
    
    def test_singleton_pattern(self):
        """Test that Config uses singleton pattern."""
        config1 = get_config()
        config2 = get_config()
        
        self.assertIs(config1, config2)
    
    def test_merge_config(self):
        """Test configuration merging."""
        config = Config()
        
        # Default values should be present
        self.assertIn('app', config._config)
        self.assertIn('grading', config._config)


class TestConfigDefaults(unittest.TestCase):
    """Test default configuration structure."""
    
    def test_required_keys(self):
        """Test that all required configuration keys exist."""
        config = Config()
        
        required_keys = [
            'app.title',
            'grading.passing_score',
            'code_execution.timeout_seconds',
        ]
        
        for key in required_keys:
            self.assertIsNotNone(
                config.get(key),
                f"Required config key missing: {key}"
            )


if __name__ == '__main__':
    unittest.main()
