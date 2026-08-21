# Agent Workspace

This repository uses `.agents/` for agent working artifacts. This file is the authority for their location, lifecycle, and tracking.

## Artifact model

- `.agents/plans/` contains local implementation plans. A plan is an execution contract that is ready to implement without unresolved product, scope, or architecture decisions.
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
  plans/                 # local and ignored; created when needed
    .archived/           # frozen local plan history
  scratch/               # local and ignored; created when needed
```

## Notes

Notes may use descriptive suffixes such as `.mission.md`, `.proposal.md`, `.research.md`, and `.decision.md`, but these are conventions rather than a closed schema. `*.plan.md` never belongs in `notes/`.

The note folder is the only lifecycle representation:

```text
proposed -> current -> retired -> archived
```

Do not duplicate lifecycle in frontmatter or the body. Optional type-specific `Status:` and `Outcome:` lines belong visibly after the title.

Treat `retired/` and `archived/` notes as frozen by default. Create a successor note instead of routinely editing either. Edit, cleanup, migration, or reactivation requires explicit user authorization.

## Implementation plans

Plans are local `.agents/plans/*.plan.md` artifacts. If an execution-relevant decision remains open, refine the plan or request clarification before implementation unless the user explicitly authorizes deciding it during execution.

After implementation, discard the plan, move it unchanged to `.agents/plans/.archived/`, or distill durable knowledge into notes or docs. Do not archive, discard, or distill without clear user intent.

## Tracking and migration

`.agents/notes/` is tracked. `.agents/plans/` and `.agents/scratch/` are never committed.

`.cursor/plans/` is a legacy local input. Move it to `.agents/plans/` and create a compatibility symlink only when the user explicitly requests that migration. Do not move, promote, or reclassify legacy material implicitly.
