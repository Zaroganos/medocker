@echo off
echo Medocker - Clinic in a box by way of docker stack
echo.
echo Choose an option:
echo 1. Configure Medocker
echo 2. Start Web Interface
echo 3. Deploy Stack
echo.
set /p choice="Enter your choice (1-3): "
echo.
if "%choice%"=="1" (
    start medocker-configure.exe --interactive
) else if "%choice%"=="2" (
    start medocker-web.exe
) else if "%choice%"=="3" (
    start medocker.exe deploy
) else (
    echo Invalid choice. Please try again.
    pause
)
