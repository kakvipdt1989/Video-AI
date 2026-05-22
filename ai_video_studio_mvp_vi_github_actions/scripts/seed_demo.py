from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.db import Base, SessionLocal, engine  # noqa: E402
from app.models import Character, Episode, Project  # noqa: E402

DEMO_SCRIPT = """
Linh đứng trước cánh cổng làng cổ vào lúc hoàng hôn. Cô cầm chiếc la bàn đồng cũ của cha, ánh mắt vừa lo lắng vừa quyết tâm. Gió thổi qua hàng tre, tiếng chuông chùa xa xa vang lên.

Minh chạy tới, thở hổn hển: "Linh, chúng ta không còn nhiều thời gian. Bản đồ nói kho báu nằm dưới giếng đá." Linh nhìn Minh, gật đầu và bước vào con đường lát gạch phủ rêu.

Hai người dừng trước giếng đá giữa sân đình. Mặt nước phản chiếu bầu trời tím. Khi Linh đặt la bàn lên thành giếng, một luồng sáng xanh hiện ra, mở ra lối đi bí mật dưới lòng đất.
""".strip()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Project).filter(Project.name == "Kho báu dưới giếng đá").first()
        if existing:
            print(f"Dự án mẫu đã tồn tại: /projects/{existing.id}")
            return
        project = Project(
            name="Kho báu dưới giếng đá",
            description="Phim phiêu lưu thiếu nhi ngắn, giữ phong cách điện ảnh Việt Nam huyền bí.",
            genre="truyện thiếu nhi phiêu lưu",
            visual_style="phim điện ảnh chân thực, làng quê Việt Nam ấm áp, hiện thực huyền ảo",
            aspect_ratio="16:9",
            language="Tiếng Việt",
            default_duration_per_scene=8,
            provider_name="mock_veo",
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        chars = [
            Character(
                project_id=project.id,
                name="Linh",
                role="nhân vật chính",
                age="12",
                gender="nữ",
                appearance="cô bé Việt Nam dáng nhỏ, nhanh nhẹn, đôi mắt sáng và biểu cảm thông minh",
                face_description="gương mặt trái xoan, mắt nâu lớn, nụ cười nhẹ, không thay đổi qua các cảnh",
                hair_description="tóc đen dài ngang vai, buộc nửa đầu bằng dây màu xanh",
                outfit_description="áo sơ mi trắng, quần jeans xanh, ba lô vải nâu, luôn đeo la bàn đồng cũ",
                dominant_colors="trắng, xanh, nâu đồng",
                personality="dũng cảm, tò mò, giàu lòng trắc ẩn",
                voice_description="giọng nữ trẻ, rõ, ấm, hơi hồi hộp khi khám phá",
            ),
            Character(
                project_id=project.id,
                name="Minh",
                role="bạn đồng hành",
                age="13",
                gender="nam",
                appearance="cậu bé Việt Nam cao hơn Linh một chút, dáng nhanh nhẹn, luôn cầm cuốn sổ bản đồ",
                face_description="mặt tròn, mắt đen, lông mày rậm, nét mặt hài hước và chân thành",
                hair_description="tóc đen ngắn hơi rối",
                outfit_description="áo thun vàng nhạt, áo khoác xanh rêu, quần kaki, giày thể thao cũ",
                dominant_colors="vàng nhạt, xanh rêu, kaki",
                personality="thông minh, hơi sợ nhưng rất trung thành",
                voice_description="giọng nam thiếu niên, nhanh, đôi lúc lắp bắp khi lo lắng",
            ),
        ]
        db.add_all(chars)
        db.add(Episode(project_id=project.id, episode_number=1, title="Ánh sáng dưới giếng", script_text=DEMO_SCRIPT, status="draft"))
        db.commit()
        print(f"Đã tạo dữ liệu mẫu: /projects/{project.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
