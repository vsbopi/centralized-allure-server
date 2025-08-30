@echo off
REM Docker build script for Allure Reports Server (Windows)

set IMAGE_NAME=allure-reports-server
set TAG=%1
set DOCKERFILE=%2

if "%TAG%"=="" set TAG=latest
if "%DOCKERFILE%"=="" set DOCKERFILE=Dockerfile

echo Building Allure Reports Server Docker image...
echo Image name: %IMAGE_NAME%:%TAG%
echo Dockerfile: %DOCKERFILE%
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found. Make sure to set environment variables when running the container.
)

REM Build the image
echo Building Docker image...
docker build -f %DOCKERFILE% -t %IMAGE_NAME%:%TAG% .

if %errorlevel% equ 0 (
    echo.
    echo ✅ Docker image built successfully!
    echo.
    echo To run the container:
    echo   docker run -p 8080:8080 --env-file .env %IMAGE_NAME%:%TAG%
    echo.
    echo Or use Docker Compose:
    echo   docker-compose up
    echo.
    echo Image details:
    docker images %IMAGE_NAME%:%TAG%
) else (
    echo.
    echo ❌ Docker build failed!
    exit /b 1
)
