#!/usr/bin/env bash
# Build portable KeyboardRepeater for macOS (run on a Mac)
# Usage: ./build-mac.sh
# Output: dist/KeyboardRepeater (copy to other Macs with same arch: x86_64 or arm64)

set -e
cd "$(dirname "$0")"

echo "Installing build deps..."
pip3 install -r requirements.txt -r requirements-build.txt -q

echo "Building..."
pyinstaller --noconfirm KeyboardRepeater-mac.spec

if [ -f "dist/KeyboardRepeater" ]; then
    echo "Done. Output: dist/KeyboardRepeater"
    echo "Run with: ./dist/KeyboardRepeater"
    echo "Note: First run may need 'Allow' in System Settings > Privacy & Security > Accessibility."
else
    echo "Build failed."
    exit 1
fi
