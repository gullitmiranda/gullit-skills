---
name: agent-notes
description: Create, transition, supersede, or distill tracked agent notes under `.agents/notes/`. Use for durable decisions, research, proposals, missions, and coordination context. Notes are routed to a destination repo by topic scope (see Routing), never to whichever project the current thread happens to run in.
---

# Agent Notes

Manage durable agent working knowledge without turning it into an execution-plan lifecycle.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists.
- Resolve the destination by topic scope (see Routing), not by the current project. A note requested from a thread in any project lands in the repo that owns that scope, even when that repo is not open.
- Create notes only under `<destination>/.agents/notes/{proposed,current,retired,archived}/`; lifecycle is represented by the folder alone.
- Never create `*.plan.md` inside `notes/`, and never copy a completed implementation plan wholesale into a note.
- Treat `retired/` and `archived/` notes as frozen by default. Create a successor instead unless the user explicitly authorizes changing the frozen record.
- Do not move a local plan, archive it, or distill it without clear user intent.

## Routing

The destination is chosen by topic scope first. Only knowledge owned by the
open project goes to that project's own `.agents/notes/`.

| Topic scope | Destination repo | Notes tree | Convention |
|---|---|---|---|
| Zed: upstream gaps, agent panel UX, context consumption, worktrees, CLI, editor tooling | `gullit-skills` | `.agents/notes/current/` | prefix `zed-`; tracker note `zed-upstream-gaps.research.md` |
| Models, benchmarks, agent runtimes and harnesses | `gullit-skills` | `.agents/notes/current/` | prefix `models-` |
| Agent workspace conventions (notes tree, plans, skills layout) | `gullit-skills` | `.agents/notes/current/` | prefix `agent-workspace-` |
| Anything owned by the open project | that project's repo | its `.agents/notes/` | follow that project's own conventions |

Rules:

- Resolve a destination repo's local clone path via the `workspace-topology`
  skill (WORKSPACE.md), never by assuming a fixed path.
- Tracker-first: when a scope has a tracker note, update it in place instead of
  creating a new note per conversation. Create a separate note only for a deep
  dive (`.research.md`) or a durable decision (`.decision.md`), and link it
  from the tracker.

## Procedure

1. Identify whether the information is durable knowledge or an implementation contract. Route contracts to `work-plan`.
2. Resolve the destination repo via Routing; read that repo's `.agents/AGENTS.md` when it exists.
2. Create or refine a note with a descriptive optional suffix such as `.decision.md`, `.research.md`, `.proposal.md`, or `.mission.md`. Add visible `Status:` or `Outcome:` lines only when useful for that note type.
3. For a lifecycle transition, move the file to the appropriate note folder. For supersession, create a current successor that links to the frozen predecessor and explains the replacement.
4. When distilling completed work, capture durable decisions, constraints, findings, outcomes, and follow-ups; omit operational checklists and incidental command history.

## Report

State the note path, lifecycle transition if any, successor relationship, and knowledge that was intentionally not preserved.
