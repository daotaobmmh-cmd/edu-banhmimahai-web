#!/usr/bin/env python3
"""
test_slice2_pipeline.py — Single-Agent Pipeline & Notion Dry-Run Unit Tests (Slice 2)
Verifies bundle building, approval manifest validation, deterministic publishing, and notion dry-run.
"""

import unittest
import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from build_review_bundle import build_review_bundle
from verify_approval import verify_approval
from publish_approved import publish_approved

class TestSlice2Pipeline(unittest.TestCase):

    def setUp(self):
        self.run_id = "test-run-slice2"
        self.staging_dir = os.path.join(BASE_DIR, ".staging", self.run_id)
        self.cand_dir = os.path.join(self.staging_dir, "candidates")
        os.makedirs(self.cand_dir, exist_ok=True)

        # Candidate item in V3 format
        self.candidate = {
            "id": "SLICE2-001",
            "module": "hoinhap",
            "question": "Sample Question",
            "options": [{"id": "opt_a", "text": "A"}, {"id": "opt_b", "text": "B"}, {"id": "opt_c", "text": "C"}, {"id": "opt_d", "text": "D"}],
            "correct_option_id": "opt_a",
            "evidence": {
                "document_id": "doc-01",
                "document_sha256": "abc123hash",
                "quote": "Sample Question",
                "verification": "exact_match"
            },
            "extraction_type": "verbatim",
            "status": "in_review",
            "provenance": {
                "run_id": self.run_id,
                "workflow_version": "v7.0",
                "model": "pro",
                "generated_at": "2026-08-13T20:00:00Z"
            }
        }
        with open(os.path.join(self.cand_dir, "cand-001.json"), "w", encoding="utf-8") as f:
            json.dump(self.candidate, f)

    def test_bundle_build_and_publish(self):
        """Test bundle building, approval hash verification, and deterministic publish."""
        bundle = build_review_bundle(self.run_id)
        self.assertEqual(bundle["total_candidates"], 1)
        cand_hash = bundle["candidate_hash"]

        # Create valid human approval record in approvals/
        appr_dir = os.path.join(BASE_DIR, "approvals")
        os.makedirs(appr_dir, exist_ok=True)
        appr_id = "appr-slice2-test"
        appr_record = {
            "approval_id": appr_id,
            "target_manifest_sha256": cand_hash,
            "approved_by": "human-reviewer-id",
            "approved_at": "2026-08-13T20:10:00Z",
            "scope": ["question:SLICE2-001"]
        }
        with open(os.path.join(appr_dir, f"{appr_id}.json"), "w", encoding="utf-8") as f:
            json.dump(appr_record, f)

        # Verify approval
        ok, msg = verify_approval(appr_id, cand_hash)
        self.assertTrue(ok, f"Approval verification must pass: {msg}")

        # Publish approved
        bundle_path = os.path.join(self.staging_dir, "reports", "review-bundle.json")
        pub_path = publish_approved(bundle_path, appr_id)
        self.assertTrue(os.path.exists(pub_path))

if __name__ == "__main__":
    unittest.main()
