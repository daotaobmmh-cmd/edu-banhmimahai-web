# Workflow: Controlled Live Deploy — Edu-BanhMiMaHai OS

## Overview
Workflow duy nhất cho phép phát hành/deploy ứng dụng lên Cloudflare Pages hoặc đẩy code lên remote repository.

## Safety Check Gates (Bắt buộc 100%)
- [ ] **Gate 1: Human Approval**: Phải nhận được xác nhận trực tiếp của người quản trị (Long / Tilog): `human_approval_granted = true`.
- [ ] **Gate 2: Regression Passed**: `python scripts/run_regression.py` đạt `100% passed`.
- [ ] **Gate 3: Clean Git Working Tree**: Không có file rác hoặc file scratch còn sót lại trong commit bundle.

## Step-by-Step Deploy Protocol
1. Kiểm tra toàn bộ 3 Safety Gates ở trên.
2. Hiển thị thông điệp xác nhận deploy kèm tóm tắt các tính năng/câu hỏi được cập nhật.
3. Thực thi lệnh đẩy code/deploy theo chỉ thị.
4. Lưu log deploy tại `logs/deploy-{timestamp}.json`.
