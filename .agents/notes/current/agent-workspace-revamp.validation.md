# Agent workspace revamp validation

Status: partially validated

## Completed checks

- All 46 current `SKILL.md` files have a unique frontmatter `name` matching their source directory.
- An isolated install from a conventional local clone discovered and linked all 38 current skills, including `agent-workspace`, `agent-notes`, `work-intake`, `work-plan`, `build-plan`, `work-closeout`, and `cursor-project-path-migration`, without legacy wrappers.
- An isolated migration fixture moved a local plan and its `.archived/` history from the legacy plan directory to `.agents/plans/` unchanged, then created the documented relative compatibility symlink. The fixture also confirmed that both the plan tree and compatibility symlink are ignored.
- Changed Markdown files passed local-link checks, whitespace checks, and project diagnostics.


## Confirmed limits

- The current `ai-skills` CLI does not accept a Git worktree as a local source because it does not recognize the worktree's `.git` file. Validation used a disposable conventional clone instead.
- The CLI can install distinct legacy and public names together, but it still lacks the migration and reconciliation behavior needed to move existing installed skills to nested source homes safely.
- Public-name simplification for `work-plan` and `build-plan` is intentionally deferred to the proposed post-migration naming review.

## Unrelated baseline finding

A repository-wide Markdown link scan found pre-existing broken example or reference links outside the changed surface. Changed Markdown files pass the same check. The unrelated links were not modified by this revamp.

## Next action

Keep source-home moves deferred until the separate CLI work provides a declared dependency manifest, installation migration, rename and retirement reconciliation, collision handling, worktree-source support, and end-to-end coverage.
