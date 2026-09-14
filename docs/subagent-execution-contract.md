# Subagent Execution Contract (v7.0)

## Strict Read-Only Tool Allowlist
All spawned subagents are bound by a read-only capability model:
- Allowed Tools: `view_file`, `grep_search`, `search_web`, `read_url_content`.
- Disallowed Tools: `run_command`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, MCP write tools, `invoke_subagent`, `define_subagent`.

## Execution Rules
1. **Depth = 1 Enforced**: Subagents CANNOT spawn child subagents (`enable_subagent_tools: false`).
2. **Text Reporting**: Subagents report findings back to Parent Agent via text/JSON messages.
3. **Parent Staging Write Only**: Only the Parent Agent is authorized to write outputs into `.staging/<run_id>/`.
