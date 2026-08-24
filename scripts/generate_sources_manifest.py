#!/usr/bin/env python3
"""
generate_sources_manifest.py — Tamper-Evident SHA-256 Manifest Generator for Edu-BanhMiMaHai OS
Computes and locks SHA-256 hashes of all files in sources/ into sources/MANIFEST.sha256.
"""

import sys
import os
import hashlib
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
MANIFEST_PATH = os.path.join(SOURCES_DIR, "MANIFEST.sha256")

def generate_manifest():
    if not os.path.exists(SOURCES_DIR):
        print("ERROR: sources directory does not exist.")
        sys.exit(1)

    manifest = {}
    for filename in sorted(os.listdir(SOURCES_DIR)):
        if filename == "MANIFEST.sha256":
            continue
            
        file_path = os.path.join(SOURCES_DIR, filename)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
            manifest[filename] = file_hash

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "passed",
        "manifest_path": MANIFEST_PATH,
        "total_locked_files": len(manifest),
        "manifest": manifest
    }, ensure_ascii=False, indent=2))
    return manifest

if __name__ == "__main__":
    generate_manifest()
