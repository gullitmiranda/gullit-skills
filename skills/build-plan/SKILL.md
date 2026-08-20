---
name: build-plan
description: Build referenced plans into committed, validated implementation work. Use when the user asks to execute, implement, build, or continue a plan, slice, handoff, checklist, roadmap item, or scoped subset of a plan with autonomous execution, commits per block, subagents, reviews, and final checks.
---

# Build Plan

Orchestrator that turns planning artifacts into completed implementation work:
reads the plan context, applies relevant domain skills, uses subagents where
useful, commits each completed block by default, and closes with reviews and
validation.

## Hard Rules

- Never implement directly on `main`/`master` unless explicitly requested;
  create or switch to a feature branch first.
- Before implementation, classify the source as a tracked lifecycle artifact, local draft or scratch, or non-plan input. When `.agents/AGENTS.md` exists, it controls plan location, format, lifecycle, and versioning.
- Do not move, promote, commit, or synchronize `.cursor/plans/` or repository-declared scratch artifacts implicitly.
- Do not commit ignored files or local-only planning artifacts unless the user
  asks and the repository versions them.
- Do not push or open/update a PR without `--pr` or an explicit user ask.
- Prepare the branch or worktree before moving a tracked executable plan from `proposed` to `active`; make that transition only for an explicit implementation request.
- Do not expand a slice stub by inference; route through `plan` or the user.
- With `--single-commit`, validate per block but commit once after final review.
- With `--no-commit`, leave a tracked plan in `active` and report that lifecycle closure remains pending.
- PR or publication text must not reference local-only files, ignored files,
  raw sensitive output, or unpushed artifacts.

## Invocation Model

Accept natural language and referenced/attached files, issues, PRs, handoffs,
and chat context as source artifacts. Classify each potential plan before using
it: record its source, type, lifecycle state, parent, execution readiness, and
next route. Infer scope only from an executable artifact or explicit user
wording; ask when ambiguity blocks safe execution.

## Options

- `--scope <text>`: limit execution to a slice, section, task range, checklist
  item, or natural-language subset.
- `--no-commit`: implement without committing; leave changes in the working tree.
- `--single-commit`: commit once at the end instead of per block.
- `--worktree` / `--no-worktree`: force a separate worktree / force the current
  one if safe.
- `--base <branch>`: use the named base branch when creating a branch/worktree.
- `--plan-only`: produce or refine the execution plan, then stop before edits.
- `--pr`: after review and plan updates, use the `pr` skill to open or update
  PR(s). Without `--pr`, leave PR creation out of scope.

## Related Skills

Compose with, do not duplicate:

- `workflow-intake`: resuming from plans, handoffs, issues, unclear next steps.
- `agents-standard`: repository plan authority, lifecycle, and local-draft boundaries.
- `engineering-workflow`: classify feature, bug, existing plan, architecture,
  parallel workstreams.
- `agent-selection`: main chat vs subagents vs worktrees vs new thread.
- `incremental-delivery`: block sequencing, acceptance criteria, quality gates.
- `safety`: git operations, commits, worktrees, destructive commands, multi-repo.
- `git`: branch and commit workflow.
- `quality`: checks, commit standards, output hygiene.
- `pr`: only when `--pr` is present.
- Domain skills relevant to the repository, language, platform, or finding type.

## Aggregator Plans And Slice Workflow

Some plans are aggregators: a main plan tracking the status of multiple slices
with an embedded slice workflow convention. When the referenced plan exposes
such a convention, follow it explicitly instead of improvising:

1. Build the slice from the correct base branch (per the plan's convention or
   `--base`).
2. Run validation for the slice.
3. Open a review loop with review agents and the user.
4. For a tracked slice, close it only after implementation is committed,
   validated, and reviewed: move `active` to `implemented` and update its
   parent mission in the same change. `implemented` does not require a PR,
   merge, or release.
5. Record PR or merge references only when known, make the next slice explicit,
   and update consuming skills when the changed surface affects them.

If the aggregator contains only a stub summary of the slice (no scope, files,
or acceptance criteria), do not infer the full contract yourself. Recommend a
prior step with the `plan` skill to expand the stub, or ask the user, before
building.

## Execution Protocol

### 1. Intake

Read the source artifacts, then inspect repository state: current branch, base
branch, dirty tree, commits ahead of base, project rules, and validation
commands. When `.agents/AGENTS.md` exists, read it before applying runtime
fallbacks and record Plan Authority: source, type (`tracked`, `local`, or
`non-plan`), lifecycle, parent, execution readiness, and next route.

### 2. Worktree And Start

Prepare the selected branch or worktree before changing a tracked plan. Default
to the current worktree when safe; use a separate one for a read-only source
branch, unrelated local changes, parallel work, a high-risk plan, or
`--worktree`.

For an explicit request to implement a tracked, executable `proposed` plan,
then move it to `active` and update its matching `Status:` line. Leave local
drafts and scratch untouched. If a tracked slice is only a stub, return to
planning rather than infer its contract.

### 3. Execution Blocks

Preserve useful plan blocks; otherwise create independently reviewable and
testable blocks. For each block define: objective, files/surfaces likely to
change, in/out of scope, dependencies, relevant skills/subagents, minimum
validation, commit boundary, and acceptance evidence.

### 4. Subagents

Delegate bounded work that returns a distilled result: exploration, finding
inventory, source validation, design review, test investigation, independent
implementation blocks, final review of a non-trivial diff. The main agent stays
orchestrator and owns scope, safety decisions, commit boundaries, and
user-facing claims. When delegating, pass repository path, branch/worktree
path, source artifacts and scope, expected output, and validation commands.

### 5. Implement And Commit Per Block

1. Mark the block in progress.
2. Make focused changes only for that block.
3. Run targeted validation for the changed surface.
4. Inspect the diff and exclude unrelated, ignored, sensitive, or local-only
   files.
5. Commit the block with a conventional commit message, unless `--no-commit` is set.
6. Record validation evidence and remaining risk.

### 6. Final Review And Checks

- Review the full diff against the requested scope.
- Run final checks from project rules or package conventions; re-run after
  fixes.
- Use domain-specific review skills or review subagents when their triggers
  apply.
- Verify commits match the intended block boundaries.
- If a required check cannot run, state why and what evidence remains missing.

### 7. Plan Closure

Close a tracked `active` slice only after its implementation is committed,
validated, and reviewed. Move it to `implemented`, update its matching
`Status:` line, and update the parent mission in the same change. `implemented`
does not require a PR, merge, or release; PR and merge references are optional
evidence when known. With `--no-commit`, keep the plan `active` and report the
pending closure.

## Output

Keep the user updated at block boundaries. At the end, report:

- Scope completed
- Plan Authority: source, type, lifecycle, parent, readiness, and next route
- Worktree/branch used
- Commits created, grouped by block
- Validation commands and outcomes
- Reviews performed (agents and user loop, when applicable)
- Plan and consuming-skill updates made (including a tracked slice's parent
  mission update and any optional known PR/merge evidence)
- Whether tracked-plan closure is complete or pending (always pending with
  `--no-commit`)
- Whether a PR was created or intentionally left pending (default without
  `--pr`)
- Files or plan items intentionally not completed
- Remaining risks or source-platform rescans still pending
