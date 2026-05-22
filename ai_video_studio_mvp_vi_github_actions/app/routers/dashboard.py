from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Episode, Project, Scene

router = APIRouter()


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    total_projects = db.query(Project).count()
    processing_episodes = db.query(Episode).filter(Episode.status.in_(["segmenting", "generating_video", "stitching"])).count()
    completed_episodes = db.query(Episode).filter(Episode.status == "completed").count()
    errors = db.query(Scene).filter(Scene.status == "error").order_by(Scene.updated_at.desc()).limit(5).all()
    recent_projects = db.query(Project).order_by(Project.updated_at.desc()).limit(5).all()
    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_projects": total_projects,
            "processing_episodes": processing_episodes,
            "completed_episodes": completed_episodes,
            "errors": errors,
            "recent_projects": recent_projects,
        },
    )
