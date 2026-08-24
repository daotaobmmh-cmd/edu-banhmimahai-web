#!/usr/bin/env python3
"""
inventory_questions.py — Read-Only Question Bank Inventory Script for Phase 0 Baseline (v7.0)
Analyzes existing Markdown & JSON question banks, counts real total records, unique/duplicate IDs,
missing fields, option formats, and file SHA-256 hashes without modifying any production file.
"""

import sys
import os
import re
import json
import hashlib
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def compute_sha256(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def analyze_markdown_bank(md_path):
    if not os.path.exists(md_path):
        return {"exists": False, "count": 0, "questions": []}

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'(?=^###\s+Câu\s+)', content, flags=re.MULTILINE)
    parsed = []

    for block in blocks:
        if not block.strip().startswith("### Câu"):
            continue

        header_match = re.search(r'^###\s+Câu\s+(\d+)\s*\((?:Mã:\s*([^)]+))\)', block, re.MULTILINE)
        if not header_match:
            continue

        q_code = header_match.group(2).strip()
        prompt_match = re.search(r'\*\*Đề bài:\*\*\s*(.+)', block)
        prompt = prompt_match.group(1).strip() if prompt_match else ""

        options = re.findall(r'-\s*\[([ xX])\]\s*\*\*([A-D])\*\*:\s*(.+)', block)
        ans_match = re.search(r'>\s*\*\*Đáp án đúng:\*\*\s*`?([A-D])`?', block)
        ans_key = ans_match.group(1) if ans_match else ""

        parsed.append({
            "id": q_code,
            "question": prompt,
            "option_count": len(options),
            "correct_answer": ans_key
        })

    return {
        "exists": True,
        "file_path": md_path,
        "sha256": compute_sha256(md_path),
        "total_parsed": len(parsed),
        "questions": parsed
    }

def analyze_json_bank(json_path):
    if not os.path.exists(json_path):
        return {"exists": False, "count": 0, "questions": []}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    return {
        "exists": True,
        "file_path": json_path,
        "sha256": compute_sha256(json_path),
        "total_parsed": len(questions),
        "questions": questions
    }

def run_inventory():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    staging_dir = os.path.join(BASE_DIR, ".staging", f"baseline-{date_str}")
    os.makedirs(staging_dir, exist_ok=True)

    md_file = os.path.join(BASE_DIR, "danh_sach_cau_hoi_hoinhap.md")
    json_file = os.path.join(BASE_DIR, "question-bank.json")

    md_res = analyze_markdown_bank(md_file)
    json_res = analyze_json_bank(json_file)

    # Collect ID statistics
    all_ids = []
    id_counts = {}
    missing_fields_count = 0

    if json_res["exists"]:
        for q in json_res["questions"]:
            qid = q.get("id")
            if qid:
                all_ids.append(qid)
                id_counts[qid] = id_counts.get(qid, 0) + 1
            if not q.get("question") or not q.get("options") or not q.get("correct_answer"):
                missing_fields_count += 1

    duplicates = [qid for qid, cnt in id_counts.items() if cnt > 1]

    inventory_report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "markdown_source": {
            "path": "danh_sach_cau_hoi_hoinhap.md",
            "exists": md_res["exists"],
            "sha256": md_res.get("sha256"),
            "total_parsed_questions": md_res["total_parsed"]
        },
        "json_source": {
            "path": "question-bank.json",
            "exists": json_res["exists"],
            "sha256": json_res.get("sha256"),
            "total_parsed_questions": json_res["total_parsed"]
        },
        "statistics": {
            "total_unique_ids": len(set(all_ids)),
            "total_duplicate_ids": len(duplicates),
            "duplicate_id_list": duplicates,
            "questions_with_missing_fields": missing_fields_count
        }
    }

    report_path = os.path.join(staging_dir, "question-inventory.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(inventory_report, f, ensure_ascii=False, indent=2)

    manifest_data = {
        "run_id": f"baseline-{date_str}",
        "workflow": "phase-0-discovery-inventory",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "file_hashes": {
            "danh_sach_cau_hoi_hoinhap.md": md_res.get("sha256"),
            "question-bank.json": json_res.get("sha256")
        },
        "inventory_report_path": report_path
    }

    manifest_path = os.path.join(staging_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "passed",
        "inventory_report": report_path,
        "manifest": manifest_path,
        "summary": {
            "markdown_questions": md_res["total_parsed"],
            "json_questions": json_res["total_parsed"],
            "unique_ids": len(set(all_ids)),
            "duplicates": len(duplicates)
        }
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run_inventory()
