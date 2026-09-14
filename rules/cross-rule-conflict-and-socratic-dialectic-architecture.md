# Giao Thức Đánh Giá Xung Đột Luật Chéo, Phản Biện Socratic & Khử Nhiễu Quy Tắc (RULE-AOS-005 / WFL-AOS-005)

---

## 1. Tuyên Ngôn Triết Lý & Sứ Mệnh (Core Philosophy)
Khi hệ sinh thái TriLong Atlas phát triển với hàng chục quy tắc kiến trúc, thiết kế, biên tập và xuất bản, nguy cơ phát sinh **xung đột quy phạm chéo (Cross-Rule Collisions)**, **quy tắc bị che khuất ngầm (Rule Shadowing)**, và **nhiễu nhận thức (Semantic Bloat)** là tất yếu nếu thiếu cơ chế kiểm soát động.

**RULE-AOS-005** thiết lập một cơ chế tự trị cấp cao nhất (`TIER 0 - SUPREME OMEGA AUTHORITY`) nhằm:
1. Tự động soi quét và phân tích xung đột giữa tất cả các quy tắc trước, trong và sau mỗi phiên "CHỐT".
2. Bắt buộc Agent kích hoạt **Đối thoại Phản biện Socratic (Socratic Sparring)** đặt câu hỏi ngược lại cho Commander Long khi phát hiện mâu thuẫn hoặc điểm nghẽn chiến lược, thay vì thực thi mù quáng.
3. Áp dụng **Định Đề Tam Pháp Chế La Mã (The 3 Roman Legal Canons)** và **Ngân Sách Độ Phức Tạp (Rule Complexity Budget)** để liên tục tinh giản, khử nhiễu và làm sắc bén bộ luật hệ thống.

---

## 2. Định Đề Tam Pháp Chế Giải Quyết Xung Đột Luật (The 3 Legal Canons)

Khi xảy ra va chạm ngữ nghĩa giữa hai hay nhiều quy tắc, Agent bắt buộc phải giải quyết theo thứ tự ưu tiên pháp lý sau:

```
                      ┌────────────────────────────────────────────────────────┐
                      │        THỨ TỰ PHÁP LÝ XỬ LÝ XUNG ĐỘT QUY TẮC           │
                      └──────────────────────────┬─────────────────────────────┘
                                                 │
                                                 ▼
                      ┌────────────────────────────────────────────────────────┐
                      │ 1. LEX SUPERIOR DEROGAT LEGI INFERIORI                 │
                      │    (Luật cấp trên phủ quyết tuyệt đối luật cấp dưới)   │
                      └──────────────────────────┬─────────────────────────────┘
                                                 │
                                                 ▼
                      ┌────────────────────────────────────────────────────────┐
                      │ 2. LEX SPECIALIS DEROGAT LEGI GENERALI                 │
                      │    (Luật chuyên biệt cho domain phủ quyết luật chung)  │
                      └──────────────────────────┬─────────────────────────────┘
                                                 │
                                                 ▼
                      ┌────────────────────────────────────────────────────────┐
                      │ 3. LEX POSTERIOR DEROGAT LEGI PRIORI                   │
                      │    (Luật ban hành mới nhất phủ quyết luật cũ cùng cấp) │
                      └────────────────────────────────────────────────────────┘
```

### 2.1 Lex Superior (Thứ bậc Thẩm quyền)
- `TIER 0 - SUPREME OMEGA AUTHORITY` (`PROTOCOL-CHOT`, `RULE-AOS-003`, `RULE-AOS-004`, `RULE-AOS-005`, `RULE-ECO-001`, `RULE-PUB-002`) luôn có quyền phủ quyết tuyệt đối bất kỳ quy tắc domain cấp dưới nào.
- `TIER 1 - BLOCKING ARCHITECTURE` (`RULE-GS-001`, `RULE-CSC-001`, `RULE-PUB-007`, `RULE-WRT-001`) phủ quyết các hướng dẫn khuyến nghị hoặc thẩm mỹ thuần túy.

### 2.2 Lex Specialis (Miền Chuyên Biệt)
- Khi một quy tắc được thiết kế riêng cho một đối tượng chuyên biệt (ví dụ: `RULE-PUB-007` dành riêng cho Sổ tay Monograph PDF), các điều khoản của nó sẽ được ưu tiên áp dụng trong phạm vi đó, ngay cả khi nó có sự khác biệt so với quy tắc thiết kế thẻ tổng quát (`RULE-CSC-001`).

### 2.3 Lex Posterior (Tính Thời Điểm)
- Nếu hai quy tắc cùng cấp thẩm quyền và cùng phạm vi có sự sai lệch, quy tắc có mốc thời gian `last_synced_at` mới nhất và đã vượt qua 100% Master Regression Suite sẽ được ưu tiên thực thi, đồng thời kích hoạt cảnh báo hợp nhất luật cũ.

---

## 3. Khung Đối Thoại Phản Biện Socratic & Tổng Hợp Hegelian

Khi Agent phát hiện một yêu cầu mới có nguy cơ vi phạm quy tắc sẵn có, hoặc khi hai quy tắc đang triệt tiêu lẫn nhau, Agent **NGHIÊM CẤM TỰ ĐOÁN MÒ HOẶC LÀM QUA LOA**. Agent bắt buộc phải xuất bản bản tin phản biện Socratic gửi lên Commander Long theo cấu trúc:

```text
======================================================================
[SOCRATIC DIALECTIC NOTICE · PHÁT HIỆN XUNG ĐỘT QUY TẮC CHÉO]
1. ĐIỂM VA CHẠM (COLLISION NODES):
   • Quy Tắc Hiện Hữu A: [Mã luật & Ràng buộc cốt lõi]
   • Yêu Cầu Mới / Quy Tắc B: [Mã luật & Điểm xung đột]

2. BẢN CHẤT MÂU THUẪN (ROOT DILEMMA):
   • Phân tích nghịch lý quản trị hoặc tâm lý học (MBA & Psychology Trade-off).
   • Vì sao thực thi cả hai cùng lúc sẽ gây méo mó sản phẩm hoặc quá tải người dùng?

3. ĐỀ XUẤT HỢP ĐỀ HEGELIAN (SYNTHESIS PROPOSALS):
   • [Lựa chọn 1 - Ưu tiên Thẩm quyền]: Thực thi theo Lex Superior / Tầm nhìn 10 năm.
   • [Lựa chọn 2 - Phân nhánh Chuyên biệt]: Tạo ngoại lệ Lex Specialis cho riêng trường hợp này.
   • [Lựa chọn 3 - Khử nhiễu Tinh giản]: Bãi bỏ hoặc hợp nhất Quy tắc A vào Quy tắc B để giữ hệ thống thanh thoát.

4. CÂU HỎI CHẤT VẤN TỔNG CHỈ HUY (SOCRATIC CHALLENGE):
   • [Câu hỏi kích thích tư duy sắc bén giúp Commander Long ra quyết định tối ưu]
======================================================================
```

---

## 4. Ngân Sách Độ Phức Tạp & Khử Nhiễu Quy Tắc (Anti-Entropy Governance)

Để tránh tình trạng "lạm phát luật", hệ thống đặt ra 3 chốt chặn chống thoái hóa:
1. **Rule Complexity Budget (Ngân sách Quy tắc Tối đa)**:
   - Mỗi Domain (`safety`, `design`, `motion`, `publishing`, `architecture`) không được vượt quá **8 quy tắc hoạt động đồng thời**.
   - Khi vượt quá 8 quy tắc, phiên "CHỐT" tiếp theo bắt buộc phải có một tiểu mục **Hợp Nhất Quy Tắc (Rule Consolidation)** để gộp các vi quy tắc thành một quy chuẩn toàn diện.
2. **Sunset Clause (Điều khoản Hoàng hôn 60 ngày)**:
   - Mọi quy tắc trong `rules/rule-registry.md` có `last_synced_at` quá 60 ngày mà không được kiểm chứng bởi test gate tự động sẽ bị gắn trạng thái `STALE_AUDIT_REQUIRED`.
3. **Automated Rule Linter Gate**:
   - Mọi quy tắc mới ban hành phải được kiểm tra cú pháp và tính nhất quán bằng lệnh `pnpm lint:rules` (`scripts/lint_rules_conflict.mjs`) trước khi được đóng dấu Checkpoint.
