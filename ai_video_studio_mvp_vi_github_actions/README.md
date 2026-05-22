# Xưởng Video AI MVP

Phần mềm web tạo video AI từ kịch bản nhiều cảnh. Bản MVP chạy cục bộ, dùng FastAPI + SQLAlchemy + Jinja2/Bootstrap, có nhà cung cấp Veo mô phỏng để tạo video mẫu bằng FFmpeg rồi ghép thành video tập hoàn chỉnh.

Giao diện, thông báo, prompt tạo video và tài liệu hướng dẫn đã được Việt hóa tiếng Việt có dấu.

## Tính năng đã có trong MVP

- Tạo dự án video.
- Khai báo thể loại, phong cách hình ảnh, tỷ lệ video, ngôn ngữ, nhà cung cấp AI.
- Thêm nhân vật với ngoại hình, gương mặt, tóc, trang phục, màu sắc, tính cách, giọng nói.
- Tự sinh Hồ sơ nhân vật cố định cho dự án.
- Tạo tập phim, nhập kịch bản.
- Phân cảnh tự động bằng bộ chia kịch bản nội bộ.
- Tạo prompt video, prompt loại trừ và ghi chú nối cảnh cho từng cảnh.
- Cho phép chỉnh prompt từng cảnh.
- Mô phỏng tạo video từng cảnh bằng FFmpeg.
- Ghép video cảnh thành video cuối bằng FFmpeg.
- Trang cài đặt API key và tên model.
- Dữ liệu mẫu có 2 nhân vật và 1 tập kịch bản.
- Có file chạy Windows `.bat`, có sẵn file launcher `Xuong Video AI.exe`, và có script tạo lại file `.exe` bằng PyInstaller nếu cần.

## Cấu trúc thư mục

```text
ai_video_studio_mvp/
  app/
    core/                  # cấu hình, kết nối database
    models/                # SQLAlchemy models
    routers/               # routes FastAPI
    services/
      video_providers/     # provider nền tảng, Veo mô phỏng, Veo chờ cấu hình
      video_stitching/     # ghép video bằng FFmpeg
      background_jobs.py
      character_bible.py
      prompt_engine.py
      script_splitter.py
      status_labels.py
    templates/             # giao diện Jinja2 HTML
    static/                # CSS/JS
    main.py
  docs/
    ARCHITECTURE.md
    SAMPLE_OUTPUT_PROMPTS.md
  migrations/
    001_init.sql
  scripts/
    init_db.py
    seed_demo.py
  windows/
    launcher_windows.py
    README_WINDOWS.md
  chay_phan_mem_windows.bat
  tao_file_exe_windows.bat
  media/                   # video output
  requirements.txt
  .env.example
```

## Yêu cầu hệ thống

- Python 3.11+.
- FFmpeg đã cài và chạy được lệnh `ffmpeg`.
- PostgreSQL nếu muốn chạy đúng stack production. Bản MVP hỗ trợ SQLite để kiểm thử nhanh cục bộ.

## Chạy nhanh trên Windows

Cách dễ nhất: bấm đúp file:

```text
Xuong Video AI.exe
```

Hoặc chạy bằng file batch:

```text
chay_phan_mem_windows.bat
```

Cả hai cách đều sẽ tự tạo môi trường `.venv`, cài thư viện, khởi tạo database và mở trình duyệt tại:

```text
http://127.0.0.1:8000
```

## Tạo lại file `.exe` trên Windows

Trong gói đã có sẵn `Xuong Video AI.exe`. Nếu muốn tự tạo lại file `.exe`, bấm đúp file:

```text
tao_file_exe_windows.bat
```

Sau khi chạy xong sẽ tạo lại file:

```text
Xuong Video AI.exe
```

Đặt file `.exe` ở thư mục gốc phần mềm, cùng cấp với `app`, `scripts`, `requirements.txt`. File `.exe` này là launcher cho phần mềm web cục bộ, không phải bản đóng gói một file duy nhất chứa toàn bộ source/media/database.

## Cài đặt thủ công bằng SQLite

```bash
cd ai_video_studio_mvp
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

Mở trình duyệt:

```text
http://127.0.0.1:8000
```

## Chạy với PostgreSQL

Tạo database:

```sql
CREATE DATABASE ai_video_studio;
```

Sửa `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@cục bộhost:5432/ai_video_studio
MEDIA_ROOT=media
DEFAULT_PROVIDER=mock_veo
FFMPEG_BIN=ffmpeg
```

Khởi tạo bảng:

```bash
python scripts/init_db.py
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

Hoặc chạy schema SQL thủ công:

```bash
psql -U postgres -d ai_video_studio -f migrations/001_init.sql
```

## Luồng sử dụng

1. Vào `/projects`, tạo dự án.
2. Vào chi tiết dự án, thêm nhân vật.
3. Tạo tập phim và nhập kịch bản.
4. Mở trang tập phim, bấm `Phân cảnh tự động`.
5. Kiểm tra/chỉnh prompt từng cảnh.
6. Bấm `Tạo video cho tất cả cảnh`.
7. Tải lại trang sau khi job chạy xong.
8. Bấm `Ghép video hoàn chỉnh`.
9. Tải lại trang và xem video cuối.

## Thư mục media

Video được lưu theo dạng:

```text
media/projects/{project_id}/episodes/{episode_id}/scenes/scene_001_xxxxxxxx.mp4
media/projects/{project_id}/episodes/{episode_id}/final/final_episode.mp4
```

## Cách thay provider mô phỏng bằng Veo thật

Lớp trừu tượng nhà cung cấp nằm ở:

```text
app/services/video_providers/base.py
app/services/video_providers/registry.py
app/services/video_providers/veo_bản chờ cấu hình.py
```

Giữ nguyên interface:

```python
generate_video(prompt, negative_prompt, duration, aspect_ratio, reference_images, output_path)
get_job_status(provider_job_id)
download_video(provider_job_id, output_path)
```

Khi có API thật, làm như sau:

1. Tạo file provider mới, ví dụ `app/services/video_providers/google_veo.py`.
2. Trong `generate_video`, gửi prompt, prompt loại trừ, duration, aspect_ratio, reference images đến API.
3. Lưu `provider_job_id` trả về.
4. Trong `get_job_status`, kiểm tra trạng thái job.
5. Trong `download_video`, tải file mp4 về `output_path`.
6. Đăng ký provider trong `registry.py`.
7. Chọn provider mới khi tạo dự án hoặc sửa trường `projects.provider_name`.

Bản bản chờ cấu hình hiện tại cố tình báo `NotImplementedError` để tránh hiểu nhầm là đã gọi API thật.

## Nâng cấp gợi ý

- Thay bộ chia cảnh heuristic bằng AI text model để trích xuất bối cảnh, hành động, cảm xúc, camera, ánh sáng tốt hơn.
- Thêm Celery + Redis thay cho FastAPI BackgroundTasks.
- Thêm đăng nhập bằng bcrypt trực tiếp.
- Thêm upload ảnh tham chiếu nhân vật.
- Thêm TTS, SRT, gắn phụ đề vào video.
- Chuẩn hóa resolution/FPS/audio nâng cao trước khi ghép video.


## Tạo bản chạy luôn trên Windows không cần cài Python/FFmpeg

Bản này đã có thêm tài liệu và script để tạo gói portable. Xem file:

```text
README_CHAY_KHONG_CAN_CAI.md
windows\tao_ban_chay_luon_windows.bat
```

Sau khi build xong trên Windows, máy người dùng cuối chỉ cần bấm `XuongVideoAI.exe`, không cần cài Python, pip hoặc FFmpeg.
