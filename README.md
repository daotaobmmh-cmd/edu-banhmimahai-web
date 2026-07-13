# Viet Street Food · Cổng Đào Tạo Nội Bộ

Hệ thống luyện tập và kiểm tra kiến thức hội nhập nội bộ dành riêng cho nhân sự Viet Street Food.

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

## Hướng dẫn Build Inline (Self-contained)
Để đóng gói tất cả các tài nguyên (CSS compiled, questions data, application logic, AlpineJS) vào duy nhất file `hoinhap/index.html` tự chạy không cần request JS phụ, khởi chạy script build bằng lệnh:
```bash
python scripts/build.py
```
Script này sẽ biên dịch Tailwind CSS tĩnh từ file nguồn `hoinhap/index.src.html` và in toàn bộ asset JS/CSS vào file đích `hoinhap/index.html`.
*Lưu ý: Mọi chỉnh sửa giao diện và cấu trúc HTML cần được thực hiện trên file nguồn [hoinhap/index.src.html](file:///d:/TRILONG-tools/website-projects/edu-banhmimahai-web/hoinhap/index.src.html).*

> [!WARNING]
> Không tự ý deploy, thực hiện lệnh `git push` lên remote repository hoặc thay đổi cấu hình DNS nếu chưa có sự phê duyệt/chỉ thị slice công việc từ Tilog / Long.
