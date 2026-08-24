#!/usr/bin/env python3
"""
verify_approval.py — Verifies Human Approval Manifests (Slice 2)
Verifies that human approval record in approvals/ matches the candidate bundle hash.
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APPROVALS_DIR = os.path.join(BASE_DIR, "approvals")

def verify_approval(approval_id, candidate_hash):
    os.makedirs(APPROVALS_DIR, exist_ok=True)
    approval_file = os.path.join(APPROVALS_DIR, f"{approval_id}.json")

    if not os.path.exists(approval_file):
        return False, f"Approval record '{approval_file}' not found."

    try:
        with open(approval_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        target_hash = data.get("target_manifest_sha256")
        if target_hash != candidate_hash:
            return False, f"Approval hash mismatch! (approval={target_hash[:8]} vs candidate={candidate_hash[:8]})"

        if not data.get("approved_by") or not data.get("approved_at"):
            return False, "Approval record missing approved_by or approved_at timestamp."

        return True, "Approval verified successfully."
    except Exception as e:
        return False, f"Failed to read approval record: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"status": "failed", "error": "Usage: verify_approval.py <approval_id> <candidate_hash>"}))
        sys.exit(1)
    ok, msg = verify_approval(sys.argv[1], sys.argv[2])
    print(json.dumps({"status": "passed" if ok else "failed", "message": msg}, ensure_ascii=False, indent=2))
    if not ok:
        sys.exit(1)
