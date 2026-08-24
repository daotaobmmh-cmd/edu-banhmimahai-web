#!/usr/bin/env python3
"""
content_hash_util.py — Deterministic Content Hash Utility for Edu-BanhMiMaHai OS
Computes SHA-256 hash using Unicode NFC normalization and \x1f separator.
"""

import unicodedata
import hashlib

def normalize_nfc_text(text):
    if not text:
        return ""
    return unicodedata.normalize("NFC", str(text)).strip()

def compute_content_hash(question_item):
    """
    Computes deterministic SHA-256 hash for (question + options[0..3] + correct_answer).
    question_item can be a dict or a question object.
    """
    q_text = question_item.get("question", "") if isinstance(question_item, dict) else getattr(question_item, "question", "")
    opts = question_item.get("options", []) if isinstance(question_item, dict) else getattr(question_item, "options", [])
    ans = question_item.get("correct_answer", "") if isinstance(question_item, dict) else getattr(question_item, "correct_answer", "")
    
    parts = [q_text] + list(opts) + [ans]
    norm_parts = [normalize_nfc_text(p) for p in parts]
    
    raw_payload = "\x1f".join(norm_parts).encode("utf-8")
    return hashlib.sha256(raw_payload).hexdigest()

if __name__ == "__main__":
    sample = {
        "question": "Vệ sinh 5S bao gồm những bước nào?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "A"
    }
    h = compute_content_hash(sample)
    print(f"Sample Content Hash: {h}")
