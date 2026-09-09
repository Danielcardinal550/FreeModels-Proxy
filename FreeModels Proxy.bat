@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM One-click source launcher. It uses an isolated .venv only when needed.
if exist ".venv\Scripts\pythonw.exe" goto RUN

where py >nul 2>&1
if errorlevel 1 (
    echo Python is required only for the SOURCE version.
    echo For normal users, download FreeModels Proxy.exe from GitHub Releases.
    pause
    exit /b 1
)

echo Preparing FreeModels Proxy for first use...
py -m venv .venv
if errorlevel 1 goto FAIL

".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 goto FAIL

:RUN
start "" ".venv\Scripts\pythonw.exe" launcher.py
exit /b 0

:FAIL
echo Setup failed. Please check your internet connection and try again.
pause
exit /b 1
