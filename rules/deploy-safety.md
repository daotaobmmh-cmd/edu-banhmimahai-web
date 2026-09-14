# Deployment Safety Rules — Edu-BanhMiMaHai OS

## 1. Hosting Architecture Overview
- **Production Host**: Cloudflare Pages / Static Hosting
- **Production Route**: `/hoinhap/` (Redirected from root `index.html`)
- **Local Testing Command**: `python -m http.server 8000` -> `http://localhost:8000/hoinhap/`

## 2. Hard Deployment Safety Rules
- **No Direct Push**: `git push` to remote `main` / `master` is strictly forbidden without prior review.
- **Local Verification Checklist**:
  1. HTML syntax check passes.
  2. `python scripts/run_regression.py` passes 100%.
  3. Local HTTP server verified at `http://localhost:8000/hoinhap/`.
  4. Human approval granted (`human_approval_granted = true`).

## 3. Controlled Deployment Gate
- Deployment MUST be executed using `workflows/controlled-deploy.md`.
- Every deployment action creates a timestamped log entry in `logs/deploy-{timestamp}.json`.
