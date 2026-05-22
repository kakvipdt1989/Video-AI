from app.models import Character, Project


def character_identity_prompt(character: Character) -> str:
    """Sinh mô tả nhận diện cố định cho một nhân vật bằng tiếng Việt."""
    if character.fixed_character_prompt:
        return character.fixed_character_prompt.strip()

    parts = [
        f"Tên: {character.name}",
        f"Vai trò: {character.role or 'chưa khai báo'}",
        f"Tuổi: {character.age or 'chưa khai báo'}",
        f"Giới tính: {character.gender or 'chưa khai báo'}",
        f"Ngoại hình: {character.appearance or 'chưa khai báo'}",
        f"Gương mặt: {character.face_description or 'chưa khai báo'}",
        f"Tóc: {character.hair_description or 'chưa khai báo'}",
        f"Trang phục mặc định: {character.outfit_description or 'chưa khai báo'}",
        f"Màu sắc chủ đạo: {character.dominant_colors or 'chưa khai báo'}",
        f"Tính cách: {character.personality or 'chưa khai báo'}",
        f"Giọng nói: {character.voice_description or 'chưa khai báo'}",
    ]
    return "; ".join(parts)


def build_character_bible(project: Project, characters: list[Character]) -> str:
    """Sinh Hồ sơ nhân vật cho toàn bộ dự án bằng tiếng Việt có dấu."""
    if not characters:
        return "Dự án chưa có nhân vật. Hãy thêm nhân vật để hệ thống giữ đồng nhất khi tạo video."

    lines = [
        f"HỒ SƠ NHÂN VẬT CỐ ĐỊNH CHO DỰ ÁN: {project.name}",
        "Quy tắc chung: mọi cảnh được tạo phải giữ nguyên danh tính nhân vật, cùng gương mặt, cùng kiểu tóc, cùng trang phục mặc định, cùng bảng màu, cùng tính cách và cùng định hướng giọng nói, trừ khi người dùng chủ động thay đổi.",
        "",
    ]
    for idx, char in enumerate(characters, start=1):
        lines.append(f"{idx}. {char.name}")
        lines.append(character_identity_prompt(char))
        if char.reference_image_path:
            lines.append(f"Đường dẫn ảnh tham chiếu: {char.reference_image_path}")
        lines.append("")
    return "\n".join(lines).strip()
