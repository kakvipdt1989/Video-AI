from sqlalchemy.orm import Session

from app.models import AppSetting
from app.services.video_providers.mock_veo import MockVeoProvider
from app.services.video_providers.veo_placeholder import VeoPlaceholderProvider


def _setting(db: Session | None, key: str) -> str | None:
    if db is None:
        return None
    item = db.query(AppSetting).filter(AppSetting.key == key).first()
    return item.value if item else None


def get_video_provider(provider_name: str | None, db: Session | None = None):
    name = provider_name or "mock_veo"
    if name == "mock_veo":
        return MockVeoProvider()
    if name == "veo_placeholder":
        return VeoPlaceholderProvider(api_key=_setting(db, "veo_api_key"), model_name=_setting(db, "veo_model") or "veo-3.1-generate-preview")
    raise ValueError(f"Nhà cung cấp video chưa được hỗ trợ: {name}")
