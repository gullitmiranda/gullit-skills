# Parallel Workstreams

Use this workflow when several plans, issues, investigations, or implementations
are active in the same repo or workspace.

## Goals

- Keep the parent chat clean.
- Avoid branch and worktree collisions.
- Let side agents work independently.
- Preserve enough state to resume any workstream.

## Workstream Record

Track each active workstream with:

```text
id:
goal:
owner/runtime:
repo:
branch/worktree:
source artifact:
current state:
decisions:
open questions:
validation state:
next action:
```

This can live in the parent chat, a local plan, an issue, or a context capsule.
Use the smallest durable artifact that fits the risk.

## Flow

```text
identify workstreams
-> assign owner/runtime with agent-selection
-> create context capsule for each child
-> isolate branch/worktree when needed
-> execute independently
-> return distilled results
-> parent chat updates supervisory state
```

## Parent Chat Rules

- Keep the workstream list current.
- Do not absorb raw child-agent logs.
- Ask each child for changed files, validation evidence, blockers, and next action.
- Merge durable decisions back into the parent summary.
- Keep implementation details in the owning workstream.

## Child Agent Rules

- Work only on the assigned workstream.
- Respect the assigned branch/worktree.
- Return a concise result.
- Do not start adjacent cleanup unless it is part of the assignment.

## Isolation Rules

Use separate worktrees when:

- Two agents may edit the same repo concurrently.
- A branch already has unrelated work.
- The implementation is long-running.
- The workstream may be paused and resumed independently.

Use the current branch only when:

- The task is small.
- No other agent is editing the repo.
- The user explicitly wants work in the current tree.

## Context Transfer

Use `context-capsule` for each child workstream. Include:

- Goal.
- Relevant source artifact.
- Branch/worktree.
- Constraints.
- Next action.
- Expected return format.

Use full transcript transfer only when exact history matters.

## Completion

A workstream is complete when:

- The assigned task is done or explicitly blocked.
- Validation state is known.
- Changed files and artifacts are reported.
- Remaining risks are stated.
- The parent chat has the next action.
