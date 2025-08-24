# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2024-2025 Iliya Yaroshevskiy
"""
Medocker Configuration Settings

This module contains configuration settings for different environments.
"""

import os
import secrets

# Base configuration shared by all environments
class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Security settings
    PREFERRED_URL_SCHEME = 'https'
    
    # Medocker settings - Use consistent relative paths for both dev and prod
    # The src/medocker/ directory is always relative to the project root
    # This works regardless of where the code is executed from
    current_file_dir = os.path.dirname(os.path.abspath(__file__))  # src/medocker/
    PROJECT_ROOT = os.path.abspath(os.path.join(current_file_dir, '..', '..'))  # project root
    
    TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')
    STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
    DEFAULT_CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config/default.yml')
    CUSTOM_CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config/custom.yml')
    SESSION_FILE_DIR = os.path.join(os.path.join(os.path.expanduser('~'), '.medocker'), 'sessions')
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '9876'))
    
    # Waitress settings
    THREADS = int(os.environ.get('THREADS', '10'))


# Development configuration
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    

# Production configuration
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = os.environ.get('SECURE_COOKIES', 'true').lower() == 'true'
    # Set higher number of threads for production
    THREADS = int(os.environ.get('THREADS', '20'))


# Testing configuration
class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    SESSION_COOKIE_SECURE = False


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Get configuration based on environment
def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'production')
    return config_by_name.get(env, ProductionConfig) 