# Workflow: Swarm Subagent Orchestration — Edu-BanhMiMaHai OS

## Overview
Workflow điều phối các Subagent chuyên biệt làm việc song song bất đồng bộ nhằm tối ưu hóa hiệu suất và chất lượng xử lý các nhiệm vụ phức tạp.

## Subagent Architecture & Matrix

```
                      ┌──────────────────────────────┐
                      │    Parent Antigravity Agent   │
                      └──────────────┬───────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ Content Researcher│       │  Frontend Coder  │       │   QA Auditor     │
│ (Model: flash)   │       │ (Model: inherit) │       │   (Model: pro)   │
└──────────────────┘       └──────────────────┘       └──────────────────┘
```

## Delegation Guidelines
1. **Content Researcher**: Tìm kiếm, bóc tách và phân tích tài liệu đào tạo thô.
2. **Frontend Coder**: Chỉnh sửa HTML/CSS/JS, xây dựng component giao diện.
3. **QA Auditor**: Chạy `scripts/run_regression.py`, kiểm tra syntax và validate schema.

## Execution Sequence
- Bước 1: Khởi tạo các Subagent bằng tool `invoke_subagent`.
- Bước 2: Theo dõi trạng thái hoàn thành phản hồi tự động qua hệ thống Reactive Messaging System.
- Bước 3: Hợp nhất kết quả từ các Subagent, chạy Regression Test tổng thể và bàn giao cho người dùng.
