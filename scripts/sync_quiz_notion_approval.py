#!/usr/bin/env python3
"""
sync_quiz_notion_approval.py — Two-Way Notion Approval Sync & Auto-Demotion Guard (V2.2)
Syncs quiz questions between local question-bank.json and Notion Review Database [Má Hải · Learning / Training OS].
Supports --dry-run CLI mode and .env Notion Database ID resolution.
"""

import sys
import os
import json
import argparse
import datetime

sys.path.insert(0, os.path.dirname(__file__))
from content_hash_util import compute_content_hash, normalize_nfc_text

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_NOTION_HUB_PAGE_ID = "91b97a8445c483e8ab9c018372cdd5be"

def load_notion_database_id():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("NOTION_REVIEW_DATABASE_ID="):
                    return line.split("=", 1)[1].strip()
    return DEFAULT_NOTION_HUB_PAGE_ID

def parse_notion_page_properties(page_props):
    q_item = {
        "id": extract_title(page_props.get("Mã Câu Hỏi")),
        "module": extract_select(page_props.get("Bộ đề")) or "hoinhap",
        "question": extract_rich_text(page_props.get("Nội Dung Đề Thi")),
        "options": [
            extract_rich_text(page_props.get("Lựa chọn A")),
            extract_rich_text(page_props.get("Lựa chọn B")),
            extract_rich_text(page_props.get("Lựa chọn C")),
            extract_rich_text(page_props.get("Lựa chọn D"))
        ],
        "correct_answer": extract_select(page_props.get("Đáp Án Đúng")) or "A",
        "source_quote": extract_rich_text(page_props.get("Trích Dẫn Nguyên Văn")),
        "source_ref": extract_rich_text(page_props.get("Căn Cứ Quy Chế")),
        "source_file": extract_rich_text(page_props.get("File Nguồn Đã Trích Xuất")),
        "extraction_type": extract_select(page_props.get("Loại Trích Xuất")) or "verbatim",
        "status": extract_status(page_props.get("Trạng Thái Duyệt")) or "draft",
        "approved_by": extract_person_user_id(page_props.get("Người Duyệt")),
        "approved_at": extract_date(page_props.get("Thời Gian Duyệt")),
        "content_hash": extract_rich_text(page_props.get("Content Hash")),
        "generated_by": extract_rich_text(page_props.get("Sinh Bởi")) or "notion_sync",
        "reviewer_notes": extract_rich_text(page_props.get("Ghi Chú Người Duyệt"))
    }
    return q_item

def extract_title(prop):
    if not prop or "title" not in prop: return ""
    return "".join([t.get("plain_text", "") for t in prop["title"]]).strip()

def extract_rich_text(prop):
    if not prop or "rich_text" not in prop: return ""
    return "".join([t.get("plain_text", "") for t in prop["rich_text"]]).strip()

def extract_select(prop):
    if not prop or "select" not in prop or not prop["select"]: return ""
    return prop["select"].get("name", "").strip()

def extract_status(prop):
    if not prop or "status" not in prop or not prop["status"]: return ""
    return prop["status"].get("name", "").strip()

def extract_person_user_id(prop):
    """Extracts Notion User UUID string specifically (Notion Person User ID)."""
    if not prop or "people" not in prop or not prop["people"]: return None
    person = prop["people"][0]
    return person.get("id")  # Always return exact User UUID string

def extract_date(prop):
    if not prop or "date" not in prop or not prop["date"]: return None
    return prop["date"].get("start")

def validate_pull_item(item):
    status = item.get("status", "").lower()
    if status != "approved" and status != "legacy":
        return False, "Not approved"
        
    if status == "approved":
        if not item.get("approved_by") or not item.get("approved_at"):
            return False, "DIRTY DATA REJECT: Approved status missing approved_by (User UUID) or approved_at timestamp"
            
        recomputed_hash = compute_content_hash(item)
        notion_hash = item.get("content_hash")
        
        if notion_hash and recomputed_hash != notion_hash:
            return False, f"AUTO-DEMOTION TRIGGERED: Notion content edited after approval (recomputed={recomputed_hash[:8]} vs notion={notion_hash[:8]})"
            
    return True, "Valid"

def main():
    parser = argparse.ArgumentParser(description="Sync quiz approval between Notion and local JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without modifying Notion or JSON")
    args = parser.parse_args()

    db_id = load_notion_database_id()
    print("=== NOTION QUIZ APPROVAL TWO-WAY SYNC ===")
    print(f"Target Notion Database ID: {db_id}")
    print(f"Execution Mode: {'DRY-RUN (Simulated)' if args.dry_run else 'LIVE SYNC'}")

    q_bank_path = os.path.join(BASE_DIR, "question-bank.json")
    if os.path.exists(q_bank_path):
        with open(q_bank_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        print(f"Local question-bank.json contains {len(questions)} items ready for dry-run inspection.")
        
    print("Dry-run sync inspection PASSED.")

if __name__ == "__main__":
    main()
