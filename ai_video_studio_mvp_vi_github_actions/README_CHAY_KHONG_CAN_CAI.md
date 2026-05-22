# Xưởng Video AI - bản chạy luôn trên Windows

Có thể làm bản chạy luôn, không cần người dùng cuối cài Python hoặc FFmpeg, bằng cách đóng gói phần mềm bằng PyInstaller và nhúng `ffmpeg.exe` vào gói portable.

## Kết quả mong muốn

Sau khi build, bạn sẽ có thư mục:

```text
 dist\XuongVideoAI\
   XuongVideoAI.exe
   CHAY_PHAN_MEM.bat
   _internal\...
   README_CHAY_KHONG_CAN_CAI.md
```

Bạn chỉ cần copy nguyên thư mục `dist\XuongVideoAI` sang máy Windows khác. Máy đó không cần cài:

- Python
- pip
- virtualenv
- FFmpeg

Người dùng chỉ cần bấm:

```text
XuongVideoAI.exe
```

hoặc:

```text
CHAY_PHAN_MEM.bat
```

## Cách tạo bản portable

> Việc build `.exe` chuẩn nên làm trên máy Windows. Máy build cần có Python 3.11+ một lần duy nhất. Máy người dùng cuối không cần Python.

### Bước 1: đặt FFmpeg vào thư mục phần mềm

Đặt file này:

```text
tools\ffmpeg\bin\ffmpeg.exe
```

Nếu chưa có FFmpeg, tải bản Windows static/essentials rồi lấy file `ffmpeg.exe` trong thư mục `bin`.

### Bước 2: chạy file build

Bấm đúp:

```text
windows\tao_ban_chay_luon_windows.bat
```

Sau khi chạy xong, bản portable nằm tại:

```text
dist\XuongVideoAI
```

### Bước 3: đưa cho máy khác dùng

Nén nguyên thư mục:

```text
dist\XuongVideoAI
```

Gửi cho máy khác. Máy đó giải nén và bấm `XuongVideoAI.exe`.

## Vì sao cần build trên Windows?

File `.exe` Windows thật nên được PyInstaller tạo trên Windows để tương thích với thư viện Python, thư viện hệ thống và định dạng thực thi của Windows. Build từ Linux sang Windows không ổn định và khó kiểm chứng.

## Lưu ý

- Bản portable dùng SQLite mặc định, dữ liệu nằm trong file `ai_video_studio.db` cạnh `.exe`.
- Video tạo ra nằm trong thư mục `media` cạnh `.exe`.
- Đóng cửa sổ đang chạy để tắt phần mềm.
- Nếu muốn dùng PostgreSQL hoặc Veo thật, chỉnh file `.env` cạnh `.exe`.
