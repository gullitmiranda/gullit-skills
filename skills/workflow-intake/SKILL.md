---
name: workflow-intake
description: Legacy compatibility entry point for work-intake. Use only when an existing prompt, configuration, or installed skill explicitly names `workflow-intake`.
---

# Workflow Intake Compatibility

`work-intake` is the single public owner of engineering-workflow discovery and routing.

## Rules

- Apply the `work-intake` contract and its artifact classification.
- Do not preserve the retired tracked-plan lifecycle or route through `engineering-workflow`.
- Do not mutate repository state during intake unless the user explicitly requests it.

Use `work-intake` for new routing work.
