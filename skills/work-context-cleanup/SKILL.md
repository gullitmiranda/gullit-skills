---
name: work-context-cleanup
description: Legacy compatibility entry point for work-closeout. Use only when an existing prompt, configuration, or installed skill explicitly names `work-context-cleanup`.
---

# Work Context Cleanup Compatibility

`work-closeout` is the public owner of plan and work-context closeout.

## Rules

- Apply the `work-closeout` classification and confirmation requirements.
- Do not archive through `plan-archive`, delete plans, or mutate related repository state without explicit user intent.
- Treat local plans as ignored artifacts and legacy plan paths as compatibility input only.

Use `work-closeout` for new closeout work.
