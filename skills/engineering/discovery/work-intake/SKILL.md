---
name: work-intake
description: Assess handoffs, plans, issues, documentation, or workspace state and route the next engineering step. Use when starting or resuming work, choosing a workflow, or deciding whether the work is ready to execute.
---

# Work Intake

Provide the single public entry point for engineering-workflow discovery and routing.

## Hard Rules

- Do not implement, move artifacts, or change repository state during intake unless the user explicitly requests it.
- Read `.agents/AGENTS.md` before classifying a potential plan when it exists.
- A local plan is `.agents/plans/*.plan.md`; it has no tracked lifecycle. `.cursor/plans/` is compatibility-only local input.
- A tracked note may have the note lifecycle `proposed`, `current`, `retired`, or `archived`, but it is not an executable plan solely because it is tracked.
- Do not claim branch, validation, review, or PR state without current evidence.
- Do not require separately installed third-party skills for the core route.

## Procedure

1. Read the provided context and inspect enough repository state to identify evidence, constraints, workstreams, and open decisions.
2. Classify each source as a local plan, tracked note, legacy local input, or non-plan. Record its path, authority, readiness, and next route; lifecycle is `n/a` for plans and non-plans.
3. Select the smallest core route: clarify or decide in the main chat; create/refine a plan with `work-plan`; execute one ready plan with `build-plan`; coordinate multiple independent deliveries with `incremental-delivery`; or assess completed work with `work-closeout`.
4. Select the runtime with `agent-selection`. For a handoff, show the completed `context-capsule` as a standalone fenced `markdown` block after the prose recommendation, then stop before implementation unless asked to continue.

## Route guide

- **Ambiguous feature or architecture**: inspect context, clarify decisions, then `work-plan`.
- **Bug or regression**: establish a reproducible feedback loop, then plan only when needed before implementation.
- **Ready implementation plan**: verify its contract, then `build-plan`; use `incremental-delivery` when independent increments are needed.
- **Parallel workstreams**: assign an owner and runtime per stream, transfer a capsule, and reconcile distilled results.

## Output

Use [output-template.md](output-template.md). Include evidence, uncertainty, an autonomy recommendation, the recommended runtime, the smallest next action, and a copyable handoff prompt only when work moves to another runtime.
