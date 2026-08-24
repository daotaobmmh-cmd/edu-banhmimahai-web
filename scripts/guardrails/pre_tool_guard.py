#!/usr/bin/env python3
"""
pre_tool_guard.py — PreToolUse Fail-Closed Hook Guard for Edu-BanhMiMaHai OS (v7.0)
Canonicalizes Windows paths, enforces protected path policies, prevents traversal attacks,
and blocks unauthorized writes outside .staging/ in draft execution mode.
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROTECTED_CONFIG = os.path.join(BASE_DIR, "security", "guardrails", "protected-paths.json")

def load_protected_paths():
    if not os.path.exists(PROTECTED_CONFIG):
        return ["security/", ".agents/", "schemas/", "approvals/", "data/published/", "scripts/guardrails/", "AGENTS.md", "workflow-assurance/", "certifications/"]
    try:
        with open(PROTECTED_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("protected_paths", [])
    except Exception:
        return ["security/", ".agents/", "schemas/", "approvals/", "data/published/", "scripts/guardrails/", "AGENTS.md", "workflow-assurance/", "certifications/"]

def canonicalize_path(target_path):
    if not target_path:
        return ""
    # Resolve relative to BASE_DIR if not absolute
    if not os.path.isabs(target_path):
        target_path = os.path.join(BASE_DIR, target_path)
    
    # Realpath resolves symlinks, junctions, and relative '..' components
    try:
        real_path = os.path.realpath(target_path)
    except Exception:
        real_path = os.path.abspath(target_path)
        
    return real_path

def is_path_inside_workspace(canonical_target):
    canonical_base = os.path.realpath(BASE_DIR)
    # Check if target is equal to or subdirectory of BASE_DIR
    common = os.path.commonpath([canonical_base, canonical_target])
    return common.lower() == canonical_base.lower()

def evaluate_tool_call(tool_name, tool_args, mode="draft"):
    """
    Evaluates a tool call and returns a fail-closed decision dict:
    {"decision": "allow"|"deny", "reason": "..."}
    """
    write_tools = ["write_to_file", "replace_file_content", "multi_replace_file_content"]
    
    if tool_name not in write_tools:
        return {"decision": "allow", "reason": "Read-only or non-write tool permitted."}

    target_file = tool_args.get("TargetFile") or tool_args.get("target_file") or tool_args.get("file_path")
    if not target_file:
        return {"decision": "deny", "reason": "DENIED: Write tool call missing target file path."}

    canonical_target = canonicalize_path(target_file)

    # 1. Path Traversal & Escape Check
    if not is_path_inside_workspace(canonical_target):
        return {"decision": "deny", "reason": f"DENIED: Path '{target_file}' resolves outside of workspace boundary!"}

    # 2. Check Protected Paths
    protected_list = load_protected_paths()
    rel_target = os.path.relpath(canonical_target, os.path.realpath(BASE_DIR)).replace("\\", "/")
    
    for prot in protected_list:
        prot_clean = prot.rstrip("/")
        if rel_target.lower() == prot_clean.lower() or rel_target.lower().startswith(prot_clean.lower() + "/"):
            return {"decision": "deny", "reason": f"DENIED: Target path '{rel_target}' is a protected control-plane path ({prot})!"}

    # 3. Mode-Based Staging Enforcement
    if mode == "draft":
        if not rel_target.startswith(".staging/"):
            return {"decision": "deny", "reason": f"DENIED: Draft execution mode requires writes to be inside '.staging/'. Target path: '{rel_target}'."}

    return {"decision": "allow", "reason": f"Target path '{rel_target}' permitted for write in mode '{mode}'."}

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"decision": "deny", "reason": "Invalid command usage."}))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        tool_args = json.loads(sys.argv[2])
    except Exception as e:
        print(json.dumps({"decision": "deny", "reason": f"Failed to parse tool args: {str(e)}"}))
        sys.exit(1)

    mode = sys.argv[3] if len(sys.argv) > 3 else "draft"
    res = evaluate_tool_call(tool_name, tool_args, mode)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if res["decision"] != "allow":
        sys.exit(1)

if __name__ == "__main__":
    main()
