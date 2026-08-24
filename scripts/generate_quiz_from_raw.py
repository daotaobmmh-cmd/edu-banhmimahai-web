#!/usr/bin/env python3
"""
generate_quiz_from_raw.py — Raw Document to Quiz Block Formatter for Edu-BanhMiMaHai OS
Formats raw item dictionary or text input into standardized Markdown quiz question blocks.
"""

import sys
import os
import re
import json

def format_question_block(q_num, q_code, prompt, options, correct_key, explanation=""):
    """
    options: list of strings [optA, optB, optC, optD]
    correct_key: string "A", "B", "C", or "D"
    """
    letters = ["A", "B", "C", "D"]
    opt_lines = []
    for i, opt in enumerate(options):
        letter = letters[i]
        is_checked = "x" if letter.upper() == correct_key.upper() else " "
        opt_lines.append(f"- [{is_checked}] **{letter}**: {opt}")

    lines = [
        f"### Câu {q_num} (Mã: {q_code})",
        f"**Đề bài:** {prompt}",
        ""
    ] + opt_lines + [
        "",
        f"> **Đáp án đúng:** `{correct_key.upper()}`",
        ">"
    ]
    if explanation:
        lines.append(f"> **Giải thích:** {explanation}")

    return "\n".join(lines)

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    # Example dry-run test formatting
    sample_block = format_question_block(
        q_num=172,
        q_code="HN-172",
        prompt="Quy trình 5S tại cửa hàng bao gồm những bước nào?",
        options=[
            "Sàng lọc, Sắp xếp, Sạch sẽ, Săn sóc, Sẵn sàng",
            "Sơn sửa, Sắp xếp, Sạch sẽ, Săn sóc, Sẵn sàng",
            "Sàng lọc, Sắp xếp, Sống tốt, Săn sóc, Sẵn sàng",
            "Tất cả đều sai"
        ],
        correct_key="A",
        explanation="5S là tiêu chuẩn quản lý tổ chức nơi làm việc gồm Sàng lọc, Sắp xếp, Sạch sẽ, Săn sóc và Sẵn sàng."
    )
    
    print("=== FORMATTED SAMPLE QUIZ BLOCK ===")
    print(sample_block)
    print("===================================")

if __name__ == "__main__":
    main()
