---
name: cursor-project-path-migration
description: Move or rename a project path while preserving Cursor workspace state, chats, and local agent artifacts. Use when a Cursor project must change location without losing recoverable context.
---

# Cursor Project Path Migration

Preserve Cursor's path-keyed state through a reversible project move.

## Hard Rules

- Cursor workspace state under `~/.cursor/projects/` is path-derived; never assume it follows a project move automatically.
- Back up relevant Cursor state and uncommitted local agent artifacts before moving anything.
- Repository plans are local under `.agents/plans/`; notes are tracked under `.agents/notes/`. Mention `.cursor/plans/` only when an explicit compatibility symlink exists.
- Do not delete the old path, old state, or backups until verification completes and the user confirms cleanup.

## Procedure

1. Inspect the current and destination paths, repository state, local plans or notes, and candidate Cursor workspace directories.
2. Create a reversible backup of the matching Cursor state and any uncommitted local agent artifacts. Prefer a full backup when the matching workspace directory is uncertain.
3. Move the project and create a symlink from the old path when preserving Cursor history matters. Open the old path through the symlink first.
4. Verify conversations, plans, and workspace behavior in Cursor. Report risk, backups, verification evidence, rollback path, and any cleanup that still requires confirmation.

## Decision guide

Prefer move plus symlink for continuity, copy plus verification for maximum reversibility, and a move without symlink only when the user accepts Cursor treating the project as new.
