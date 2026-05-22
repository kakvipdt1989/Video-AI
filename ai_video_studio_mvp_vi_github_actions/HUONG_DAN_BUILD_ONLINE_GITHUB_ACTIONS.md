# Hướng dẫn tạo bản Windows chạy luôn bằng GitHub Actions

Mục tiêu của cách này:

- Máy của bạn không cần cài Python.
- Máy của bạn không cần cài FFmpeg.
- Máy của bạn không cần cài PyInstaller.
- GitHub sẽ dùng máy Windows online để tự đóng gói.
- Sau khi build xong, bạn tải về file `XuongVideoAI-Windows-Portable.zip`.
- Người dùng cuối chỉ cần giải nén và bấm `XuongVideoAI.exe`.

## 1. Tạo repository trên GitHub

1. Đăng nhập GitHub.
2. Bấm **New repository**.
3. Đặt tên ví dụ: `xuong-video-ai`.
4. Chọn **Private** hoặc **Public** đều được.
5. Bấm **Create repository**.

## 2. Upload source code

1. Giải nén gói source này.
2. Vào repository vừa tạo trên GitHub.
3. Bấm **Add file** > **Upload files**.
4. Kéo toàn bộ nội dung trong thư mục source lên GitHub.

Lưu ý quan trọng: cần upload cả thư mục ẩn `.github` vì trong đó có workflow build Windows.

Cấu trúc trên GitHub phải giống như sau:

```text
.github/workflows/build-windows-portable.yml
app/
windows/
requirements.txt
README.md
```

Nếu không thấy thư mục `.github`, hãy bật hiển thị file ẩn trên máy của bạn trước khi upload.

## 3. Chạy workflow build

1. Vào tab **Actions** trên GitHub repository.
2. Chọn workflow **Tạo bản Windows Portable**.
3. Bấm **Run workflow**.
4. Chọn branch `main` hoặc `master`.
5. Bấm nút **Run workflow** màu xanh.

GitHub sẽ tự làm các việc sau:

- Cài Python trên máy Windows của GitHub.
- Cài thư viện trong `requirements.txt`.
- Cài PyInstaller.
- Tải FFmpeg Windows.
- Nhúng FFmpeg vào phần mềm.
- Đóng gói thành `XuongVideoAI.exe`.
- Nén thành `XuongVideoAI-Windows-Portable.zip`.

## 4. Tải file chạy luôn

Sau khi workflow hiện dấu tích xanh:

1. Bấm vào lần chạy mới nhất.
2. Kéo xuống phần **Artifacts**.
3. Tải artifact tên **XuongVideoAI-Windows-Portable**.
4. Giải nén file vừa tải.
5. Bên trong sẽ có file:

```text
XuongVideoAI-Windows-Portable.zip
```

Giải nén tiếp file đó, bạn sẽ có thư mục:

```text
XuongVideoAI/
├── XuongVideoAI.exe
├── CHAY_PHAN_MEM.bat
├── README_CHAY_KHONG_CAN_CAI.md
└── _internal/
```

## 5. Chạy phần mềm

Mở thư mục `XuongVideoAI`, bấm đúp:

```text
XuongVideoAI.exe
```

Hoặc bấm:

```text
CHAY_PHAN_MEM.bat
```

Trình duyệt sẽ tự mở tại:

```text
http://127.0.0.1:8000
```

## 6. Máy người dùng cuối có cần cài gì không?

Không. Máy người dùng cuối chỉ cần Windows và trình duyệt web.

Không cần cài:

- Python
- pip
- PyInstaller
- FFmpeg
- PostgreSQL
- Redis

Bản MVP này mặc định dùng SQLite local và FFmpeg đã được nhúng vào gói portable.

## 7. Nếu GitHub báo lỗi không thấy workflow

Kiểm tra lại source trên GitHub có file này chưa:

```text
.github/workflows/build-windows-portable.yml
```

Nếu chưa có, upload lại thư mục `.github`.

## 8. Nếu tải artifact về bị lồng nhiều lớp ZIP

Điều này bình thường. GitHub artifact thường tải về thành một file zip chứa file zip thành phẩm.

Bạn chỉ cần giải nén lần lượt cho đến khi thấy thư mục:

```text
XuongVideoAI/
```

Trong đó có:

```text
XuongVideoAI.exe
```
