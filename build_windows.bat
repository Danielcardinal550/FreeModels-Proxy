@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title FreeModels Proxy - Build Release

where py >nul 2>&1
if errorlevel 1 (
  echo Python is required only to build the release.
  pause
  exit /b 1
)

py -m pip install --upgrade pip
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto FAIL

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building standalone Windows EXE...
py -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name "FreeModels Proxy" ^
  --icon "assets\freemodels-proxy.ico" ^
  --add-data "assets;assets" ^
  --collect-all fastapi ^
  --collect-all starlette ^
  --collect-all uvicorn ^
  --collect-all httpx ^
  launcher.py
if errorlevel 1 goto FAIL

echo.
echo SUCCESS
echo Your release file is:
echo dist\FreeModels Proxy.exe
echo.
echo End users run the EXE directly.
echo No Python, pip, PowerShell or dependency installation is required.
pause
exit /b 0

:FAIL
echo.
echo Build failed.
pause
exit /b 1
