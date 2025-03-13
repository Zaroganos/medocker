#!/bin/bash
echo "Redirecting to scripts/launch/run_medocker.sh..."
echo
cd ../scripts/launch
chmod +x run_medocker.sh
./run_medocker.sh "$@"
cd ../.. 