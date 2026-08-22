# `.agents/AGENTS.md` template

Adapt this concise contract to the repository. Do not create folders until their first artifact is needed.

```markdown
# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans/` contains local implementation plans that are ready to execute without unresolved product, scope, or architecture decisions.
- `.agents/notes/` contains tracked working knowledge: missions, proposals, research, decisions, and coordination context.
- `.agents/scratch/` contains local disposable material.
- `docs/` contains canonical repository documentation.

## Layout

```text
.agents/
  AGENTS.md
  .gitignore
  notes/
    proposed/
    current/
    retired/
    archived/
  plans/
    .archived/
  scratch/
```

## Notes

`*.plan.md` never belongs in `notes/`. The note folder is its only lifecycle representation:

```text
proposed -> current -> retired -> archived
```

Use visible `Status:` or `Outcome:` lines only when type-specific context is useful. Treat `retired/` and `archived/` notes as frozen unless the user explicitly authorizes a change.

## Implementation plans

Plans are local `.agents/plans/*.plan.md` artifacts and are never committed. If execution-relevant decisions remain open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding them during execution.

After implementation, discard the plan, archive it unchanged under `.agents/plans/.archived/`, or distill durable knowledge into notes or docs. Require clear user intent before any of those actions.

## Migration

`.cursor/plans/` is a legacy local input. Move it to `.agents/plans/` and create a compatibility symlink only when the user explicitly requests that migration. Do not implicitly move, promote, or reclassify legacy artifacts.
```
