# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans/` is the only physical local home for implementation plans. A plan is an execution contract that is ready to implement without unresolved product, scope, or architecture decisions.
- `.cursor/plans` may be a local compatibility symlink to that tree so Cursor resolves the same files. It is not a second plan home.
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
  plans/                 # local and ignored; only physical plan tree
    .archived/           # frozen local plan history
  scratch/               # local and ignored; created when needed
.cursor/
  plans -> ../.agents/plans   # optional compatibility symlink
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

Plans are local `.agents/plans/*.plan.md` artifacts. Reading or editing through a `.cursor/plans` symlink is fine when it points at the same tree. Never create a second real plan directory.

If an execution-relevant decision remains open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding it during execution.

After implementation, discard the plan, move it unchanged to `.agents/plans/.archived/`, or distill durable knowledge into notes or docs. Do not archive, discard, or distill without clear user intent.

## Tracking and unification

`.agents/notes/` is tracked. `.agents/plans/`, `.cursor/plans`, and `.agents/scratch/` are never committed.

If both plan paths exist as real directories, unify into `.agents/plans/` and replace `.cursor/plans` with the compatibility symlink only when the user explicitly requests that migration. Never publish links to either path (`publish-safe-links`).
