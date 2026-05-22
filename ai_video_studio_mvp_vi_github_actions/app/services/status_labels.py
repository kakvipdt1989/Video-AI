"""Nhãn tiếng Việt cho các trạng thái nội bộ.

Database vẫn lưu mã trạng thái ngắn bằng tiếng Anh để dễ xử lý logic.
Giao diện gọi `vn_status` để hiển thị tiếng Việt có dấu.
"""

STATUS_LABELS: dict[str, str] = {
    "draft": "Bản nháp",
    "segmenting": "Đang phân cảnh",
    "segmented": "Đã phân cảnh",
    "queued": "Đang chờ xử lý",
    "processing": "Đang xử lý",
    "generating_video": "Đang tạo video",
    "ready_to_stitch": "Sẵn sàng ghép video",
    "stitching": "Đang ghép video",
    "completed": "Hoàn thành",
    "error": "Có lỗi",
    "failed": "Thất bại",
}


def vn_status(value: str | None) -> str:
    if not value:
        return "Không rõ"
    return STATUS_LABELS.get(value, value)
