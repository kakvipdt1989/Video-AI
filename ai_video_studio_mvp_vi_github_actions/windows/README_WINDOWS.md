# Chạy trên Windows

## Cách 1: chạy ngay bằng file `.exe` hoặc `.bat`

Bấm đúp file ở thư mục gốc:

```text
Xuong Video AI.exe
```

Hoặc bấm đúp:

```text
chay_phan_mem_windows.bat
```

File chạy sẽ tự tạo môi trường `.venv`, cài thư viện, tạo database và mở trình duyệt tại:

```text
http://127.0.0.1:8000
```

## Cách 2: tạo lại file `.exe`

Trong gói đã có sẵn file `Xuong Video AI.exe`. Trên máy Windows, nếu muốn tạo lại, bấm đúp file:

```text
tao_file_exe_windows.bat
```

Sau khi chạy xong sẽ có file:

```text
Xuong Video AI.exe
```

Đặt file `.exe` này ở thư mục gốc phần mềm, cùng cấp với `app`, `scripts`, `requirements.txt`, `.env.example`.

## Yêu cầu

- Windows 10/11.
- Python 3.11+ và đã tick `Add Python to PATH` khi cài.
- FFmpeg đã cài và gọi được lệnh `ffmpeg` trong Command Prompt.

## Lưu ý về file `.exe`

File `.exe` được tạo bởi PyInstaller chỉ là launcher để chạy phần mềm web cục bộ. Nó không nhúng toàn bộ mã nguồn, database và thư mục media vào một file duy nhất. Cách này phù hợp cho MVP vì vẫn dễ sửa code và thay provider AI thật sau này.
