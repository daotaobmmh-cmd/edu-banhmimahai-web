# Workflow: Validate Result — Edu-BanhMiMaHai OS

## Overview
Workflow thực hiện đọc lại trạng thái sau khi chỉnh sửa (Read-back verification) và kiểm tra delta giữa trước và sau khi thay đổi.

## Steps
1. Đọc lại nội dung file vừa được ghi từ đĩa.
2. Chạy validator tương ứng (`validate_questions.py` hoặc `compare_html_delta.py`).
3. Đảm bảo không phát sinh lỗi cú pháp hay thiếu sót thẻ đóng HTML.
4. Trả về kết quả xác nhận cho `final-report.md`.
