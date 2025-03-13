#!/bin/bash
# Medocker Packaging Script for Linux/macOS
echo "Checking for pathlib issues..."
python3 fix_pathlib.py
if [ $? -ne 0 ]; then
    echo "Failed to fix pathlib issue. Please run with sudo."
    exit 1
fi

echo "Building Medocker standalone executables..."
python3 build_auto.py
if [ $? -ne 0 ]; then
    echo "Build failed! See error messages above."
    exit 1
fi

echo
echo "Build completed successfully!"
echo "Executables are available in the releases directory and as a zip file."
echo 