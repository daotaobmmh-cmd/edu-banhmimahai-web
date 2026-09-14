# Workflow: Update UI Component — Edu-BanhMiMaHai OS

## Overview
Workflow dành cho việc thay đổi, nâng cấp giao diện trang web tĩnh (HTML, CSS, JS) cho các module đào tạo (như `/hoinhap/`, `/nhuongquyen/`).

## Execution Pipeline

### Step 1: Read Target Component
- Đọc nội dung file HTML/CSS/JS cần sửa.
- Đối chiếu với các quy tắc thiết kế trong `rules/web-ui-standards.md`.

### Step 2: DOM Integrity & Syntax Check
- Kiểm tra tính toàn vẹn của các ID phần tử quan trọng (`id="quiz-container"`, `id="submit-btn"`, v.v.).
- Đảm bảo không làm hỏng script hoặc phá vỡ layout trên thiết bị di động.

### Step 3: Dry-Run & Staging Preview
- Tạo file xem trước hoặc hiển thị đoạn mã diff rõ ràng.
- Hướng dẫn người dùng lệnh kiểm tra local: `python -m http.server 8000`.

### Step 4: Approval & File Apply
- Chờ xác nhận duyệt từ người dùng (`human_approval_granted = true`).
- Thực hiện áp dụng thay đổi vào codebase.

### Step 5: Verification & Audit
- Chạy `python scripts/compare_html_delta.py` để ghi nhận các điểm thay đổi.
- Chạy `python scripts/run_regression.py`.
- Xuất log nhiệm vụ tại `logs/{task_id}.json`.
