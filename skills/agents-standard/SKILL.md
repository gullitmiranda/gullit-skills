---
name: agents-standard
description: Legacy compatibility entry point for the agent-workspace contract. Use only when an existing prompt, configuration, or installed skill explicitly names `agents-standard`.
---

# Agents Standard Compatibility

`agent-workspace` is the public owner of the workspace model.

## Rules

- Apply the `agent-workspace` contract rather than the retired tracked-plan lifecycle.
- Treat `.agents/plans/` as ignored local implementation plans and `.agents/notes/` as tracked lifecycle knowledge.
- Treat `.cursor/plans/` as an explicit-migration compatibility input only.
- Do not create, promote, or edit artifacts just because this compatibility entry point loaded.

Use `agent-workspace` for new setup, migration, or workspace-policy work.
