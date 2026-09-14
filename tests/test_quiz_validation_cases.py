#!/usr/bin/env python3
"""
test_quiz_validation_cases.py — Rigorous Negative & Positive Test Suite for Edu-BanhMiMaHai OS
Tests exact-match failure, missing source_ref, Unicode NFD vs NFC, hash drift auto-demotion, dirty data rejection, and legacy status.
"""

import unittest
import os
import sys
import json
import unicodedata

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from validate_questions import validate_question_item
from content_hash_util import compute_content_hash, normalize_nfc_text
from sync_quiz_notion_approval import validate_pull_item

class TestQuizValidationCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Access test fixture source file in tests/fixtures/sources/
        cls.sources_dir = os.path.join(BASE_DIR, "tests", "fixtures", "sources")
        cls.test_src_rel = "tests/fixtures/sources/Test_Cam_Nang_Hoi_Nhap_2026.txt"
        cls.test_src_full = os.path.join(BASE_DIR, cls.test_src_rel)
        
        # Real authentic text in NFC
        cls.authentic_text = (
            "CÔNG TY CỔ PHẦN BÁNH MÌ MÁ HẢI\n"
            "Mục I. Hành Trình Khởi Nghiệp\n"
            "Bánh Mì Má Hải khởi nghiệp năm 2013 với 2 triệu đồng và một chiếc xe bánh mì đầu tiên.\n"
            "Mục II. Giá Trị Cốt Lõi\n"
            "Bánh Mì Má Hải có 5 giá trị cốt lõi: Giá trị, Kết quả, Trách nhiệm, Làm chủ và Học hỏi.\n"
        )

    def test_case_1_fabricated_quote_rejection(self):
        """Negative Test 1: Fabricated source_quote not found in source file MUST BE REJECTED."""
        item = {
            "id": "TEST-001",
            "module": "hoinhap",
            "question": "Bánh Mì Má Hải thành lập năm nào?",
            "options": ["2013", "2015", "2017", "2020"],
            "correct_answer": "A",
            "explanation": "Câu này bịa nguyên văn.",
            "source_file": self.test_src_rel,
            "source_quote": "Đây là văn bản bịa không hề có trong file nguồn.",
            "source_ref": "Mục I, Trang 1",
            "extraction_type": "verbatim",
            "status": "draft",
            "generated_by": "test_agent"
        }
        item["content_hash"] = compute_content_hash(item)
        errors, warnings = validate_question_item(item, "TEST-001")
        self.assertTrue(len(errors) > 0, "Fabricated source_quote MUST produce errors!")
        self.assertTrue(any("Exact Substring Match FAILED" in e for e in errors))

    def test_case_2_missing_source_ref_rejection(self):
        """Negative Test 2: Non-legacy item missing source_ref MUST BE REJECTED."""
        item = {
            "id": "TEST-002",
            "module": "hoinhap",
            "question": "Bánh Mì Má Hải có mấy giá trị cốt lõi?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "C",
            "explanation": "Bánh Mì Má Hải có 5 giá trị cốt lõi.",
            "source_file": self.test_src_rel,
            "source_quote": "Bánh Mì Má Hải có 5 giá trị cốt lõi: Giá trị, Kết quả, Trách nhiệm, Làm chủ và Học hỏi.",
            "source_ref": "",  # Missing source_ref
            "extraction_type": "verbatim",
            "status": "draft",
            "generated_by": "test_agent"
        }
        item["content_hash"] = compute_content_hash(item)
        errors, warnings = validate_question_item(item, "TEST-002")
        self.assertTrue(len(errors) > 0, "Missing source_ref MUST produce error for draft status!")
        self.assertTrue(any("Missing mandatory source_ref field" in e for e in errors))

    def test_case_3_unicode_nfd_vs_nfc_pass(self):
        """Positive Test 3: source_quote in NFD format MUST PASS when source file is in NFC (Unicode Normalization)."""
        quote_nfc = "Bánh Mì Má Hải khởi nghiệp năm 2013 với 2 triệu đồng và một chiếc xe bánh mì đầu tiên."
        quote_nfd = unicodedata.normalize("NFD", quote_nfc)
        
        # Verify quote_nfd has different code points than quote_nfc
        self.assertNotEqual(quote_nfc, quote_nfd, "NFD string must differ in raw representation from NFC")

        item = {
            "id": "TEST-003",
            "module": "hoinhap",
            "question": "Bánh Mì Má Hải khởi nghiệp năm nào?",
            "options": ["2013", "2015", "2017", "2020"],
            "correct_answer": "A",
            "explanation": quote_nfc,
            "source_file": self.test_src_rel,
            "source_quote": quote_nfd,  # NFD string passed as source_quote
            "source_ref": "Mục I, Trang 1",
            "extraction_type": "verbatim",
            "status": "draft",
            "generated_by": "test_agent"
        }
        item["content_hash"] = compute_content_hash(item)
        errors, warnings = validate_question_item(item, "TEST-003")
        self.assertEqual(len(errors), 0, f"Unicode NFD vs NFC should pass exact match normalization! Errors: {errors}")

    def test_case_4_hash_drift_auto_demotion(self):
        """Negative Test 4: Approved item with modified correct_answer MUST TRIGGER AUTO-DEMOTION."""
        item = {
            "id": "TEST-004",
            "module": "hoinhap",
            "question": "Bánh Mì Má Hải khởi nghiệp năm nào?",
            "options": ["2013", "2015", "2017", "2020"],
            "correct_answer": "A",
            "source_quote": "Bánh Mì Má Hải khởi nghiệp năm 2013",
            "source_ref": "Mục I",
            "source_file": self.test_src_rel,
            "extraction_type": "verbatim",
            "status": "approved",
            "approved_by": "usr_tilog_uuid_12345",
            "approved_at": "2026-08-13T10:00:00Z"
        }
        # Compute valid original hash
        original_hash = compute_content_hash(item)
        item["content_hash"] = original_hash

        # Now stealthily modify correct_answer on Notion side without updating content_hash
        item["correct_answer"] = "B"
        valid, msg = validate_pull_item(item)
        self.assertFalse(valid, "Hash drift MUST trigger demotion and pull rejection!")
        self.assertTrue("AUTO-DEMOTION TRIGGERED" in msg)

    def test_case_5_approved_missing_approver_rejection(self):
        """Negative Test 5: Approved status missing approved_by MUST BE REJECTED AS DIRTY DATA."""
        item = {
            "id": "TEST-005",
            "module": "hoinhap",
            "question": "Sample Question",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "status": "approved",
            "approved_by": None,  # Missing approver UUID
            "approved_at": "2026-08-13T10:00:00Z"
        }
        item["content_hash"] = compute_content_hash(item)
        valid, msg = validate_pull_item(item)
        self.assertFalse(valid, "Approved item missing approved_by MUST be rejected as dirty data!")
        self.assertTrue("DIRTY DATA REJECT" in msg)

    def test_case_6_legacy_status_warning_only(self):
        """Positive Test 6: Legacy item missing source_ref MUST ISSUE WARNING ONLY (NOT REJECT)."""
        item = {
            "id": "TEST-006",
            "module": "hoinhap",
            "question": "Sample Legacy Question",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "status": "legacy"
        }
        errors, warnings = validate_question_item(item, "TEST-006")
        self.assertEqual(len(errors), 0, "Legacy item MUST NOT produce hard errors for missing source_ref!")
        self.assertTrue(len(warnings) > 0, "Legacy item MUST issue backfill pending warning!")

if __name__ == "__main__":
    unittest.main()
