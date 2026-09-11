---
name: incremental-delivery
description: Coordinate a large implementation as small, independent, reviewable increments. Use when work needs staged delivery, safer rollout, or separate validation and handoff per increment.
---

# Incremental Delivery

Coordinate multiple deliveries; do not replace planning, execution, or guardrails.

## Hard Rules

- Start only after the target outcome and execution-relevant decisions are resolved. Route open decisions to `work-plan` or the user.
- Follow `user-preferences` and use the isolation, branch, commit, validation, and publication rules from `git-worktree`, `git`, `quality`, `safety`, and `pr`; do not restate or weaken them here.
- Scope each increment to independently testable user value. When pull requests are requested, use one pull request per increment unless the user approves an exception.
- Treat failing or unrun validation as incomplete evidence, not a completed increment.
- Deliver **one increment at a time**. Inside each increment, execution follows
  `build-plan` and the cast from `agent-selection` (disjoint writers, clean
  reviews, models per role)—do not collapse an increment into one uncast
  sequential agent by default.

## Procedure

1. Define the final target as a small set of verifiable acceptance criteria.
2. Map and sequence independent vertical increments, each with scope, dependencies, risks, validation, acceptance evidence, and a commit boundary when the applicable cadence calls for incremental commits.
3. For the current increment, obtain/refresh the orchestration cast (`agent-selection`), then execute via `build-plan` in the isolated delivery context. Commit after validation when the cadence authorizes it, before starting the next increment.
4. Report what each increment delivered, validation evidence, remaining risks, dependencies, and the next increment.

## Avoid

Do not split a mixed source branch by subtracting commits, bundle unrelated objectives into one increment, or use a delivery boundary to bypass repository guardrails.
