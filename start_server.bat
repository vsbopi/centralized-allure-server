@echo off
echo Starting Centralized Allure Reports Server...
echo.

REM Check if .env exists
if not exist .env (
    echo Warning: .env file not found!
    echo Please copy .env.example to .env and configure your AWS credentials.
    echo.
    pause
    exit /b 1
)

REM Start the server
python app.py

pause
