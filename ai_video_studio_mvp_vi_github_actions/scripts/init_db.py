from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.db import Base, engine  # noqa: E402
from app import models  # noqa: F401,E402


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Đã tạo/cập nhật các bảng dữ liệu.")
