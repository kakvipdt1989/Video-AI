from pathlib import Path
import uuid

from app.core.config import get_settings
from app.core.db import SessionLocal
from app.models import Episode, Scene, VideoJob
from app.services.media import absolute_media_path, relative_to_media
from app.services.video_providers import get_video_provider
from app.services.video_stitching import stitch_videos


def _scene_output_path(project_id: int, episode_id: int, scene_number: int) -> Path:
    root = get_settings().media_root_path
    filename = f"scene_{scene_number:03d}_{uuid.uuid4().hex[:8]}.mp4"
    return root / "projects" / str(project_id) / "episodes" / str(episode_id) / "scenes" / filename


def _final_output_path(project_id: int, episode_id: int) -> Path:
    root = get_settings().media_root_path
    return root / "projects" / str(project_id) / "episodes" / str(episode_id) / "final" / "final_episode.mp4"


def generate_scene_video(scene_id: int) -> None:
    db = SessionLocal()
    try:
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if scene is None:
            return
        episode = scene.episode
        project = episode.project

        scene.status = "processing"
        scene.error_message = None
        episode.status = "generating_video"
        db.commit()

        provider = get_video_provider(project.provider_name, db)
        output_path = _scene_output_path(project.id, episode.id, scene.scene_number)
        reference_images = [char.reference_image_path for char in project.characters if char.reference_image_path]

        request_payload = {
            "prompt": scene.video_prompt,
            "negative_prompt": scene.negative_prompt,
            "duration": scene.duration_seconds,
            "aspect_ratio": project.aspect_ratio,
            "reference_images": reference_images,
        }
        job = VideoJob(scene_id=scene.id, provider=provider.provider_name, status="processing", request_payload=request_payload)
        db.add(job)
        db.commit()
        db.refresh(job)

        result = provider.generate_video(
            prompt=scene.video_prompt or scene.scene_text,
            negative_prompt=scene.negative_prompt or "",
            duration=scene.duration_seconds,
            aspect_ratio=project.aspect_ratio,
            reference_images=reference_images,
            output_path=output_path,
        )

        rel_path = relative_to_media(result.video_path) if result.video_path else None
        job.provider_job_id = result.provider_job_id
        job.status = result.status
        job.response_payload = result.raw_response
        job.result_video_path = rel_path

        scene.video_job_id = result.provider_job_id
        scene.video_path = rel_path
        scene.status = "completed"
        db.commit()

        all_scenes = db.query(Scene).filter(Scene.episode_id == episode.id).all()
        if all_scenes and all(s.status == "completed" for s in all_scenes):
            episode.status = "ready_to_stitch"
            db.commit()
    except Exception as exc:
        db.rollback()
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if scene:
            scene.status = "error"
            scene.error_message = str(exc)
            scene.episode.status = "error"
            db.commit()
    finally:
        db.close()


def generate_episode_scenes(episode_id: int) -> None:
    db = SessionLocal()
    try:
        scene_ids = [s.id for s in db.query(Scene).filter(Scene.episode_id == episode_id).order_by(Scene.scene_number).all()]
    finally:
        db.close()
    for scene_id in scene_ids:
        generate_scene_video(scene_id)


def stitch_episode_video(episode_id: int) -> None:
    db = SessionLocal()
    try:
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        if episode is None:
            return
        project = episode.project
        scenes = db.query(Scene).filter(Scene.episode_id == episode.id).order_by(Scene.scene_number).all()
        if not scenes:
            raise RuntimeError("Tập phim chưa có cảnh.")
        not_ready = [s.scene_number for s in scenes if s.status != "completed" or not s.video_path]
        if not_ready:
            raise RuntimeError(f"Các cảnh chưa hoàn thành: {not_ready}")

        episode.status = "stitching"
        db.commit()

        input_paths = []
        for scene in scenes:
            path = absolute_media_path(scene.video_path)
            if path is None or not path.exists():
                raise RuntimeError(f"Không tìm thấy video cho cảnh {scene.scene_number}.")
            input_paths.append(path)

        output_path = _final_output_path(project.id, episode.id)
        stitch_videos(input_paths, output_path)

        episode.final_video_path = relative_to_media(output_path)
        episode.duration_seconds = sum(s.duration_seconds or 0 for s in scenes)
        episode.status = "completed"
        db.commit()
    except Exception as exc:
        db.rollback()
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        if episode:
            episode.status = "error"
            db.commit()
        print(f"[stitch_episode_video] error: {exc}")
    finally:
        db.close()
