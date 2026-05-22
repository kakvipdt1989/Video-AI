@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0\.."

echo ========================================
echo   TAO BAN PORTABLE CHAY LUON WINDOWS
echo ========================================
echo.
echo Ban build xong se nam o: dist\XuongVideoAI
echo May nguoi dung cuoi KHONG can cai Python, pip hoac FFmpeg.
echo.

if not exist "tools\ffmpeg\bin\ffmpeg.exe" (
  echo CHUA CO FFMPEG DE NHUNG VAO BAN PORTABLE.
  echo Hay dat ffmpeg.exe vao:
  echo   tools\ffmpeg\bin\ffmpeg.exe
  echo.
  echo Sau do chay lai file nay.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo May dung de BUILD can co Python 3.11+.
  echo Luu y: chi may build can Python, may nguoi dung cuoi KHONG can Python.
  pause
  exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

rmdir /s /q build 2>nul
rmdir /s /q dist\XuongVideoAI 2>nul

echo.
echo Dang dong goi, vui long doi...
pyinstaller --noconfirm --clean --onedir --name "XuongVideoAI" ^
  --add-data "app\templates;app\templates" ^
  --add-data "app\static;app\static" ^
  --add-data ".env.example;." ^
  --add-data "docs;docs" ^
  --add-data "migrations;migrations" ^
  --add-data "scripts;scripts" ^
  --add-binary "tools\ffmpeg\bin\ffmpeg.exe;tools\ffmpeg\bin" ^
  --collect-submodules app ^
  --collect-submodules scripts ^
  --hidden-import uvicorn.logging ^
  --hidden-import uvicorn.loops ^
  --hidden-import uvicorn.loops.auto ^
  --hidden-import uvicorn.protocols ^
  --hidden-import uvicorn.protocols.http ^
  --hidden-import uvicorn.protocols.http.auto ^
  --hidden-import uvicorn.protocols.websockets ^
  --hidden-import uvicorn.protocols.websockets.auto ^
  --hidden-import uvicorn.lifespan ^
  --hidden-import uvicorn.lifespan.on ^
  windows\portable_launcher.py

if errorlevel 1 (
  echo.
  echo Dong goi that bai.
  pause
  exit /b 1
)

copy /Y README_CHAY_KHONG_CAN_CAI.md "dist\XuongVideoAI\README_CHAY_KHONG_CAN_CAI.md" >nul
copy /Y README.md "dist\XuongVideoAI\README_GOC.md" >nul

echo @echo off> "dist\XuongVideoAI\CHAY_PHAN_MEM.bat"
echo chcp 65001 ^>nul>> "dist\XuongVideoAI\CHAY_PHAN_MEM.bat"
echo cd /d "%%~dp0">> "dist\XuongVideoAI\CHAY_PHAN_MEM.bat"
echo start "" "XuongVideoAI.exe">> "dist\XuongVideoAI\CHAY_PHAN_MEM.bat"

echo.
echo DA TAO XONG BAN CHAY LUON:
echo   dist\XuongVideoAI\XuongVideoAI.exe
echo.
echo Hay nen/toan bo thu muc dist\XuongVideoAI va chuyen sang may Windows khac.
echo May do chi can bam XuongVideoAI.exe hoac CHAY_PHAN_MEM.bat.
pause
