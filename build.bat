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

echo Building executable with PyInstaller...
python -m PyInstaller medocker.spec --clean
if %ERRORLEVEL% neq 0 (
    echo Error: PyInstaller build failed.
    exit /b 1
)

echo Creating releases directory if it doesn't exist...
if not exist "releases\medocker-windows" mkdir releases\medocker-windows

echo Copying executable to releases directory...
copy dist\medocker.exe releases\medocker-windows\

echo Copying supporting files...
if exist templates xcopy /E /I templates releases\medocker-windows\templates
if exist static xcopy /E /I static releases\medocker-windows\static
if exist config xcopy /E /I config releases\medocker-windows\config
if exist docs xcopy /E /I docs releases\medocker-windows\docs

echo Creating launcher batch file...
(
echo @echo off
echo ===============================================
echo             Medocker Launcher
echo ===============================================
echo.
echo REM Change to the directory where the launcher.bat is located
echo cd /d "%%~dp0"
echo.
echo echo Starting Medocker from %%CD%%...
echo echo.
echo echo If a browser window doesn't open automatically, 
echo echo please visit: http://localhost:5000
echo echo.
echo echo Press Ctrl+C to stop the server when finished.
echo echo.
echo.
echo REM Run the executable
echo medocker.exe
echo.
echo REM This will only execute if the executable quits
echo echo.
echo echo Medocker has exited with code: %%ERRORLEVEL%%
echo pause
) > releases\medocker-windows\launcher.bat

echo Creating README for the release...
(
echo # Medocker - Medical Practice in a Box
echo.
echo ## Quick Start
echo.
echo 1. Double-click on `launcher.bat` to start Medocker
echo 2. A web browser should open automatically to http://localhost:5000
echo 3. If a browser doesn't open, navigate to http://localhost:5000 manually
echo 4. Use the web interface to configure and deploy your Medocker stack
echo 5. Press Ctrl+C in the console window to stop the Medocker server when finished
echo.
echo ## Important Notes
echo.
echo - The executable must be run from its directory, which the launcher handles automatically
echo - All configuration files are stored in the `config` directory
echo - For more information, see the documentation in the `docs` directory
) > releases\medocker-windows\README.md

echo Build completed successfully!
echo Distribution package is available in the releases directory.
echo.
echo To launch Medocker, run: releases\medocker-windows\launcher.bat
pause 