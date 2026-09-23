# `.agents/AGENTS.md` template

Adapt this concise contract to the repository. Do not create folders until their first artifact is needed.

```markdown
# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans` and `.cursor/plans` are the same ignored local plan tree. One path is a real directory; the other is a relative symlink. Either direction is valid. Plans are ready to execute without unresolved product, scope, or architecture decisions.
- In Cursor, create, edit, and archive plans through `.cursor/plans`. Do not ask which path to use.
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
  plans/                 # same ignored tree as .cursor/plans
    .archived/
  scratch/
.cursor/
  plans                  # same tree; real directory or relative symlink
```

## Notes

`*.plan.md` never belongs in `notes/`. The note folder is its only lifecycle representation:

```text
proposed -> current -> retired -> archived
```

Use visible `Status:` or `Outcome:` lines only when type-specific context is useful. Treat `retired/` and `archived/` notes as frozen unless the user explicitly authorizes a change.

## Implementation plans

Plans are local files on that shared tree and are never committed. In Cursor, the path is `.cursor/plans/*.plan.md`.

If execution-relevant decisions remain open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding them during execution.

After implementation, discard the plan, archive it unchanged under the tree's `.archived/`, or distill durable knowledge into notes or docs. Require clear user intent before any of those actions.

## Tracking

`.agents/notes/` is tracked. `.agents/plans`, `.cursor/plans`, and `.agents/scratch/` are never committed.

If both plan paths are real directories, make them one tree: replace an empty directory with a relative symlink; if both have files, keep one real directory, move non-colliding files into it, and symlink the other. Do not ask which side is canonical. Stop only when the same filename has different content. Do not leave two independent plan trees.
```
