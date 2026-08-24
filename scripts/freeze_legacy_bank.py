#!/usr/bin/env python3
"""
freeze_legacy_bank.py — Freezes current 301 legacy question bank into data/legacy/ (Slice 1)
Generates legacy-published.json and legacy-manifest.json with SHA-256 baseline.
"""

import sys
import os
import json
import hashlib
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEGACY_DIR = os.path.join(BASE_DIR, "data", "legacy")

def freeze_legacy_bank():
    os.makedirs(LEGACY_DIR, exist_ok=True)
    src_bank = os.path.join(BASE_DIR, "question-bank.json")

    if not os.path.exists(src_bank):
        print("ERROR: question-bank.json not found.")
        sys.exit(1)

    with open(src_bank, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    
    # 1. Write legacy-published.json
    pub_path = os.path.join(LEGACY_DIR, "legacy-published.json")
    with open(pub_path, "w", encoding="utf-8") as f:
        json.dump({"questions": questions}, f, ensure_ascii=False, indent=2)

    # 2. Compute SHA-256 and write legacy-manifest.json
    with open(pub_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    manifest_data = {
        "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_records": len(questions),
        "sha256": sha256,
        "legacy_file": "data/legacy/legacy-published.json",
        "status": "FROZEN_READ_ONLY"
    }

    manifest_path = os.path.join(LEGACY_DIR, "legacy-manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "passed",
        "total_frozen": len(questions),
        "published": pub_path,
        "manifest": manifest_path,
        "sha256": sha256
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    freeze_legacy_bank()
