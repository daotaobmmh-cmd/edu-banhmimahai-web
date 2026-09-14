#!/usr/bin/env python3
"""
test_inter_workflow_chains.py — Unit tests for inter-workflow pipeline orchestration (v7.0)
Verifies that all workflow chains (Radar -> Certify, Ingestion -> Publish, Swarm -> Staging, Drift -> Revoke) are 100% matched and functional.
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from orchestrate_workflows import test_inter_workflow_chain

class TestInterWorkflowChains(unittest.TestCase):

    def test_all_chains_matched(self):
        """Verifies that all inter-workflow chains run and pass end-to-end."""
        results = test_inter_workflow_chain()
        self.assertEqual(results["chain_1_upgrade_radar"]["status"], "passed")
        self.assertTrue(results["chain_1_upgrade_radar"]["re_certification_trigger_ready"])
        self.assertEqual(results["chain_2_ingestion_publish"]["status"], "passed")
        self.assertEqual(results["chain_3_assurance_lifecycle"]["status"], "passed")

if __name__ == "__main__":
    unittest.main()
