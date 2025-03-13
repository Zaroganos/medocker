#!/bin/bash

echo "=== Medocker Build Script ==="

echo "Checking for Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found. Please install Python 3.8 or newer."
    exit 1
fi

echo "Checking for PyInstaller..."
python3 -c "import PyInstaller" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "Error installing PyInstaller."
        exit 1
    fi
fi

echo "Running Python to check for pathlib conflicts..."
python3 fix_pathlib.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to fix pathlib conflicts."
    exit 1
fi
echo "Pathlib check passed."

echo "Building executable with PyInstaller..."
python3 -m PyInstaller medocker.spec --clean
if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed."
    exit 1
fi

echo "Creating distribution package..."
python3 scripts/build/build_auto.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to create distribution package."
    exit 1
fi

echo "Build completed successfully!"
echo "Distribution package is available in the releases directory."

# Make the script executable
chmod +x "$(dirname "$0")/releases/medocker-$(uname | tr '[:upper:]' '[:lower:]')/medocker"
chmod +x "$(dirname "$0")/releases/medocker-$(uname | tr '[:upper:]' '[:lower:]')/launcher.sh" 