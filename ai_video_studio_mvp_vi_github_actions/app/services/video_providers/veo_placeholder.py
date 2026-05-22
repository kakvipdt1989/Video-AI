from pathlib import Path

from app.services.video_providers.base import ProviderResult


class VeoPlaceholderProvider:
    """Khung adapter cho API Google Veo / Gemini / Vertex AI thật.

    Hãy thay file này sau khi có endpoint chính thức, phương thức xác thực,
    mã model và schema phản hồi. Giữ nguyên các public method để phần còn lại
    của ứng dụng không cần thay đổi.
    """

    provider_name = "veo_placeholder"

    def __init__(self, api_key: str | None = None, model_name: str = "veo-3.1-generate-preview") -> None:
        self.api_key = api_key
        self.model_name = model_name

    def generate_video(
        self,
        prompt: str,
        negative_prompt: str,
        duration: int,
        aspect_ratio: str,
        reference_images: list[str] | None,
        output_path: Path,
    ) -> ProviderResult:
        raise NotImplementedError(
            "VeoPlaceholderProvider chưa gọi API thật. Hãy thay bằng Gemini API hoặc Vertex AI wrapper chính thức."
        )

    def get_job_status(self, provider_job_id: str) -> dict:
        raise NotImplementedError

    def download_video(self, provider_job_id: str, output_path: Path) -> Path:
        raise NotImplementedError
