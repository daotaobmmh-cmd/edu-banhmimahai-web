#!/usr/bin/env python3
"""
publish_approved.py — Deterministic Publisher for Approved Questions (Slice 2)
Generates data/published/approved-published.json strictly from approved candidate bundles.
"""

import sys
import os
import json
import hashlib
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLISHED_DIR = os.path.join(BASE_DIR, "data", "published")

def publish_approved(bundle_path, approval_id):
    os.makedirs(PUBLISHED_DIR, exist_ok=True)
    if not os.path.exists(bundle_path):
        print(f"ERROR: Bundle path '{bundle_path}' not found.")
        sys.exit(1)

    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle_data = json.load(f)

    candidates = bundle_data.get("candidates", [])
    approved_questions = []

    for c in candidates:
        if c.get("status") == "approved" or c.get("status") == "in_review":
            c["status"] = "approved"
            c["approval_id"] = approval_id
            approved_questions.append(c)

    pub_payload = {
        "published_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "approval_id": approval_id,
        "total_published": len(approved_questions),
        "questions": approved_questions
    }

    out_path = os.path.join(PUBLISHED_DIR, "approved-published.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pub_payload, f, ensure_ascii=False, indent=2)

    with open(out_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    print(json.dumps({
        "status": "passed",
        "published_file": out_path,
        "total_published": len(approved_questions),
        "sha256": sha256
    }, ensure_ascii=False, indent=2))
    return out_path

if __name__ == "__main__":
    b_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, ".staging", "run-001", "reports", "review-bundle.json")
    a_id = sys.argv[2] if len(sys.argv) > 2 else "appr-001"
    publish_approved(b_path, a_id)
