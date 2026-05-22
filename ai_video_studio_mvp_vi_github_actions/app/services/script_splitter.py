from dataclasses import dataclass
import re

from app.models import Character, Episode, Project
from app.services.prompt_engine import build_video_prompt


@dataclass
class SceneDraft:
    scene_number: int
    title: str
    scene_text: str
    characters: list[str]
    location: str
    action: str
    emotion: str
    camera: str
    lighting: str
    sound: str
    dialogue: str
    duration_seconds: int
    video_prompt: str
    negative_prompt: str
    continuity_notes: str


def _split_text(script_text: str) -> list[str]:
    cleaned = script_text.strip()
    if not cleaned:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", cleaned) if p.strip()]
    chunks: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) <= 650:
            chunks.append(paragraph)
            continue
        sentences = re.split(r"(?<=[.!?。！？])\s+", paragraph)
        buf = ""
        for sentence in sentences:
            if len(buf) + len(sentence) > 650 and buf:
                chunks.append(buf.strip())
                buf = sentence
            else:
                buf = f"{buf} {sentence}".strip()
        if buf:
            chunks.append(buf.strip())
    return chunks


def _detect_characters(text: str, characters: list[Character]) -> list[str]:
    text_lower = text.lower()
    matched = [char.name for char in characters if char.name.lower() in text_lower]
    if not matched and characters:
        matched = [characters[0].name]
    return matched


def _extract_dialogue(text: str) -> str:
    quoted = re.findall(r"[\"“”']([^\"“”']{2,200})[\"“”']", text)
    if quoted:
        return " | ".join(quoted[:4])
    colon_lines = [line.strip() for line in text.splitlines() if ":" in line and len(line) < 220]
    return " | ".join(colon_lines[:4])


def split_episode_script(project: Project, episode: Episode, characters: list[Character]) -> list[SceneDraft]:
    """MVP splitter: chia kịch bản theo đoạn văn, sau này có thể thay bằng AI text model."""
    chunks = _split_text(episode.script_text)
    drafts: list[SceneDraft] = []
    previous_summary: str | None = None

    for idx, chunk in enumerate(chunks, start=1):
        title = chunk.split(".")[0].strip()[:80] or f"Cảnh {idx}"
        detected_chars = _detect_characters(chunk, characters)
        scene_like = type("SceneLike", (), {})()
        scene_like.scene_number = idx
        scene_like.title = title
        scene_like.scene_text = chunk
        scene_like.characters_json = detected_chars
        scene_like.location = "Bối cảnh theo kịch bản; giữ thống nhất với thế giới của dự án."
        scene_like.action = chunk[:500]
        scene_like.emotion = "phù hợp với nhịp cảm xúc của kịch bản"
        scene_like.camera = "góc máy trung, chuyển động camera mượt, ngang tầm mắt, phong cách điện ảnh"
        scene_like.lighting = "ánh sáng điện ảnh, nhất quán trong toàn bộ tập phim"
        scene_like.sound = "âm thanh nền phù hợp với bối cảnh"
        scene_like.dialogue = _extract_dialogue(chunk)
        scene_like.duration_seconds = project.default_duration_per_scene or 8

        prompt_pack = build_video_prompt(project, episode, scene_like, characters, previous_summary)
        drafts.append(
            SceneDraft(
                scene_number=idx,
                title=title,
                scene_text=chunk,
                characters=detected_chars,
                location=scene_like.location,
                action=scene_like.action,
                emotion=scene_like.emotion,
                camera=scene_like.camera,
                lighting=scene_like.lighting,
                sound=scene_like.sound,
                dialogue=scene_like.dialogue,
                duration_seconds=scene_like.duration_seconds,
                video_prompt=prompt_pack["video_prompt"],
                negative_prompt=prompt_pack["negative_prompt"],
                continuity_notes=prompt_pack["continuity_notes"],
            )
        )
        previous_summary = chunk[:300]

    return drafts
