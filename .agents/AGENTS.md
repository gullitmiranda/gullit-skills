# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans` and `.cursor/plans` are the same ignored local plan tree. One path is a real directory; the other is a relative symlink. Either direction is valid. A plan is an execution contract that is ready to implement without unresolved product, scope, or architecture decisions.
- In Cursor, create, edit, and archive plans through `.cursor/plans`. Do not ask which path to use.
- `.agents/notes/` contains tracked working knowledge: missions, proposals, research, decisions, and other context that may guide later work.
- `.agents/scratch/` contains local disposable material.
- `docs/` contains canonical repository documentation for readers.

Create folders only with their first artifact.

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
    .archived/           # frozen local plan history
  scratch/               # local and ignored; created when needed
.cursor/
  plans                  # same tree; real directory or relative symlink
```

## Notes

Notes may use descriptive suffixes such as `.mission.md`, `.proposal.md`, `.research.md`, and `.decision.md`, but these are conventions rather than a closed schema. `*.plan.md` never belongs in `notes/`.

The note folder is the only lifecycle representation:

```text
proposed -> current -> retired -> archived
```

Do not duplicate lifecycle in frontmatter or the body. Optional type-specific `Status:` and `Outcome:` lines belong visibly after the title.

Treat `retired/` and `archived/` notes as frozen by default. Create a successor note instead of routinely editing either. Edit, cleanup, migration, or reactivation requires explicit user authorization.

## Documentation boundaries

- Do not add runtime-command invocation or collision guidance to tracked docs or skills based only on a migration discussion or static inference. Keep it local until the user explicitly requests publication or verified runtime evidence justifies it.
- Do not restate an agent workspace path in a runtime adapter unless the adapter needs that path to operate.

## Implementation plans

Plans are local files on that shared tree and are never committed. In Cursor, the path is `.cursor/plans/*.plan.md`. Never create a second real plan directory.

If an execution-relevant decision remains open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding it during execution.

After implementation, discard the plan, move it unchanged to the tree's `.archived/`, or distill durable knowledge into notes or docs. Do not archive, discard, or distill without clear user intent.

## Tracking and unification

`.agents/notes/` is tracked. `.agents/plans`, `.cursor/plans`, and `.agents/scratch/` are never committed.

If both plan paths are real directories, make them one tree without asking which side is canonical. Replace an empty directory with a relative symlink. If both have files, keep one real directory, move non-colliding files into it, and symlink the other. Stop only when the same filename has different content. Never publish links to either path (`publish-safe-links`).
