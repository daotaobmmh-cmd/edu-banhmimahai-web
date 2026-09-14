# Workflow: Generate Quiz From Raw Document — Edu-BanhMiMaHai OS

## Overview
Workflow tự động chuyển đổi tài liệu đào tạo thô (PDF, Word, Text, thông báo nội bộ) thành các câu hỏi trắc nghiệm chuẩn cấu trúc, có đáp án và giải thích chi tiết, tuân thủ `schemas/question-bank.json`.

## Pipeline Execution

### Step 1: Raw Document Ingestion
- Đọc nội dung văn bản nguồn từ file hoặc câu lệnh của người dùng.
- Bóc tách các thông tin chính: Quy định, mốc thời gian, tiêu chí an toàn thực phẩm, bước vận hành.

### Step 2: Question & Distractor Generation
- Sinh ra các câu hỏi trắc nghiệm gồm 4 lựa chọn (A, B, C, D).
- Xây dựng phương án đúng chuẩn xác và 3 phương án nhiễu hợp lý (distractors).
- Trích xuất trích dẫn quy định làm phần **Giải thích (Explanation)**.

### Step 3: Validation & Deduplication
- Gọi script `scripts/generate_quiz_from_raw.py`.
- Chạy `scripts/check_duplicate_questions.py` để đảm bảo câu hỏi không bị lặp với 171 câu hiện có.
- Chạy `scripts/validate_questions.py` kiểm tra cú pháp Markdown/JSON.

### Step 4: Preview & Human Approval Gate
- Tạo diff preview trình người dùng.
- Chờ duyệt (`human_approval_granted = true`).
- Ghi câu hỏi mới vào ngân hàng câu hỏi `danh_sach_cau_hoi_hoinhap.md`.

### Step 5: Regression & Log
- Chạy `python scripts/run_regression.py`.
- Xuất log tại `logs/{task_id}.json`.
