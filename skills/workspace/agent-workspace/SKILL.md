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
- `.agents/plans/*.plan.md` are local implementation plans: never commit, promote, or give them a tracked lifecycle.
- `.agents/notes/` is tracked working knowledge; `*.plan.md` never belongs there.
- Treat `.cursor/plans/` as a compatibility input only. Do not move it, create a symlink, or reclassify its contents without explicit user approval.
- `retired/` and `archived/` notes are frozen unless the user explicitly authorizes a correction, migration, cleanup, or reactivation.
- Do not create empty lifecycle folders or placeholder files.

## Procedure

1. Determine the mode from the user's request: guardrail by default, setup or migration only when explicitly requested.
2. In guardrail mode, follow an existing `.agents/AGENTS.md`; otherwise apply the artifact model without configuring the repository. Create only the plan, note, or scratch artifact required by the task.
3. For explicit setup, inspect existing `.agents/`, `.cursor/plans/`, project instructions, and documentation. Explain the proposed layout and ask separately whether legacy migration is wanted.
4. Create or adapt `.agents/AGENTS.md` from [the template](templates/agents-AGENTS.md), plus `.agents/.gitignore` for `plans/` and `scratch/`. If migration is explicitly approved, move legacy plans mechanically and create the compatibility symlink.
5. Report created, changed, migrated, and deliberately untouched artifacts, including whether each plan is local or each note is tracked.

## Artifact model

```text
.agents/
  notes/      tracked working knowledge
  plans/      ignored local implementation plans
  scratch/    ignored disposable material
docs/         canonical reader documentation
```

Notes move only through `proposed`, `current`, `retired`, and `archived` folders. The folder is the lifecycle; visible `Status:` and `Outcome:` lines are optional type-specific context, not lifecycle metadata.
