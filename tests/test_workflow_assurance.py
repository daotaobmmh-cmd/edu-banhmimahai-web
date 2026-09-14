#!/usr/bin/env python3
"""
test_workflow_assurance.py — Unit & Mutation Tests for Workflow Assurance Gate (Slice 0B)
Verifies that all 12 intentional failure mutations are 100% REJECTED,
and valid candidates pass assessment, evidence verification, promotion, and revocation.
"""

import unittest
import os
import sys
import json
import hashlib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WA_SCRIPTS = os.path.join(BASE_DIR, "workflow-assurance", "scripts")
sys.path.insert(0, WA_SCRIPTS)

from lint_contract import lint_contract
from audit_permissions import audit_permissions
from run_assessment import run_assessment
from verify_evidence import verify_evidence
from promote_workflow import promote_workflow
from revoke_workflow import revoke_workflow

class TestWorkflowAssurance(unittest.TestCase):

    def setUp(self):
        self.mutations_dir = os.path.join(BASE_DIR, "workflow-assurance", "tests", "mutations")

    def test_all_12_mutations_rejected(self):
        """Verifies that all 12 intentional failure mutation candidates are 100% REJECTED."""
        if not os.path.exists(self.mutations_dir):
            self.skipTest("Mutations directory does not exist")

        mutation_files = [f for f in os.listdir(self.mutations_dir) if f.endswith(".json")]
        self.assertEqual(len(mutation_files), 12, "Must test exactly 12 mutation files")

        rejected_count = 0
        for mf in mutation_files:
            fp = os.path.join(self.mutations_dir, mf)
            evidence = run_assessment(fp, assessment_id=f"test-mut-{mf.replace('.json', '')}")
            if evidence["verdict"] == "REJECTED":
                rejected_count += 1

        self.assertEqual(rejected_count, 12, f"All 12 mutations must be REJECTED! (Got {rejected_count}/12)")

    def test_valid_candidate_assessment_and_promotion(self):
        """Verifies valid candidate assessment, evidence verification, promotion, and revocation."""
        # Create valid candidate manifest
        valid_manifest = {
            "name": "pilot-quiz-gen",
            "version": "1.0.0",
            "owner": "quiz-team",
            "purpose": "Pilot quiz generation workflow",
            "execution_risk": "E1",
            "trigger": { "type": "manual" },
            "inputs": [{ "name": "doc_id", "type": "string", "required": True }],
            "outputs": [{ "path": ".staging/run-pilot/quiz.json" }],
            "permissions": {
                "tools": ["view_file", "write_to_file"],
                "write_paths": [".staging/run-pilot/"],
                "can_spawn_subagents": False
            },
            "preconditions": ["doc_id exists"],
            "postconditions": ["quiz output schema validated"],
            "failure_policy": { "unknown_tool": "deny", "missing_evidence": "fail", "retries": 0 },
            "rollback": { "type": "delete_staging_run" },
            "tests": ["happy_path"]
        }

        tmp_dir = os.path.join(BASE_DIR, ".staging", "test-valid-cand")
        os.makedirs(tmp_dir, exist_ok=True)
        cand_path = os.path.join(tmp_dir, "pilot-quiz-gen.json")
        with open(cand_path, "w", encoding="utf-8") as f:
            json.dump(valid_manifest, f)

        # Create candidate markdown file
        md_path = os.path.join(tmp_dir, "pilot-quiz-gen.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Pilot Quiz Gen Workflow Specification")

        # 1. Run assessment
        evidence = run_assessment(cand_path, assessment_id="test-valid-run")
        self.assertEqual(evidence["verdict"], "NEEDS_HUMAN_REVIEW")
        self.assertEqual(evidence["gates"]["contract"], "PASS")
        self.assertEqual(evidence["gates"]["permissions"], "PASS")

        # 2. Verify evidence
        ev_path = os.path.join(BASE_DIR, ".staging", "workflow-assurance", "test-valid-run", "evidence-manifest.json")
        ok, msg = verify_evidence(ev_path)
        self.assertTrue(ok, f"Evidence verification must pass: {msg}")

        # 3. Create certificate (use md_path SHA256)
        with open(md_path, "rb") as mf:
            md_sha256 = hashlib.sha256(mf.read()).hexdigest()

        cert_data = {
            "certificate_id": "cert-pilot-quiz-gen-1.0.0",
            "assessment_id": "test-valid-run",
            "target_manifest_sha256": md_sha256,
            "dependency_closure_sha256": evidence["target"]["dependency_closure_sha256"],
            "approved_permissions_sha256": evidence["target"]["dependency_closure_sha256"],
            "approved_by": "human-reviewer-01",
            "approved_at": "2026-08-13T20:40:00Z",
            "verdict": "CERTIFIED"
        }
        cert_path = os.path.join(tmp_dir, "cert-pilot-quiz-gen-1.0.0.json")
        with open(cert_path, "w", encoding="utf-8") as f:
            json.dump(cert_data, f)

        # 4. Promote workflow
        prom_path = promote_workflow(md_path, cert_path)
        self.assertTrue(os.path.exists(prom_path))

        # 5. Revoke workflow
        revoke_res = revoke_workflow("pilot-quiz-gen", reason="Test revocation")
        self.assertEqual(revoke_res["status"], "passed")
        self.assertFalse(os.path.exists(prom_path))

if __name__ == "__main__":
    unittest.main()
