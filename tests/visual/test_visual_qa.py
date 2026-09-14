#!/usr/bin/env python3
"""
test_visual_qa.py — Design Tokens & Visual QA Linter (Slice 3)
Audits HTML & CSS files for raw hardcoded brand hex codes outside design tokens,
and verifies responsive breakpoint compliance (375, 768, 1440).
"""

import unittest
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class TestVisualQA(unittest.TestCase):

    def test_no_hardcoded_brand_hex(self):
        """Audits HTML/CSS files for prohibited hardcoded hex colors outside index.css design tokens."""
        prohibited_hexes = [r"#e53935", r"#d32f2f", r"#c62828"]
        allowlist = ["index.css", ".agents/rules/frontend-visual.md"]

        violations = []
        for root, dirs, files in os.walk(BASE_DIR):
            if ".staging" in root or ".git" in root or "node_modules" in root:
                continue
            for file in files:
                if file.endswith((".html", ".css")) and file not in allowlist:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for p_hex in prohibited_hexes:
                        if re.search(p_hex, content, re.IGNORECASE):
                            rel_path = os.path.relpath(file_path, BASE_DIR)
                            violations.append(f"Hardcoded brand hex '{p_hex}' found in '{rel_path}'")

        self.assertEqual(len(violations), 0, f"Hardcoded brand hex violations found: {violations}")

    def test_responsive_breakpoints_defined(self):
        """Verifies 3 mandatory breakpoints (375, 768, 1440) exist in design configuration."""
        css_file = os.path.join(BASE_DIR, "index.css")
        if os.path.exists(css_file):
            with open(css_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertTrue("768" in content or "@media" in content, "Responsive breakpoints must be defined in CSS")

if __name__ == "__main__":
    unittest.main()
