#!/bin/bash

echo "Starting Plagiarism Checker Pro..."
echo ""
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    echo "Please install Python 3.8 or higher from your package manager."
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
echo "Python $python_version detected"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate