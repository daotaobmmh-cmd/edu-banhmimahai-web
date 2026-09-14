# Workflow: Deep Analysis & Root-Cause Investigation — Edu-BanhMiMaHai OS

## Overview
Workflow thực thi phân tích nguyên nhân gốc (RCA) khi xảy ra sự cố kỹ thuật đối với ngân hàng câu hỏi, giao diện web HTML/CSS hoặc logic ứng dụng `edu-banhmimahai-web`.

## Step-by-Step Execution Sequence

### Step 1: Freeze & Containment
- Dừng ngay mọi thao tác sửa đè tự do.
- Đọc lại file log gần nhất tại `logs/`.
- Xác định phạm vi ảnh hưởng: Ngân hàng câu hỏi `danh_sach_cau_hoi_hoinhap.md` hay giao diện HTML/CSS.

### Step 2: Problem Contract Definition
- Xác định **Expected State** (Trạng thái kỳ vọng) vs **Actual State** (Trạng thái thực tế).
- Thu thập bằng chứng lỗi từ log hoặc file mã nguồn.

### Step 3: Root-Cause Investigation & Causal Chain
- Phân tích chuỗi nhân quả: `Trigger ➔ Occurrence Cause ➔ Escape Point`.
- Đánh giá nguyên nhân tại sao validator hoặc test suite không phát hiện được lỗi sớm hơn.

### Step 4: Self-Critique Gate (7-Step Adversarial Check)
- Đóng vai Kiến trúc sư phản biện để đánh giá 7 rủi ro của phương án sửa đổi đề xuất.

### Step 5: Implement Four-Layer Fix
1. **Layer 1 (Containment)**: Dừng việc nạp file hỏng.
2. **Layer 2 (Correction)**: Sửa lại câu hỏi hoặc thẻ HTML bị lỗi.
3. **Layer 3 (Prevention)**: Bổ sung rule vào `rules/quiz-content-rules.md` hoặc `rules/web-ui-standards.md`.
4. **Layer 4 (Detection)**: Viết test case mới vào `tests/` và cập nhật `scripts/run_regression.py`.

### Step 6: Post-Fix Read-Back & Regression Test
- Chạy `python scripts/run_regression.py` để đảm bảo hệ thống đạt `passed`.
- Xuất báo cáo 20 mục lưu tại `logs/rca-{timestamp}.json`.
