@echo off
REM Docker run script for Allure Reports Server (Windows)

set IMAGE_NAME=allure-reports-server
set TAG=%1
set CONTAINER_NAME=allure-reports
set PORT=%2

if "%TAG%"=="" set TAG=latest
if "%PORT%"=="" set PORT=8080

echo Starting Allure Reports Server container...

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create a .env file with your AWS credentials:
    echo   copy .env.example .env
    echo   REM Edit .env with your actual AWS credentials
    exit /b 1
)

REM Stop and remove existing container if it exists
docker stop %CONTAINER_NAME% >nul 2>&1
docker rm %CONTAINER_NAME% >nul 2>&1

REM Run the container
echo Starting container...
docker run -d ^
    --name %CONTAINER_NAME% ^
    -p %PORT%:8080 ^
    --env-file .env ^
    --restart unless-stopped ^
    %IMAGE_NAME%:%TAG%

if %errorlevel% equ 0 (
    echo.
    echo ✅ Container started successfully!
    echo.
    echo Container details:
    docker ps -f name=%CONTAINER_NAME%
    echo.
    echo Access your allure reports at: http://localhost:%PORT%
    echo.
    echo Useful commands:
    echo   View logs:     docker logs -f %CONTAINER_NAME%
    echo   Stop:          docker stop %CONTAINER_NAME%
    echo   Restart:       docker restart %CONTAINER_NAME%
    echo   Shell access:  docker exec -it %CONTAINER_NAME% /bin/bash
    echo.
    echo Health check: curl http://localhost:%PORT%/health
) else (
    echo.
    echo ❌ Failed to start container!
    exit /b 1
)
