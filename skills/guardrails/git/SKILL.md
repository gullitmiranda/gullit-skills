---
name: git
description: >-
  Safe Git workflow — conventional commits, branch safety, reset with backup, multi-repo status, and Trunk-safe agent commits (CI=1 / --ci -y / no PTY hangs). Use when committing, creating branches, resetting, checking git status, or before any agent git commit in a Trunk-enabled repo.
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

Applies to **every** repository with Trunk (`.trunk/trunk.yaml` or `core.hooksPath` pointing at Trunk git-hooks) — not only one project.

Trunk's pre-commit hook opens `/dev/tty` when stderr looks like a TTY. Agent runners often allocate a PTY, so the hook becomes interactive (Prettier "autoformat?", `Continue anyway?`) and **hangs forever**. Closing stdin alone is not enough if stderr is still a TTY.

### Mandatory sequence before every agent `git commit`

1. **Load this skill** (`git`) before committing when Trunk may be present.
2. **Format and check non-interactively first** (so the hook has nothing interactive left to ask):
   ```bash
   CI=1 trunk fmt --ci -y --upstream HEAD --no-progress </dev/null
   CI=1 trunk check --ci -y --upstream HEAD --no-progress </dev/null
   ```
   - `--ci` → fail fast, no "Continue anyway?"
   - `-y` → apply autofixes without prompting
   - `CI=1` → mark the environment as non-interactive for tooling
3. **Stage any files Trunk rewrote**, then commit.
4. **Every `git commit` must**:
   - close stdin: `</dev/null`
   - set `CI=1 GIT_TERMINAL_PROMPT=0`
   - use a harness timeout (`timeout_ms` / equivalent); if it hits the timeout, treat it as a hook hang — kill and recover, never leave spinning
   - prefer a non-PTY shell for the commit command when the harness allows it (PTY + Trunk hook = hang risk)
5. **Escape hatch: `--no-verify`** only after a clean `trunk fmt` + `trunk check` above, when the hook still blocks. Always say so explicitly ("committed with `--no-verify` because …"). Never silent. Do not use `trunk daemon shutdown` as a commit workaround.

### Do not

- Rely on the pre-commit hook to format for you during agent commits.
- Run `trunk check --fix` or `trunk fmt` **without** `--ci -y` in agent sessions.
- Leave a commit command running for minutes hoping the hook finishes.

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

- Use `git merge --no-ff` for branch merges unless the user explicitly requests fast-forward. For post-merge synchronization, use the PR workflow's `git pull --ff-only` protocol.
- After a remote PR or stack merge is confirmed, reconcile the local base before ending the workflow; never force-sync a dirty or diverged worktree.
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
