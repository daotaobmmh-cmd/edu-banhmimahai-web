#!/usr/bin/env python3
"""
test_html_integrity.py — Unit test for static HTML file inspection
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from compare_html_delta import inspect_html_file

class TestHTMLIntegrity(unittest.TestCase):

    def test_root_index_html(self):
        index_file = os.path.join(BASE_DIR, "index.html")
        if os.path.exists(index_file):
            res = inspect_html_file(index_file)
            self.assertEqual(res["status"], "passed", f"HTML errors: {res.get('errors')}")

    def test_hoinhap_index_html(self):
        hoinhap_file = os.path.join(BASE_DIR, "hoinhap", "index.html")
        if os.path.exists(hoinhap_file):
            res = inspect_html_file(hoinhap_file)
            self.assertEqual(res["status"], "passed", f"HTML errors: {res.get('errors')}")

if __name__ == "__main__":
    unittest.main()
