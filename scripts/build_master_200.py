# scripts/build_master_200.py
"""
Assembles all 8 sections (200 canonical questions) for /kynangsale/.
Enforces invariants:
- Exactly 200 questions (25 per section)
- Exactly 50 A, 50 B, 50 C, 50 D (25.0% each)
- Zero composite/forbidden phrases
- Generates kynangsale/questions.js and kynangsale/DANH_SACH_200_CAU_HOI_KYNANGSALE.md
"""

import os
import json
import sys

# Set encoding
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

from data.sec1 import SECTION_1
from data.sec2 import SECTION_2
from data.sec3 import SECTION_3
from data.sec4 import SECTION_4
from data.sec5 import SECTION_5
from data.sec6 import SECTION_6
from data.sec7 import SECTION_7
from data.sec8 import SECTION_8

sections = [
    (1, "Nhập môn Nhượng quyền & Lợi thế Mô hình", SECTION_1),
    (2, "Phân loại Khách hàng & Kỹ năng Tư vấn", SECTION_2),
    (3, "Khảo sát Vị trí, Mặt bằng & Khung giờ Bán hàng", SECTION_3),
    (4, "Kỹ thuật Chiên chả, Làm bánh & An toàn Vệ sinh", SECTION_4),
    (5, "Xử lý Từ chối & Tháo gỡ Rào cản Đối tác", SECTION_5),
    (6, "Kỹ năng Vận hành Ca sáng & Xử lý Sự cố Điểm bán", SECTION_6),
    (7, "Pháp lý, Quan hệ Cộng đồng & Phát triển Bền vững", SECTION_7),
    (8, "Chốt Deal Thực chiến, Tối ưu Lợi nhuận & Onboarding", SECTION_8)
]

all_questions = []
for sec_num, sec_name, sec_data in sections:
    assert len(sec_data) == 25, f"Section {sec_num} does not have 25 questions, got {len(sec_data)}"
    for q in sec_data:
        assert q['sectionNo'] == sec_num
        assert q['sectionName'] == sec_name
        all_questions.append(q)

assert len(all_questions) == 200, f"Expected 200 questions, got {len(all_questions)}"

# Invariant 1: Golden Answer Distribution (50 A, 50 B, 50 C, 50 D)
ans_counts = {}
for q in all_questions:
    ans_counts[q['correctAnswer']] = ans_counts.get(q['correctAnswer'], 0) + 1

print(f"Total Questions: {len(all_questions)}")
print(f"Answer Distribution: {ans_counts}")
for key in ['a', 'b', 'c', 'd']:
    assert ans_counts.get(key, 0) == 50, f"Key '{key}' count is {ans_counts.get(key, 0)}, expected 50!"

# Invariant 2: Zero forbidden phrases
forbidden_phrases = [
    'tất cả', 'cả a và', 'cả b và', 'cả c và', 'cả 3', 'cả ba',
    'các phương án trên', 'không có phương án', 'không có đáp án', 'cả hai'
]
for q in all_questions:
    for opt in q['options']:
        for phrase in forbidden_phrases:
            if phrase in opt['text'].lower():
                raise ValueError(f"Forbidden phrase '{phrase}' in {q['id']} opt {opt['key']}: {opt['text']}")

# Generate kynangsale/questions.js
js_content = "/**\n"
js_content += " * Ngân hàng câu hỏi Kỹ năng Tư vấn & Mở xe Nhượng quyền Má Hải (200 câu)\n"
js_content += " * Chuẩn mực 8 Phần x 25 Câu | Cân bằng 50A - 50B - 50C - 50D | 0% Phương án gộp/lười\n"
js_content += " * Phiên bản: kynangsale-v2.0 (Master Release)\n"
js_content += " */\n\n"
js_content += "const questions = " + json.dumps(all_questions, ensure_ascii=False, indent=2) + ";\n\n"
js_content += "if (typeof module !== 'undefined' && module.exports) {\n"
js_content += "    module.exports = questions;\n"
js_content += "}\n"
js_content += "if (typeof window !== 'undefined') {\n"
js_content += "    window.KYNANGSALE_QUESTIONS = questions;\n"
js_content += "    window.HOINHAP_QUESTIONS = questions;\n"
js_content += "    window.questionsData = questions;\n"
js_content += "}\n"

questions_js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kynangsale", "questions.js")
with open(questions_js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Successfully generated: {questions_js_path}")

# Generate kynangsale/DANH_SACH_200_CAU_HOI_KYNANGSALE.md
md_content = "# BỘ 200 CÂU HỎI TRẮC NGHIỆM CHUẨN HÓA KỸ NĂNG SALE & MỞ XE NHƯỢNG QUYỀN MÁ HẢI\n\n"
md_content += "> **Phiên bản:** `v2.0 — Master Canonical Matrix`  \n"
md_content += "> **Quy mô:** 8 Phần x 25 Câu = 200 Câu hỏi chuẩn mực  \n"
md_content += "> **Phân bổ đáp án:** 50 A (25.0%) | 50 B (25.0%) | 50 C (25.0%) | 50 D (25.0%)  \n"
md_content += "> **Tiêu chuẩn chất lượng:** 100% Phương án độc lập, không dùng câu hỏi gộp template, số liệu vận hành chính xác 100%.\n\n"
md_content += "---\n\n"

for sec_num, sec_name, sec_data in sections:
    start_no = (sec_num - 1) * 25 + 1
    end_no = sec_num * 25
    md_content += f"## PHẦN {sec_num}: {sec_name.upper()} (CÂU {start_no:03d} – {end_no:03d})\n\n"
    
    for idx, q in enumerate(sec_data):
        q_num = start_no + idx
        md_content += f"### Câu {q_num:03d} [{q['id']}]\n"
        md_content += f"**Câu hỏi:** {q['question']}\n\n"
        for opt in q['options']:
            md_content += f"- **{opt['key'].upper()}.** {opt['text']}\n"
        md_content += f"\n- **Đáp án đúng:** `{q['correctAnswer'].upper()}`\n"
        md_content += f"- **Giải thích:** {q['explanation']}\n"
        md_content += f"- **Lời thoại thực chiến:** *\"{q['quote']}\"*\n\n"
    md_content += "---\n\n"

md_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kynangsale", "DANH_SACH_200_CAU_HOI_KYNANGSALE.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Successfully generated: {md_path}")
print("ALL MASTER 200 ASSETS COMPILED AND VALIDATED SUCCESSFULLY!")
