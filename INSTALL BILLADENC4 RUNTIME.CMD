@echo off
setlocal

fltmc >nul 2>&1
if not "%errorlevel%"=="0" (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-BILLADENC4-Runtime.ps1"
set "INSTALL_EXIT=%errorlevel%"
pause
exit /b %INSTALL_EXIT%
