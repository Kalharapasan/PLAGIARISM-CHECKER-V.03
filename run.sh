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
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
if [ ! -f "requirements_installed.flag" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch requirements_installed.flag
fi

echo ""
echo "Starting Plagiarism Checker Pro..."
echo ""
echo "Choose mode:"
echo "1. Basic GUI (Recommended for students)"
echo "2. Advanced GUI (Recommended for educators)"
echo "3. Command Line Interface"
echo "4. Batch Processing"
echo ""
read -p "Enter mode (1-4, default=1): " mode

case $mode in
    1)
        python3 main.py --mode basic
        ;;
    2)
        python3 main.py --mode advanced
        ;;
    3)
        read -p "Enter document path: " document
        python3 main.py --mode cli --document "$document"
        ;;
    4)
        read -p "Enter input directory: " input_dir
        python3 main.py --mode batch --input-dir "$input_dir"
        ;;
    *)
        python3 main.py --mode basic
        ;;
esac

