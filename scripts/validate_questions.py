#!/usr/bin/env python3
"""
validate_questions.py — Question Bank Validator for Edu-BanhMiMaHai OS (V2.2)
Validates Markdown quiz documents and JSON question banks with Substring Exact-Match & Content Hash verification.
"""

import sys
import os
import re
import json
import hashlib
import unicodedata

# Ensure current scripts directory is in sys.path
sys.path.insert(0, os.path.dirname(__file__))
from content_hash_util import normalize_nfc_text, compute_content_hash

def verify_sources_manifest():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(base_dir, "sources", "MANIFEST.sha256")
    if not os.path.exists(manifest_path):
        return True, "Manifest file not found, skipping manifest tamper check"
        
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            locked_manifest = json.load(f)
            
        for filename, expected_hash in locked_manifest.items():
            full_path = os.path.join(base_dir, "sources", filename)
            if not os.path.exists(full_path):
                return False, f"ERR_SOURCE_GROUNDING_TAMPERED: Locked source file '{filename}' is missing!"
            
            with open(full_path, "rb") as sf:
                actual_hash = hashlib.sha256(sf.read()).hexdigest()
            if actual_hash != expected_hash:
                return False, f"ERR_SOURCE_GROUNDING_TAMPERED: Locked source file '{filename}' was tampered with or modified!"
                
        return True, "Manifest integrity verified"
    except Exception as e:
        return False, f"ERR_SOURCE_GROUNDING_TAMPERED: Manifest verification failed: {str(e)}"

def validate_question_item(q, index_label=""):
    errors = []
    warnings = []

    status = q.get("status", "draft")
    
    # 1. Content Hash Verification
    calculated_hash = compute_content_hash(q)
    declared_hash = q.get("content_hash")
    if declared_hash and declared_hash != calculated_hash:
        errors.append(f"{index_label}: Content hash mismatch! Content may have been modified without updating hash.")

    # 2. Status-based Validation Rules
    if status == "legacy":
        if not q.get("source_ref"):
            warnings.append(f"{index_label}: Legacy question lacks source_ref (Backfill pending).")
    else:
        # Strict Zero-Trust validation for non-legacy items
        if not q.get("source_ref"):
            errors.append(f"{index_label}: Missing mandatory source_ref field.")
            
        if not q.get("source_quote"):
            errors.append(f"{index_label}: Missing mandatory source_quote field.")

        # Substring Exact-Match Validation against source_file
        source_file = q.get("source_file")
        source_quote = q.get("source_quote")
        if source_file and source_quote:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            full_src_path = os.path.join(base_dir, source_file)
            if not os.path.exists(full_src_path):
                errors.append(f"{index_label}: Source file '{source_file}' not found at '{full_src_path}'.")
            else:
                try:
                    with open(full_src_path, "r", encoding="utf-8") as sf:
                        src_content = sf.read()
                    
                    norm_src = normalize_nfc_text(src_content)
                    norm_quote = normalize_nfc_text(source_quote)

                    if norm_quote not in norm_src:
                        errors.append(f"{index_label}: Exact Substring Match FAILED! source_quote does not exist verbatim inside '{source_file}'.")
                except Exception as e:
                    errors.append(f"{index_label}: Failed to read source file '{source_file}': {str(e)}")

    return errors, warnings

def validate_markdown_file(file_path):
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'(?=^###\s+Câu\s+)', content, flags=re.MULTILINE)
    
    questions = []
    errors = []
    warnings = []

    for idx, block in enumerate(blocks):
        if not block.strip().startswith("### Câu"):
            continue
        
        header_match = re.search(r'^###\s+Câu\s+(\d+)\s*\((?:Mã:\s*([^)]+))\)', block, re.MULTILINE)
        if not header_match:
            errors.append(f"Block #{idx}: Malformed question header format.")
            continue
        
        q_num = header_match.group(1)
        q_code = header_match.group(2).strip()

        prompt_match = re.search(r'\*\*Đề bài:\*\*\s*(.+)', block)
        prompt = prompt_match.group(1).strip() if prompt_match else ""

        options = re.findall(r'-\s*\[([ xX])\]\s*\*\*([A-D])\*\*:\s*(.+)', block)
        if len(options) < 2:
            errors.append(f"Question {q_code} (Câu {q_num}): Must have at least 2 choice options.")

        checked_choices = [opt[1] for opt in options if opt[0].lower() == 'x']
        ans_match = re.search(r'>\s*\*\*Đáp án đúng:\*\*\s*`?([A-D])`?', block)
        ans_key = ans_match.group(1) if ans_match else None

        if ans_key and checked_choices and ans_key not in checked_choices:
            errors.append(f"Question {q_code} (Câu {q_num}): Mismatch between checked choice [{checked_choices[0]}] and declared answer key [{ans_key}].")

        exp_match = re.search(r'>\s*\*\*Giải thích:\*\*\s*(.+)', block)
        explanation = exp_match.group(1).strip() if exp_match else ""

        q_item = {
            "id": q_code,
            "question": prompt,
            "options": [opt[2].strip() for opt in options],
            "correct_answer": ans_key or "",
            "explanation": explanation,
            "status": "legacy"  # Markdown questions default to legacy status
        }

        item_errors, item_warnings = validate_question_item(q_item, f"Question {q_code}")
        errors.extend(item_errors)
        warnings.extend(item_warnings)

        questions.append(q_item)

    status = "passed" if len(errors) == 0 else "failed"
    return {
        "status": status,
        "file_path": file_path,
        "total_questions_parsed": len(questions),
        "errors": errors,
        "warnings": warnings
    }

def main():
    ok, msg = verify_sources_manifest()
    if not ok:
        print(json.dumps({"status": "failed", "errors": [msg]}, ensure_ascii=False, indent=2))
        sys.exit(1)
        
    target_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "danh_sach_cau_hoi_hoinhap.md")
    result = validate_markdown_file(target_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "passed":
        sys.exit(1)

if __name__ == "__main__":
    main()
