# Workflow Specification: `workflow-assurance-gate` — "QA của QA"

Slash Command: `/certify-workflow`  
Operational Release: `v7.0 — Slice 0B Root Assurance Control`

## 1. Core Principles & Governance
1. **No Self-Certification**: Workflow Assurance Gate NEVER certifies itself. Root of trust is immutable and external (`workflow-assurance/schemas/`, static validators, evidence verifier, human approver).
2. **Deterministic Evidence Verification**: Raw tool outputs, exit codes, and before/after state diffs are evaluated independently from target workflow reports.
3. **Fail-Closed Gate Evaluation**: If any hard gate (Gate A through Gate G) fails, verdict is `REJECTED` or `BLOCKED`. Zero false PASS allowed.

## 2. Gate Pipeline Execution Sequence

- **Step 1 — Static Contract Linting (Gate A)**: Run `python workflow-assurance/scripts/lint_contract.py <candidate_manifest.json>`.
- **Step 2 — Permission Minimization & Risk Classifier (Gate B)**: Run `python workflow-assurance/scripts/audit_permissions.py <candidate_manifest.json>`.
- **Step 3 — Build Dependency Closure**: Run `python workflow-assurance/scripts/build_dependency_closure.py <candidate_dir>`.
- **Step 4 — Dynamic Sandbox Assessment (Gates C-F)**: Run `python workflow-assurance/scripts/run_assessment.py <candidate_manifest.json>`.
- **Step 5 — Independent Evidence Verification (Gate F)**: Run `python workflow-assurance/scripts/verify_evidence.py <evidence_manifest.json>`.
- **Step 6 — Human Review & Approval Hash Gate (Gate G)**: Require explicit human approval matching exact candidate SHA-256 hash.
- **Step 7 — Atomic Promotion**: Run `python workflow-assurance/scripts/promote_workflow.py <candidate_markdown_path> <certificate_path>`.
