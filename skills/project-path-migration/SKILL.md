---
name: project-path-migration
description: Safely migrate or rename a project path while preserving Cursor workspace state, chats, plans, and local metadata. Use when the user asks to move or rename a project, change a workspace path, reorganize folders, or preserve Cursor history tied to ~/.cursor/projects.
---

# Project Path Migration

## Quick Start

Use this skill when a project may be moved or renamed and the user wants to keep Cursor context.

Default safe approach:

1. Inspect the current project path and relevant state under `~/.cursor/projects/`.
2. Back up any matching Cursor workspace directories before changing paths.
3. Ensure important repo-backed files such as `.cursor/plans/` are present and, if needed, committed or copied.
4. Prefer moving the project and leaving a symlink at the old path first.
5. Reopen the project in Cursor and verify chats, plans, and other local state before deleting anything.

## Core Rules

- Treat `~/.cursor/projects/` as local workspace state that may be keyed by path-derived identifiers.
- Treat files inside the repository, such as `.cursor/plans/*.plan.md`, as normal project files that survive path moves.
- Never assume Cursor will automatically remap old workspace state to a new path.
- Never delete the old project path or old Cursor state until verification is complete.
- Prefer reversible steps over one-shot moves.

## What To Preserve

Check both categories:

- Repository-backed state:
  - `.cursor/plans/`
  - `.cursor/skills/`
  - any markdown notes or config files inside the repo
- Local Cursor state outside the repo:
  - matching directories in `~/.cursor/projects/`
  - related terminal state
  - local transcripts, caches, and workspace metadata

## Workflow

### 1. Inspect

Identify:

- current project path
- destination path
- whether the project is a git repo
- whether important plans or notes exist inside the repo
- which directories in `~/.cursor/projects/` appear to correspond to the current project

Do not rely on naming alone if multiple matches exist. Prefer recent modification time and contents that mention the current project path.

### 2. Back Up Cursor State

Create a backup before any move or rename.

Recommended minimum:

- back up the matching workspace directory or directories under `~/.cursor/projects/`
- if matching is uncertain, back up the whole `~/.cursor/projects/` tree

Use this backup layout:

- project-specific backups: `~/.cursor-backups/projects/<project-name>/<timestamp>/`
- full backups: `~/.cursor-backups/projects/_full/<timestamp>/`

Use project-specific backup by default. Use a full backup when:

- the matching workspace directory is uncertain
- the user is reorganizing multiple projects
- the user prefers maximum safety over smaller backups

Preferred backup command pattern:

```bash
backup_dir="$HOME/.cursor-backups/projects/_full/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
tar -czf "$backup_dir/cursor-projects.tgz" "$HOME/.cursor/projects"
```

If the backup must be narrower:

```bash
backup_dir="$HOME/.cursor-backups/projects/<project-name>/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
tar -czf "$backup_dir/project-workspace.tgz" "$HOME/.cursor/projects/<workspace-dir>"
```

### 3. Back Up Project Files

If important plans or notes are only in the working tree and not committed yet, preserve them before moving:

- verify `.cursor/plans/` exists when relevant
- verify any uncommitted notes the user cares about
- if needed, copy them to a temporary backup location before the move

Example:

```bash
backup_dir="$HOME/.cursor-backups/projects/<project-name>/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
cp -R "/path/to/project/.cursor" "$backup_dir/repo-cursor-dir"
```

### 4. Prefer the Symlink Strategy

When the user is specifically worried about losing Cursor history, use this default:

1. Move the project to the new location.
2. Create a symlink from the old path to the new path.
3. Open the old path first through the symlink.
4. Verify that Cursor still surfaces the expected history and local state.

Example:

```bash
mv "/old/project/path" "/new/project/path"
ln -s "/new/project/path" "/old/project/path"
```

Why this is the default:

- it preserves a path-shaped compatibility layer
- it keeps rollback simple
- it reduces the chance that path-bound Cursor state becomes unreachable

### 5. Verify Before Cleanup

After the move:

- open the project in Cursor
- confirm important plans are present
- confirm expected conversations or local history are still visible
- confirm the workspace behaves normally

If history appears missing:

- stop
- keep the symlink and backups intact
- inspect whether Cursor created a new workspace directory for the new path
- restore from backup only if necessary

### 6. Cleanup Only After Confirmation

Cleanup is the final step, not part of the initial migration.

Only after the user confirms the new setup is stable:

- optionally remove the symlink
- optionally archive old backups
- optionally remove obsolete workspace state

## Decision Guide

Use this order of preference:

1. `move + symlink`
   Best default when preserving local Cursor history matters.
2. `copy + verify + switch later`
   Use when the user wants an even safer migration with easy rollback.
3. `move without symlink`
   Use only when the user accepts the risk of Cursor treating it as a new workspace.

## Suggested Response Format

When helping the user, structure the answer like this:

```markdown
Risk: [low/medium/high]

What is safe:
- ...

What may be lost without backup:
- ...

Recommended approach:
1. ...
2. ...
3. ...

Verification:
- ...

Rollback:
- ...
```

## Example Triggers

Apply this skill when the user says things like:

- "move this project to another folder"
- "rename my repo folder"
- "change the path of this workspace"
- "reorganize my project directories"
- "preserve Cursor history"
- "keep chats and plans when moving a project"

## Anti-Patterns

- Do not say that Cursor definitely migrates history automatically.
- Do not delete `~/.cursor/projects/` entries before the move is validated.
- Do not assume repo files and local Cursor state are stored together.
- Do not recommend destructive cleanup as part of the first pass.
