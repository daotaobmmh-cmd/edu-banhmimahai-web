# Global Safety Rules — Edu-BanhMiMaHai OS (v7.0)

## Dual-Axis Risk Matrix
- **`R0` (Cosmetic)**: Typo, comments, whitespace ➔ Fast Path + log.
- **`R1` (Functional)**: Layout, routing, component logic ➔ DEEP Mode + diff review.
- **`R2` (Data / Security)**: Question answers, schema, credentials, approval, publish ➔ DEEP Mode + RFC + Human Approval.
- **`P0` (Critical / Outage)**: Production failure, active security vulnerability ➔ Emergency fix.

## Security Controls
- **Protected Paths**: Files in `security/`, `.agents/`, `schemas/`, `approvals/`, and `data/published/` are R2 control-plane paths. Agent cannot modify without human R2 approval.
- **No Unapproved Live Production Deploy**: Execution of `git push` or production deploys is STRICTLY BLOCKED (`ERR_LIVE_DEPLOY_DISABLED`).
