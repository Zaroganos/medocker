#!/usr/bin/env python3
"""
Fix pathlib backport issue for PyInstaller

This script uninstalls the pathlib backport package which conflicts with PyInstaller.
"""

import sys
import subprocess
import importlib.util

def main():
    # Check if pathlib backport is installed
    pathlib_spec = importlib.util.find_spec("pathlib")
    if pathlib_spec and "site-packages" in str(pathlib_spec.origin):
        print("Detected 'pathlib' backport package which conflicts with PyInstaller.")
        print("Uninstalling pathlib backport...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pathlib"])
            print("Pathlib uninstalled successfully.")
            return 0
        except subprocess.CalledProcessError:
            print("Failed to uninstall pathlib. You may need to run this script with administrator privileges.")
            return 1
    else:
        print("Pathlib backport not detected or is a standard library module.")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 