from functools import lru_cache
from pathlib import Path
import os
import shutil
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict


def runtime_root() -> Path:
    """Thư mục chứa dữ liệu chạy thật của phần mềm.

    - Khi chạy source: là thư mục hiện tại.
    - Khi chạy file .exe PyInstaller: là thư mục đặt file .exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd().resolve()


def bundled_root() -> Path:
    """Thư mục tài nguyên được PyInstaller giải nén khi chạy onefile."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()  # type: ignore[attr-defined]
    return runtime_root()


def find_ffmpeg(configured_value: str = "ffmpeg") -> str:
    """Tìm FFmpeg theo thứ tự ưu tiên cho bản portable Windows.

    Người dùng cuối không cần cài FFmpeg nếu file ffmpeg.exe được đặt tại:
    - tools/ffmpeg/bin/ffmpeg.exe
    - tools/ffmpeg/ffmpeg.exe
    - ffmpeg.exe nằm cùng thư mục với file chạy
    Hoặc nếu FFmpeg đã có trong PATH thì vẫn dùng bình thường.
    """
    value = configured_value or "ffmpeg"
    expanded = Path(os.path.expandvars(value)).expanduser()
    if expanded.is_absolute() and expanded.exists():
        return str(expanded)

    root = runtime_root()
    bundle = bundled_root()
    candidates = [
        root / value,
        root / "ffmpeg.exe",
        root / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe",
        root / "tools" / "ffmpeg" / "ffmpeg.exe",
        bundle / value,
        bundle / "ffmpeg.exe",
        bundle / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe",
        bundle / "tools" / "ffmpeg" / "ffmpeg.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    found = shutil.which(value)
    if found:
        return found
    found = shutil.which("ffmpeg")
    if found:
        return found
    return value


class Settings(BaseSettings):
    app_name: str = "Xưởng Video AI MVP"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./ai_video_studio.db"
    media_root: str = "media"
    default_provider: str = "mock_veo"
    ffmpeg_bin: str = "ffmpeg"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def media_root_path(self) -> Path:
        media_path = Path(self.media_root)
        if not media_path.is_absolute():
            media_path = runtime_root() / media_path
        return media_path.resolve()

    @property
    def ffmpeg_path(self) -> str:
        return find_ffmpeg(self.ffmpeg_bin)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.media_root_path.mkdir(parents=True, exist_ok=True)
    return settings
