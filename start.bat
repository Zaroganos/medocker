@echo off
rem Medocker Startup Script for Windows
rem This script helps users get started with Medocker using Poetry

echo Checking for Poetry installation...

where poetry >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Poetry is required but not installed. Please install Poetry using:
    echo.
    echo   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing^).Content ^| python -
    echo.
    echo Then run this script again.
    exit /b 1
)

rem Install dependencies
echo Installing Medocker dependencies...
poetry install

rem Provide usage instructions
echo.
echo ===============================================
echo Medocker has been set up successfully!
echo ===============================================
echo.
echo To start using Medocker, run one of the following commands:
echo.
echo 1. Configure Medocker interactively:
echo    poetry run medocker configure --interactive
echo.
echo 2. Start the web interface:
echo    poetry run medocker web
echo.
echo 3. Deploy the configured stack:
echo    poetry run medocker deploy
echo.
echo For more information, see the README.md file.
echo =============================================== 