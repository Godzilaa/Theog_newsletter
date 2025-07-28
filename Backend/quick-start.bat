@echo off
echo Starting Newsletter Backend (Quick Start)...
echo ==========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install only essential dependencies
echo Installing essential dependencies...
pip install flask python-dotenv requests
if errorlevel 1 (
    echo Failed to install essential dependencies
    pause
    exit /b 1
)

REM Try to install Flask-CORS (optional)
echo Installing Flask-CORS...
pip install flask-cors
if errorlevel 1 (
    echo Warning: Flask-CORS installation failed, but continuing...
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul 2>&1
        echo Created .env file from template
    ) else (
        echo # Environment variables > .env
        echo NEWS_API_KEY=your_news_api_key_here >> .env
        echo GNEWS_API_KEY=your_gnews_api_key_here >> .env
        echo FLASK_ENV=development >> .env
        echo FLASK_DEBUG=True >> .env
        echo Created basic .env file
    )
)

echo.
echo ========================================
echo Quick setup completed!
echo ========================================
echo.
echo Your API is ready to run with basic functionality:
echo - Hacker News stories
echo - NewsAPI headlines (if you add API key)
echo.
echo To configure API keys:
echo 1. Edit .env file
echo 2. Add your NewsAPI key from https://newsapi.org/
echo 3. Add your GNews key from https://gnews.io/
echo.
echo Starting the server...
python Scraper.py
