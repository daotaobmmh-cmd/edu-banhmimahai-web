# Bánh Mì Má Hải · Cổng Đào Tạo Nội Bộ

> [!IMPORTANT]
> **🤖 Antigravity Operational Directive**:
> Antigravity Agent khi làm việc trong repository này **BẮT BUỘC** phải đọc và tuân thủ tuyệt đối [AGENTS.md](AGENTS.md), các bộ quy tắc trong `rules/` và quy trình trong `workflows/`. Bắt buộc chạy `python scripts/run_regression.py` trước khi hoàn tất nhiệm vụ.

Hệ thống luyện tập và kiểm tra kiến thức hội nhập nội bộ dành riêng cho nhân sự Bánh Mì Má Hải.

## Hướng dẫn chạy thử nghiệm Local
Để chạy thử nghiệm ứng dụng ở môi trường local, khởi chạy một web server tĩnh tại thư mục gốc:
```bash
python -m http.server 8000
```
Sau đó truy cập qua trình duyệt tại địa chỉ:
`http://localhost:8000/hoinhap/`

## Cấu hình Static Hosting (Cloudflare Pages)
- **Deploy Root**: Thư mục gốc dự án (`edu-banhmimahai-web`)
- **Build Command**: Không có (*để trống*)
- **Output Directory**: `.` (*Thư mục gốc, do chứa index.html tự động redirect vào /hoinhap/*)
- **Production Route**: `/hoinhap/`

> [!WARNING]
> Không tự ý deploy, thực hiện lệnh `git push` lên remote repository hoặc thay đổi cấu hình DNS nếu chưa có sự phê duyệt/chỉ thị slice công việc từ Tilog / Long.
