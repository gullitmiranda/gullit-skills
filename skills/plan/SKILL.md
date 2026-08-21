---
name: plan
description: Legacy compatibility entry point for local implementation planning. Use only when an existing prompt, configuration, or installed skill explicitly names `plan`.
---

# Plan Compatibility

`work-plan` is the public owner of implementation-plan authoring.

## Rules

- Follow the `work-plan` contract for new or revised implementation plans.
- Create workspace-standard plans in `.agents/plans/`, never as tracked notes.
- Treat `.cursor/plans/` as a legacy local input and do not migrate it implicitly.
- Do not preserve the retired tracked-plan lifecycle or promotion behavior.

Use `work-plan` for new planning work.
