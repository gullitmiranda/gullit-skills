---
name: project-path-migration
description: Legacy compatibility entry point for cursor-project-path-migration. Use only when an existing prompt, configuration, or installed skill explicitly names `project-path-migration`.
---

# Project Path Migration Compatibility

`cursor-project-path-migration` is the public owner of Cursor-specific project path migrations.

## Rules

- Apply the `cursor-project-path-migration` backup, verification, and rollback contract.
- Treat `.agents/plans/` as local plans and `.agents/notes/` as tracked knowledge.
- Mention `.cursor/plans/` only when an explicit compatibility symlink exists.

Use `cursor-project-path-migration` for new work.
