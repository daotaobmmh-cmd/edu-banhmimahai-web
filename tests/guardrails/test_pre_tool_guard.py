#!/usr/bin/env python3
"""
test_pre_tool_guard.py — Unit Tests for PreToolUse Hook Guard (v7.0)
Tests positive path allowed writes, and negative path denials (traversal, protected paths, staging bypass).
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts", "guardrails")
sys.path.insert(0, SCRIPTS_DIR)

from pre_tool_guard import evaluate_tool_call

class TestPreToolGuard(unittest.TestCase):

    def test_positive_read_tool_allowed(self):
        """Read-only tools MUST ALWAYS be allowed."""
        res = evaluate_tool_call("view_file", {"AbsolutePath": "index.html"}, mode="draft")
        self.assertEqual(res["decision"], "allow")

    def test_positive_staging_write_allowed(self):
        """Writing to .staging/<run_id>/ in draft mode MUST be allowed."""
        res = evaluate_tool_call("write_to_file", {"TargetFile": ".staging/run-101/candidate.json"}, mode="draft")
        self.assertEqual(res["decision"], "allow")

    def test_negative_protected_path_denied(self):
        """Attempting to modify protected path (security/, .agents/, AGENTS.md) MUST BE DENIED."""
        res = evaluate_tool_call("write_to_file", {"TargetFile": "AGENTS.md"}, mode="draft")
        self.assertEqual(res["decision"], "deny")
        self.assertTrue("protected control-plane path" in res["reason"])

        res2 = evaluate_tool_call("write_to_file", {"TargetFile": ".agents/rules/global-safety.md"}, mode="draft")
        self.assertEqual(res2["decision"], "deny")

    def test_negative_staging_bypass_denied(self):
        """Attempting to write outside .staging/ in draft mode MUST BE DENIED."""
        res = evaluate_tool_call("write_to_file", {"TargetFile": "index.html"}, mode="draft")
        self.assertEqual(res["decision"], "deny")
        self.assertTrue("Draft execution mode requires writes to be inside '.staging/'" in res["reason"])

    def test_negative_path_traversal_denied(self):
        """Attempting path traversal ('../outside.txt') MUST BE DENIED."""
        res = evaluate_tool_call("write_to_file", {"TargetFile": ".staging/../../outside.txt"}, mode="draft")
        self.assertEqual(res["decision"], "deny")
        self.assertTrue("resolves outside of workspace boundary" in res["reason"])

if __name__ == "__main__":
    unittest.main()
