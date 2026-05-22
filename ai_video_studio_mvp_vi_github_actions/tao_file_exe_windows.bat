@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ========================================
echo   DONG GOI FILE EXE CHO WINDOWS
echo ========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Khong tim thay Python. Hay cai Python 3.11+ va tick Add Python to PATH.
  pause
  exit /b 1
)
python -m pip install --upgrade pip
python -m pip install pyinstaller
pyinstaller --onefile --name "Xuong Video AI" windows\launcher_windows.py
if errorlevel 1 (
  echo Dong goi exe that bai.
  pause
  exit /b 1
)
copy /Y "dist\Xuong Video AI.exe" "Xuong Video AI.exe" >nul
echo.
echo Da tao file: Xuong Video AI.exe
echo Hay de file exe nam trong thu muc goc cua phan mem, cung cap voi app, scripts, requirements.txt.
pause
