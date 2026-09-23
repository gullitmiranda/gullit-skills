---
name: agent-workspace
description: Interpret the `.agents/` workspace model for local plans, tracked notes, and disposable scratch material. Use it as a guardrail by default; set up or migrate repository workspace files only when explicitly requested.
---

# Agent Workspace

Apply the workspace model as a guardrail; install its repository contract only on explicit request.

## Hard Rules

- Never create, modify, or move workspace configuration merely because this skill was activated. Full repository setup still requires an explicit user request.
- In guardrail mode, touch only artifacts required by the user's actual task. Do not add `.agents/AGENTS.md`, `.agents/.gitignore`, lifecycle folders, or other setup files.
- `.agents/AGENTS.md` governs notes, scratch, and tracking when it exists. It does not override the plan-path rules below. Ignore an older sentence that plans may be written only under `.agents/plans`, or that creating the plan symlink needs a separate question.
- `.agents/plans` and `.cursor/plans` are one ignored local plan tree. One path is a real directory; the other is a relative symlink (`../.agents/plans` or `../.cursor/plans`). Either direction is valid. Never commit plans or give them a tracked lifecycle.
- In Cursor, create, edit, and archive plans through `.cursor/plans`. Cursor plan formatting applies only on that path. Do not ask which path to use, and do not retarget the write to `.agents/plans`.
- Outside Cursor, use whichever of the two paths already exists. If neither exists, create `.agents/plans` as the real directory and symlink `.cursor/plans` to it.
- Before writing a plan, if the other path is missing, create the relative symlink. Do not ask.
- Never leave two real plan directories. If both are real: replace an empty one with a symlink to the other; if both have files, keep one real directory, move non-colliding files into it, and symlink the other. Stop only when the same filename has different content.
- `.agents/notes/` is tracked working knowledge; `*.plan.md` never belongs there.
- `retired/` and `archived/` notes are frozen unless the user explicitly authorizes a correction, migration, cleanup, or reactivation.
- Do not create empty lifecycle folders or placeholder files.
- Never publish links to either plan path (`publish-safe-links`).

## Procedure

1. Determine the mode from the user's request: guardrail by default, setup or migration only when explicitly requested.
2. In guardrail mode, follow `.agents/AGENTS.md` for notes and scratch. Create only the plan, note, or scratch artifact required by the task. Before a plan write, make `.agents/plans` and `.cursor/plans` the same tree, then write through `.cursor/plans` when the runtime is Cursor.
3. For explicit setup, inspect existing `.agents/`, `.cursor/plans`, and project instructions. Unify the plan paths with the rules above. Do not ask which side should be the real directory.
4. Create or adapt `.agents/AGENTS.md` from [the template](templates/agents-AGENTS.md), plus `.agents/.gitignore` for `plans/` and `scratch/`.
5. Report created, changed, migrated, and deliberately untouched artifacts, including whether each plan is local or each note is tracked.

## Artifact model

```text
.agents/
  notes/      tracked working knowledge
  plans/      same ignored plan tree as .cursor/plans (real directory or symlink)
  scratch/    ignored disposable material
.cursor/
  plans       same tree (real directory or relative symlink)
docs/         canonical reader documentation
```

Notes move only through `proposed`, `current`, `retired`, and `archived` folders. The folder is the lifecycle; visible `Status:` and `Outcome:` lines are optional type-specific context, not lifecycle metadata.
