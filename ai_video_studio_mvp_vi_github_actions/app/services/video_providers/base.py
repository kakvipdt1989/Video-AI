from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class ProviderResult:
    provider_job_id: str
    status: str
    video_path: Path | None
    raw_response: dict


class VideoProvider(Protocol):
    provider_name: str

    def generate_video(
        self,
        prompt: str,
        negative_prompt: str,
        duration: int,
        aspect_ratio: str,
        reference_images: list[str] | None,
        output_path: Path,
    ) -> ProviderResult:
        ...

    def get_job_status(self, provider_job_id: str) -> dict:
        ...

    def download_video(self, provider_job_id: str, output_path: Path) -> Path:
        ...
