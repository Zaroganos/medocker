#!/bin/bash
echo "Redirecting to scripts/launch/run_web.sh..."
echo
cd scripts/launch
chmod +x run_web.sh
./run_web.sh "$@"
cd ../.. 