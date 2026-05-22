@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ========================================
echo   XUONG VIDEO AI MVP - CHAY TREN WINDOWS
echo ========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Khong tim thay Python. Hay cai Python 3.11+ va tick Add Python to PATH.
  pause
  exit /b 1
)
python windows\launcher_windows.py
pause
