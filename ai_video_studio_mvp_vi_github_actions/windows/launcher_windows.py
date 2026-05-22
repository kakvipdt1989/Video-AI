"""Launcher Windows cho Xưởng Video AI MVP.

File này có thể chạy trực tiếp bằng Python hoặc đóng gói thành .exe bằng PyInstaller.
Nó sẽ chuẩn bị môi trường ảo, cài thư viện, khởi tạo database và mở trình duyệt.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import webbrowser

HOST = "127.0.0.1"
PORT = "8000"
URL = f"http://{HOST}:{PORT}"


def project_root() -> Path:
    # Khi chạy file .py trong thư mục windows.
    here = Path(__file__).resolve()
    if here.parent.name.lower() == "windows":
        return here.parents[1]
    # Khi đã đóng gói .exe và đặt exe ở thư mục gốc dự án.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return here.parent


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print("\n> " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd), env=env)


def find_python(root: Path) -> Path | str:
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return venv_python
    for name in ("py", "python"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("Không tìm thấy Python. Hãy cài Python 3.11+ và chọn Add Python to PATH.")


def main() -> None:
    root = project_root()
    os.chdir(root)
    print("XƯỞNG VIDEO AI MVP")
    print(f"Thư mục phần mềm: {root}")

    if not (root / "app" / "main.py").exists():
        raise RuntimeError("Không tìm thấy mã nguồn app/main.py. Hãy đặt file chạy ở thư mục gốc dự án.")

    if not (root / ".env").exists() and (root / ".env.example").exists():
        shutil.copyfile(root / ".env.example", root / ".env")
        print("Đã tạo file .env từ .env.example")

    db_existed_before_start = (root / "ai_video_studio.db").exists()

    base_python = find_python(root)
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        run([str(base_python), "-m", "venv", ".venv"], root)

    python_exe = str(venv_python)
    run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], root)
    run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], root)
    run([python_exe, "scripts\\init_db.py"], root)

    # Chỉ seed dữ liệu mẫu khi database SQLite chưa tồn tại trước lúc khởi động để tránh tạo trùng.
    if not db_existed_before_start:
        try:
            run([python_exe, "scripts\\seed_demo.py"], root)
        except Exception as exc:
            print(f"Bỏ qua dữ liệu mẫu vì có lỗi: {exc}")

    print(f"\nĐang mở phần mềm tại {URL}")
    time.sleep(1)
    webbrowser.open(URL)
    subprocess.call([python_exe, "-m", "uvicorn", "app.main:app", "--host", HOST, "--port", PORT], cwd=str(root))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nCÓ LỖI KHI CHẠY PHẦN MỀM")
        print(str(exc))
        input("\nNhấn Enter để đóng cửa sổ...")
        raise
