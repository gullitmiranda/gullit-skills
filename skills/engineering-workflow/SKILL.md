---
name: engineering-workflow
description: Legacy compatibility entry point for work-intake. Use only when an existing prompt, configuration, or installed skill explicitly names `engineering-workflow`.
---

# Engineering Workflow Compatibility

`work-intake` is the single public owner of engineering-workflow discovery and routing.

## Rules

- Apply the `work-intake` core route without requiring third-party skills.
- Use `agent-selection` and `context-capsule` when their boundaries apply.
- Do not create a competing router or mutate repository state solely because this compatibility entry point loaded.

Use `work-intake` for new workflow-routing work.
