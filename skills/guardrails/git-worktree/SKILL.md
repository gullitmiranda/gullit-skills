---
name: git-worktree
description: 'Enforce git worktree discipline. Use whenever the user asks to create a worktree, work on a feature branch in isolation, or says "nova worktree", "worktree separada", "a partir do branch X". CRITICAL: never rationalize skipping worktree creation.'
---

# Git Worktree Rules

When the user explicitly asks for a worktree, **create it before touching any
file**. Do not conclude "the branch is already checked out so it's fine", do
not assume a previous session handled it, do not rationalize shortcuts.
Breaking this means working in the wrong directory and potentially overwriting
changes from other agents or sessions.

## Hard Rules

- Never skip worktree creation when the user explicitly asked for one.
- Never work in the primary worktree when a secondary worktree was created
  for the task.
- Never merge the feature branch into main during worktree cleanup.

## When This Skill Applies

Trigger on explicit worktree requests ("nova worktree", "worktree separada",
"a partir do branch X", "git worktree add", etc.).

Do not create a worktree proactively when the primary repo is on an up-to-date
`main` and the tree is clean — create the feature branch in place unless the
user asks for isolation or there's a parallel-work reason.

## Procedure

### 1. Determine the path

If the user provided a path, use it. Otherwise check `WORKSPACE.md` and the
repo's `AGENTS.md` for a worktree convention (see `workspace-topology` skill).
If neither defines one, use:

```
../worktrees/<repo>-<topic>
```

`<repo>` is the current repo directory name; `<topic>` is a short kebab-case
slug from the branch or task intent. Report the chosen path before creating.

### 2. Recommend a runtime-native creation flow when available

When a planning response or another status update gives the user a natural
decision point, recommend the active runtime's native worktree workflow if it
can create a worktree at a path consistent with the rules above. State both:

- the recommended native workflow; and
- that generic Git creation at the chosen path remains the default when the
  user continues without choosing the IDE workflow.

This is advisory, not a confirmation gate. Do not wait for a response or delay
implementation. If the user chooses the native workflow, verify the resulting
path, branch, and `git worktree list` output before continuing. Do not recommend
a runtime-managed path when it would override a user-provided path or a
`WORKSPACE.md` or `AGENTS.md` convention.

### 3. Create the worktree

Fetch and fast-forward the base branch first so the worktree starts from the
latest base.

```bash
git worktree add <path> <branch>
# or create a new branch from base:
git worktree add -b <new-branch> <path> <base-branch>
```

Verify with `git worktree list`.

### 4. Confirm and work inside it

Report the path, branch, and `git worktree list` output. Only then proceed.
Every edit, every command, every commit must happen inside the worktree path.

If generic Git creation left the worktree outside the current runtime's native
file-tool scope, give one optional post-creation recommendation for opening or
attaching that checkout in the runtime. Do not repeat the pre-creation advice,
require a reply, or block the existing terminal workflow.

## Finishing a Worktree

When the user says "finalizar worktree", "remover worktree", or "trazer para
a main worktree":

1. In the primary worktree: `git pull` to update main
2. Switch to the feature branch: `git checkout <branch>`
3. Rebase on updated main if needed
4. Remove the secondary worktree: `git worktree remove <path>`
5. Confirm with `git worktree list`

**Never merge the feature branch into main.**
