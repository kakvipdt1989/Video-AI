from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Episode, Scene
from app.services.background_jobs import generate_episode_scenes, generate_scene_video, stitch_episode_video
from app.services.media import media_url
from app.services.script_splitter import split_episode_script

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get("/{episode_id}")
def episode_detail(episode_id: int, request: Request, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        return RedirectResponse(url="/projects?message=Không tìm thấy tập phim", status_code=303)
    scenes = db.query(Scene).filter(Scene.episode_id == episode.id).order_by(Scene.scene_number).all()
    return request.app.state.templates.TemplateResponse(
        "episodes/detail.html",
        {
            "request": request,
            "episode": episode,
            "project": episode.project,
            "scenes": scenes,
            "media_url": media_url,
            "message": request.query_params.get("message"),
        },
    )


@router.post("/{episode_id}/script")
def update_script(episode_id: int, script_text: str = Form(""), db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if episode:
        episode.script_text = script_text
        episode.status = "draft"
        db.commit()
    return RedirectResponse(url=f"/episodes/{episode_id}?message=Đã lưu kịch bản", status_code=303)


@router.post("/{episode_id}/analyze")
def analyze_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        return RedirectResponse(url="/projects?message=Không tìm thấy tập phim", status_code=303)

    episode.status = "segmenting"
    db.query(Scene).filter(Scene.episode_id == episode.id).delete()
    db.commit()

    drafts = split_episode_script(episode.project, episode, episode.project.characters)
    for draft in drafts:
        scene = Scene(
            episode_id=episode.id,
            scene_number=draft.scene_number,
            title=draft.title,
            scene_text=draft.scene_text,
            characters_json=draft.characters,
            location=draft.location,
            action=draft.action,
            emotion=draft.emotion,
            camera=draft.camera,
            lighting=draft.lighting,
            sound=draft.sound,
            dialogue=draft.dialogue,
            duration_seconds=draft.duration_seconds,
            video_prompt=draft.video_prompt,
            negative_prompt=draft.negative_prompt,
            continuity_notes=draft.continuity_notes,
            status="draft",
        )
        db.add(scene)
    episode.status = "segmented" if drafts else "draft"
    db.commit()
    return RedirectResponse(url=f"/episodes/{episode.id}?message=Đã phân cảnh và tạo prompt", status_code=303)


@router.post("/{episode_id}/generate-all")
def generate_all(episode_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_episode_scenes, episode_id)
    return RedirectResponse(url=f"/episodes/{episode_id}?message=Đã đưa tất cả cảnh vào hàng đợi tạo video", status_code=303)


@router.post("/{episode_id}/stitch")
def stitch_episode(episode_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(stitch_episode_video, episode_id)
    return RedirectResponse(url=f"/episodes/{episode_id}?message=Đã đưa tập phim vào hàng đợi ghép video", status_code=303)


@router.post("/{episode_id}/delete")
def delete_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    project_id = episode.project_id if episode else None
    if episode:
        db.delete(episode)
        db.commit()
    url = f"/projects/{project_id}?message=Đã xóa tập phim" if project_id else "/projects"
    return RedirectResponse(url=url, status_code=303)


@router.post("/scenes/{scene_id}/prompt")
def update_scene_prompt(
    scene_id: int,
    title: str = Form(""),
    scene_text: str = Form(""),
    duration_seconds: int = Form(8),
    video_prompt: str = Form(""),
    negative_prompt: str = Form(""),
    db: Session = Depends(get_db),
):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if scene:
        scene.title = title
        scene.scene_text = scene_text
        scene.duration_seconds = duration_seconds
        scene.video_prompt = video_prompt
        scene.negative_prompt = negative_prompt
        scene.status = "draft"
        db.commit()
        return RedirectResponse(url=f"/episodes/{scene.episode_id}?message=Đã cập nhật cảnh", status_code=303)
    return RedirectResponse(url="/projects?message=Không tìm thấy cảnh", status_code=303)


@router.post("/scenes/{scene_id}/generate")
def generate_single_scene(scene_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if scene is None:
        return RedirectResponse(url="/projects?message=Không tìm thấy cảnh", status_code=303)
    episode_id = scene.episode_id
    background_tasks.add_task(generate_scene_video, scene_id)
    return RedirectResponse(url=f"/episodes/{episode_id}?message=Đã đưa cảnh vào hàng đợi tạo video", status_code=303)


@router.post("/scenes/{scene_id}/delete")
def delete_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if scene:
        episode_id = scene.episode_id
        db.delete(scene)
        db.commit()
        return RedirectResponse(url=f"/episodes/{episode_id}?message=Đã xóa cảnh", status_code=303)
    return RedirectResponse(url="/projects?message=Không tìm thấy cảnh", status_code=303)
