---
name: workflow
description: Retired compatibility entry point for broad workflow rules. Use only when an existing prompt, configuration, or installed skill explicitly names `workflow`.
---

# Workflow Compatibility

This broad router is retired. Its rules belong to topical owners.

## Rules

- Use `work-intake` for workflow discovery and routing.
- Use `agent-workspace` and `work-plan` for artifact rules.
- Use `safety`, `git`, `quality`, `user-preferences`, and `zeropath` for their respective guardrails.
- Do not use this compatibility entry point to create a new workflow policy layer.
