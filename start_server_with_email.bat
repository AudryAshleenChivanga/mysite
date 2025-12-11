@echo off
echo ========================================
echo Portfolio Server with Email Support
echo ========================================
echo.
echo To enable email functionality, you need to set your Gmail App Password.
echo.
echo Steps:
echo 1. Go to https://myaccount.google.com/apppasswords
echo 2. Generate an App Password for "Mail"
echo 3. Copy the 16-character password
echo.
set /p APP_PASSWORD="Enter your Gmail App Password (or press Enter to skip): "

if "%APP_PASSWORD%"=="" (
    echo.
    echo Starting server WITHOUT email functionality...
    echo (Messages will be logged to console only)
    echo.
    python server.py
) else (
    echo.
    echo Setting Gmail App Password...
    set GMAIL_APP_PASSWORD=%APP_PASSWORD%
    echo.
    echo Starting server WITH email functionality...
    echo Emails will be sent to: audryashleenchivanga@gmail.com
    echo.
    python server.py
)

pause

