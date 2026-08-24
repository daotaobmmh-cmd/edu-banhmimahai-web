#!/usr/bin/env python3
"""
cleanup_staging.py — Staging Directory Cleanup Utility for Edu-BanhMiMaHai OS
Purges files in .staging/ older than 7 days.
"""

import sys
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(BASE_DIR, ".staging")

def cleanup_staging(max_days=7):
    if not os.path.exists(STAGING_DIR):
        return {"status": "skipped", "message": ".staging directory does not exist"}
        
    now = time.time()
    cutoff = now - (max_days * 86400)
    removed_files = []

    for filename in os.listdir(STAGING_DIR):
        if filename == ".gitignore":
            continue
            
        file_path = os.path.join(STAGING_DIR, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                os.remove(file_path)
                removed_files.append(filename)

    return {
        "status": "passed",
        "total_removed": len(removed_files),
        "removed_files": removed_files
    }

def main():
    res = cleanup_staging()
    print(res)

if __name__ == "__main__":
    main()
