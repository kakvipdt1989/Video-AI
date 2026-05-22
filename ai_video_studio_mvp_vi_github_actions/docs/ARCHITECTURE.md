# Kiến trúc tổng thể - Xưởng Video AI MVP

## Mục tiêu

Hệ thống tạo video AI từ kịch bản nhiều tập. Bản MVP ưu tiên chạy được trên máy cục bộ:

1. Tạo dự án.
2. Thêm nhân vật.
3. Tạo tập phim và nhập kịch bản.
4. Phân cảnh tự động bằng bộ chia nội bộ.
5. Tạo prompt video cho từng cảnh dựa trên Hồ sơ nhân vật cố định.
6. Mô phỏng tạo video ngắn bằng FFmpeg.
7. Ghép các video cảnh thành video tập hoàn chỉnh.

## Thành phần chính

- `app/main.py`: khởi tạo FastAPI, Jinja2, static/media, routers, database và filter hiển thị trạng thái tiếng Việt.
- `app/models/entities.py`: schema SQLAlchemy cho dự án, nhân vật, tập phim, cảnh, job video, tài sản dự án, cài đặt ứng dụng.
- `app/routers`: route web cho bảng điều khiển, dự án, tập phim, cài đặt.
- `app/services/script_splitter.py`: chia kịch bản thành cảnh bằng heuristic, có thể thay bằng AI text model.
- `app/services/character_bible.py`: sinh Hồ sơ nhân vật cố định và prompt nhận diện nhân vật.
- `app/services/prompt_engine.py`: tạo prompt video, prompt loại trừ, ghi chú nối cảnh bằng tiếng Việt.
- `app/services/status_labels.py`: chuyển mã trạng thái nội bộ sang nhãn tiếng Việt có dấu.
- `app/services/video_providers`: abstraction provider, Veo mô phỏng, bản chờ cấu hình cho Veo thật.
- `app/services/background_jobs.py`: xử lý tạo video cảnh và ghép video bằng background task của FastAPI.
- `app/services/video_stitching/ffmpeg_stitcher.py`: ghép video bằng FFmpeg concat.
- `windows/launcher_windows.py`: launcher Windows, có thể đóng gói thành `.exe`.
- `media/`: lưu video cảnh và video cuối.

## Luồng dữ liệu

```text
Dự án + Nhân vật -> Hồ sơ nhân vật cố định
Kịch bản tập -> Bộ chia cảnh -> Cảnh + Prompt
Cảnh -> Nhà cung cấp video -> File MP4 từng cảnh
Các cảnh hoàn thành -> FFmpeg stitcher -> MP4 tập hoàn chỉnh
```

## Lớp trừu tượng nhà cung cấp

Interface provider gồm:

```python
generate_video(prompt, negative_prompt, duration, aspect_ratio, reference_images, output_path)
get_job_status(provider_job_id)
download_video(provider_job_id, output_path)
```

Bản MVP dùng `MockVeoProvider`, tạo clip màu bằng FFmpeg để test toàn bộ luồng mà chưa cần API key.

## Cách giữ đồng nhất nhân vật

- Mỗi nhân vật có mô tả cố định về gương mặt, tóc, trang phục, màu sắc, tính cách và giọng nói.
- `build_character_bible()` gom các mô tả này thành Hồ sơ nhân vật cố định.
- `build_video_prompt()` luôn chèn Hồ sơ nhân vật vào prompt từng cảnh.
- Prompt luôn nhấn mạnh: giữ cùng danh tính, cùng gương mặt, cùng kiểu tóc, cùng trang phục, cùng bảng màu, cùng phong cách hình ảnh và cùng thế giới truyện.

## Mở rộng sau MVP

- Thay `script_splitter.py` bằng AI text model để phân cảnh sâu hơn.
- Thay `VeoPlaceholderProvider` bằng Gemini API hoặc Vertex AI wrapper thật.
- Chuyển background task sang Celery + Redis.
- Thêm đăng nhập, phân quyền, thanh toán.
- Thêm upload ảnh tham chiếu nhân vật.
- Thêm SRT, giọng đọc AI, gắn phụ đề vào video.
- Thêm chuẩn hóa video nâng cao trước khi ghép.
