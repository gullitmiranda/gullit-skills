---
name: agent-notes
description: Create, transition, supersede, or distill tracked agent notes under `.agents/notes/`. Use for durable decisions, research, proposals, missions, and coordination context.
---

# Agent Notes

Manage durable agent working knowledge without turning it into an execution-plan lifecycle.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists.
- Create notes only under `.agents/notes/{proposed,current,retired,archived}/`; lifecycle is represented by the folder alone.
- Never create `*.plan.md` inside `notes/`, and never copy a completed implementation plan wholesale into a note.
- Treat `retired/` and `archived/` notes as frozen by default. Create a successor instead unless the user explicitly authorizes changing the frozen record.
- Do not move a local plan, archive it, or distill it without clear user intent.

## Procedure

1. Identify whether the information is durable knowledge or an implementation contract. Route contracts to `work-plan`.
2. Create or refine a note with a descriptive optional suffix such as `.decision.md`, `.research.md`, `.proposal.md`, or `.mission.md`. Add visible `Status:` or `Outcome:` lines only when useful for that note type.
3. For a lifecycle transition, move the file to the appropriate note folder. For supersession, create a current successor that links to the frozen predecessor and explains the replacement.
4. When distilling completed work, capture durable decisions, constraints, findings, outcomes, and follow-ups; omit operational checklists and incidental command history.

## Report

State the note path, lifecycle transition if any, successor relationship, and knowledge that was intentionally not preserved.
