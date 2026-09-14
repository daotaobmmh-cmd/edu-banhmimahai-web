# Workflow: Visual QA & Frontend Audit — Edu-BanhMiMaHai OS

## Overview
Workflow thực hiện kiểm thử tự động giao diện trang web tĩnh (HTML/CSS), kiểm tra màu sắc chuẩn thương hiệu Bánh Mì Má Hải, độ tương thích di động và sự hiện diện của các thuộc tính `id` quan trọng.

## Audit Checklist
1. **Brand Color Check**: Kiểm tra sự có mặt của bảng màu chính (`#E53935`, `#FF6F00`, `#1E293B`).
2. **Element ID Audit**: Kiểm tra các thẻ chứa quiz (`#quiz-container`, `#submit-btn`, `#score-display`).
3. **HTML Tag Match**: Đối chiếu thẻ đóng mở thông qua `scripts/compare_html_delta.py`.
4. **Responsive Meta Tag**: Bắt buộc có `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.

## Output
Báo cáo audit chi tiết trả về màn hình và xuất file `reports/visual-qa-latest.json`.
