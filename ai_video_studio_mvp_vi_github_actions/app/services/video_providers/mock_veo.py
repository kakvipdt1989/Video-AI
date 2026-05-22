from pathlib import Path
import hashlib
import shutil
import subprocess
import uuid

from app.core.config import get_settings
from app.services.video_providers.base import ProviderResult


class MockVeoProvider:
    provider_name = "mock_veo"

    def __init__(self) -> None:
        self.settings = get_settings()

    def _resolution(self, aspect_ratio: str) -> tuple[int, int]:
        if aspect_ratio == "9:16":
            return 720, 1280
        if aspect_ratio == "1:1":
            return 1080, 1080
        return 1280, 720

    def _color_for_prompt(self, prompt: str) -> str:
        # Nguồn màu của FFmpeg nhận mã màu dạng 0xRRGGBB.
        digest = hashlib.md5(prompt.encode("utf-8")).hexdigest()[:6]
        return f"0x{digest}"

    def generate_video(
        self,
        prompt: str,
        negative_prompt: str,
        duration: int,
        aspect_ratio: str,
        reference_images: list[str] | None,
        output_path: Path,
    ) -> ProviderResult:
        ffmpeg_exe = self.settings.ffmpeg_path
        if not Path(ffmpeg_exe).exists() and not shutil.which(ffmpeg_exe):
            raise RuntimeError(r"Không tìm thấy FFmpeg. Với bản portable, hãy đặt ffmpeg.exe vào tools\ffmpeg\bin\ffmpeg.exe hoặc cấu hình FFMPEG_BIN trong .env.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = self._resolution(aspect_ratio)
        color = self._color_for_prompt(prompt)
        provider_job_id = f"mock-{uuid.uuid4().hex}"

        cmd = [
            ffmpeg_exe,
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={width}x{height}:d={max(1, int(duration))}",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        return ProviderResult(
            provider_job_id=provider_job_id,
            status="completed",
            video_path=output_path,
            raw_response={
                "provider": self.provider_name,
                "provider_job_id": provider_job_id,
                "mock": True,
                "resolution": f"{width}x{height}",
                "reference_images": reference_images or [],
            },
        )

    def get_job_status(self, provider_job_id: str) -> dict:
        return {"provider_job_id": provider_job_id, "status": "completed", "mock": True}

    def download_video(self, provider_job_id: str, output_path: Path) -> Path:
        return output_path
