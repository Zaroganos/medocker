# Copyright (C) 2024-2025 Iliya Yaroshevskiy
"""
Medocker - A comprehensive Docker packaging system for medical practice software.

This package provides tools for configuring and deploying medical practice software stacks
using Docker Compose and Ansible.
"""

__version__ = "0.1.0"
__author__ = "Iliya Yaroshevskiy"
__email__ = "iyarosh1@binghamton.edu"

# Export main functions for easy access
from .medocker import main as medocker_main
from .configure import main as configure_main
from .run_web import main as web_main

# Make these available at package level
__all__ = ["medocker_main", "configure_main", "web_main"]
