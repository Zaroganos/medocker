@echo off
echo Medocker 0.1.0 Launcher
echo.
echo 1. Start Web Interface (default)
echo 2. Configure Medocker
echo 3. Deploy Docker Stack
echo 4. Exit
echo.
set /p choice=Enter your choice (1-4) or press Enter for Web Interface: 

if "%choice%"=="" (
    medocker.exe
    goto end
)
if "%choice%"=="1" (
    medocker.exe
    goto end
)
if "%choice%"=="2" (
    medocker.exe configure --interactive
    goto end
)
if "%choice%"=="3" (
    medocker.exe deploy
    goto end
)
if "%choice%"=="4" (
    exit /b
)

echo Invalid choice, please try again.

:end
pause
