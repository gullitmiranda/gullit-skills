---
name: work-closeout
description: Assess and close a local plan or work context using implementation evidence, with confirmed archival, discard, or distillation actions. Use when wrapping up work, reviewing plan status, or cleaning a current context or workspace.
---

# Work Closeout

Assess work without mutating plans, branches, or remote state until the user chooses an action.

## Hard Rules

- Read `.agents/AGENTS.md` first. Treat `.agents/plans/` as local, ignored plan material and `.cursor/plans/` as compatibility-only input.
- Default to read-only assessment. Do not archive, discard, distill, commit, push, remove a worktree, close a pull request, or delete a branch without clear user intent.
- Archive only after explicit confirmation of the exact plan and destination. Move it unchanged to `.agents/plans/.archived/`; archived plan content is frozen.
- Distill only durable decisions, constraints, findings, outcomes, and follow-ups into notes or documentation. Do not copy a plan wholesale.
- Treat missing validation, review, deployment, or branch evidence as uncertainty, not completion.

## Modes

- **Focused plan closeout**: assess one named local plan.
- **Current-context closeout**: assess the current repository, branch, worktree, and related plan.
- **Workspace closeout**: inspect multiple contexts only when the user explicitly asks.

## Procedure

1. Confirm the scope and inspect local plans, branch/worktree, commits, review state, validation evidence, and relevant handoff context using read-only commands.
2. Classify each context as `active`, `awaiting-evidence`, `ready-to-close`, `stale`, or `superseded`, citing evidence and uncertainty.
3. Recommend the smallest next action. Await confirmation before an archive, discard, distillation, repository cleanup, or remote-state change.
4. When confirmed, perform only the selected action and report the changed artifact, destination, and retained evidence.

## Output

For each context, state status, evidence, uncertainty, recommended action, and decisions required. If no state-changing action is authorized, leave all artifacts unchanged.
