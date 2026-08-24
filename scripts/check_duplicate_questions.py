#!/usr/bin/env python3
"""
check_duplicate_questions.py — Duplicate Question Checker for Edu-BanhMiMaHai OS
Detects duplicate question IDs or duplicate question prompts in Markdown/JSON files.
"""

import sys
import os
import re
import json

def check_duplicates(file_path):
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'(?=^###\s+Câu\s+)', content, flags=re.MULTILINE)
    
    seen_codes = {}
    seen_prompts = {}
    duplicates = []

    for block in blocks:
        if not block.strip().startswith("### Câu"):
            continue

        header_match = re.search(r'^###\s+Câu\s+(\d+)\s*\((?:Mã:\s*([^)]+))\)', block, re.MULTILINE)
        prompt_match = re.search(r'\*\*Đề bài:\*\*\s*(.+)', block)
        
        if header_match:
            q_code = header_match.group(2).strip()
            if q_code in seen_codes:
                duplicates.append(f"Duplicate Question Code: {q_code}")
            else:
                seen_codes[q_code] = True

        if prompt_match:
            prompt = prompt_match.group(1).strip().lower()
            if prompt in seen_prompts:
                duplicates.append(f"Duplicate Question Prompt: '{prompt[:50]}...'")
            else:
                seen_prompts[prompt] = True

    status = "passed" if len(duplicates) == 0 else "failed"
    return {
        "status": status,
        "total_unique_codes": len(seen_codes),
        "duplicates": duplicates
    }

def main():
    target_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "danh_sach_cau_hoi_hoinhap.md")
    result = check_duplicates(target_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "passed":
        sys.exit(1)

if __name__ == "__main__":
    main()
