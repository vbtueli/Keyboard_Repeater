#!/usr/bin/env bash
# Build portable KeyboardRepeater binary for Linux (run on Ubuntu/Fedora etc.)
# Usage: ./build.sh
# Output: dist/KeyboardRepeater (no extension; copy to any Linux with same arch)

set -e
cd "$(dirname "$0")"

echo "Installing build deps..."
pip3 install -r requirements.txt -r requirements-build.txt -q

echo "Building..."
pyinstaller --noconfirm KeyboardRepeater-linux.spec

if [ -f "dist/KeyboardRepeater" ]; then
    echo "Done. Output: dist/KeyboardRepeater"
    echo "Run with: ./dist/KeyboardRepeater"
else
    echo "Build failed."
    exit 1
fi
