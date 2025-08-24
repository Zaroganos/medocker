#!/bin/bash
echo "Running Medocker Web Interface..."

# Try to use the built executable if it exists
if [ -f "../../dist/medocker" ]; then
    ../../dist/medocker --web "$@"
else
    # Fall back to running the Python script directly
    echo "No executable found, running Python script instead..."
    python3 ../../src/medocker/run_web.py "$@"
fi

echo
echo "Executable finished with exit code $?"
read -p "Press Enter to continue..." 