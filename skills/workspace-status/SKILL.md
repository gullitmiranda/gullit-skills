---
name: workspace-status
description: Multi-repository workspace status overview and analysis. Use when checking workspace state, understanding repo boundaries, or before running git operations in multi-repo workspaces.
---
# Workspace Status Command

## Description

Multi-repository workspace status overview with comprehensive analysis.

## Workflow

1. Always check current working directory and understand repository boundaries
2. Never assume single git repository when working in multi-repo workspace
3. Always verify which repository operations are targeting
4. Identify which specific repository changes belong to
5. Navigate to correct repository directory before running git operations
6. Treat each repository as separate entity with its own git state

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
Workspace: /path/to/workspace
Repositories: 3

Repository 1: /path/to/repo1
  Branch: main
  Status: clean
  Last commit: 2 hours ago
  Remote: origin/main

Repository 2: /path/to/repo2
  Branch: feature/new-feature
  Status: dirty
  Staged: 2 files
  Modified: 1 file
  Last commit: 1 hour ago
  Remote: origin/feature/new-feature

Repository 3: /path/to/repo3
  Branch: develop
  Status: clean
  Last commit: 3 hours ago
  Remote: origin/develop
```

## Examples

```bash
# Check workspace status
/workspace-status

# Check specific workspace
/workspace-status /path/to/workspace

# Detailed status with file changes
/workspace-status --detailed
```

## Features

- Multi-repository detection
- Cross-repository dependency analysis
- Conflict detection and reporting
- Workspace boundary identification
- Git state analysis per repository

## Integration

- Works with all git commands
- Integrates with PR workflow
- Supports Linear issue tracking
- Compatible with branch management
