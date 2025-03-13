#!/bin/bash
echo "Running Medocker CLI..."

# Try to use the built executable if it exists
if [ -f "../../dist/medocker" ]; then
    ../../dist/medocker "$@"
else
    # Fall back to running the Python script directly
    echo "No executable found, running Python script instead..."
    python3 ../../src/medocker.py "$@"
fi

echo
echo "Executable finished with exit code $?"
read -p "Press Enter to continue..." 