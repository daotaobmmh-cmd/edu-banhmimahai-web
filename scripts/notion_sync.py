#!/usr/bin/env python3
"""
notion_sync.py — Notion Sync CLI Adapter (Slice 2)
Supports --dry-run CLI mode printing DRY_RUN_READY without executing Notion mutations.
"""

import sys
import os
import json
import argparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    parser = argparse.ArgumentParser(description="Notion Sync CLI Adapter")
    parser.add_argument("--dry-run", action="store_true", help="Perform simulated dry-run inspection")
    args = parser.parse_args()

    if args.dry_run:
        print(json.dumps({
            "status": "DRY_RUN_READY",
            "message": "Notion sync dry-run adapter ready. Zero mutations performed on Notion.",
            "target_database_id": "c5e1f7052a064952947065655e3c468b"
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    print("Live Notion sync requires explicit human approval and NOTION_TOKEN in .env")

if __name__ == "__main__":
    main()
