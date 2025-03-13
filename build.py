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
import importlib.util
from pathlib import Path

def check_prerequisites():
    """Check if PyInstaller is installed and handle pathlib issue."""
    # Check for pathlib backport which conflicts with PyInstaller
    pathlib_spec = importlib.util.find_spec("pathlib")
    if pathlib_spec and "site-packages" in str(pathlib_spec.origin):
        print("Detected 'pathlib' backport package which conflicts with PyInstaller.")
        uninstall = input("Would you like to uninstall it? (y/n): ")
        if uninstall.lower() == 'y':
            print("Uninstalling pathlib backport...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pathlib"])
            print("Pathlib uninstalled successfully.")
        else:
            print("PyInstaller requires the pathlib backport to be uninstalled. Exiting.")
            return False
    
    # Check for PyInstaller
    try:
        import PyInstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")
    
    return True

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
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller", 
            "medocker.spec", 
            "--clean"
        ])
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executables: {e}")
        return False

def create_distribution_package():
    """Create distribution packages for each platform."""
    dist_dir = Path("dist")
    
    if not dist_dir.exists():
        print("Error: Build directory not found.")
        return
    
    system = platform.system().lower()
    print(f"Creating distribution package for {system}...")
    
    # Create output directory for releases if it doesn't exist
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)
    
    # Get executables
    executables = {
        "medocker": dist_dir / "medocker",
        "medocker-web": dist_dir / "medocker-web",
        "medocker-configure": dist_dir / "medocker-configure"
    }
    
    # Add extension for Windows
    if system == 'windows':
        executables = {name: path.with_suffix('.exe') for name, path in executables.items()}
    
    # Copy executables to the releases directory
    for name, path in executables.items():
        if path.exists():
            dest_path = releases_dir / path.name
            print(f"Copying {path.name} to releases directory...")
            shutil.copy2(path, dest_path)
        else:
            print(f"Warning: {path.name} not found in dist directory.")
    
    # Create a README for the releases
    readme_path = releases_dir / "README.txt"
    with open(readme_path, "w") as f:
        f.write("Medocker Standalone Executables\n")
        f.write("===============================\n\n")
        f.write("This package contains standalone executables for Medocker:\n\n")
        f.write("- medocker: Main CLI application with all commands\n")
        f.write("- medocker-configure: Configuration tool\n")
        f.write("- medocker-web: Web-based configuration interface\n\n")
        f.write("Getting Started:\n")
        f.write("1. Run 'medocker' to see available commands\n")
        f.write("2. Run 'medocker-configure --interactive' to set up your configuration\n")
        f.write("3. Run 'medocker-web' to start the web interface\n")
        f.write("4. Run 'medocker deploy' to deploy your Docker stack\n\n")
        f.write("For more information, visit: https://github.com/yourusername/medocker\n")
    
    # Create a simple launcher script
    if system == 'windows':
        # Windows batch file
        launcher_path = releases_dir / "Medocker.bat"
        with open(launcher_path, "w") as f:
            f.write('@echo off\r\n')
            f.write('echo Medocker - Clinic in a box by way of docker stack\r\n')
            f.write('echo.\r\n')
            f.write('echo Choose an option:\r\n')
            f.write('echo 1. Configure Medocker\r\n')
            f.write('echo 2. Start Web Interface\r\n')
            f.write('echo 3. Deploy Stack\r\n')
            f.write('echo.\r\n')
            f.write('set /p choice="Enter your choice (1-3): "\r\n')
            f.write('echo.\r\n')
            f.write('if "%choice%"=="1" (\r\n')
            f.write('    start medocker-configure.exe --interactive\r\n')
            f.write(') else if "%choice%"=="2" (\r\n')
            f.write('    start medocker-web.exe\r\n')
            f.write(') else if "%choice%"=="3" (\r\n')
            f.write('    start medocker.exe deploy\r\n')
            f.write(') else (\r\n')
            f.write('    echo Invalid choice. Please try again.\r\n')
            f.write('    pause\r\n')
            f.write(')\r\n')
    else:
        # Linux/macOS shell script
        launcher_path = releases_dir / "medocker.sh"
        with open(launcher_path, "w") as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Medocker - Clinic in a box by way of docker stack"\n')
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
    
    # Create a zip archive of the releases directory
    platform_name = {
        'windows': 'windows',
        'linux': 'linux',
        'darwin': 'macos'
    }.get(system, system)
    
    zip_path = f"medocker-{platform_name}"
    if os.path.exists(f"{zip_path}.zip"):
        os.remove(f"{zip_path}.zip")
    
    print(f"Creating ZIP archive: {zip_path}.zip")
    shutil.make_archive(zip_path, "zip", releases_dir)
    
    print(f"Distribution package created: {zip_path}.zip")

def main():
    """Main entry point for the build script."""
    print("=== Medocker Build Script ===")
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Clean build directories
    clean_build_directories()
    
    # Build executables
    if build_executables():
        # Create distribution package
        create_distribution_package()
        print("Build process completed successfully!")
    else:
        print("Build process failed.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 