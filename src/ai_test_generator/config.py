"""
Configuration Module
Handles loading and managing configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_CONFIG = {
    'test_framework': 'pytest',
    'include_edge_cases': True,
    'include_mocks': True,
    'max_tests_per_function': 10,
    'confidence_threshold': 0.7,
    'output_directory': 'tests/',
    'file_naming': 'test_{filename}.py',
    'model_path': None,
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or use defaults.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Try to load from file
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f)
            if file_config:
                config.update(file_config)
    
    # Try to load from default location
    elif Path('.ai-test-gen.yml').exists():
        with open('.ai-test-gen.yml', 'r') as f:
            file_config = yaml.safe_load(f)
            if file_config:
                config.update(file_config)
    
    # Override with environment variables
    env_config = load_from_env()
    config.update(env_config)
    
    return config


def load_from_env() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Returns:
        Configuration dictionary from environment
    """
    config = {}
    
    # Model path
    if 'AI_TEST_GEN_MODEL_PATH' in os.environ:
        config['model_path'] = os.environ['AI_TEST_GEN_MODEL_PATH']
    
    # Test framework
    if 'AI_TEST_GEN_FRAMEWORK' in os.environ:
        config['test_framework'] = os.environ['AI_TEST_GEN_FRAMEWORK']
    
    # Output directory
    if 'AI_TEST_GEN_OUTPUT_DIR' in os.environ:
        config['output_directory'] = os.environ['AI_TEST_GEN_OUTPUT_DIR']
    
    # Include edge cases
    if 'AI_TEST_GEN_EDGE_CASES' in os.environ:
        config['include_edge_cases'] = os.environ['AI_TEST_GEN_EDGE_CASES'].lower() == 'true'
    
    return config


def save_config(config: Dict[str, Any], output_path: str = '.ai-test-gen.yml'):
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        output_path: Path to save configuration
    """
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def create_default_config(output_path: str = '.ai-test-gen.yml'):
    """
    Create a default configuration file.
    
    Args:
        output_path: Path to save configuration
    """
    save_config(DEFAULT_CONFIG, output_path)
    print(f"Default configuration created at {output_path}")
