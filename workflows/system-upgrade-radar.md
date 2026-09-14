# Workflow: System Upgrade Radar & Global Tech Scanner (Slice 5)

Operational Release: `v7.0 — Autonomous Tech Radar & Threat Scanner`

## Workflow Pipeline Sequence

1. **Step 1 — Read Registered Sources**: Inspect `docs/radar-sources.md` to reference official security benchmarks (OWASP Agentic Top 10, NIST AI Agent Initiative, AGENTS.md format).
2. **Step 2 — Execute Local AST & Secret Scanner**: Run `python scripts/run_system_upgrade_radar.py`.
3. **Step 3 — Generate RFC Proposal**: Write proposals to `.staging/upgrade-radar/<date>/proposal.json` (Max 5 proposals, zero automatic code mutations).
4. **Step 4 — Human Review Gate**: Present RFC proposals to human reviewer. Require explicit human approval (`human_approval_granted = true`) before applying any upgrade.
