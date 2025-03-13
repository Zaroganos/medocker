@echo off
echo Running Medocker Web Interface...

REM Try to use the built executable if it exists
if exist "..\..\dist\medocker-web.exe" (
    ..\..\dist\medocker-web.exe %*
) else (
    REM Fall back to running the Python script directly
    echo No executable found, running Python script instead...
    python ..\..\src\run_web.py %*
)

echo.
echo Executable finished with exit code %ERRORLEVEL%
pause 