@echo off
echo === Medocker Build Script ===

echo Checking for Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found. Please install Python 3.8 or newer.
    exit /b 1
)

echo Checking for PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if %ERRORLEVEL% neq 0 (
        echo Error installing PyInstaller.
        exit /b 1
    )
)

echo Running Python to check for pathlib conflicts...
python fix_pathlib.py
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to fix pathlib conflicts.
    exit /b 1
)
echo Pathlib check passed.

echo Building executable with PyInstaller...
python -m PyInstaller medocker.spec --clean
if %ERRORLEVEL% neq 0 (
    echo Error: PyInstaller build failed.
    exit /b 1
)

echo Creating distribution package...
python scripts\build\build_auto.py
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to create distribution package.
    exit /b 1
)

echo Build completed successfully!
echo Distribution package is available in the releases directory. 