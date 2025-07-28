@echo off
echo Setting up Newsletter Backend...
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Running setup script...
python setup.py

if errorlevel 1 (
    echo Setup failed!
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Edit .env file with your API keys
echo 3. Run: python Scraper.py
echo.
pause
