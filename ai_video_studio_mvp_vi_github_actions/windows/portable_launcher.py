"""Launcher portable cho Xưởng Video AI.

File này được dùng để đóng gói bằng PyInstaller thành bản Windows chạy luôn.
Bản đã build xong không cần cài Python, không cần tạo venv, không cần pip install.
Nếu ffmpeg.exe được nhúng khi build, người dùng cuối cũng không cần cài FFmpeg.
"""
from __future__ import annotations

from pathlib import Path
import os
import shutil
import sys
import time
import webbrowser

import uvicorn

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"


def exe_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def bundle_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()  # type: ignore[attr-defined]
    return exe_root()


def prepare_environment() -> None:
    root = exe_root()
    os.chdir(root)

    env_file = root / ".env"
    env_example_candidates = [root / ".env.example", bundle_root() / ".env.example"]
    if not env_file.exists():
        for candidate in env_example_candidates:
            if candidate.exists():
                shutil.copyfile(candidate, env_file)
                break
        else:
            env_file.write_text(
                "APP_NAME=Xưởng Video AI MVP\n"
                "DATABASE_URL=sqlite:///./ai_video_studio.db\n"
                "MEDIA_ROOT=media\n"
                "DEFAULT_PROVIDER=mock_veo\n"
                "FFMPEG_BIN=ffmpeg\n",
                encoding="utf-8",
            )

    (root / "media").mkdir(parents=True, exist_ok=True)

    # Ưu tiên ffmpeg.exe nằm cạnh file chạy hoặc trong gói PyInstaller.
    ffmpeg_candidates = [
        root / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe",
        root / "ffmpeg.exe",
        bundle_root() / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe",
        bundle_root() / "ffmpeg.exe",
    ]
    for ffmpeg in ffmpeg_candidates:
        if ffmpeg.exists():
            os.environ["FFMPEG_BIN"] = str(ffmpeg)
            break


def init_database_and_demo() -> None:
    from app.core.db import Base, SessionLocal, engine
    from app.models import Project

    db_path = exe_root() / "ai_video_studio.db"
    first_run = not db_path.exists()
    Base.metadata.create_all(bind=engine)

    if first_run:
        try:
            from scripts.seed_demo import main as seed_demo

            seed_demo()
        except Exception as exc:  # pragma: no cover - chỉ để launcher không bị tắt vì lỗi demo
            print(f"Không tạo được dữ liệu mẫu, vẫn tiếp tục chạy phần mềm: {exc}")
    else:
        db = SessionLocal()
        try:
            _ = db.query(Project).count()
        finally:
            db.close()


def main() -> None:
    print("========================================")
    print("        XƯỞNG VIDEO AI - BẢN PORTABLE")
    print("========================================")
    print("Đang chuẩn bị dữ liệu...")
    prepare_environment()
    init_database_and_demo()

    print(f"\nPhần mềm đang chạy tại: {URL}")
    print("Trình duyệt sẽ tự mở. Đóng cửa sổ này để tắt phần mềm.")
    time.sleep(1)
    webbrowser.open(URL)

    # Import sau khi đã chuẩn bị .env và thư mục chạy.
    from app.main import app

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nCÓ LỖI KHI CHẠY PHẦN MỀM")
        print(str(exc))
        input("\nNhấn Enter để đóng cửa sổ...")
        raise
