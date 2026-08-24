#!/usr/bin/env python3
"""
build_review_bundle.py — Bundles quiz candidates into a review bundle (Slice 2)
Bundles candidates in .staging/<run_id>/candidates/ into .staging/<run_id>/reports/review-bundle.json
and computes deterministic candidate hash.
"""

import sys
import os
import json
import hashlib
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def build_review_bundle(run_id="run-001"):
    staging_dir = os.path.join(BASE_DIR, ".staging", run_id)
    cand_dir = os.path.join(staging_dir, "candidates")
    reports_dir = os.path.join(staging_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    candidates = []
    if os.path.exists(cand_dir):
        for f in os.listdir(cand_dir):
            if f.endswith(".json"):
                with open(os.path.join(cand_dir, f), "r", encoding="utf-8") as cf:
                    candidates.append(json.load(cf))

    raw_bytes = json.dumps(candidates, sort_keys=True, ensure_ascii=False).encode("utf-8")
    candidate_hash = hashlib.sha256(raw_bytes).hexdigest()

    bundle = {
        "run_id": run_id,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_candidates": len(candidates),
        "candidate_hash": candidate_hash,
        "candidates": candidates
    }

    bundle_path = os.path.join(reports_dir, "review-bundle.json")
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "passed",
        "bundle_path": bundle_path,
        "candidate_hash": candidate_hash,
        "total_candidates": len(candidates)
    }, ensure_ascii=False, indent=2))
    return bundle

if __name__ == "__main__":
    run_id_arg = sys.argv[1] if len(sys.argv) > 1 else "run-001"
    build_review_bundle(run_id_arg)
