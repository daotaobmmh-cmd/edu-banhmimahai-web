#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/audit_web_integrity.py — Deep Web Integrity, Brand, Responsive & Security Audit Engine

Audits edu-banhmimahai-web workspace:
1. Cross-Rule Conflict & Hierarchy Check (node scripts/lint_rules_conflict.mjs)
2. Question Bank Sanity & 4-Option Distribution Parity (python scripts/validate_kynangsale.py)
3. Secret Leakage & Staging Cleanliness (.env, Vercel tokens, API keys)
4. Mobile-First Viewport & Meta Tags Assertion (index.html, hoinhap/, kynangsale/)
5. Brand SSOT & Internal Nomenclature Audit (Má Hải, University)

Usage:
  python scripts/audit_web_integrity.py
"""

import os
import sys
import json
import re
import subprocess
import datetime

sys.stdout.reconfigure(encoding='utf-8')

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def load_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def run_web_integrity_audit(repo_dir=None, verbose=True):
    if repo_dir is None:
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    passed_checks = []
    findings = []

    def record_pass(category, desc):
        passed_checks.append({"category": category, "description": desc, "status": "PASSED"})
        if verbose:
            print(f"  [ PASS ] [{category}] {desc}")

    def record_fail(category, desc, details=None):
        finding = {"category": category, "description": desc, "details": details, "status": "FAILED"}
        findings.append(finding)
        if verbose:
            print(f"  [ FAIL ] [{category}] {desc}")
            if details:
                print(f"           --> Details: {details}")

    if verbose:
        print("================================================================================")
        print("   AUTOMATED DEEP WEB INTEGRITY & BRAND GOVERNANCE ENGINE (EDU MÁ HẢI)         ")
        print("================================================================================\n")

    # 1. CROSS-RULE CONFLICT & HIERARCHY CHECK
    if verbose:
        print("--- [Audit 1/5] Cross-Rule Conflict & Authority Hierarchy Gate ---")
    conflict_script = os.path.join(repo_dir, "scripts", "lint_rules_conflict.mjs")
    if os.path.exists(conflict_script):
        code, out, err = run_cmd("node scripts/lint_rules_conflict.mjs", cwd=repo_dir)
        if code == 0:
            record_pass("RULES", "Cross-Rule Conflict Linter verified (CRCM clean, 0 conflicts)")
        else:
            record_fail("RULES", "lint_rules_conflict.mjs detected rule conflicts", out or err)
    else:
        record_fail("RULES", "scripts/lint_rules_conflict.mjs missing")

    # 2. QUESTION BANK SANITY & ANSWER BALANCE (200 QUESTIONS)
    if verbose:
        print("\n--- [Audit 2/5] Sales Question Bank Sanity & 50-50-50-50 Answer Distribution ---")
    kns_validator = os.path.join(repo_dir, "scripts", "validate_kynangsale.py")
    if os.path.exists(kns_validator):
        code, out, err = run_cmd("python scripts/validate_kynangsale.py", cwd=repo_dir)
        if code == 0 and "PASSED PERFECTLY" in out:
            record_pass("EXAM_SANITY", "200 Kỹ năng sale questions pass 50-50-50-50 balanced distribution")
        else:
            record_fail("EXAM_SANITY", "validate_kynangsale.py check failed", out or err)
    else:
        record_pass("EXAM_SANITY", "validate_kynangsale.py not present, skipping")

    # 3. SECRET LEAKAGE & REPO CLEANLINESS
    if verbose:
        print("\n--- [Audit 3/5] Secret Leakage & Staging Cleanliness Gate ---")
    code, tracked_env, _ = run_cmd("git ls-files .env* **/.env*", cwd=repo_dir)
    if tracked_env.strip():
        record_fail("SECURITY", f"Credential file tracked in git index: {tracked_env.strip()}")
    else:
        record_pass("SECURITY", "Zero .env credential files tracked in git index")

    # Scan for Vercel token or exposed API secrets
    secret_patterns = [
        (r"\bvercel_[a-zA-Z0-9]{20,}\b", "Vercel Deployment Token"),
        (r"\bsk-[a-zA-Z0-9]{25,}\b", "OpenAI API Key"),
        (r"\bntn_[a-zA-Z0-9]{25,}\b", "Notion Token")
    ]
    code_dirs = ["scripts", "src", "api"]
    leak_found = False
    for cd in code_dirs:
        full_cd = os.path.join(repo_dir, cd)
        if not os.path.exists(full_cd):
            continue
        for root, _, files in os.walk(full_cd):
            for fname in files:
                if fname.endswith((".py", ".js", ".mjs", ".ts", ".html")):
                    fpath = os.path.join(root, fname)
                    content = load_file(fpath)
                    if not content:
                        continue
                    for pat, label in secret_patterns:
                        if re.search(pat, content):
                            rel_p = os.path.relpath(fpath, repo_dir).replace("\\", "/")
                            record_fail("SECURITY", f"Secret leak in {rel_p}: {label}")
                            leak_found = True
                            break
    if not leak_found:
        record_pass("SECURITY", "Zero exposed API keys/tokens detected in web scripts and source code")

    # 4. MOBILE-FIRST VIEWPORT & META TAGS ASSERTION
    if verbose:
        print("\n--- [Audit 4/5] Mobile-First Viewport & Web Standards Gate ---")
    html_targets = ["index.html", "hoinhap/index.html", "kynangsale/index.html"]
    viewport_clean = True
    for ht in html_targets:
        full_ht = os.path.join(repo_dir, ht)
        if os.path.exists(full_ht):
            html_text = load_file(full_ht)
            if 'name="viewport"' in html_text and 'width=device-width' in html_text:
                record_pass("MOBILE_FIRST", f"{ht} has valid mobile-first viewport meta tag")
            else:
                record_fail("MOBILE_FIRST", f"{ht} missing standard responsive viewport meta tag")
                viewport_clean = False
    if viewport_clean:
        record_pass("MOBILE_FIRST", "All critical web entrypoints enforce mobile-first responsive viewport")

    # 5. BRAND SSOT & NOMENCLATURE PARITY
    if verbose:
        print("\n--- [Audit 5/5] Brand SSOT & Enterprise Nomenclature Gate ---")
    index_content = load_file(os.path.join(repo_dir, "index.html"))
    if index_content and ("Bánh Mì Má Hải" in index_content or "Má Hải" in index_content):
        record_pass("BRAND_SSOT", "Root portal prominently reflects official brand 'Bánh Mì Má Hải'")
    else:
        record_fail("BRAND_SSOT", "index.html missing official Má Hải brand identity")

    total_checks = len(passed_checks) + len(findings)
    status = "PASSED" if len(findings) == 0 else "FAILED"

    if verbose:
        print("\n================================================================================")
        print(f"  WEB INTEGRITY AUDIT SUMMARY: {status}")
        print(f"  Total Checks Passed : {len(passed_checks)} / {total_checks}")
        print(f"  Total Issues Found  : {len(findings)}")
        print("================================================================================\n")

    return 0 if status == "PASSED" else 1

if __name__ == "__main__":
    code = run_web_integrity_audit()
    sys.exit(code)
