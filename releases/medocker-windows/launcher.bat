@echo off
===============================================
            Medocker Launcher
===============================================

REM Change to the directory where the launcher.bat is located
cd /d "%~dp0"

echo Starting Medocker from %CD%...
echo.
echo If a browser window doesn't open automatically, 
echo please visit: http://localhost:9876
echo.
echo Press Ctrl+C to stop the server when finished.
echo.

REM Run the executable
medocker.exe

REM This will only execute if the executable quits
echo.
echo Medocker has exited with code: %ERRORLEVEL%
pause
