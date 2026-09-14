# Runbook: Release Procedure (v7.0)

## Release Execution Steps

1. **Clean Baseline Check**: Verify `git status` is clean or changes are tracked in `.staging/`.
2. **Execute Question Inventory**: Run `python scripts/inventory_questions.py` and confirm zero duplicate IDs.
3. **Execute PreToolUse Guard Unit Tests**: Run `python -m unittest tests/guardrails/test_pre_tool_guard.py`.
4. **Execute Master Regression Test Suite**: Run `python scripts/run_regression.py` and verify `overall_status == "passed"`.
5. **Verify Approval Record**: Run `python scripts/verify_approval.py <approval_id> <candidate_hash>`.
6. **Publish Approved Artifact**: Run `python scripts/publish_approved.py` to generate `data/published/approved-published.json`.
7. **Production Cutover**: Point frontend application exclusively to `data/published/approved-published.json` and `data/legacy/legacy-published.json`.
