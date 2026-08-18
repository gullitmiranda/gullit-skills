---
name: build-plan
description: Build referenced plans into committed, validated implementation work. Use when the user asks to execute, implement, build, or continue a plan, slice, handoff, checklist, roadmap item, or scoped subset of a plan with autonomous execution, commits per block, subagents, reviews, and final checks.
---

# Build Plan

Orchestrator that turns planning artifacts into completed implementation work:
reads the plan context, applies relevant domain skills, uses subagents where
useful, commits each completed block by default, and closes with reviews and
validation.

## Invocation Model

Accept natural language and referenced/attached files, issues, PRs, handoffs,
and chat context as source artifacts. Infer a primary plan and scope from the
user's wording; ask only when ambiguity blocks safe execution.

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
4. Update the aggregator plan at the end: mark the slice completed, record
   PR/merge references, and make the next slice explicit.
5. Update consuming skills when the changed surface affects them.

If the aggregator contains only a stub summary of the slice (no scope, files,
or acceptance criteria), do not infer the full contract yourself. Recommend a
prior step with the `plan` skill to expand the stub, or ask the user, before
building.

## Execution Protocol

### 1. Intake

Read the source artifacts, then inspect repository state: current branch, base
branch, dirty tree, commits ahead of base, project rules, and validation
commands.

### 2. Worktree

Default to the current worktree when safe. Use a separate one only with a
concrete reason: source branch that must stay read-only, unrelated local
changes, parallel work, high-risk plan, or `--worktree`.

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
5. Commit the block with a conventional commit message.
6. Record validation evidence and remaining risk.

### 6. Final Review And Checks

- Review the full diff against the requested scope.
- Run final checks from project rules or package conventions; re-run after
  fixes.
- Use domain-specific review skills or review subagents when their triggers
  apply.
- Verify commits match the intended block boundaries.
- If a required check cannot run, state why and what evidence remains missing.

## Hard Rules

- Never implement directly on `main`/`master` unless explicitly requested;
  create or switch to a feature branch first.
- Do not commit ignored files or local-only planning artifacts unless the user
  asks and the repository versions them.
- Do not push or open/update a PR without `--pr` or an explicit user ask.
- Do not expand a slice stub by inference; route through `plan` or the user.
- With `--single-commit`, validate per block but commit once after final review.
- PR or publication text must not reference local-only files, ignored files,
  raw sensitive output, or unpushed artifacts.

## Output

Keep the user updated at block boundaries. At the end, report:

- Scope completed
- Worktree/branch used
- Commits created, grouped by block
- Validation commands and outcomes
- Reviews performed (agents and user loop, when applicable)
- Plan and consuming-skill updates made (for aggregator plans: slice status,
  PR/merge refs, next slice)
- Whether a PR was created or intentionally left pending (default without
  `--pr`)
- Files or plan items intentionally not completed
- Remaining risks or source-platform rescans still pending
