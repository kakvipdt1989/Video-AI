from pathlib import Path

from app.core.config import get_settings


def absolute_media_path(relative_path: str | None) -> Path | None:
    if not relative_path:
        return None
    return get_settings().media_root_path / relative_path


def relative_to_media(path: Path) -> str:
    return str(path.resolve().relative_to(get_settings().media_root_path)).replace("\\", "/")


def media_url(relative_path: str | None) -> str:
    if not relative_path:
        return ""
    return f"/media/{relative_path}"
