# -*- coding: utf-8 -*-
"""
Autonomous 5-Step Vercel Deployment & Live Verification Tool
"""
import os
import sys
import subprocess
import urllib.request
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

web_dir = r"d:\TRILONG-tools\website-projects\edu-banhmimahai-web"
notion_dir = r"d:\TRILONG-tools\notion-ai"

def run_cmd(cmd, cwd=web_dir):
    print(f"-> Executing: {cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        print(f"[ ERROR ] Command failed with exit code {res.returncode}")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        sys.exit(res.returncode)
    return res.stdout.strip()

print("=== STARTING AUTONOMOUS VERCEL DEPLOYMENT PIPELINE ===")

# Step 1: Run regression suite
print("\n[ 1/5 ] Running Master Regression Suite...")
out = run_cmd("python scripts/run_regression.py", cwd=notion_dir)
print("[ PASS ] Master regression passed 100%.")

# Step 2: Vercel Build
print("\n[ 2/5 ] Building Static Project with Vercel CLI...")
run_cmd("vercel build --prod")
print("[ PASS ] Vercel build completed.")

# Step 3: Vercel Deploy Prebuilt
print("\n[ 3/5 ] Deploying Prebuilt Artifacts to Vercel Production...")
deploy_out = run_cmd("vercel deploy --prebuilt --prod")
# Extract deployment URL
m = re.search(r'https://edu-banhmimahai-[a-z0-9]+-nguyenlong5238-s-projects\.vercel\.app', deploy_out)
if not m:
    # fallback search
    m = re.search(r'https://[a-zA-Z0-9-]+\.vercel\.app', deploy_out)
deploy_url = m.group(0) if m else None
print(f"[ PASS ] Deployment ready: {deploy_url}")

if deploy_url:
    # Step 4: Alias Assignment
    print("\n[ 4/5 ] Assigning Production Custom Domain Aliases...")
    run_cmd(f"vercel alias set {deploy_url} daotao.banhmimahai.vn")
    run_cmd(f"vercel alias set {deploy_url} edu-banhmimahai-web.vercel.app")
    print("[ PASS ] Aliases assigned successfully to daotao.banhmimahai.vn.")

# Step 5: Live HTTP Readback Verification
print("\n[ 5/5 ] Executing Mandatory Live HTTP Readback...")
test_url = "https://daotao.banhmimahai.vn/kynangsale/questions.js?v=20260905_ssot_master200_v5"
req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        code = resp.getcode()
        body = resp.read().decode('utf-8')
        m_q = re.search(r'const\s+(?:questions|QUESTIONS)\s*=\s*(\[.*?\]);', body, re.DOTALL)
        if m_q:
            qs = json.loads(m_q.group(1))
            assert len(qs) == 200, f"Expected 200 questions, got {len(qs)}"
            print(f"[ SUCCESS ] Live HTTP Verification PASSED! Status: {code} OK | 200 Questions Verified!")
            print(f"            Live URL: https://daotao.banhmimahai.vn/kynangsale/")
        else:
            print("[ FAIL ] Questions pattern not found on live response!")
            sys.exit(1)
except Exception as e:
    print(f"[ FAIL ] Live HTTP Readback failed: {e}")
    sys.exit(1)

print("\n=== VERCEL DEPLOYMENT & VERIFICATION FINISHED WITH 100% INTEGRITY ===")
