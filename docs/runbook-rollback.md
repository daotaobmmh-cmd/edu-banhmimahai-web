# Runbook: Rollback Procedure (v7.0)

## Rollback Execution Steps

1. **Detect Outage / Integrity Anomaly**: If a published question or layout defect is detected post-release, initiate emergency rollback.
2. **Revert Published Artifact**: Restore `data/published/approved-published.json` to the previous immutable git commit baseline using `git checkout <previous_commit> -- data/published/approved-published.json`.
3. **Revert Legacy Artifact**: Confirm `data/legacy/legacy-published.json` matches SHA-256 hash recorded in `data/legacy/legacy-manifest.json`.
4. **Log Incident Evidence Pack**: Save raw failure logs, error tracebacks, and git diff into `.staging/incidents/<date>-rollback/manifest.json`.
5. **Execute Verification**: Run `python scripts/run_regression.py` to confirm system stability post-rollback.
