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
- If product, scope, or architecture decisions needed to execute remain open, stop and route to `work-plan` or the user.
- Follow `user-preferences`, `safety`, `git`, `quality`, `data-boundary`, and `publish-safe-links`; do not duplicate their policy.
- Do not push or create a pull request without explicit user direction.
- Before the first block, produce an **orchestration cast** via `agent-selection`
  (runtime + model per role, write sets, review capsules). Do not default to a
  solo sequential monolith; that shape needs an explicit exception from
  `agent-selection`.
- Subagent writers must have disjoint write sets. The orchestrator reconciles,
  validates, and commits; it does not absorb parallelizable work without cause.
- Per block: run scoped validation and an independent review with a **review**
  `context-capsule` (or `code-review`). Review may overlap scoped validation.
  Do not review inside the implementer's debug transcript when a subagent or
  clean handoff is available.

## Procedure

1. Inspect plan scope, repository instructions, branch/worktree, local changes, relevant files, validation commands, and applicable commit cadence. Record the plan as local, its readiness, and `n/a` lifecycle.
2. Publish the orchestration cast (`agent-selection`). Prepare the execution branch or worktree when needed. Break the work into reviewable blocks with minimum validation and commit boundaries when the cadence calls for them.
3. Execute each block through the cast: implement only within assigned write sets, run scoped validation, run clean-context review (overlap allowed), then commit when authorized. Never include ignored local plans.
4. After the final block, run full-diff review and report implementation evidence, validation, uncompleted items, risks, and the next route. Use `work-closeout` when the user asks to assess or change the local plan after execution.

## Scope

For multi-increment work, use `incremental-delivery` to coordinate deliveries. Do not infer a larger plan or convert a tracked note into an execution contract.
