---
name: work-plan
description: Create or refine one local implementation plan that is ready for execution. Use when work needs an executable scope, approach, constraints, and validation contract before implementation.
---

# Work Plan

Produce one local execution contract, not a tracked lifecycle artifact.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists. It does not choose a different plan path than this skill.
- Plans are local and never committed.
- In Cursor, create and refine the plan at `.cursor/plans/<slug>.plan.md`. Do not ask which path to use, and do not retarget the write to `.agents/plans`.
- Keep `.agents/plans` and `.cursor/plans` as one tree (real directory plus relative symlink, either direction) using `agent-workspace`. Do not stop to ask how to unify unless two files share a name and differ.
- Outside Cursor, write the plan under the existing plan path. If none exists, use `.agents/plans/<slug>.plan.md` and symlink `.cursor/plans` to that directory.
- Do not create a plan under `.agents/notes/`, and do not assign plans note lifecycle states.
- If a product, scope, or architecture decision needed for execution remains open, propose a refinement or ask the user. Decide it during implementation only with explicit authorization.
- Follow `user-preferences` and repository policies when forming the execution contract.

## Procedure

1. Inspect the request, authority, relevant code or documentation, and the existing local plan. State unresolved execution-relevant decisions. Do not ask about the plan directory.
2. Create or refine one local plan with objective, scope, approach, constraints, implementation steps, validation, acceptance criteria, commit cadence for multi-block work, and meaningful alternatives or risks. Omit timelines and estimates unless the user explicitly asks for them.
3. Confirm the plan is executable without making relevant product, scope, or architecture decisions. Otherwise return the smallest decision or refinement needed.
4. Report the path written, readiness, open decisions, validation expectation, and next route: `build-plan`, `incremental-delivery`, or user decision. In Cursor, report `.cursor/plans/<slug>.plan.md`.

## Fallback

In Cursor, still use `.cursor/plans`. Outside Cursor, use the runtime's local planning convention when the repository has no workspace authority. Do not create a second real plan directory.
