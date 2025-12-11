@echo off
echo.
echo ==========================================
echo   Mission Portfolio Server Starting...
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Flask...
    pip install flask
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

echo Starting Flask server...
echo.
echo Your portfolio will be available at:
echo   Website: http://localhost:5000
echo   Admin Panel: http://localhost:5000/admin
echo.
echo Admin Credentials:
echo   Username: audry
echo   Password: healthcare2025
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python server.py

pause
