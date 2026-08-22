---
name: agent-workspace
description: Establish or interpret the `.agents/` workspace model for local implementation plans, tracked notes, and disposable scratch material. Use when setting up an agent workspace, migrating its artifacts, or resolving their locations and tracking rules.
---

# Agent Workspace

Define the repository contract for agent working artifacts.

## Hard Rules

- When `.agents/AGENTS.md` exists, it overrides this skill.
- `.agents/plans/*.plan.md` are local implementation plans: never commit, promote, or give them a tracked lifecycle.
- `.agents/notes/` is tracked working knowledge; `*.plan.md` never belongs there.
- Treat `.cursor/plans/` as a compatibility input only. Do not move it, create a symlink, or reclassify its contents without explicit user approval.
- `retired/` and `archived/` notes are frozen unless the user explicitly authorizes a correction, migration, cleanup, or reactivation.
- Do not create empty lifecycle folders or placeholder files.

## Procedure

1. Inspect existing `.agents/`, `.cursor/plans/`, project instructions, and documentation. Explain the proposed layout and ask whether legacy migration is wanted.
2. Create or adapt `.agents/AGENTS.md` from [the template](templates/agents-AGENTS.md), plus `.agents/.gitignore` for `plans/` and `scratch/`. Track notes, not plans or scratch.
3. If migration is explicitly approved, move legacy local plans mechanically to `.agents/plans/`, preserving names and `.archived/` history, then create the local compatibility symlink. Classify prior tracked plan-tree artifacts individually before moving durable knowledge to notes.
4. Report created, changed, migrated, and deliberately untouched artifacts, including whether a plan is local or a note is tracked.

## Artifact model

```text
.agents/
  notes/      tracked working knowledge
  plans/      ignored local implementation plans
  scratch/    ignored disposable material
docs/         canonical reader documentation
```

Notes move only through `proposed`, `current`, `retired`, and `archived` folders. The folder is the lifecycle; visible `Status:` and `Outcome:` lines are optional type-specific context, not lifecycle metadata.
