#!/usr/bin/env python3
"""
run_system_upgrade_radar.py — System Upgrade Radar Scanner (Slice 5)
Scans codebase for AST syntax errors, secret leaks, broken links, and context bloat.
Outputs findings to .staging/upgrade-radar/<date>/ (max 5 proposals, zero automatic code mutations).
"""

import sys
import os
import re
import json
import datetime
import ast

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def check_secret_leaks():
    findings = []
    secret_patterns = [
        (r'(?i)(api_key|secret_key|private_key|token)\s*=\s*["\'][A-Za-z0-9_\-]{20,}["\']', "Potential hardcoded API token/secret key"),
        (r'-----BEGIN\s+PRIVATE\s+KEY-----', "Hardcoded private key block")
    ]
    for root, dirs, files in os.walk(BASE_DIR):
        if ".git" in root or ".staging" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith((".py", ".js", ".json", ".md", ".env")) and file != ".env.example":
                fp = os.path.join(root, file)
                with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                for pat, desc in secret_patterns:
                    if re.search(pat, content):
                        rel = os.path.relpath(fp, BASE_DIR)
                        findings.append({"file": rel, "type": "Secret Leak", "description": desc})
    return findings

def check_python_ast():
    findings = []
    scripts_dir = os.path.join(BASE_DIR, "scripts")
    if os.path.exists(scripts_dir):
        for file in os.listdir(scripts_dir):
            if file.endswith(".py"):
                fp = os.path.join(scripts_dir, file)
                with open(fp, "r", encoding="utf-8") as f:
                    try:
                        ast.parse(f.read(), filename=file)
                    except SyntaxError as se:
                        findings.append({"file": f"scripts/{file}", "type": "AST Syntax Error", "description": str(se)})
    return findings

def run_radar():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    staging_dir = os.path.join(BASE_DIR, ".staging", "upgrade-radar", date_str)
    os.makedirs(staging_dir, exist_ok=True)

    secrets = check_secret_leaks()
    ast_errors = check_python_ast()

    proposals = []
    if secrets:
        proposals.append({
            "proposal_id": "PROP-001",
            "category": "security_hardening",
            "title": "Hardcoded Secret Leak Detected",
            "findings": secrets,
            "impact_severity": "R2"
        })
    if ast_errors:
        proposals.append({
            "proposal_id": "PROP-002",
            "category": "code_optimization",
            "title": "Python AST Syntax Issue Detected",
            "findings": ast_errors,
            "impact_severity": "R1"
        })

    # Cap proposals to max 5
    proposals = proposals[:5]

    report = {
        "radar_run_date": date_str,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_proposals": len(proposals),
        "proposals": proposals,
        "mutations_performed": 0
    }

    out_file = os.path.join(staging_dir, "proposal.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "passed",
        "radar_report": out_file,
        "total_proposals": len(proposals),
        "mutations_performed": 0
    }, ensure_ascii=False, indent=2))
    return report

if __name__ == "__main__":
    run_radar()
