@echo off
echo Running Medocker Configure...
dist\medocker-configure.exe %*
echo.
echo Executable finished with exit code %ERRORLEVEL%
pause 