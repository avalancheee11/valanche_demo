"""
Configuration settings for Valanche Ambience Recorder
"""

import os
from typing import Dict, Any

# Audio Recording Settings
RECORDING_CONFIG = {
    'default_duration': 15,  # seconds
    'default_sample_rate': 44100,  # Hz
    'min_duration': 5,  # seconds
    'max_duration': 60,  # seconds
    'channels': 1,  # mono
    'dtype': 'int16',
    'countdown_seconds': 3,
    'meter_update_interval': 0.1,  # seconds
}

# Granular Synthesis Settings
GRANULAR_CONFIG = {
    'default_grain_size_ms': 100,
    'default_overlap': 0.5,
    'default_loop_duration': 10,  # seconds
    'min_grain_size_ms': 20,
    'max_grain_size_ms': 500,
    'min_overlap': 0.0,
    'max_overlap': 0.9,
    'default_texture_density': 0.7,
    'crossfade_duration': 0.1,  # seconds
}

# Analysis Settings
ANALYSIS_CONFIG = {
    'yamnet_sample_rate': 16000,  # Hz
    'quality_thresholds': {
        'good_signal_db': -30,
        'low_signal_db': -60,
        'low_noise_zcr': 0.1,
        'high_noise_zcr': 0.3,
    }
}

# File Settings
FILE_CONFIG = {
    'temp_dir': 'temp',
    'output_dir': 'output',
    'supported_formats': ['.wav', '.mp3', '.flac'],
    'max_file_size_mb': 100,
}

# UI Settings
UI_CONFIG = {
    'page_title': 'Valanche Ambience Recorder',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'theme': {
        'primaryColor': '#667eea',
        'backgroundColor': '#ffffff',
        'secondaryBackgroundColor': '#f0f2f6',
        'textColor': '#262730',
    }
}

# Model Settings
MODEL_CONFIG = {
    'yamnet_model_handle': 'https://tfhub.dev/google/yamnet/1',
    'class_map_url': 'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv',
    'cache_models': True,
}

def get_config() -> Dict[str, Any]:
    """Get all configuration settings"""
    return {
        'recording': RECORDING_CONFIG,
        'granular': GRANULAR_CONFIG,
        'analysis': ANALYSIS_CONFIG,
        'file': FILE_CONFIG,
        'ui': UI_CONFIG,
        'model': MODEL_CONFIG,
    }

def create_directories():
    """Create necessary directories"""
    dirs = [FILE_CONFIG['temp_dir'], FILE_CONFIG['output_dir']]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def get_temp_file_path(filename: str) -> str:
    """Get full path for temporary file"""
    return os.path.join(FILE_CONFIG['temp_dir'], filename)

def get_output_file_path(filename: str) -> str:
    """Get full path for output file"""
    return os.path.join(FILE_CONFIG['output_dir'], filename) 