# Workflow: Final Report & Log Generation — Edu-BanhMiMaHai OS

## Overview
Tổng kết nhiệm vụ, tạo file log nhiệm vụ dạng JSON trong thư mục `logs/`, và tự động khởi tạo Đề xuất Cải tiến (Improvement Proposal) nếu phát hiện cơ hội tối ưu.

## Outputs
1. **Task Execution Log**: `logs/task-{task_id}.json` tuân thủ `schemas/task-log.json`.
2. **Improvement Proposal** (Nếu có): `improvement-proposals/prop-{proposal_id}.json` tuân thủ `schemas/improvement-proposal.json`. Khởi tạo mặc định: `approval_status: "pending"`, `applied: false`.
3. **User Summary**: Báo cáo ngắn gọn, rõ ràng cho người dùng kèm các đường dẫn tới file liên quan.
