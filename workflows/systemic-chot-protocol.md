# Master Protocol: The Autonomous Systemic "CHỐT" Engine (v2.0.0 Standard) — TriLong Atlas

## 1. Overview & Authority
- **Protocol ID**: `PROTOCOL-CHOT-002` / `WFL-CHOT-001`
- **Authority**: `TIER_0_SUPREME_OMEGA_COMMAND` (Cấp thẩm quyền tối cao bậc 0)
- **Priority**: 0 (Tuyệt đối ưu tiên trên mọi Domain Workflows & Rules)
- **Owner**: Long (Commander-in-Chief). **Planner/Reviewer**: Tilog. **Executor**: AG (Antigravity).
- **Trigger Patterns**: `"Chốt"`, `"Chốt đi"`, `"Chốt triển khai"`, `"CHỐT"`, `"ok chốt"`.

Giao thức **"CHỐT" v2.0.0** là mệnh lệnh tối cao kích hoạt đồng thời **Cỗ Máy Thực Thi Kỹ Thuật (Precision Execution Engine)**, **Cỗ Máy Tự Tiến Hóa & Khử Nhiễu Quy Tắc (Autonomous Meta-Evolution & Anti-Entropy Engine)**, và **Khung Đối Thoại Phản Biện Socratic (Socratic Dialectic Dialogue)** mà không cần bất kỳ lời nhắc bổ sung nào từ Tổng Chỉ Huy.

---

## 2. Kiến Trúc 4 Tầng Vận Hành Nâng Cấp (The 4-Tier Operating Architecture)

```
                                  MỆNH LỆNH: "CHỐT"
                                         │
 ┌───────────────────────────────────────┼───────────────────────────────────────┐
 ▼                                       ▼                                       ▼
[TẦNG 1: THỰC THI CHUẨN XÁC]    [TẦNG 2: TIẾN HÓA & KHỬ NHIỄU]          [TẦNG 3: ĐÓNG DẤU NEO]
(Execution & Master Regression) (Meta-Evolution & Linter)               (Git Checkpoint & Tag)
• Hoàn tất mã nguồn slice.      ┌──────────────────────────────┐        • Chạy `pnpm checkpoint`.
• 100% Pass Master Regression.  │ 2.1 Cross-Rule Conflict Lint │        • Tạo Git Commit + Tag.
• Khóa Mutation Lock.           │ 2.2 Socratic Dissent Loop    │        • Sẵn sàng `pnpm rollback`.
• Build tĩnh không lỗi.         │ 2.3 Anti-Entropy Rule Pruning│
                                │ 2.4 Auto Test Gate Injection │
                                └──────────────┬───────────────┘
                                               │
                                               ▼
                                [TẦNG 4: BẢN TIN TỔNG CHỈ HUY]
                                (High-Gravity Executive Briefing)
                                • Báo cáo RUN_PAD_UPDATE chuẩn mực.
                                • Báo cáo Ma trận Xung đột Luật (CRCM).
                                • Bản tin Phản biện Socratic (nếu có).
                                • Điểm neo Git Checkpoint & Next Horizon.
```

---

## 3. Quy Trình Chi Tiết Từng Tầng

### 🎯 Tầng 1: Thực Thi Chuẩn Xác & Khóa An Toàn (Execution Engine)
1. **Thi hành mã nguồn**: Hoàn thiện toàn bộ logic, styling, typography, và layout theo đúng phạm vi được duyệt.
2. **Khóa đột biến (Mutation Lock)**: Tuyệt đối không sửa file ngoài phạm vi slice. Không dùng `git add .` bừa bãi.
3. **Kiểm thử tự động**: Chạy build tĩnh (`pnpm build`) và Master Regression Suite (`pnpm test:regression`). Bắt buộc 100% kiểm thử xanh lá mới được tiếp tục.

### 🧬 Tầng 2: Tự Tiến Hóa, Khử Nhiễu Quy Tắc & Phản Biện Socratic (Meta-Evolution & Linter Engine)

#### 2.1 Quét Xung Đột Quy Tắc Tự Động (Cross-Rule Conflict Linting):
- Tự động chạy `pnpm lint:rules` (`scripts/lint_rules_conflict.mjs`) kiểm tra:
  - Tính nhất quán thứ bậc thẩm quyền (`Lex Superior`).
  - Xung đột từ khóa và phạm vi ràng buộc giữa các domain (`Shadowing & Conflicts`).
  - Phát hiện quy tắc mồ côi hoặc không gắn với test gate.

#### 2.2 Kích Hoạt Vòng Lặp Phản Biện Socratic (Socratic Dissent Loop):
- Nếu phát hiện xung đột quy phạm hoặc yêu cầu mới có nguy cơ làm xói mòn tầm nhìn 10 năm / kiến trúc tĩnh:
  - **DỪNG LẠI & XUẤT BẢN BẢN TIN PHẢN BIỆN SOCRATIC**:
    1. *Điểm va chạm quy tắc chéo.*
    2. *Phân tích nghịch lý quản trị (MBA / Psychology Trade-off).*
    3. *3 Đề xuất Hợp đề Hegelian (Thẩm quyền / Ngoại lệ chuyên biệt / Tinh giản).*
    4. *Câu hỏi chất vấn ngược lại để Commander Long quyết định.*

#### 2.3 Khử Nhiễu Quy Tắc & Kiểm Soát Ngân Sách (Anti-Entropy Pruning):
- Kiểm soát không để bất kỳ domain nào vượt quá 8 quy tắc hoạt động đồng thời.
- Chủ động đề xuất hợp nhất các vi quy tắc cũ thành quy chuẩn toàn diện.

#### 2.4 Bơm Bài Kiểm Thử Tự Động (Automated Test Gate Injection):
- Thêm assertion kiểm tra tĩnh/động vào `scripts/run_atlas_regression.mjs` (`TC-CMP-xxx`) để biến bài học thành cổng gác vĩnh viễn.

### 🛡️ Tầng 3: Đóng Dấu Git Checkpoint & Neo An Toàn (Checkpoint Engine)
1. **Kích hoạt tự động**: Tự động thực thi `node scripts/create_chot_checkpoint.mjs` (hoặc lệnh `pnpm checkpoint`).
2. **Đóng băng mã nguồn có cấu trúc**: Stage toàn bộ thư mục lõi (`src/`, `rules/`, `workflows/`, `scripts/`, `public/`, `docs/`, `package.json`, `.memory-bank/`).
3. **Tạo Git Commit & Annotated Tag**: Tạo commit `CHOT(TR-xx)` và tag `checkpoint-TR-xx`.
4. **Trang bị khả năng hoàn tác 1 giây (`pnpm rollback`)**: Bất kỳ khi nào gặp sự cố ở phiên sau, chỉ cần gõ `pnpm rollback` là toàn bộ mã nguồn lập tức lùi về chính xác phiên bản Chốt này!

### 📢 Tầng 4: Bản Tin Tổng Chỉ Huy (High-Gravity Executive Briefing)
Cuối mỗi chu trình "CHỐT", Agent bắt buộc xuất bản báo cáo theo định dạng:
1. Khối **RUN_PAD_UPDATE** chuẩn quy ước `AGENTS.md`.
2. Khối **MA TRẬN XUNG ĐỘT QUY TẮC (CRCM STATUS)**: Kết quả từ `pnpm lint:rules`.
3. Khối **BẢN TIN PHẢN BIỆN SOCRATIC** (nếu phát sinh điểm phân giải chiến lược).
4. Khối **THÔNG TIN ĐIỂM NEO CHECKPOINT** (Commit Hash, Tag Name).
5. Khối **CHÂN TRỜI ĐỘT PHÁ TIẾP THEO (NEXT HORIZON)**: Nêu rõ lựa chọn tối ưu tiếp theo cho Commander duyệt.

---

## 4. Bảng Tiêu Chuẩn Nghiệm Thu Giao Thức (Definition of Done)
- [ ] Tự động kích hoạt khi Commander Long gõ các biến thể của từ "Chốt".
- [ ] Tuân thủ nghiêm ngặt 4 tầng tác chiến (Thực thi -> Tiến hóa & Khử nhiễu -> Đóng dấu Checkpoint -> Bản tin).
- [ ] Tự động chạy và xác thực 100% `pnpm lint:rules` và `pnpm test:regression`.
- [ ] Tự động tạo Git Commit và Tag checkpoint an toàn sau mỗi mốc thành công.
- [ ] Sẵn sàng phản biện và đặt câu hỏi chất vấn ngược lại để bảo vệ hệ sinh thái.
