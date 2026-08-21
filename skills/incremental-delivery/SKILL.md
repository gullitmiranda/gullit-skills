---
name: incremental-delivery
description: Coordinate a large implementation as small, independent, reviewable increments. Use when work needs staged delivery, safer rollout, or separate validation and handoff per increment.
---

# Incremental Delivery

Coordinate multiple deliveries; do not replace planning, execution, or guardrails.

## Hard Rules

- Start only after the target outcome and execution-relevant decisions are resolved. Route open decisions to `plan` or the user.
- Use the isolation, branch, commit, validation, and publication rules from `git-worktree`, `git`, `quality`, `safety`, and `pr`; do not restate or weaken them here.
- Scope each increment to independently testable user value. When pull requests are requested, use one pull request per increment unless the user approves an exception.
- Treat failing or unrun validation as incomplete evidence, not a completed increment.

## Procedure

1. Define the final target as a small set of verifiable acceptance criteria.
2. Map and sequence independent vertical increments, each with scope, dependencies, risks, validation, and acceptance evidence.
3. Coordinate implementation and handoff for one increment at a time in the appropriate isolated delivery context.
4. Report what each increment delivered, validation evidence, remaining risks, dependencies, and the next increment.

## Avoid

Do not split a mixed source branch by subtracting commits, bundle unrelated objectives into one increment, or use a delivery boundary to bypass repository guardrails.
