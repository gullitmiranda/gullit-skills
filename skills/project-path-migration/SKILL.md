---
name: project-path-migration
description: Safely migrate or rename a project path while preserving Cursor workspace state, chats, plans, and local metadata. Use when the user asks to move or rename a project, change a workspace path, reorganize folders, or preserve Cursor history tied to ~/.cursor/projects.
---

# Project Path Migration

## Hard Rules

- `~/.cursor/projects/` is local workspace state keyed by path-derived identifiers. Never assume Cursor remaps old state to a new path automatically.
- Repo files (`.cursor/plans/`, `.cursor/skills/`, notes) survive path moves; local Cursor state outside the repo does not.
- Never delete the old project path or old Cursor state until verification is complete. Prefer reversible steps.
- Do not recommend destructive cleanup as part of the first pass.

## Workflow

### 1. Inspect

Identify current path, destination path, whether the project is a git repo, whether important plans/notes exist in the repo, and which directories in `~/.cursor/projects/` correspond to the project. Do not rely on naming alone if multiple matches exist — prefer recent modification time and contents that mention the current project path.

### 2. Back Up Cursor State

Back up before any move or rename. Layout:

- project-specific: `~/.cursor-backups/projects/<project-name>/<timestamp>/` (default)
- full: `~/.cursor-backups/projects/_full/<timestamp>/` — use when the matching workspace dir is uncertain, when reorganizing multiple projects, or when the user prefers maximum safety

```bash
backup_dir="$HOME/.cursor-backups/projects/_full/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
tar -czf "$backup_dir/cursor-projects.tgz" "$HOME/.cursor/projects"
```

Narrower, when the workspace dir is known:

```bash
backup_dir="$HOME/.cursor-backups/projects/<project-name>/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
tar -czf "$backup_dir/project-workspace.tgz" "$HOME/.cursor/projects/<workspace-dir>"
```

### 3. Back Up Uncommitted Project Files

If important plans or notes exist only in the working tree, copy them before moving:

```bash
backup_dir="$HOME/.cursor-backups/projects/<project-name>/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
cp -R "/path/to/project/.cursor" "$backup_dir/repo-cursor-dir"
```

### 4. Move + Symlink (default when preserving Cursor history matters)

```bash
mv "/old/project/path" "/new/project/path"
ln -s "/new/project/path" "/old/project/path"
```

Open the old path first through the symlink and verify Cursor still surfaces the expected history. The symlink preserves a path-shaped compatibility layer and keeps rollback simple.

### 5. Verify Before Cleanup

Open the project in Cursor; confirm plans, conversations, and local history are present and the workspace behaves normally. If history appears missing: stop, keep the symlink and backups intact, inspect whether Cursor created a new workspace directory for the new path, and restore from backup only if necessary.

### 6. Cleanup Only After Confirmation

Only after the user confirms the new setup is stable: optionally remove the symlink, archive old backups, remove obsolete workspace state.

## Decision Guide

1. `move + symlink` — default when preserving local Cursor history matters.
2. `copy + verify + switch later` — even safer, easy rollback.
3. `move without symlink` — only when the user accepts the risk of Cursor treating it as a new workspace.
