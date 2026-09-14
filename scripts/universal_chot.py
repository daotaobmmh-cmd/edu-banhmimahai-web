#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/universal_chot.py — Universal SOTA Checkpoint & Integrity Governance Engine

A portable, enterprise-grade GitOps & Quality Assurance engine for all Má Hải workspaces:
- Functional Regression Verification (Phase 1)
- Static Semantic & Secret Leak Integrity Audit (Phase 2)
- Whitelisted Git Snapshot Commit (Phase 3)
- Semantic Annotated Git Tagging (Phase 4)
- Instant Safe Rollback & Dry-Run Simulation

Usage:
  python scripts/universal_chot.py "Your custom commit description"
  python scripts/universal_chot.py --dry-run
  python scripts/universal_chot.py --rollback
"""

import os
import sys
import json
import subprocess
import datetime
import argparse

sys.stdout.reconfigure(encoding='utf-8')

CONFIG_FILE = "chot.config.json"

DEFAULT_CONFIG = {
    "project_name": "edu-banhmimahai-web",
    "project_code": "WEB",
    "tag_prefix": "checkpoint-WEB",
    "version_file": "package.json",
    "pipeline": {
        "phase_1_regression": {
            "command": "python scripts/run_regression.py",
            "required": True,
            "description": "Functional regression testing"
        },
        "phase_2_integrity_audit": {
            "command": "python scripts/audit_web_integrity.py",
            "required": True,
            "description": "Cross-rule conflict, mobile responsiveness, sales persona, brand token & secret audit"
        },
        "phase_3_git_snapshot": {
            "stage_whitelist": [
                "rules/", "workflows/", "scripts/", "data/", "tests/", "schemas/",
                "reports/", "docs/", "hoinhap/", "kynangsale/", "nhuongquyen/",
                "assets/", "images/", "config/", ".agents/", "AGENTS.md",
                "README.md", "package.json", "vercel.json", "chot.config.json", "index.html"
            ],
            "commit_convention": "CHOT({TAG}): {DESCRIPTION}"
        },
        "phase_4_checkpoint_tag": {
            "tag_format": "{PREFIX}-{NUMBER:02d}",
            "annotation_template": "Release Checkpoint {TAG} - {TIMESTAMP}"
        }
    }
}

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def load_config(repo_dir):
    cfg_path = os.path.join(repo_dir, CONFIG_FILE)
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Error loading {CONFIG_FILE}, falling back to defaults: {e}")
    return DEFAULT_CONFIG

def execute_rollback(repo_dir, target_tag=None):
    print("=== EXECUTING AUTOMATED ROLLBACK PROTOCOL ===")
    code, tags_out, _ = run_cmd("git tag -l \"checkpoint-*\"", cwd=repo_dir)
    tags = [t for t in tags_out.splitlines() if t.strip()]
    if not tags:
        print("[ FAIL ] No checkpoint tags found in this repository.")
        return 1

    if target_tag:
        chosen_tag = target_tag
    else:
        chosen_tag = tags[-1]

    print(f"--> Target Checkpoint: {chosen_tag}")
    print("--> Resetting HEAD and staging area safely (git reset --keep)...")
    code, out, err = run_cmd(f"git reset --keep {chosen_tag}", cwd=repo_dir)
    if code != 0:
        print(f"[ FAIL ] Rollback error: {err}")
        return 1
    print(f"[ SUCCESS ] Repository rolled back safely to: {chosen_tag}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Universal SOTA Checkpoint & Integrity Governance Engine (Má Hải OS)")
    parser.add_argument("description", nargs="?", default="", help="Custom commit/checkpoint description")
    parser.add_argument("--dry-run", action="store_true", help="Run Phase 1 & 2 preflight checks without committing/tagging")
    parser.add_argument("--rollback", nargs="?", const="LATEST", help="Rollback workspace to latest or specified checkpoint tag")
    args = parser.parse_args()

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if args.rollback:
        target = None if args.rollback == "LATEST" else args.rollback
        sys.exit(execute_rollback(repo_dir, target))

    config = load_config(repo_dir)
    pipeline = config.get("pipeline", {})

    print("================================================================================")
    print(f"   UNIVERSAL CHỐT ENGINE — SOTA GOVERNANCE PIPELINE ({config.get('project_name')})")
    print("================================================================================\n")

    # PHASE 1: FUNCTIONAL REGRESSION
    p1 = pipeline.get("phase_1_regression", {})
    p1_cmd = p1.get("command")
    if p1_cmd:
        print(f"[ 1/4 ] Verifying Quality Gates & Regression ({p1_cmd})...")
        code, out, err = run_cmd(p1_cmd, cwd=repo_dir)
        if code != 0:
            print("\n[ FAIL ] Phase 1 Regression Suite failed! Halting checkpoint.")
            print(out or err)
            sys.exit(1)
        print("[ PASS ] All functional tests passed 100% (Zero Failures).")
    else:
        print("[ 1/4 ] Phase 1 skipped (no command defined).")

    # PHASE 2: STATIC SEMANTIC & SECRET LEAK INTEGRITY AUDIT
    p2 = pipeline.get("phase_2_integrity_audit", {})
    p2_cmd = p2.get("command")
    if p2_cmd:
        print(f"\n[ 2/4 ] Running Deep System Integrity & Secret Leak Audit ({p2_cmd})...")
        code, out, err = run_cmd(p2_cmd, cwd=repo_dir)
        if code != 0:
            print("\n[ FAIL ] Phase 2 Integrity Audit detected conflicts/noise/leaks! Halting checkpoint.")
            print(out or err)
            sys.exit(1)
        print(out)
        print("[ PASS ] Zero system conflicts, leaks, or drift detected.")
    else:
        print("[ 2/4 ] Phase 2 skipped (no command defined).")

    if args.dry_run:
        print("\n================================================================================")
        print("  [ DRY-RUN SUCCESS ] All preflight gates passed. No commits or tags created.")
        print("================================================================================\n")
        sys.exit(0)

    # PHASE 3: GIT SNAPSHOT COMMIT
    p3 = pipeline.get("phase_3_git_snapshot", {})
    whitelist = p3.get("stage_whitelist", [])
    commit_convention = p3.get("commit_convention", "CHOT({TAG}): {DESCRIPTION}")

    # Determine next tag number
    tag_prefix = config.get("tag_prefix", "checkpoint-WEB")
    code, tags_out, _ = run_cmd(f'git tag -l "{tag_prefix}-*"', cwd=repo_dir)
    existing_tags = [t for t in tags_out.splitlines() if t.strip()]
    next_num = len(existing_tags) + 1
    tag_name = f"{tag_prefix}-{next_num:02d}"

    desc = args.description.strip() if args.description.strip() else f"Universal Checkpoint release {tag_name}"
    commit_msg = commit_convention.replace("{TAG}", tag_name).replace("{DESCRIPTION}", desc)

    print(f"\n[ 3/4 ] Staging Whitelist & Creating Git Snapshot Commit...")
    # Only stage paths that actually exist
    existing_paths = [p for p in whitelist if os.path.exists(os.path.join(repo_dir, p))]
    stage_str = ' '.join(f'"{p}"' for p in existing_paths)
    run_cmd(f"git add {stage_str}", cwd=repo_dir)
    code, out, err = run_cmd(f'git commit -m "{commit_msg}"', cwd=repo_dir)
    if code != 0 and "nothing to commit" not in out.lower():
        print(f"[ WARN ] Git commit message: {out or err}")

    # PHASE 4: ANNOTATED CHECKPOINT TAGGING
    print(f"\n[ 4/4 ] Tagging Checkpoint '{tag_name}'...")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_cmd(f'git tag -a "{tag_name}" -m "Release Checkpoint {tag_name} - {now_str}"', cwd=repo_dir)

    code, commit_hash, _ = run_cmd("git rev-parse --short HEAD", cwd=repo_dir)
    print("\n================================================================================")
    print(f"[ SUCCESS ] Universal Checkpoint created successfully!")
    print(f"            Project : {config.get('project_name')}")
    print(f"            Tag     : {tag_name}")
    print(f"            Commit  : {commit_hash}")
    print(f"            Message : {commit_msg}")
    print("================================================================================\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
