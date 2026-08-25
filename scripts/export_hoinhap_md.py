# scripts/export_hoinhap_md.py
"""
Generates a clean, comprehensive, standardized Markdown file for the 171 /hoinhap/ questions.
Writes to:
- hoinhap/DANH_SACH_171_CAU_HOI_HOINHAP.md
- danh_sach_cau_hoi_hoinhap.md
"""

import os
import sys
import re

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

root = os.path.dirname(os.path.dirname(__file__))
questions_file = os.path.join(root, "hoinhap", "questions.js")

with open(questions_file, "r", encoding="utf-8") as f:
    content = f.read()

# Load questions from JS using Node
import subprocess
import json

node_script = """
const fs = require('fs');
const content = fs.readFileSync('./hoinhap/questions.js', 'utf8');
const win = {};
const fn = new Function('window', content);
fn(win);
const questions = win.HOINHAP_QUESTIONS || win.questionsData || [];
console.log(JSON.stringify(questions));
"""

result = subprocess.run(["node", "-e", node_script], cwd=root, capture_output=True, text=True, encoding='utf-8')
questions = json.loads(result.stdout)

print(f"Loaded {len(questions)} questions from hoinhap/questions.js")

canonical_titles = [
    "Hành trình, sản phẩm và địa điểm Má Hải",
    "Hệ giá trị và tư duy làm việc",
    "Hợp đồng lao động và kỷ luật",
    "Nghỉ phép, chấm công và quy trình HR",
    "Phúc lợi, đánh giá và phát triển",
    "Tác phong và giao tiếp khách hàng",
    "Văn hóa nội bộ và tinh thần đồng đội",
    "12 Chữ vàng và phục vụ khách hàng",
    "12 Trái cấm, bảo mật và tài sản",
    "Công cụ, sơ đồ tổ chức và báo cáo",
    "An toàn, PCCC, vệ sinh và môi trường",
    "Má Hải Ways — 5 nguyên lý nền tảng",
    "Làm chủ công việc và dám nhận thử thách",
    "Tập trung, thời gian và nguồn lực",
    "Biết ơn và yêu mến",
    "Làm vì người khác, 5 node và đại sứ thương hiệu",
    "Học hỏi, cải tiến và tiến bộ mỗi ngày",
    "Làm chuẩn, làm thật và kỷ luật vận hành"
]

# Group by section
sections_map = {}
for q in questions:
    sec_no = q.get('sectionNo', 1)
    if sec_no not in sections_map:
        sections_map[sec_no] = []
    sections_map[sec_no].append(q)

md_content = "# BỘ 171 CÂU HỎI ÔN TẬP ĐÀO TẠO HỘI NHẬP BÁNH MÌ MÁ HẢI\n\n"
md_content += "> **Phân hệ:** `/hoinhap/` (Truy cập tại: `daotao.banhmimahai.vn/hoinhap/`)  \n"
md_content += f"> **Quy mô:** {len(questions)} Câu hỏi trắc nghiệm chia thành {len(sections_map)} Phần  \n"
md_content += "> **Tiêu chuẩn:** Tài liệu đào tạo nội bộ chuẩn hóa dành cho Đồng nghiệp Nhà Má Hải  \n\n"
md_content += "---\n\n"

for sec_no in sorted(sections_map.keys()):
    sec_title = canonical_titles[sec_no - 1] if sec_no <= len(canonical_titles) else f"Phần {sec_no}"
    sec_questions = sections_map[sec_no]
    
    start_q = sec_questions[0].get('displayNumber', 1)
    end_q = sec_questions[-1].get('displayNumber', len(sec_questions))
    
    md_content += f"## PHẦN {sec_no}: {sec_title.upper()} (CÂU {start_q:03d} – {end_q:03d})\n\n"
    
    for q in sec_questions:
        num = q.get('displayNumber', q.get('id', ''))
        q_id = q.get('id', '')
        question_text = q.get('question', '')
        options = q.get('options', [])
        correct_ans = q.get('correctAnswer', '').upper()
        explanation = q.get('explanation', '')
        
        md_content += f"### Câu {num:03d} [{q_id}]\n"
        md_content += f"**Đề bài:** {question_text}\n\n"
        
        for opt in options:
            opt_key = opt.get('key', '').upper()
            opt_text = opt.get('text', '')
            is_correct = (opt_key == correct_ans)
            mark = "[x]" if is_correct else "[ ]"
            md_content += f"- {mark} **{opt_key}.** {opt_text}\n"
        
        md_content += f"\n> **Đáp án đúng:** `{correct_ans}`\n"
        if explanation:
            md_content += f">\n> **Giải thích:** {explanation}\n"
        md_content += "\n---\n\n"

# Write out to hoinhap/DANH_SACH_171_CAU_HOI_HOINHAP.md
out_path1 = os.path.join(root, "hoinhap", "DANH_SACH_171_CAU_HOI_HOINHAP.md")
with open(out_path1, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Generated: {out_path1}")

# Also update danh_sach_cau_hoi_hoinhap.md in root
out_path2 = os.path.join(root, "danh_sach_cau_hoi_hoinhap.md")
with open(out_path2, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Generated: {out_path2}")
