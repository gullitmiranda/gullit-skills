---
name: build-plan
description: Execute one ready local implementation plan through focused changes, validation, and review. Use when the user asks to implement or continue a plan whose execution-relevant decisions are resolved.
---

# Build Plan

Execute one local implementation contract without assigning it a tracked lifecycle.

## Hard Rules

- Do not implement on `main` or `master` unless the user explicitly requests it.
- Read `.agents/AGENTS.md` and classify the source before editing. A workspace-standard implementation plan is local under `.agents/plans/` and is never committed.
- Do not move, promote, synchronize, archive, discard, or distill a local plan without clear user intent.
- If product, scope, or architecture decisions needed to execute remain open, stop and route to `plan` or the user.
- Follow `safety`, `git`, `quality`, `data-boundary`, and `publish-safe-links`; do not duplicate their policy.
- Do not push or create a pull request without explicit user direction.

## Procedure

1. Inspect plan scope, repository instructions, branch/worktree, local changes, relevant files, and validation commands. Record the plan as local, its readiness, and `n/a` lifecycle.
2. Prepare the execution branch or worktree when needed. Break the work into reviewable blocks, each with focused scope and minimum validation.
3. Implement and validate each block. Commit only when the user request or plan contract explicitly calls for commits; never include ignored local plans.
4. Review the full diff and report implementation evidence, validation, uncompleted items, risks, and the next route. Use `work-closeout` when the user asks to assess or change the local plan after execution.

## Scope

For multi-increment work, use `incremental-delivery` to coordinate deliveries. Do not infer a larger plan or convert a tracked note into an execution contract.
