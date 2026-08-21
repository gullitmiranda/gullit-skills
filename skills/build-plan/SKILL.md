---
name: build-plan
description: Legacy compatibility entry point for build. Use only when an existing prompt, configuration, or installed skill explicitly names `build-plan`.
---

# Build Plan Compatibility

`build` is the public owner of ready local implementation-plan execution.

## Rules

- Apply the `build` contract and classify the source before implementation.
- Do not assign a tracked lifecycle to a local plan or move it without clear user intent.
- Route unresolved product, scope, or architecture decisions to `work-plan` or the user.

Use `build` for new execution work.
