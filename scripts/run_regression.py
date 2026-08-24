#!/usr/bin/env python3
"""
run_regression.py — Master Regression Test Suite for Edu-BanhMiMaHai OS
Runs all project validators, HTML checks, question bank validation, and outputs reports/regression-latest.json.
"""

import sys
import os
import json
import datetime
import subprocess

# Ensure scripts directory is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from validate_questions import validate_markdown_file
from check_duplicate_questions import check_duplicates
from compare_html_delta import inspect_html_file

def run_regression_suite():
    results = []
    overall_status = "passed"

    # Test 1: Validate Question Bank (danh_sach_cau_hoi_hoinhap.md)
    q_file = os.path.join(BASE_DIR, "danh_sach_cau_hoi_hoinhap.md")
    if os.path.exists(q_file):
        res1 = validate_markdown_file(q_file)
        test1 = {
            "name": "Validate Question Bank Syntax",
            "target": "danh_sach_cau_hoi_hoinhap.md",
            "status": res1["status"],
            "parsed_questions": res1.get("total_questions_parsed", 0),
            "errors": res1.get("errors", [])
        }
        if res1["status"] != "passed":
            overall_status = "failed"
        results.append(test1)

        # Test 2: Check Duplicate Questions
        res2 = check_duplicates(q_file)
        test2 = {
            "name": "Check Duplicate Questions",
            "target": "danh_sach_cau_hoi_hoinhap.md",
            "status": res2["status"],
            "unique_codes": res2.get("total_unique_codes", 0),
            "duplicates": res2.get("duplicates", [])
        }
        if res2["status"] != "passed":
            overall_status = "failed"
        results.append(test2)
    else:
        results.append({
            "name": "Question Bank Existence Check",
            "status": "failed",
            "errors": ["danh_sach_cau_hoi_hoinhap.md not found"]
        })
        overall_status = "failed"

    # Test 3: HTML Structure Inspection (index.html)
    index_html = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_html):
        res3 = inspect_html_file(index_html)
        test3 = {
            "name": "Inspect Root Index HTML",
            "target": "index.html",
            "status": res3["status"],
            "errors": res3.get("errors", [])
        }
        if res3["status"] != "passed":
            overall_status = "failed"
        results.append(test3)

    # Test 4: Inspect /hoinhap/ index.html if exists
    hoinhap_html = os.path.join(BASE_DIR, "hoinhap", "index.html")
    if os.path.exists(hoinhap_html):
        res4 = inspect_html_file(hoinhap_html)
        test4 = {
            "name": "Inspect HoiNhap Index HTML",
            "target": "hoinhap/index.html",
            "status": res4["status"],
            "errors": res4.get("errors", [])
        }
        if res4["status"] != "passed":
            overall_status = "failed"
        results.append(test4)

    # Build report output
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_status": overall_status,
        "total_tests": len(results),
        "passed_tests": sum(1 for r in results if r["status"] == "passed"),
        "failed_tests": sum(1 for r in results if r["status"] != "passed"),
        "details": results
    }

    # Save to reports/regression-latest.json
    reports_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, "regression-latest.json")
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report

def main():
    report = run_regression_suite()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["overall_status"] != "passed":
        sys.exit(1)

if __name__ == "__main__":
    main()
