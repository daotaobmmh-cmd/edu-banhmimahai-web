# Workflow: Add Quiz Questions — Edu-BanhMiMaHai OS

## Overview
Workflow hướng dẫn việc thêm hoặc cập nhật các câu hỏi ôn tập/hội nhập vào ngân hàng dữ liệu câu hỏi (`danh_sach_cau_hoi_hoinhap.md` hoặc các file JSON tương ứng).

## Step-by-Step Execution Sequence

### Step 1: Context Loading & Structure Inspection
- Đọc file ngân hàng câu hỏi hiện tại (`danh_sach_cau_hoi_hoinhap.md`).
- Đánh giá cấu trúc câu hỏi cuối cùng để xác định Question ID kế tiếp.

### Step 2: Validate Input & Check Duplicate
- Kiểm tra tính trùng lặp của nội dung câu hỏi mới qua `python scripts/check_duplicate_questions.py`.
- Đảm bảo câu hỏi có đầy đủ: Nội dung, các lựa chọn (A, B, C, D), Đáp án đúng, và Giải thích.

### Step 3: Dry-Run Preview Generation
- Tạo bản so sánh Git Diff hiển thị phần câu hỏi sẽ được bổ sung/chỉnh sửa.
- Gọi `workflows/preview-changes.md`.

### Step 4: Approval Gate & File Modification
- Yêu cầu xác nhận từ người dùng (`human_approval_granted = true`).
- Ghi nội dung vào file sau khi được duyệt.

### Step 5: Verification & Regression Run
- Chạy `python scripts/validate_questions.py` để đảm bảo file markdown hợp lệ 100%.
- Chạy `python scripts/run_regression.py` để xác nhận hệ thống đạt chuẩn `passed`.
- Ghi log vào `logs/{task_id}.json`.
