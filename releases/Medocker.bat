@echo off

echo Medocker - Clinic in a box by way of docker stack

echo.

echo Choose an option:

echo 1. Configure Medocker

echo 2. Start Web Interface

echo 3. Deploy Stack

echo 4. Show Help

echo.

set /p choice="Enter your choice (1-4): "

echo.

if "%choice%"=="1" (

    echo Running Medocker Configuration Tool...
    .\medocker-configure.exe --interactive
    echo.
    echo Configuration tool finished with exit code %ERRORLEVEL%

) else if "%choice%"=="2" (

    echo Running Medocker Web Interface...
    echo (This will open a browser window and start a server. Press Ctrl+C to stop)
    echo.
    .\medocker-web.exe
    echo.
    echo Web interface server finished with exit code %ERRORLEVEL%

) else if "%choice%"=="3" (

    echo Deploying Medocker Stack...
    .\medocker.exe deploy
    echo.
    echo Deployment finished with exit code %ERRORLEVEL%

) else if "%choice%"=="4" (

    echo Showing Medocker Help...
    .\medocker.exe --help
    echo.
    echo For configuration help: .\medocker-configure.exe --help
    echo For web interface help: .\medocker-web.exe --help

) else (

    echo Invalid choice. Please try again.

)

echo.
pause

