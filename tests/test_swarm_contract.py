#!/usr/bin/env python3
"""
test_swarm_contract.py — Subagent Swarm Read-Only Contract Verification (Slice 4)
Verifies that all subagent profile files (.agents/agents/*.md) strictly specify read-only tool allowlists and disable subagent spawning.
"""

import unittest
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(BASE_DIR, ".agents", "agents")

class TestSwarmContract(unittest.TestCase):

    def test_subagents_read_only_tools_only(self):
        """Verifies subagent profile files (.agents/agents/*.md) specify read-only tools and enable_subagent_tools: false."""
        if not os.path.exists(AGENTS_DIR):
            self.skipTest(".agents/agents/ directory does not exist")

        disallowed_tools = ["write_to_file", "replace_file_content", "run_command", "invoke_subagent"]
        subagent_files = [f for f in os.listdir(AGENTS_DIR) if f.endswith(".md")]

        self.assertTrue(len(subagent_files) >= 3, "Must have at least 3 subagent profile files")

        for f in subagent_files:
            file_path = os.path.join(AGENTS_DIR, f)
            with open(file_path, "r", encoding="utf-8") as sf:
                content = sf.read()

            self.assertTrue("enable_subagent_tools: false" in content, f"Subagent '{f}' must set enable_subagent_tools: false")

            for dt in disallowed_tools:
                self.assertFalse(f"- {dt}" in content, f"Subagent '{f}' must NOT include disallowed tool '{dt}'")

if __name__ == "__main__":
    unittest.main()
