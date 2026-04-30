---
name: safety
description: Git, command, Kubernetes, data, workspace, and temporary files safety rules. Use when committing, pushing, using kubectl, handling multi-repo workspaces, or performing destructive operations.
---
# Safety Rules

## Git Safety

### Absolute Rules (Cannot be broken)

- Do not commit unless explicitly requested
- Do not push unless explicitly requested
- Never commit to main/master branch unless explicitly requested
- Never run `git reset --hard` without explicit user approval
- Never add gitignored files to git (`git add`) — at most, show the command for the user to run themselves
- **Never commit files under `.cursor/plans/`** — they are local-only/gitignored; this breaks the user's setup and has been corrected multiple times
- When splitting, stacking, or consolidating work from an existing feature/draft
  branch, **never execute the mission on the source branch**. First create a new
  working branch (or worktree) from the agreed base and treat the source branch
  as read-only input.
- **Never `git add`/`commit`/`push` inside `~/.ai-skills/repos/`**. That path is
  the ai-skills CLI cache (managed clone), not a working repo. Before any git
  write op, resolve the cwd (`pwd -P`) and check for `.ai-skills-cache` at the
  repo root or any `~/.ai-skills/repos/` prefix. If detected, stop and either
  edit in the source clone (e.g. `~/code/gullit/<repo>/`) or use
  `ai-skills publish <repo>` when available.

### Core Safety Guidelines

- Do not change git stage without being asked
- Do not make commits without reviews unless explicitly requested
- Always create feature branches for changes
- Use `/git-branch` command for safe branch creation
- `/commit` command automatically creates feature branch when on main/master
- For incremental delivery, branch-split, or PR-stack work, create the delivery
  branch/worktree before editing anything
- Verify branch before committing
- Never commit unstaged changes without explicit request
- Always validate conventional commit format
- Create backups before destructive operations
- Show what will be committed before execution
- Never push directly to main/master
- Always create pull requests for main branch changes
- Use `/pr-create` command for safe PR creation
- Verify remote branch exists before pushing

## Command Safety

### Shell Safety

- Prefer terminal commands over GUI operations when possible

### Kubernetes Safety

- Never execute `kubectl delete` or `kubectl apply`
- Use `/k8s-check` for safe inspection
- Use `/k8s-validate` for manifest validation
- Use `/k8s-diff` for change preview

### Git Destructive Operations

- Never run `git reset --hard` without explicit approval
- Use `/git-reset` for safe reset with backup
- Always create stash before destructive operations
- Provide recovery instructions

## Data Safety

- Always create backups before destructive operations
- Use git stash for uncommitted changes
- Document recovery procedures
- Test backup restoration

## Workspace Safety

### Multi-Repository Handling

- Always check current working directory and understand repository boundaries
- Never assume single git repository when working in multi-repo workspace
- Always verify which repository operations are targeting before execution
- When working with staged changes, identify which specific repository they belong to
- Navigate to correct repository directory before running git operations
- Treat each repository as separate entity with its own git state

### Error Prevention

- Always ask for clarification when workspace structure is unclear
- Confirm target repository before running git commands
- Use non-destructive commands first (git stash, git log) to understand situation

## Temporary Files Safety

- When creating temporary files, use temporary directories (`./tmp` or system tmp)
- Automatically clean up temporary files after use
- Never commit temporary files to version control
