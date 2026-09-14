# Edu-BanhMiMaHai Agent Control Plane

Operational Release: `v7.0 — Zero-Trust Educational Validation & Control Platform`

## Core Invariants
- **No Direct Production Deploy**: Execution of `git push` or production deploys is STRICTLY BLOCKED unless routed through `workflows/controlled-deploy.md`.
- **Three Mode Permission Boundaries**:
  - `Research`: Read-Only. Cannot write files or execute commands.
  - `Generation`: Write ONLY to `.staging/<run_id>/`. Candidate/dry-run generation only. No approval, no publish.
  - `Release`: Write ONLY to predetermined build artifacts. Publish by deterministic script after Human Approval.
- **Read-Only Sources & Manifest**: Files in `data/sources/` are read-only to agents (`ERR_SOURCE_GROUNDING_TAMPERED`). Agents MUST NOT execute `scripts/generate_sources_manifest.py`.
- **Depth = 1 Subagent Isolation**: Subagents are restricted to read-only tool allowlist (`view_file`, `grep_search`, `search_web`, `read_url_content`). No shell, no write tools, no child subagent spawning (`enable_subagent_tools: false`).

## Command Router
- **Run Question Inventory**: `python scripts/inventory_questions.py`
- **Validate Question Bank**: `python scripts/validate_questions.py`
- **Run Master Regression Test Suite**: `python scripts/run_regression.py`
- **Clean Staging Files**: `python scripts/cleanup_staging.py`

## Scoped Rules & Workflows
- Security & Boundaries: `.agents/rules/global-safety.md`
- Question Data Contract: `.agents/rules/question-data.md`
- Frontend & Visual Standards: `.agents/rules/frontend-visual.md`
- Subagent Execution Contract: `docs/subagent-execution-contract.md`
- PreToolUse Hooks Policy: `.agents/hooks.json`


## 3.1. Giao Thức Mệnh Lệnh Tối Cao — Cấp Thẩm Quyền Bậc 0 (Supreme Omega Command — PROTOCOL-CHOT-002)
- **Cấp Thẩm Quyền**: `TIER 0 - SUPREME OMEGA AUTHORITY` (Cấp cao nhất toàn bộ hệ thống).
- **Mã định danh**: `PROTOCOL-CHOT-002` / `WFL-CHOT-001`.
- **Trigger Mệnh lệnh**: Khi Commander Long phát lệnh `"Chốt"`, `"Chốt đi"`, `"Chốt triển khai"`, hoặc `"CHỐT"`.
- **Nghĩa vụ thi hành bắt buộc**:
  1. **Tầng 1 (Thực thi Chuẩn xác)**: Thi hành trọn vẹn slice và xác thực 100% Master Regression / Verification gates.
  2. **Tầng 2 (Tự Tiến hóa & Khử Nhiễu Quy Tắc)**: Tự động chạy `pnpm lint:rules`, mổ xẻ nguyên nhân gốc, ban hành Rule mới, nâng cấp Workflow, và kích hoạt đối thoại phản biện Socratic khi phát hiện xung đột quy tắc chéo (`RULE-AOS-005`).
  3. **Tầng 3 (Đóng Dấu Git Checkpoint & Neo An Toàn)**: Tự động tạo Git Snapshot Commit có cấu trúc + Annotated Tag `checkpoint-TR-xx` (`pnpm checkpoint`), kích hoạt khả năng hoàn tác 1 giây (`pnpm rollback`).
  4. **Tầng 4 (Bản tin Tổng Chỉ Huy)**: Báo cáo RUN_PAD_UPDATE chuẩn mực, công bố Commit Hash, Tag Name, Delta tiến hóa hệ thống và chân trời tiếp theo.

## 3.2. Giao Thức Phản Biện Đa Chiều & Tự Soi Lỗi Khép Kín (RULE-AOS-003 / RULE-AOS-005)
- **Cấp Thẩm Quyền**: `TIER 0 - SUPREME OMEGA AUTHORITY`.
- **Mã định danh**: `RULE-AOS-003` / `RULE-AOS-005`.
- **Nguyên tắc cốt lõi**:
  1. **Phản biện đầu vào (Inbound Strategic Dialectic)**: Không gật đầu mù quáng. Luôn đối chiếu yêu cầu với Hệ giá trị cốt lõi, phát hiện góc khuất và mâu thuẫn quy tắc trước khi lập plan.
  2. **Thực thi chuẩn xác (Rigorous Execution)**: Bám sát plan, hoàn thiện mọi tiêu chuẩn nghiệm thu.
  3. **Tự soi gương chất vấn sau thực thi (Post-Execution Self-Critique)**: Không nộp bài ngay. Tự chất vấn: Đã làm đúng cam kết chưa? Bằng chứng đâu? Có vi phạm luật chéo nào không?
  4. **Vòng lặp tự động tối ưu hóa đến hoàn hảo (Autonomous Perfection Loop)**: Tự sửa lỗi ngay trong phiên, tự build, tự kiểm tra trước khi bàn giao.

## 3.3. Quy Tắc Quản Trị Tri Thức: Phân Loại "Chốt" (Repo Rules) vs "/learn" (Personal/Session Memory)

Mỗi khi phát sinh một kinh nghiệm mới, bài học fix bug phức tạp, quy ước code mới hoặc khi được người dùng chỉ dẫn/sửa sai, Agent PHẢI chủ động phân tích và đưa ra đề xuất theo tiêu chuẩn sau trước khi tiếp tục:

### 1. Tiêu chí phân loại:
- **Đề xuất "CHỐT" (Cập nhật vào `AGENTS.md` / repo rules)** nếu:
  - Là quy chuẩn kiến trúc, luồng xử lý API, convention đặt tên, cấu trúc thư mục.
  - Là quy định về thư viện, dependency hoặc tiêu chuẩn áp dụng chung cho cả dự án/team.
  - Mang tính chất lâu dài, bất biến và cần commit vào Git.

- **Đề xuất "/learn" (Ghi nhớ cá nhân / kinh nghiệm môi trường)** nếu:
  - Là lỗi đặc thù của môi trường máy cá nhân (OS, PowerShell, xung đột port, path separator...).
  - Là mẹo (workaround) xử lý lỗi tạm thời của bên thứ 3.
  - Là thói quen, phong cách lập trình hoặc sở thích làm việc riêng của người dùng.

### 2. Quy trình thực hiện:
Khi giải quyết xong một vấn đề thuộc 2 nhóm trên, Agent hãy:
1. Tóm tắt ngắn gọn bài học (1-2 câu).
2. Nêu rõ đề xuất: Nên **"Chốt vào file rules"** hay **"Gợi ý dùng `/learn`"**.
3. Hỏi ý kiến người dùng trước khi trực tiếp sửa file rules hoặc chuyển sang tác vụ khác.

