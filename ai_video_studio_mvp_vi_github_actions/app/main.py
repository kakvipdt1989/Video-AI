from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.core.db import Base, engine
from app import models  # noqa: F401 - bảo đảm models được import trước create_all
from app.routers import dashboard, episodes, projects, settings
from app.services.status_labels import vn_status

config_settings = get_settings()

app = FastAPI(title=config_settings.app_name)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/media", StaticFiles(directory=config_settings.media_root_path), name="media")
app.state.templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.state.templates.env.filters["vn_status"] = vn_status

app.include_router(dashboard.router)
app.include_router(projects.router)
app.include_router(episodes.router)
app.include_router(settings.router)


@app.on_event("startup")
def on_startup() -> None:
    config_settings.media_root_path.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
