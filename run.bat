@echo off
echo Starting Plagiarism Checker Pro...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "python_version=%%i"
echo Python %python_version% detected

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

if not exist "requirements_installed.flag" (
    echo Installing requirements...
    pip install -r requirements.txt
    echo. > requirements_installed.flag
)

echo.
echo Starting Plagiarism Checker Pro...
echo.
echo Choose mode:
echo 1. Basic GUI (Recommended for students)
echo 2. Advanced GUI (Recommended for educators)
echo 3. Command Line Interface
echo 4. Batch Processing
echo.
set /p mode="Enter mode (1-4, default=1): "

if "%mode%"=="1" (
    python main.py --mode basic
) else if "%mode%"=="2" (
    python main.py --mode advanced
) else if "%mode%"=="3" (
    set /p document="Enter document path: "
    python main.py --mode cli --document "%document%"
) else if "%mode%"=="4" (
    set /p input_dir="Enter input directory: "
    python main.py --mode batch --input-dir "%input_dir%"
) else (
    python main.py --mode basic
)

pause