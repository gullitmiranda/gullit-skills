---
name: git
description: Safe Git workflow - commit with conventional format and branch safety, create branches, reset with backup, and multi-repo status. Use when committing, creating branches, resetting, or checking git status in multi-repo workspaces.
---

# /commit - Smart Git Commit

## Steps

1. **Branch safety**: if on main/master and `/commit` was invoked without `--main`, automatically create a feature branch from the detected changes (see Auto Branch Creation) before committing. `--main` allows committing directly to main/master — emergency fixes only.
2. **Analyze changes**: `git status` and `git diff --cached` (or `git diff` for all changes with `--all`). Detect the conventional commit type (`feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`) and any issue references.
3. **Generate message**: `<type>(<scope>): <description>` — concise, present tense, imperative. Include issue references only when present in the prompt or staged content: GitHub Issues by default (`#123` or `owner/repo#123`); Linear `TEAM-123` IDs only when explicitly referenced.
4. **Commit**: heredoc for multi-line messages; commit staged changes only unless `--all` (stages everything). Confirm with `git log`.

## Auto Branch Creation

When on main/master without `--main`, create a branch named by change type before committing:

- `feature/<type>-<short-description>` for features
- `fix/<short-description>` for fixes
- `chore/<short-description>` for chores
- `docs/<short-description>` for docs

## Trunk-backed Commit Safety

When the repository has Trunk configured (`.trunk/trunk.yaml` exists), agent-driven commits must not hang on interactive hook prompts:

1. **Always run Trunk first, before committing** — fix findings before the hook ever runs:
   - `trunk fmt --ci --upstream HEAD --no-progress </dev/null`
   - `trunk check --ci --upstream HEAD --no-progress </dev/null`
   The `--ci` flag makes Trunk fail fast instead of prompting `Continue anyway? (Y/n)` — an interactive prompt in a non-interactive terminal hangs the commit indefinitely.
2. **Every `git commit` runs with stdin closed and a timeout** (`</dev/null` + `timeout_ms`), trunk or not — zero cost when healthy, and it prevents the pathological hang: hook stdin saved via `cat` waits forever for EOF in agent pseudo-terminals. If a commit hangs, a hook is waiting for input — never leave it hanging.
3. **Escape hatch: `--no-verify`** when the hook still blocks after a clean `trunk check`. Always declare it explicitly in the response ("committed with `--no-verify` because …") — a visible bypass, never a silent one. Do not use `trunk daemon shutdown` as a commit workaround.

## Safety Checks

- Never commit to main/master without explicit approval (unless `--main`).
- Never commit unstaged changes without being asked (unless `--all`).
- Never push automatically.
- Always show what will be committed before executing.
- Automatically create a feature branch when on main/master.
- `--main` bypasses main/master protection — emergency fixes only.

## Worktree Workflow

When instructed to use a "nova WT", "WT separada", or "git paralelo", always
use `git worktree add` to create a separate worktree and do all work there.
Never change the primary worktree.

When instructed to "finalizar a worktree", "puxar para a main worktree",
"traga estas mudancas para main worktree", or "/main-worktree": in the primary
worktree, update `main` (git pull), create/switch to the feature branch, and
rebase the worktree commits onto the updated `main`. Then remove the secondary
worktree. The branch stays as a feature branch - do NOT merge into `main`.
The goal is to continue working on the feature branch from the primary worktree
with `main` as a fresh base. NEVER merge the feature branch into `main`.

## Merge and Init Defaults

- Always use `git merge --no-ff` when merging branches. Only use fast-forward when the user explicitly requests it.
- Initialize new Git projects on `main` by default.
- Respect ignored files and explicitly mention ignored-file handling in action summaries.

## Issue Linking

- Default tracker is GitHub Issues. Reference with `#123` (same repo) or `owner/repo#123` (cross-repo); prefer full markdown URLs (`[#123: Title](https://github.com/owner/repo/issues/123)`) when the title is known.
- Use magic words like `Closes`, `Fixes`, `Resolves` so GitHub auto-closes the issue on merge.
- Linear is supported only when explicitly referenced (URL or `TEAM-123` ID); never invent a Linear reference.

## Arguments

- `/commit` — staged changes only (default)
- `/commit --all` — stage and commit all changes (unstaged + staged)
- `/commit --main` — commit directly to main/master (emergency fixes only)
- `/commit --main --all` — stage all and commit directly to main/master (emergency fixes only)

---

# /git-branch

Safe branch creation following project conventions.

1. Create from main/master unless specified otherwise; validate the base exists and no conflicting branch name exists.
2. Naming: `feature/`, `fix/`, `chore/`, `hotfix/`, `docs/`, `refactor/`, `test/` + short description. Suggest a valid name if the given one is invalid.
3. Switch to the new branch after creation.

---

# /git-reset

Safe reset with automatic backup and recovery.

1. Use `git status` and `git log` to understand current state first.
2. Stash uncommitted changes before any destructive operation.
3. Reset types: `--soft` (keep staged), `--mixed` (keep in working dir, default), `--hard` (discard all — requires explicit user approval).
4. Provide recovery instructions (restore from stash, `git reflog`) after destructive resets.

---

# /git-status

Multi-repository aware status check.

1. Never assume a single git repository in a multi-repo workspace. Identify repository boundaries and which repo each change belongs to.
2. Show status per repository found in the workspace; highlight cross-repository dependencies or conflicts.
3. When workspace structure is unclear, ask for clarification and confirm the target repository before running git commands. Use non-destructive commands first (`git stash`, `git log`) to understand the situation.
4. Non-destructive operations only.
