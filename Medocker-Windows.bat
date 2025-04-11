@echo off

REM: This launches the Medocker web interface. Preferred method on Windows.
echo Starting Medocker Web Interface...
cd src
poetry run python run_web.py
pause 