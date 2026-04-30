---
name: incremental-delivery
description: Break large implementations into small, reviewable, testable increments. Use when the user asks for smaller PRs, incremental delivery, safer rollout, or higher confidence in final outcomes.
---

# Incremental Delivery

## Goal

Turn a large implementation into a sequence of small increments, each with clear scope, explicit validation, and controlled risk.

## When to apply

Activate this skill when the user asks for:

- smaller PRs
- incremental delivery
- safer rollout
- easier reviews
- higher confidence in outcomes
- splitting work into parts

## Branch safety (see also `safety/SKILL.md`)

The absolute rules — "treat the source branch as read-only", "create a new delivery branch/worktree from the agreed base before editing", "never execute the mission on the source branch" — live in `safety/SKILL.md` (Git Safety > Absolute Rules). They apply unconditionally and cannot be relaxed for incremental work.

Procedural specifics that are **unique to incremental delivery** and complement those rules:

- Build each increment by **cherry-picking or reapplying only the commits that belong to that slice**. Do not bring along unrelated commits "because they are already there".
- If the new execution branch/worktree does not exist yet, **stop and create it before any planning or implementation continues** — even reading and analyzing changes that will end up in increment 1 should happen on the new branch, not on the source branch.
- When the source branch already contains a mix of work that will be split across multiple slices, treat each slice as an independent rebuild from the base, not a subtraction from the source.

## Mandatory protocol

1. **Define the final target in 3-6 verifiable criteria**
   - What must work at the end.
   - Objective acceptance criteria with no ambiguity.

2. **Map independent vertical slices**
   - Each slice should deliver testable end-to-end value.
   - Prefer one objective per PR.
   - Do not mix broad refactors with core feature work in the same slice.

3. **Build the increment sequence**
   For each increment, record:
   - Scope (in / out)
   - Dependencies
   - Risks
   - Minimum validation (test/lint/typecheck/build as needed)
   - Acceptance evidence (command + expected outcome)

4. **Apply a quality gate per increment**
   - No increment is done with failing tests/lint/typecheck.
   - Run fast checks during iteration and full checks at slice closure.

5. **Keep branches/PRs small and progressive**
   - One increment per PR (max two only when tightly coupled).
   - If PRs depend on each other, use an explicit stack.
   - Clearly state "depends on" and "unblocks" in PR description.

6. **Close each slice with a short handoff**
   - What was delivered
   - How to validate locally
   - What remains for the next slice
   - Remaining risks

## Standard branch naming

Use this default convention unless the repo already enforces another one:

- Single increment branch: `<owner>/feat/<epic>-slice-<nn>-<slug>`
- Stacked increment branch: `<owner>/stack/<epic>/<nn>-<slug>`
- Hardening/refactor-only increment: `<owner>/chore/<epic>-slice-<nn>-<slug>`

Rules:

- `<nn>` is a two-digit sequence (`01`, `02`, ...).
- `<owner>` is required but must be dynamic (never hardcoded in the skill). Use the current user/team handle for the workspace.
- Keep branch names stable after PR creation.
- If base branch is another slice branch, mark PR as draft until dependency merges.

## Validation checklist (mandatory per increment)

Run this checklist for every increment (adapt to repo scripts if they exist):

1. Targeted tests for changed modules.
2. Repo lint (or equivalent static checks).
3. Typecheck.
4. Build.
5. Full test suite before handoff when increment is marked done.
6. Smoke check of the user-visible path changed by the increment.

**Command runner priority (check in this order):**

1. If the repo has a `mise.toml` or `.mise.toml` with relevant tasks — use `mise run <task>`.
2. If the repo already uses another runner (`Makefile`, `package.json` scripts, `justfile`, etc.) — use those exact commands. Do not migrate existing projects to mise.
3. If no runner is configured — run the language-native commands directly (e.g. `go test`, `cargo build`, `npm run`).

Never introduce mise into a repo that does not already use it.

## Recommended increment size

- **Target diff**: small enough for quick review.
- **Target duration**: short cycle with same-cycle validation.
- **Technical scope**: one primary change plus minimal integration adjustments.

## Anti-patterns

- One giant PR with multiple objectives.
- "Almost done" without executed validation.
- Increments that depend on unresolved product/architecture decisions.
- Mixing broad cleanup with critical behavior changes.
- Using the branch being split as the branch where new extraction work is performed.

## Output template (always use)

For each increment:

1. **Name**
2. **Objective**
3. **Includes / Excludes**
4. **Dependencies**
5. **Required validation**
6. **Acceptance criteria**
7. **Main risk + mitigation**
8. **Next increment**
