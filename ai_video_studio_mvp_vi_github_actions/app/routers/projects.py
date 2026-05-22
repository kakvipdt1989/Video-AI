from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.models import Character, Episode, Project
from app.services.character_bible import build_character_bible

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def project_list(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.updated_at.desc()).all()
    return request.app.state.templates.TemplateResponse(
        "projects/list.html",
        {"request": request, "projects": projects, "message": request.query_params.get("message")},
    )


@router.post("")
def create_project(
    name: str = Form(...),
    description: str = Form(""),
    genre: str = Form("phim ngắn"),
    visual_style: str = Form("điện ảnh chân thực"),
    aspect_ratio: str = Form("16:9"),
    language: str = Form("Tiếng Việt"),
    default_duration_per_scene: int = Form(8),
    provider_name: str = Form("mock_veo"),
    db: Session = Depends(get_db),
):
    project = Project(
        name=name,
        description=description,
        genre=genre,
        visual_style=visual_style,
        aspect_ratio=aspect_ratio,
        language=language,
        default_duration_per_scene=default_duration_per_scene,
        provider_name=provider_name,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return RedirectResponse(url=f"/projects/{project.id}?message=Đã tạo dự án", status_code=303)


@router.get("/{project_id}")
def project_detail(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return RedirectResponse(url="/projects?message=Không tìm thấy dự án", status_code=303)
    bible = build_character_bible(project, project.characters)
    return request.app.state.templates.TemplateResponse(
        "projects/detail.html",
        {
            "request": request,
            "project": project,
            "character_bible": bible,
            "message": request.query_params.get("message"),
        },
    )


@router.post("/{project_id}/delete")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    return RedirectResponse(url="/projects?message=Đã xóa dự án", status_code=303)


@router.post("/{project_id}/characters")
def create_character(
    project_id: int,
    name: str = Form(...),
    role: str = Form(""),
    age: str = Form(""),
    gender: str = Form(""),
    appearance: str = Form(""),
    face_description: str = Form(""),
    hair_description: str = Form(""),
    outfit_description: str = Form(""),
    dominant_colors: str = Form(""),
    personality: str = Form(""),
    voice_description: str = Form(""),
    fixed_character_prompt: str = Form(""),
    db: Session = Depends(get_db),
):
    character = Character(
        project_id=project_id,
        name=name,
        role=role,
        age=age,
        gender=gender,
        appearance=appearance,
        face_description=face_description,
        hair_description=hair_description,
        outfit_description=outfit_description,
        dominant_colors=dominant_colors,
        personality=personality,
        voice_description=voice_description,
        fixed_character_prompt=fixed_character_prompt,
    )
    db.add(character)
    db.commit()
    return RedirectResponse(url=f"/projects/{project_id}?message=Đã thêm nhân vật", status_code=303)


@router.post("/{project_id}/episodes")
def create_episode(
    project_id: int,
    episode_number: int = Form(1),
    title: str = Form(...),
    script_text: str = Form(""),
    db: Session = Depends(get_db),
):
    episode = Episode(project_id=project_id, episode_number=episode_number, title=title, script_text=script_text, status="draft")
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return RedirectResponse(url=f"/episodes/{episode.id}?message=Đã tạo tập phim", status_code=303)


@router.post("/{project_id}/characters/{character_id}/delete")
def delete_character(project_id: int, character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id, Character.project_id == project_id).first()
    if character:
        db.delete(character)
        db.commit()
    return RedirectResponse(url=f"/projects/{project_id}?message=Đã xóa nhân vật", status_code=303)
