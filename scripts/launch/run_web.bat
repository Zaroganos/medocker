@echo off
echo Running Medocker Web Interface...
dist\medocker-web.exe %*
echo.
echo Executable finished with exit code %ERRORLEVEL%
pause 