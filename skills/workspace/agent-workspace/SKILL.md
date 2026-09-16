---
name: agent-workspace
description: Interpret the `.agents/` workspace model for local plans, tracked notes, and disposable scratch material. Use it as a guardrail by default; set up or migrate repository workspace files only when explicitly requested.
---

# Agent Workspace

Apply the workspace model as a guardrail; install its repository contract only on explicit request.

## Hard Rules

- Never create, modify, move, or symlink workspace configuration merely because this skill was activated. Repository setup or migration requires an explicit user request.
- In guardrail mode, touch only artifacts required by the user's actual task; do not add `.agents/AGENTS.md`, `.agents/.gitignore`, compatibility symlinks, lifecycle folders, or other setup files.
- When `.agents/AGENTS.md` exists, it overrides this skill.
- There is one physical local plan tree: `.agents/plans/`. Never commit, promote, or give plans a tracked lifecycle.
- `.cursor/plans` may exist only as a symlink to that tree (typically `../.agents/plans`) so Cursor Plan Mode / UI resolve the same files. It is not a second plan home.
- Never create a second real plan directory. If both `.agents/plans/` and `.cursor/plans/` are real directories, stop and ask to unify before writing plans.
- `.agents/notes/` is tracked working knowledge; `*.plan.md` never belongs there.
- `retired/` and `archived/` notes are frozen unless the user explicitly authorizes a correction, migration, cleanup, or reactivation.
- Do not create empty lifecycle folders or placeholder files.

## Local plans (one tree)

- Canonical physical home: `.agents/plans/` (ignored).
- Cursor-facing path: `.cursor/plans` → symlink to the canonical tree when both paths must resolve.
- Reading or editing through either path is fine when they resolve to the same tree.
- Create and archive new plans under `.agents/plans/` (including `.agents/plans/.archived/`).
- Never publish links to either path (`publish-safe-links`).
- Create or repair the compatibility symlink only on explicit user request (setup or unification).

## Procedure

1. Determine the mode from the user's request: guardrail by default, setup or migration only when explicitly requested.
2. In guardrail mode, follow an existing `.agents/AGENTS.md`; otherwise apply the artifact model without configuring the repository. Create only the plan, note, or scratch artifact required by the task. Before writing a plan, confirm there is not a second real plan directory.
3. For explicit setup, inspect existing `.agents/`, `.cursor/plans/`, project instructions, and documentation. Explain the one-tree layout and ask separately whether to migrate an existing real `.cursor/plans/` tree and create the compatibility symlink.
4. Create or adapt `.agents/AGENTS.md` from [the template](templates/agents-AGENTS.md), plus `.agents/.gitignore` for `plans/` and `scratch/`. If migration is explicitly approved, move plans into `.agents/plans/` unchanged and create `.cursor/plans` → `../.agents/plans`.
5. Report created, changed, migrated, and deliberately untouched artifacts, including whether each plan is local or each note is tracked.

## Artifact model

```text
.agents/
  notes/      tracked working knowledge
  plans/      ignored local implementation plans (only physical tree)
  scratch/    ignored disposable material
.cursor/
  plans -> ../.agents/plans   # optional compatibility symlink; not a second tree
docs/         canonical reader documentation
```

Notes move only through `proposed`, `current`, `retired`, and `archived` folders. The folder is the lifecycle; visible `Status:` and `Outcome:` lines are optional type-specific context, not lifecycle metadata.
