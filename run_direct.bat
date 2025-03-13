@echo off
echo Running Medocker CLI directly...

REM Try to use the built executable if it exists
if exist "dist\medocker.exe" (
    dist\medocker.exe %*
) else (
    REM Fall back to running the Python script directly
    echo No executable found, running Python script instead...
    python src\medocker.py %*
)

echo.
echo Executable finished with exit code %ERRORLEVEL%
pause 