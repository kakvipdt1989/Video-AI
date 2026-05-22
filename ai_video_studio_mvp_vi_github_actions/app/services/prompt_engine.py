from app.models import Character, Episode, Project, Scene
from app.services.character_bible import build_character_bible, character_identity_prompt

DEFAULT_NEGATIVE_PROMPT = (
    "Không thay đổi nhân vật ngẫu nhiên, không đổi trang phục sai mạch truyện, "
    "không méo mặt, không thừa tay chân, không biến dạng bàn tay, không chữ lỗi trong hình, "
    "không logo, không watermark, không phụ đề gắn cứng nếu chưa được yêu cầu, "
    "không mặt bị nhòe, không nhấp nháy hình, không nhân vật bị nhân đôi, "
    "không thay đổi tuổi đột ngột, không đổi phong cách hình ảnh giữa các cảnh."
)


def _characters_for_scene(scene: Scene, characters: list[Character]) -> list[Character]:
    names = set(scene.characters_json or [])
    if not names:
        return characters
    return [char for char in characters if char.name in names]


def build_video_prompt(
    project: Project,
    episode: Episode,
    scene: Scene,
    characters: list[Character],
    previous_scene_summary: str | None = None,
) -> dict[str, str]:
    """Tạo prompt video bằng tiếng Việt, luôn chèn Hồ sơ nhân vật để giữ đồng nhất."""
    scene_characters = _characters_for_scene(scene, characters)
    bible = build_character_bible(project, scene_characters)
    previous_note = previous_scene_summary or "Đây là cảnh đầu tiên hoặc chưa có tóm tắt cảnh trước."
    subject_text = "\n".join(character_identity_prompt(char) for char in scene_characters) or "Cảnh này không có nhân vật được đặt tên."

    prompt = f"""
Tạo một cảnh video AI dài {scene.duration_seconds} giây, tỷ lệ khung hình {project.aspect_ratio}.

Chủ thể / nhân vật:
{subject_text}

Quy tắc giữ đồng nhất nhân vật:
Sử dụng đúng Hồ sơ nhân vật của dự án. Nhân vật phải giữ nguyên danh tính, cùng gương mặt, cùng kiểu tóc, cùng trang phục, cùng bảng màu, cùng tính cách và cùng định hướng giọng nói trong toàn bộ dự án. Không tự ý thêm nhân vật chính mới.

Hồ sơ nhân vật của dự án:
{bible}

Tập phim:
Tên tập: {episode.title}
Ngôn ngữ: {project.language}

Mô tả cảnh:
{scene.scene_text}

Hành động chính:
{scene.action or scene.scene_text}

Bối cảnh / phông nền:
{scene.location or 'Dựa trên thế giới của dự án và ngữ cảnh trong kịch bản.'}

Góc máy / chuyển động camera:
{scene.camera or 'góc máy ngang tầm mắt, chuyển động dolly-in chậm, phong cách điện ảnh'}

Ánh sáng:
{scene.lighting or 'ánh sáng điện ảnh tự nhiên, nhất quán với cảm xúc của cảnh'}

Tâm trạng / cảm xúc:
{scene.emotion or 'rõ cảm xúc, điện ảnh, mạch lạc với kịch bản'}

Phong cách hình ảnh:
{project.visual_style}

Âm thanh / lời thoại / lời dẫn:
{scene.sound or 'âm thanh môi trường nhẹ, phù hợp bối cảnh'}
{scene.dialogue or 'Không có lời thoại, trừ khi kịch bản yêu cầu.'}

Thời lượng:
{scene.duration_seconds} giây

Tỷ lệ video:
{project.aspect_ratio}

Ghi chú nối cảnh:
Tóm tắt cảnh trước: {previous_note}
Bảo đảm nối mạch với cảnh trước và cảnh sau. Giữ cùng thế giới, cùng phong cách hình ảnh, logic ánh sáng thống nhất và cùng nhận diện nhân vật. Tránh mọi thay đổi ngẫu nhiên về quần áo, tuổi, gương mặt, kiểu tóc, đạo cụ hoặc môi trường.
""".strip()

    continuity_notes = (
        "Luôn giữ cùng danh tính nhân vật, cùng gương mặt, cùng kiểu tóc, cùng trang phục, "
        "cùng phong cách hình ảnh, cùng thế giới truyện và tính liên tục của camera/ánh sáng giữa các cảnh."
    )

    return {
        "video_prompt": prompt,
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "continuity_notes": continuity_notes,
    }
