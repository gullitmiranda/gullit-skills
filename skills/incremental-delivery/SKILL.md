---
name: incremental-delivery
description: Break large implementations into small, reviewable, testable increments. Use when the user asks for smaller PRs, incremental delivery, safer rollout, or higher confidence in final outcomes.
---

# Incremental Delivery

Turn a large implementation into a sequence of small increments, each with clear scope, explicit validation, and controlled risk.

## Hard Rules

- Branch safety absolute rules (source branch is read-only; create a new delivery branch/worktree from the agreed base before editing; never execute the mission on the source branch) live in `safety/SKILL.md` and apply unconditionally.
- If the execution branch/worktree does not exist yet, **stop and create it before any planning or implementation continues** — even analysis for increment 1 happens on the new branch.
- Build each increment by cherry-picking or reapplying only the commits that belong to that slice. Treat each slice as an independent rebuild from the base, not a subtraction from a mixed source branch.
- One increment per PR (max two only when tightly coupled).
- No increment is done with failing tests/lint/typecheck.
- Never introduce mise into a repo that does not already use it.

## Protocol

1. **Define the final target** in 3-6 verifiable, unambiguous acceptance criteria.
2. **Map independent vertical slices** — each delivers testable end-to-end value, one objective per PR, no broad refactors mixed with feature work.
3. **Sequence the increments** — for each, record scope (in/out), dependencies, risks, minimum validation, and acceptance evidence (command + expected outcome).
4. **Gate each increment** — fast checks during iteration, full checks at slice closure (see validation checklist).
5. **Close each slice with a short handoff** — what was delivered, how to validate locally, what remains, remaining risks.

For dependent PRs, use an explicit stack: manage with `gh stack` when the `gh-stack` skill is available, otherwise fall back to manual base-branch chaining. State "depends on" / "unblocks" in PR descriptions.

## Branch naming

Default convention unless the repo enforces another:

- Single increment: `<owner>/feat/<epic>-slice-<nn>-<slug>`
- Stacked increment: `<owner>/stack/<epic>/<nn>-<slug>`
- Hardening/refactor-only: `<owner>/chore/<epic>-slice-<nn>-<slug>`

`<nn>` is two-digit; `<owner>` is the current user/team handle (never hardcoded). Keep branch names stable after PR creation. If the base branch is another slice branch, mark the PR as draft until the dependency merges.

## Validation checklist (per increment)

1. Targeted tests for changed modules.
2. Lint / static checks.
3. Typecheck.
4. Build.
5. Full test suite before handoff.
6. Smoke check of the user-visible path changed.

**Command runner priority:** `mise run <task>` if `mise.toml`/`.mise.toml` exists → existing runner (`Makefile`, `package.json`, `justfile`) as-is → language-native commands.

## Anti-patterns

- One giant PR with multiple objectives.
- "Almost done" without executed validation.
- Increments depending on unresolved product/architecture decisions.
- Mixing broad cleanup with critical behavior changes.
- Performing extraction work on the branch being split.

## Output template (per increment)

1. **Name** 2. **Objective** 3. **Includes / Excludes** 4. **Dependencies** 5. **Required validation** 6. **Acceptance criteria** 7. **Main risk + mitigation** 8. **Next increment**
