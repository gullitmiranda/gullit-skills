---
name: work-plan
description: Create or refine one local implementation plan that is ready for execution. Use when work needs an executable scope, approach, constraints, and validation contract before implementation.
---

# Work Plan

Produce one local execution contract, not a tracked lifecycle artifact.

## Hard Rules

- Read `.agents/AGENTS.md` first when it exists.
- Create new workspace-standard plans only as `.agents/plans/<slug>.plan.md`; they are local and never committed.
- Treat `.cursor/plans/` as legacy compatibility input. Do not move, promote, synchronize, or reclassify it without explicit user authorization.
- Do not create a plan under `.agents/notes/`, and do not assign plans note lifecycle states.
- If a product, scope, or architecture decision needed for execution remains open, propose a refinement or ask the user. Decide it during implementation only with explicit authorization.

## Procedure

1. Inspect the request, authority, relevant code or documentation, and existing local plan input. State unresolved execution-relevant decisions.
2. Create or refine one local plan with objective, scope, approach, constraints, implementation steps, validation, acceptance criteria, and meaningful alternatives or risks.
3. Confirm the plan is executable without making relevant product, scope, or architecture decisions. Otherwise return the smallest decision or refinement needed.
4. Report the local path, readiness, open decisions, validation expectation, and next route: `build`, `incremental-delivery`, or user decision.

## Fallback

Without a repository workspace authority, use the runtime's local planning convention. Do not infer that a runtime-local plan is tracked knowledge or permission to migrate it.
