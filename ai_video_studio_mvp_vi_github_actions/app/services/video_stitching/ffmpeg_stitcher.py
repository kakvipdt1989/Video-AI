from pathlib import Path
import shutil
import subprocess
import tempfile

from app.core.config import get_settings


def stitch_videos(input_paths: list[Path], output_path: Path) -> Path:
    settings = get_settings()
    ffmpeg_exe = settings.ffmpeg_path
    if not Path(ffmpeg_exe).exists() and not shutil.which(ffmpeg_exe):
        raise RuntimeError(r"Không tìm thấy FFmpeg. Với bản portable, hãy đặt ffmpeg.exe vào tools\ffmpeg\bin\ffmpeg.exe hoặc cấu hình FFMPEG_BIN trong .env.")
    if not input_paths:
        raise ValueError("Không có video cảnh để ghép.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        list_file = Path(f.name)
        for path in input_paths:
            escaped = str(path.resolve()).replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")

    try:
        copy_cmd = [
            ffmpeg_exe,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(output_path),
        ]
        result = subprocess.run(copy_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            reencode_cmd = [
                ffmpeg_exe,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_file),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                str(output_path),
            ]
            subprocess.run(reencode_cmd, check=True, capture_output=True, text=True)
    finally:
        list_file.unlink(missing_ok=True)

    return output_path
