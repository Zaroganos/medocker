#!/bin/bash
# Medocker Startup Script
# This script helps users get started with Medocker using Poetry

set -e

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is required but not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for this session
    export PATH="$HOME/.poetry/bin:$PATH"
    
    echo "Poetry installed successfully!"
fi

# Install dependencies
echo "Installing Medocker dependencies..."
poetry install

# Provide usage instructions
echo ""
echo "==============================================="
echo "Medocker has been set up successfully!"
echo "==============================================="
echo ""
echo "To start using Medocker, run one of the following commands:"
echo ""
echo "1. Configure Medocker interactively:"
echo "   poetry run medocker configure --interactive"
echo ""
echo "2. Start the web interface:"
echo "   poetry run medocker web"
echo ""
echo "3. Deploy the configured stack:"
echo "   poetry run medocker deploy"
echo ""
echo "For more information, see the README.md file."
echo "===============================================" 