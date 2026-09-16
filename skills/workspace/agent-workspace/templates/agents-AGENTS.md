# `.agents/AGENTS.md` template

Adapt this concise contract to the repository. Do not create folders until their first artifact is needed.

```markdown
# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans/` is the only physical local home for implementation plans. Plans are ready to execute without unresolved product, scope, or architecture decisions.
- `.cursor/plans` may be a local compatibility symlink to that tree so Cursor resolves the same files. It is not a second plan home.
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
.cursor/
  plans -> ../.agents/plans   # optional; create only when needed
```

## Notes

`*.plan.md` never belongs in `notes/`. The note folder is its only lifecycle representation:

```text
proposed -> current -> retired -> archived
```

Use visible `Status:` or `Outcome:` lines only when type-specific context is useful. Treat `retired/` and `archived/` notes as frozen unless the user explicitly authorizes a change.

## Implementation plans

Plans are local `.agents/plans/*.plan.md` artifacts and are never committed. Reading or editing through a `.cursor/plans` symlink is fine when it points at the same tree. Never create a second real plan directory.

If execution-relevant decisions remain open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding them during execution.

After implementation, discard the plan, archive it unchanged under `.agents/plans/.archived/`, or distill durable knowledge into notes or docs. Require clear user intent before any of those actions.

## Tracking and unification

`.agents/notes/` is tracked. `.agents/plans/`, `.cursor/plans`, and `.agents/scratch/` are never committed.

If both plan paths exist as real directories, unify into `.agents/plans/` and replace `.cursor/plans` with the compatibility symlink only when the user explicitly requests that migration. Do not leave two independent plan trees.
```
