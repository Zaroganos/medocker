#!/bin/bash
# Medocker Configuration Script

echo "Medocker Configuration Script"
echo "============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not found. Please install pip for Python 3 and try again."
    exit 1
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

# Run the configuration script in interactive mode
echo ""
echo "Starting interactive configuration..."
python3 configure.py --interactive

echo ""
echo "Configuration complete!"
echo "You can now start the Medocker stack with 'docker-compose up -d'" 