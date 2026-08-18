---
name: workspace-status
description: Multi-repository workspace status overview and analysis. Use when checking workspace state, understanding repo boundaries, or before running git operations in multi-repo workspaces.
---

# Workspace Status

Show git state for every repository in a multi-repo workspace, respecting
each repo as an independent unit.

## Hard Rules

- Never assume a single git repository in a multi-repo workspace.
- Always verify which repository a git operation targets before running it.
- Navigate to the correct repository directory before running git commands.
- Ask for clarification when workspace structure is unclear.
- Use non-destructive git commands first (`git stash`, `git log`) to
  understand the situation.

## Procedure

1. Identify all git repositories in the workspace (check for `.git` dirs).
2. For each repo, report: path, branch, status (clean/dirty), staged/modified
   counts, last commit time, remote tracking branch.
3. When a `WORKSPACE.md` exists in the workspace root or any ancestor, consult
   it to confirm each repo belongs there. Report repos whose location conflicts
   with the applicable rules (e.g. a primary clone inside a reserved worktree
   area). See the `workspace-topology` skill for hierarchical rule resolution.
4. Highlight cross-repository dependencies or conflicts when found.
