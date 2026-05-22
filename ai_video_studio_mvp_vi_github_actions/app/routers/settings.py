from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.services.settings_service import get_setting, set_setting

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def settings_page(request: Request, db: Session = Depends(get_db)):
    keys = ["text_model_api_key", "veo_api_key", "veo_model", "default_resolution", "default_fps"]
    values = {key: get_setting(db, key, "") for key in keys}
    return request.app.state.templates.TemplateResponse(
        "settings/index.html",
        {
            "request": request,
            "values": values,
            "media_root": get_settings().media_root,
            "ffmpeg_bin": get_settings().ffmpeg_bin,
            "message": request.query_params.get("message"),
        },
    )


@router.post("")
def save_settings(
    text_model_api_key: str = Form(""),
    veo_api_key: str = Form(""),
    veo_model: str = Form("veo-3.1-generate-preview"),
    default_resolution: str = Form("1280x720"),
    default_fps: str = Form("30"),
    db: Session = Depends(get_db),
):
    set_setting(db, "text_model_api_key", text_model_api_key, is_secret=True)
    set_setting(db, "veo_api_key", veo_api_key, is_secret=True)
    set_setting(db, "veo_model", veo_model)
    set_setting(db, "default_resolution", default_resolution)
    set_setting(db, "default_fps", default_fps)
    return RedirectResponse(url="/settings?message=Đã lưu cài đặt", status_code=303)
