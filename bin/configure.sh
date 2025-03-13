#!/bin/bash
echo "Redirecting to scripts/launch/run_configure.sh..."
echo
cd scripts/launch
chmod +x run_configure.sh
./run_configure.sh "$@"
cd ../.. 