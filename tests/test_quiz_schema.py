#!/usr/bin/env python3
"""
test_quiz_schema.py — Unit test for question bank validation logic
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from validate_questions import validate_markdown_file
from check_duplicate_questions import check_duplicates

class TestQuizSchema(unittest.TestCase):

    def test_danh_sach_cau_hoi_exist(self):
        q_file = os.path.join(BASE_DIR, "danh_sach_cau_hoi_hoinhap.md")
        self.assertTrue(os.path.exists(q_file), "danh_sach_cau_hoi_hoinhap.md must exist")

    def test_danh_sach_cau_hoi_valid(self):
        q_file = os.path.join(BASE_DIR, "danh_sach_cau_hoi_hoinhap.md")
        res = validate_markdown_file(q_file)
        self.assertEqual(res["status"], "passed", f"Errors in quiz validation: {res.get('errors')}")

    def test_danh_sach_cau_hoi_no_duplicates(self):
        q_file = os.path.join(BASE_DIR, "danh_sach_cau_hoi_hoinhap.md")
        res = check_duplicates(q_file)
        self.assertEqual(res["status"], "passed", f"Duplicates found: {res.get('duplicates')}")

if __name__ == "__main__":
    unittest.main()
