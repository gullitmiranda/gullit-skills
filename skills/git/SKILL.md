---
name: git
description: Safe Git workflow - commit with conventional format and branch safety, create branches, reset with backup, and multi-repo status. Use when committing, creating branches, resetting, or checking git status in multi-repo workspaces.
---

# /commit - Smart Git Commit

## Overview

You are a git commit specialist that creates conventional commits with automatic type detection and safety checks.

## Steps

1. **Branch Safety Check**:
   - Check if currently on main/master branch
   - If yes and using `/commit` (without `--main` flag), automatically create a feature branch based on the changes detected
   - If using `/commit --main`, allow direct commit to main/master branch (emergency fixes only)

2. **Analyze Changes**:
   - Run `git status` and `git diff --cached` (or `git diff` for all changes if `--all` flag is used)
   - Detect conventional commit type from changes:
     - `feat`: New features, components, functionality
     - `fix`: Bug fixes, error corrections
     - `chore`: Dependencies, build, config, tooling
     - `docs`: Documentation changes
     - `style`: Code formatting, style changes
     - `refactor`: Code restructuring without behavior change
     - `test`: Adding or updating tests
   - Check for Linear issue references in commit message or staged changes

3. **Generate Commit Message**:
   - Format: `<type>(<scope>): <description>`
   - Scope should be component/area affected (optional)
   - Description should be concise and clear
   - Use present tense, imperative mood
   - Include Linear issue references (e.g., `ENG-123`, `PROJ-456`) in description for auto-linking

4. **Execute Commit**:
   - Use heredoc format for multi-line commit messages
   - Commit only staged changes (unless `--all` flag is used)
   - If `--all` flag is used, stage and commit all changes (unstaged + staged)
   - Confirm successful commit with git log

5. **Validation**:
   - Ensure commit follows conventional format
   - Verify only intended changes were committed

## Auto Branch Creation

When on main/master branch and using `/commit` (without `--main` flag):

1. **Analyze Changes**: Detect commit type from staged/unstaged changes
2. **Generate Branch Name**:
   - For features: `feature/<type>-<short-description>`
   - For fixes: `fix/<short-description>`
   - For chores: `chore/<short-description>`
   - For docs: `docs/<short-description>`
3. **Create Branch**: `git checkout -b <generated-branch-name>`
4. **Proceed with Commit**: Continue with normal commit process

**Example Branch Names**:

- `feature/feat-user-auth` (for new authentication feature)
- `fix/login-bug` (for login bug fix)
- `chore/update-deps` (for dependency updates)

## Safety Checks

- Never commit to main/master without explicit approval (unless using `--main` flag)
- Never commit unstaged changes without being asked (unless using `--all` flag is used)
- Never push automatically
- Always validate conventional commit format
- Always show what will be committed before executing
- Include Linear issue references for GitHub auto-linking
- Automatically create feature branch when on main/master
- `--main` flag bypasses main/master protection - use only for emergency fixes

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

## Examples

With staged changes to authentication system:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add JWT token validation middleware

- Implement token verification for protected routes
- Add error handling for expired tokens
- Update authentication flow documentation

Closes ENG-123
EOF
)"
```

With all changes (including unstaged):

```bash
# This will stage and commit all changes
/commit --all
```

Emergency fix directly to main branch:

```bash
# This bypasses main/master branch protection for emergency fixes
/commit --main
```

Emergency fix with all changes to main branch:

```bash
# This bypasses main/master branch protection and stages all changes
/commit --main --all
```

Auto branch creation when on main/master:

```bash
# When on main branch with staged changes for new feature
# Command automatically creates: feature/feat-user-auth
# Then switches to new branch and commits
/commit

# When on main branch with bug fix changes
# Command automatically creates: fix/login-validation
# Then switches to new branch and commits
/commit --all
```

Linear Integration:

- Include Linear issue IDs (e.g., `ENG-123`, `PROJ-456`) in commit messages
- Use magic words like "Closes", "Fixes", "Resolves" followed by issue ID
- Linear will auto-link commits to issues when GitHub integration is enabled
- Reference: https://linear.app/docs/github#enable-autolink

## Arguments

Arguments: $ARGUMENTS (optional: additional commit message details)

- Use `/commit` for staged changes only (default behavior)
- Use `/commit --all` to stage and commit all changes (unstaged + staged)
- Use `/commit --main` to commit directly to main/master branch (emergency fixes only)
- Use `/commit --main --all` to stage and commit all changes directly to main/master branch (emergency fixes only)

---

# /git-branch

## Description

Safe branch creation following project conventions and best practices.

## Workflow

1. Create feature branches from main/master unless specified otherwise
2. Use descriptive branch names following project conventions
3. Ensure branch is created from correct base branch
4. Switch to new branch after creation
5. Provide feedback on branch naming and setup

## Naming Conventions

- `feature/description` - New features
- `fix/description` - Bug fixes
- `chore/description` - Maintenance tasks
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

## Examples

```bash
# Create feature branch
/git-branch feature/user-authentication

# Create fix branch
/git-branch fix/login-bug

# Create chore branch
/git-branch chore/update-dependencies
```

## Safety Features

- Prevents creation of branches with invalid names
- Validates base branch exists
- Checks for existing branch conflicts
- Provides naming suggestions if invalid

## Integration

- Works with Linear issue references
- Integrates with PR creation workflow
- Supports multi-repository workspaces

---

# /git-reset

## Description

Safe reset with automatic backup and recovery options.

## Workflow

1. Create backup/stash before any destructive operations
2. Use git status and git log to understand current state
3. Offer different reset options (soft, mixed, hard) with explanations
4. Always confirm before executing destructive operations
5. Provide recovery instructions if something goes wrong

## Reset Types

- **Soft**: Keep changes in staging area
- **Mixed**: Keep changes in working directory (default)
- **Hard**: Discard all changes (destructive)

## Safety Measures

- Always stash uncommitted changes first
- Never run without understanding current state
- Require explicit user approval for --hard reset
- Create automatic backups before destructive operations
- Provide recovery instructions

## Examples

```bash
# Safe soft reset
/git-reset --soft HEAD~1

# Safe mixed reset (default)
/git-reset HEAD~1

# Safe hard reset with confirmation
/git-reset --hard HEAD~1

# Reset to specific commit
/git-reset --soft abc1234
```

## Backup Strategy

- Create stash before destructive operations
- Save current state information
- Provide rollback instructions
- Document what will be lost

## Recovery Options

- Restore from stash
- Recover from backup
- Use git reflog for commit recovery
- Provide step-by-step recovery guide

## Integration

- Works with multi-repository workspaces
- Integrates with branch protection
- Supports Linear issue references
- Compatible with PR workflow

---

# /git-status

## Description

Multi-repository aware status check with comprehensive workspace analysis.

## Workflow

1. Check current working directory and understand repository boundaries
2. Never assume single git repository in multi-repo workspace
3. Identify which specific repository changes belong to
4. Show status for current repo and detect other repos in workspace
5. Provide clear indication of which repo each change belongs to

## Multi-Repository Handling

- When working with staged changes, identify which specific repository they belong to
- Provide clear indication of repository boundaries
- Show status for each repository found in workspace
- Highlight any cross-repository dependencies or conflicts

## Error Prevention

- Always ask for clarification when workspace structure is unclear
- Confirm target repository before running git commands
- Use non-destructive git commands first (git stash, git log) to understand situation

## Output Format

```
Repository: /path/to/repo1
  Branch: main
  Status: clean
  Staged: 2 files
  Modified: 1 file
  Untracked: 3 files

Repository: /path/to/repo2
  Branch: feature/new-feature
  Status: dirty
  Staged: 0 files
  Modified: 2 files
  Untracked: 0 files
```

## Examples

```bash
# Check current repository status
/git-status

# Check specific repository
/git-status /path/to/specific/repo

# Check all repositories in workspace
/git-status --all
```

## Safety Features

- Non-destructive operations only
- Clear repository identification
- Conflict detection and reporting
- Workspace boundary awareness
