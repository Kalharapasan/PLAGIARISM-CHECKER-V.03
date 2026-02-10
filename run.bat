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