---
name: build-plan
description: Build referenced plans into committed, validated implementation work. Use when the user asks to execute, implement, build, or continue a plan, slice, handoff, checklist, roadmap item, or scoped subset of a plan with autonomous execution, commits per block, subagents, reviews, and final checks.
---

# Build Plan

Use this skill to turn one or more planning artifacts into completed implementation
work. The skill is an orchestrator: it reads the plan context, chooses the safest
execution shape, applies relevant domain skills, uses subagents where useful,
commits each completed block by default, and closes with reviews and validation.

## Invocation Model

Accept natural language first. The user may reference files directly instead of
using flags:

```text
/build-plan @plans/main.plan.md @plans/slice-11.plan.md
Execute only the dependency and scanner blocks.
```

Treat referenced files, attached files, open files, issues, PRs, handoffs, and
chat context as candidate source artifacts. Identify their roles:

- Primary plan
- Related plan or handoff
- Scope constraint
- Acceptance criteria
- Reference documentation

Ask only when ambiguity blocks safe execution. Otherwise infer a reasonable
primary plan and scope from the user's wording.

## Options

Recognize these optional controls when present:

- `--scope <text>`: limit execution to a slice, section, task range, checklist
  item, or natural-language subset.
- `--no-commit`: implement without committing; leave changes in the working tree.
- `--single-commit`: commit once at the end instead of per block.
- `--worktree`: force a separate worktree.
- `--no-worktree`: force the current worktree if safe.
- `--base <branch>`: use the named base branch when creating a branch/worktree.
- `--plan-only`: produce or refine the execution plan, then stop before edits.

By default, `build-plan` means implementation is requested and commits are
authorized per block. If the user's wording asks only for analysis, planning, or
review, do not edit or commit.

## Related Skills

Before implementation, compose with the skills that fit the task:

- `workflow-intake`: when resuming from plans, handoffs, issues, or unclear next
  steps.
- `engineering-workflow`: to classify feature, bug, existing plan, architecture,
  or parallel workstreams.
- `agent-selection`: to choose main chat, subagents, worktrees, terminal agents,
  or a new thread.
- `incremental-delivery`: for block sequencing, acceptance criteria, and quality
  gates per increment.
- `safety`: before git operations, commits, worktrees, destructive commands, or
  multi-repository work.
- `git`: for branch and commit workflow.
- `quality`: for checks, commit standards, PR-quality expectations, and output
  hygiene.
- Domain skills relevant to the repository, language, platform, or source
  finding type.

Do not duplicate those skills. Load and follow them when their triggers apply.

## Execution Protocol

### 1. Intake

Read the source artifacts first. Then inspect enough repository state to know:

- Current repository and branch
- Base branch, if known
- Dirty working tree and staged files
- Existing commits ahead of base
- Relevant local project rules, skills, and validation commands
- Whether referenced plans are local-only inputs or versioned deliverables

Do not commit ignored files or local-only planning artifacts unless the user
explicitly requests that and the repository expects them to be versioned.

### 2. Decide Current Worktree vs Separate Worktree

Use the current worktree by default when it is safe.

Stay in the current worktree when:

- The current branch is already an appropriate implementation branch, or a new
  branch can be created in place before editing.
- Local changes are clean or clearly part of this work.
- The plan is not expected to run in parallel with other active work.
- Tooling limitations make a separate worktree unnecessarily costly.

Use a separate worktree when there is a concrete reason:

- Current branch is a source branch that must remain read-only.
- Current working tree has unrelated or conflicting local changes.
- The work should run in parallel with ongoing edits.
- The plan is high-risk, broad, or likely to need rollback isolation.
- The user passes `--worktree`.

If the user passes `--no-worktree`, stay in the current worktree unless doing so
would violate safety rules. Explain the blocker and ask before continuing.

Never implement directly on `main` or `master` unless the user explicitly
requests that exact behavior. Create or switch to a feature branch first.

### 3. Build The Execution Blocks

If the plan already has useful blocks, preserve them. If not, create blocks that
are independently reviewable and testable.

For each block, define:

- Objective
- Files or surfaces likely to change
- In-scope and out-of-scope work
- Dependencies
- Relevant skills/subagents
- Minimum validation
- Commit boundary
- Acceptance evidence

Prefer vertical blocks that produce coherent behavior. Avoid mixing unrelated
refactors, dependency changes, docs, and feature behavior unless the plan makes
that coupling necessary.

### 4. Use Subagents Deliberately

Use subagents for bounded work that can return a distilled result:

- Codebase exploration
- Finding inventory
- Source validation
- Architecture or design review
- Test and validation investigation
- Independent implementation blocks
- Final review of a non-trivial diff

Keep the main agent as orchestrator. It owns scope, safety decisions, commit
boundaries, final synthesis, and user-facing claims.

When delegating, pass a compact context that includes:

- Repository path
- Branch/worktree path
- Source artifacts and scope
- Expected output
- Sensitive-output restrictions, if any
- Validation commands or evidence required

Do not use subagents when the task is small and linear.

### 5. Implement And Commit Per Block

For each block:

1. Mark the block in progress.
2. Make focused changes only for that block.
3. Run targeted validation for the changed surface.
4. Inspect the diff and exclude unrelated, ignored, sensitive, or local-only files.
5. Commit the block with a conventional commit message.
6. Record validation evidence and remaining risk.

If `--no-commit` is present, stop after validation with changes left uncommitted.
If `--single-commit` is present, validate per block but commit only once after the
final review.

Do not push or open/update a PR unless the user explicitly asks.

### 6. Final Review And Checks

Before finishing:

- Review the full diff against the requested scope.
- Run relevant final checks from project rules or package conventions.
- Use domain-specific review skills or review subagents when their trigger
  conditions are met.
- Re-run failed focused checks after fixes.
- Verify commits match the intended block boundaries.
- Check that PR or publication text, if created, does not reference local-only
  files, ignored files, raw sensitive output, or unpushed artifacts.

If a required check cannot run, state why and what evidence remains missing.

## Output

During execution, keep the user updated at block boundaries. At the end, report:

- Scope completed
- Worktree/branch used
- Commits created, grouped by block
- Validation commands and outcomes
- Reviews performed
- Files or plan items intentionally not completed
- Remaining risks or source-platform rescans still pending

Do not over-report raw command output. Summarize the evidence that matters.
