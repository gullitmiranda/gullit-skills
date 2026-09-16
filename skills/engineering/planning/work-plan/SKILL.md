---
name: work-plan
description: Create or refine one local implementation plan that is ready for execution. Use when work needs an executable scope, approach, constraints, and validation contract before implementation.
---

# Work Plan

Produce one local execution contract, not a tracked lifecycle artifact.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists.
- Create new plans only under `.agents/plans/<slug>.plan.md`; they are local and never committed.
- `.cursor/plans` is usable only when it is a symlink to the same tree (or when it is the sole existing real tree pending explicit unification). Never create a second real plan directory.
- If both `.agents/plans/` and `.cursor/plans/` are real directories, stop and ask to unify before writing.
- Do not create a plan under `.agents/notes/`, and do not assign plans note lifecycle states.
- If a product, scope, or architecture decision needed for execution remains open, propose a refinement or ask the user. Decide it during implementation only with explicit authorization.
- Follow `user-preferences` and repository policies when forming the execution contract.

## Procedure

1. Inspect the request, authority, relevant code or documentation, and existing local plan input (including a `.cursor/plans` symlink that resolves to `.agents/plans/`). State unresolved execution-relevant decisions.
2. Create or refine one local plan with objective, scope, approach, constraints, implementation steps, validation, acceptance criteria, commit cadence for multi-block work, and meaningful alternatives or risks. Omit timelines and estimates unless the user explicitly asks for them.
3. Confirm the plan is executable without making relevant product, scope, or architecture decisions. Otherwise return the smallest decision or refinement needed.
4. Report the local path, readiness, open decisions, validation expectation, and next route: `build-plan`, `incremental-delivery`, or user decision.

## Fallback

Without a repository workspace authority, use the runtime's local planning convention. Do not infer that a runtime-local plan is tracked knowledge or permission to migrate it. Still avoid creating a second real plan directory in the same repository.
