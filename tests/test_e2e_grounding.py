#!/usr/bin/env python3
"""
test_e2e_grounding.py — End-to-End Grounding Integration Test for Edu-BanhMiMaHai OS
Tests real non-mock question items against authentic exported policy files in sources/.
Skips gracefully when authentic sources/ policy files are not yet exported from Notion.
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from validate_questions import validate_question_item, verify_sources_manifest
from content_hash_util import compute_content_hash

SOURCES_DIR = os.path.join(BASE_DIR, "sources")
AUTHENTIC_FILES_EXIST = os.path.exists(SOURCES_DIR) and any(
    f.endswith((".md", ".txt")) and f != "MANIFEST.sha256" for f in os.listdir(SOURCES_DIR)
)

class TestE2EGrounding(unittest.TestCase):

    @unittest.skipIf(not AUTHENTIC_FILES_EXIST, "Awaiting authentic exported Notion corporate policy files in sources/")
    def test_e2e_real_file_verbatim_grounding(self):
        """End-to-End Test: Validates a non-legacy draft question against authentic files in sources/."""
        
        manifest_ok, manifest_msg = verify_sources_manifest()
        self.assertTrue(manifest_ok, f"Manifest integrity MUST be valid before E2E test: {manifest_msg}")

        # Pick first available authentic source file in sources/
        source_files = [f for f in os.listdir(SOURCES_DIR) if f.endswith((".md", ".txt")) and f != "MANIFEST.sha256"]
        target_src_file = os.path.join("sources", source_files[0])
        
        with open(os.path.join(BASE_DIR, target_src_file), "r", encoding="utf-8") as sf:
            content = sf.read()
            
        first_line = content.splitlines()[0].strip() if content.splitlines() else "Default Quote"

        item = {
            "id": "E2E-001",
            "module": "hoinhap",
            "question": "E2E Question",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "explanation": first_line,
            "source_file": target_src_file,
            "source_quote": first_line,
            "source_ref": "Authentic Notion Policy Doc",
            "extraction_type": "verbatim",
            "status": "draft",
            "generated_by": "e2e_grounding_test"
        }
        item["content_hash"] = compute_content_hash(item)

        errors, warnings = validate_question_item(item, "E2E-001")
        self.assertEqual(len(errors), 0, f"Real source E2E validation MUST PASS! Errors: {errors}")

if __name__ == "__main__":
    unittest.main()
