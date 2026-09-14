# Global Safety Rules — Edu-BanhMiMaHai OS

## 1. Severity Standard & Execution Triggers (P0 - P2)
- **P0 (Critical / Showstopper)**: Hỏng ngân hàng câu hỏi, sai logic chấm điểm, trôi dữ liệu ➔ BẮT BUỘC gọi `workflows/deep-analysis-rca.md`.
- **P1 (High)**: Vỡ layout di động, hỏng đường dẫn route ➔ BẮT BUỘC gọi `workflows/deep-analysis-rca.md`.
- **P2 (Cosmetic / Minor)**: Lỗi chính tả nhỏ trong phần giải thích, lệch 1 padding CSS ➔ **Fast Path** (sửa trực tiếp + ghi log).

> ⚠️ **RANH GIỚI BẮT BUỘC (FAST PATH BOUNDARY)**:
> Mọi thay đổi đối với `Nội Dung Đề Thi` (`question`), `Lựa chọn A/B/C/D` (`options`), hoặc `Đáp Án Đúng` (`correct_answer`) **TUYỆT ĐỐI KHÔNG BAO GIỜ THUỘC P2 (FAST PATH)**.
> Mọi sửa đổi nội dung thi bắt buộc:
> 1. Cấp `source_ref` mới (Căn Cứ Quy Chế) và `source_quote` mới (Trích Dẫn Nguyên Văn).
> 2. Tính toán lại `content_hash` (SHA-256 Unicode NFC).
> 3. Tự động hạ trạng thái về `Draft` (Hàng chờ duyệt) và ghi lý do vào cột `Ghi Chú Người Duyệt`.

## 2. Core Safety Principles
- **No Unapproved Live Production Deploy**: Execution of `git push`, Cloudflare Pages production deployment, or Vercel deploy is STRICTLY BLOCKED unless routed through `workflows/controlled-deploy.md` with explicit human approval (`ERR_LIVE_DEPLOY_DISABLED`).
- **No Direct Data Destruction**: Never delete site modules (`/hoinhap/`, `/nhuongquyen/`) or truncate question bank files.
- **Batch Modification Limit**: Maximum 5 HTML files or 20 quiz questions modified per batch (`max_batch_size: 5` files / `20` questions).

## 3. Data Integrity & Validation Rules
- **Schema Compliance**: Any quiz question item must comply with `schemas/question-bank.json` (Draft-07 `allOf` conditional validation).
- **Exact Substring Grounding**: `source_quote` must match verbatim inside `sources/<file>.extracted.txt` (Unicode NFC normalized).
- **Duplicate Prevention**: Every quiz question must have a unique prompt or question ID verified by `scripts/check_duplicate_questions.py`.
- **Encoding Standard**: All text, markdown, and web files must be written in UTF-8 encoding without BOM.

## 4. Grounding & Read-Only Sources Boundary
- **Read-Only Sources Rule**: Agents MUST NEVER modify or write to files inside `sources/` directory (`ERR_SOURCE_GROUNDING_TAMPERED`). Files in `sources/` represent authentic corporate policy documents provided by human administrators.
- **Forbidden Manifest Generation**: Agents are STRICTLY FORBIDDEN from running `scripts/generate_sources_manifest.py` (`ERR_AGENT_MANIFEST_GENERATION_DISALLOWED`). Only human administrators execute manifest generation after placing official corporate policy files into `sources/`.
- **Git Commit Enforcement**: `sources/MANIFEST.sha256` must be committed to Git. Any uncommitted git diff or manifest hash mismatch triggers immediate validation abort.
- **Staging Directory**: Temporary outputs must be written ONLY to `.staging/<agent_name>-<timestamp>.json`. Only the Parent Agent is authorized to merge staging files into main database files.
