#!/usr/bin/env python3
"""
Medocker Build Script

This script builds standalone executables for the Medocker application using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def check_prerequisites():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")

def clean_build_directories():
    """Clean build and dist directories."""
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            print(f"Removing {directory} directory...")
            shutil.rmtree(directory)
    
    # Also remove any .spec files created by PyInstaller
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'medocker.spec':  # Don't remove our custom spec file
            print(f"Removing {spec_file}...")
            spec_file.unlink()

def build_executables():
    """Build the executables using PyInstaller."""
    print("Building Medocker executables...")
    
    # Run PyInstaller with our spec file
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "medocker.spec", 
        "--clean"
    ])
    
    print("Build completed successfully!")

def create_distribution_package():
    """Create a distribution package based on the platform."""
    dist_dir = Path("dist")
    medocker_dir = dist_dir / "medocker"
    
    if not medocker_dir.exists():
        print("Error: Build directory not found.")
        return
    
    print("Creating distribution package...")
    
    # Create a platform-specific distribution
    system = platform.system().lower()
    if system == 'windows':
        # Create a simple batch file launcher for Windows
        print("Creating Windows launcher...")
        with open(medocker_dir / "Medocker.bat", "w") as f:
            f.write('@echo off\r\n')
            f.write('echo Starting Medocker...\r\n')
            f.write('echo.\r\n')
            f.write('echo Choose an option:\r\n')
            f.write('echo 1. Configure Medocker\r\n')
            f.write('echo 2. Start Web Interface\r\n')
            f.write('echo 3. Deploy Stack\r\n')
            f.write('echo.\r\n')
            f.write('set /p choice="Enter your choice (1-3): "\r\n')
            f.write('echo.\r\n')
            f.write('if "%choice%"=="1" (\r\n')
            f.write('    start medocker-configure --interactive\r\n')
            f.write(') else if "%choice%"=="2" (\r\n')
            f.write('    start medocker-web\r\n')
            f.write(') else if "%choice%"=="3" (\r\n')
            f.write('    start medocker deploy\r\n')
            f.write(') else (\r\n')
            f.write('    echo Invalid choice. Please try again.\r\n')
            f.write('    pause\r\n')
            f.write(')\r\n')
        
        # Create a ZIP file
        shutil.make_archive(f"medocker-windows", "zip", dist_dir, "medocker")
        print(f"Created distribution package: medocker-windows.zip")
    
    elif system == 'linux' or system == 'darwin':
        # Create a shell script launcher for Linux/macOS
        print(f"Creating {'macOS' if system == 'darwin' else 'Linux'} launcher...")
        launcher_path = medocker_dir / "medocker.sh"
        with open(launcher_path, "w") as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting Medocker..."\n')
            f.write('echo\n')
            f.write('echo "Choose an option:"\n')
            f.write('echo "1. Configure Medocker"\n')
            f.write('echo "2. Start Web Interface"\n')
            f.write('echo "3. Deploy Stack"\n')
            f.write('echo\n')
            f.write('read -p "Enter your choice (1-3): " choice\n')
            f.write('echo\n')
            f.write('case $choice in\n')
            f.write('    1) ./medocker-configure --interactive ;;\n')
            f.write('    2) ./medocker-web ;;\n')
            f.write('    3) ./medocker deploy ;;\n')
            f.write('    *) echo "Invalid choice. Please try again." ;;\n')
            f.write('esac\n')
        
        # Make the launcher executable
        launcher_path.chmod(0o755)
        
        # Create a tarball
        platform_name = "macos" if system == "darwin" else "linux"
        shutil.make_archive(f"medocker-{platform_name}", "gztar", dist_dir, "medocker")
        print(f"Created distribution package: medocker-{platform_name}.tar.gz")
    
    else:
        print(f"Unsupported platform: {system}")

def main():
    """Main entry point for the build script."""
    print("=== Medocker Build Script ===")
    check_prerequisites()
    clean_build_directories()
    build_executables()
    create_distribution_package()
    print("Build process completed successfully!")

if __name__ == '__main__':
    main() 