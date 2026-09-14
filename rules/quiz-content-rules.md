# Quiz Content Rules — Edu-BanhMiMaHai OS

## 1. Question Bank Structure Standard
- Every question item must contain:
  1. **Question ID / Number** (e.g., `Cau_001` or `1.`)
  2. **Question Prompt** (Text clearly stating the query)
  3. **Options / Choice List** (Minimum 2 choices, typically A, B, C, D)
  4. **Correct Answer Key** (Explicitly specified correct choice)
  5. **Explanation / Note** (Optional but recommended rationale for internal training)

## 2. Formatting Rules for `danh_sach_cau_hoi_hoinhap.md`
- Markdown headings must follow logical hierarchy: `# Module -> ## Category -> ### Question`.
- Choice options must use bold identifiers (e.g., **A.**, **B.**, **C.**, **D.**).
- Correct answer key must be demarcated clearly (e.g., `> **Đáp án đúng:** A` or `*Đáp án:* A`).

## 3. Quality Control Invariants
- **No Ambiguous Keys**: Every question MUST have exactly 1 unambiguous correct answer unless multi-select is explicitly enabled.
- **No Empty Explanations**: For safety and compliance questions (e.g., Food Safety & Hygiene / Vệ sinh an toàn thực phẩm), explanations must cite the relevant standard or rule.
- **Validation**: All additions must pass `python scripts/validate_questions.py`.
