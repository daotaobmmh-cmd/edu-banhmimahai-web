#!/usr/bin/env python3
"""
compare_html_delta.py — HTML Delta & Structural Inspector for Edu-BanhMiMaHai OS
Inspects HTML files for syntax errors, missing closing tags, or missing essential element IDs.
"""

import sys
import os
import re
import json

def inspect_html_file(file_path, required_ids=None):
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Check basic HTML structure
    if not re.search(r'<!DOCTYPE\s+html>', content, re.IGNORECASE) and not re.search(r'<html', content, re.IGNORECASE):
        errors.append("Missing <!DOCTYPE html> or <html> tag.")

    # Check matching tags basic count
    open_divs = len(re.findall(r'<div[\s>]', content, re.IGNORECASE))
    close_divs = len(re.findall(r'</div>', content, re.IGNORECASE))
    if open_divs != close_divs:
        errors.append(f"Unmatched <div> tags count: open={open_divs}, close={close_divs}")

    # Check required element IDs if specified
    if required_ids:
        for req_id in required_ids:
            if not re.search(rf'id=["\']{re.escape(req_id)}["\']', content):
                errors.append(f"Missing required element ID: '{req_id}'")

    status = "passed" if len(errors) == 0 else "failed"
    return {
        "status": status,
        "file_path": file_path,
        "errors": errors
    }

def main():
    target_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "index.html")
    result = inspect_html_file(target_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "passed":
        sys.exit(1)

if __name__ == "__main__":
    main()
