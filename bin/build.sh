#!/bin/bash
echo "Redirecting to scripts/build/package.sh..."
echo
cd scripts/build
chmod +x package.sh
./package.sh
cd ../.. 