@echo off
REM Medocker Packaging Script for Windows
echo Checking for pathlib issues...
python fix_pathlib.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to fix pathlib issue. Please run as administrator.
    pause
    exit /b 1
)

echo Building Medocker standalone executables...
python build_auto.py
if %ERRORLEVEL% NEQ 0 (
    echo Build failed! See error messages above.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executables are available in the releases directory and as a zip file.
echo.
pause 