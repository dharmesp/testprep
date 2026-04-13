@echo off
echo ========================================
echo   Test Prep Quiz App - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo.
echo Starting Flask application...
echo.
echo ========================================
echo   Server will start at:
echo   http://127.0.0.1:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

REM If app exits, pause to show any error messages
pause
