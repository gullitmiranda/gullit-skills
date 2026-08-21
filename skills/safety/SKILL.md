---
name: safety
description: Git, command, Kubernetes, data, workspace, and temporary files safety rules. Use when committing, pushing, using kubectl, handling multi-repo workspaces, or performing destructive operations.
---

# Safety Rules

## Hard Rules

- Do not commit unless explicitly requested.
- Do not push unless explicitly requested; never push directly to main/master.
- Never commit to main/master unless explicitly requested.
- Never run `git reset --hard` without explicit user approval.
- Never add gitignored files to git (`git add`) — at most, show the command for the user to run themselves.
- Never commit files under `.agents/plans/` or `.cursor/plans/` — both are local-only plan paths; the latter is legacy compatibility input.
- Never execute `kubectl delete` or `kubectl apply`.
- Do not change git stage without being asked; never commit unstaged changes without explicit request.
- When splitting, stacking, or consolidating work from an existing feature/draft branch, never execute the mission on the source branch. Create a new working branch (or worktree) from the agreed base and treat the source branch as read-only input.

## Git

- In repos with Trunk git hooks, close stdin on `git commit` by appending `</dev/null` to prevent hook hangs in pseudo-terminals. If Trunk still appears stuck or logs `Socket closed`, `Connection refused`, or `Daemon stopped`, use `trunk daemon shutdown` only as fallback recovery before retrying the commit.
- Always create feature branches for changes; use `/git-branch` for safe branch creation. `/commit` automatically creates a feature branch when on main/master.
- For incremental delivery, branch-split, or PR-stack work, create the delivery branch/worktree before editing anything (see `incremental-delivery/SKILL.md` for the full protocol — slice mapping, cherry-picking, validation per increment).
- Verify branch before committing; validate conventional commit format; show what will be committed before execution.
- Always create pull requests for main branch changes; use `/pr-create` for safe PR creation; verify the remote branch exists before pushing.

## Destructive Operations & Backups

- Always create backups before destructive operations; use git stash for uncommitted changes.
- Use `/git-reset` for safe reset with backup.
- Document recovery procedures and test backup restoration.

## Kubernetes

- Use `/k8s-check` for safe inspection, `/k8s-validate` for manifest validation, `/k8s-diff` for change preview.

## Commands

- Prefer terminal commands over GUI operations when possible.

## Multi-Repository Workspaces

- Always check the current working directory and understand repository boundaries; never assume a single git repository in a multi-repo workspace.
- Verify which repository an operation targets before execution; navigate to the correct repository directory before running git operations.
- When working with staged changes, identify which specific repository they belong to.
- Treat each repository as a separate entity with its own git state.
- Use non-destructive commands first (`git stash`, `git log`) to understand the situation.
- Ask for clarification when workspace structure is unclear; confirm the target repository before running git commands.

## Temporary Files

- Use temporary directories (`./tmp` or system tmp); clean up temporary files after use; never commit them to version control.
