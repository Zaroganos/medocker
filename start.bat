@echo off
rem Medocker Launcher for Developers
rem This script is for development only - end users should use the PyInstaller builds

echo Medocker Development Launcher
echo ===============================================

rem Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is required but not installed.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

rem Check for Poetry
where poetry >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Poetry is required for development.
    echo To install Poetry, run:
    echo   pip install poetry
    echo.
    echo For more information, visit: https://python-poetry.org/docs/#installation
    pause
    exit /b 1
)

rem Install dependencies
echo Installing development dependencies...
poetry install

echo.
echo ===============================================
echo Medocker development environment is ready!
echo ===============================================
echo.
echo Options:
echo.
echo 1. Run configuration tool:
echo    poetry run python configure.py --interactive
echo.
echo 2. Run web interface:
echo    poetry run python run_web.py
echo.
echo 3. Run through unified CLI:
echo    poetry run python medocker.py --help
echo.
echo 4. Build standalone executables:
echo    poetry run python build.py
echo.
echo For more information, see the README.md file.
echo ===============================================

echo.
echo Press any key to exit...
pause > nul 