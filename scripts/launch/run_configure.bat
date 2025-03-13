@echo off
echo Running Medocker Configure...

REM Try to use the built executable if it exists
if exist "..\..\dist\medocker-configure.exe" (
    ..\..\dist\medocker-configure.exe %*
) else (
    REM Fall back to running the Python script directly
    echo No executable found, running Python script instead...
    python ..\..\src\configure.py %*
)

echo.
echo Executable finished with exit code %ERRORLEVEL%
pause 