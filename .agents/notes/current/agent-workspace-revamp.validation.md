# Agent workspace revamp validation

Status: partially validated

## Completed checks

- All 46 current `SKILL.md` files have a unique frontmatter `name` matching their source directory.
- An isolated install from a conventional local clone discovered and linked all 46 skills, including `agent-workspace`, `agent-notes`, `work-intake`, `work-plan`, `build`, `work-closeout`, and `cursor-project-path-migration`.
- An isolated migration fixture moved a local plan and its `.archived/` history from the legacy plan directory to `.agents/plans/` unchanged, then created the documented relative compatibility symlink. The fixture also confirmed that both the plan tree and compatibility symlink are ignored.
- Changed Markdown files passed local-link checks, whitespace checks, and project diagnostics.
- Cursor, Zed, terminal/ACP, and Pi adapter documents state that `work-plan` and `build` are public skill names and do not assume `/plan` or `/build` is a universal slash command.

## Confirmed limits

- The current `ai-skills` CLI does not accept a Git worktree as a local source because it does not recognize the worktree's `.git` file. Validation used a disposable conventional clone instead.
- The CLI can install distinct legacy and public names together, but it still lacks the migration and reconciliation behavior needed to move existing installed skills to nested source homes safely.
- No supported runtime in this repository test environment can load the isolated installation and execute slash commands. Runtime-specific slash-command behavior remains documented rather than dynamically verified.

## Unrelated baseline finding

A repository-wide Markdown link scan found pre-existing broken example or reference links outside the changed surface. Changed Markdown files pass the same check. The unrelated links were not modified by this revamp.

## Next action

Keep source-home moves deferred until the separate CLI work provides a declared dependency manifest, installation migration, rename and retirement reconciliation, collision handling, worktree-source support, and end-to-end coverage.
