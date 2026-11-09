---
name: end
description: Close the current work session - run the hygiene that removes pending state, archive the current plan, and tear down the finished worktree and branch. Use when the user runs /end, /end clean, /end keep, /archive, or /arq, or asks to wrap up and archive the current work.
---

# Session Closeout

End the current session: leave nothing pending, archive the plan, and remove the finished worktree and branch when the evidence supports it.

Routes: `/end` and `/end clean` run full closeout. `/end keep` preserves the worktree and branch. `/archive` and `/arq` are aliases of `/end`.

## Hard Rules

- Invoking this skill authorizes hygiene and plan archival for the current context only. It does not authorize merging or closing a pull request, `git reset --hard`, or changes in other repositories of a workspace.
- Scope is the current repository and worktree unless the user names more.
- Delegate behavior to the owning skills: `quality` for command execution and checks, `git` for commits, `pr` for PR metadata and post-merge reconciliation, `agent-workspace` for plan paths, `agent-notes` for distillation.
- Archive the plan unchanged into `.archived/` of the shared plan tree. Archived content is frozen.
- An open pull request with no actionable follow-up counts as review requested or not needed. Record the assumption and never claim reviewers were requested when they were not. A draft pull request is a decision for the user, not something to promote on your own.
- Never use `git branch -D`, never remove the primary clone, and never remove a worktree that holds pending or unrecorded local state.
- A failed teardown gate blocks only the teardown: finish hygiene, archive the plan, then report the reason and the exact command that completes the removal later.

## Procedure

1. Classify the context with `work-closeout` first: plan, branch, worktree, commits, PR state, review threads, validation evidence. Stop at `blocked` before archiving when committed work is missing, commits are unpushed, plan steps are undelivered, required checks fail, or an actionable review thread is open.
2. Run hygiene: the repository's format, lint, typecheck, and tests; commit what remains; push the branch; reconcile PR title and body against `git diff <base>...HEAD`; resolve actionable threads; empty `.agents/scratch/`.
3. Distill only durable decisions, findings, and follow-ups with `agent-notes`. Never copy the plan.
4. Archive the plan and report the destination.
5. Teardown unless the route is `/end keep`. Require a clean `git status`, `HEAD` equal to `origin/<branch>`, PR `MERGED` or no PR with a pushed branch, no open actionable thread, no stack membership (delegate those to `gh-stack`), the branch not checked out in another worktree, and `git status --ignored --short` listing only regenerable artifacts. Then `git worktree remove` for a linked worktree, or switch the primary clone to base and `git pull --ff-only`; finish with `git branch -d`.

## Report

State `closed`, `closed-kept`, or `blocked`; then plan destination, hygiene performed, teardown result or skip reason, the review assumption used, and real follow-ups as full `owner/repo#id` links.
