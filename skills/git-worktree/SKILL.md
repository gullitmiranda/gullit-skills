---
name: git-worktree
description: Enforce git worktree discipline. Use whenever the user asks to create a worktree, work on a feature branch in isolation, or says "nova worktree", "worktree separada", "a partir do branch X". CRITICAL: never rationalize skipping worktree creation.
---

# Git Worktree Rules

## CRITICAL — Read This First

When the user explicitly asks to create a git worktree, **you MUST create it before touching any file**.

Do NOT:
- Conclude that "the branch is already checked out so it's fine"
- Assume a previous session already handled it
- Start implementing anything before the worktree exists and is confirmed
- Rationalize any shortcut

This is a hard constraint. Breaking it means working in the wrong directory, potentially overwriting changes made by other agents or sessions on the same branch.

## When This Skill Applies

Trigger on any of these signals:
- "crie uma worktree"
- "nova worktree"
- "worktree separada"
- "a partir do branch X"
- "git worktree add"
- "trabalhe em uma worktree"
- Any explicit instruction to isolate work in a separate worktree

## Mandatory Protocol

### Step 1 — Confirm worktree path

If the user did not specify a path, ask before proceeding:
```
Qual o caminho para a worktree? (ex: ../helm-charts-cw-app)
```

Do not assume a path. Do not proceed without one.

### Step 2 — Create the worktree

```bash
git worktree add <path> <branch>
# or create a new branch from base:
git worktree add -b <new-branch> <path> <base-branch>
```

Verify it was created:
```bash
git worktree list
```

### Step 3 — Confirm to the user

Report back:
- Worktree path
- Branch it is on
- Output of `git worktree list`

Only after this confirmation proceed with any implementation work.

### Step 4 — All work happens inside the worktree

Every file edit, every `helm template`, every commit must happen inside `<path>`, not in the primary worktree.

## Finishing a Worktree

When the user says "finalizar worktree", "remover worktree", or "trazer para a main worktree":

1. In the primary worktree: `git pull` to update main
2. Switch to the feature branch: `git checkout <branch>`
3. Rebase on updated main if needed
4. Remove the secondary worktree: `git worktree remove <path>`
5. Confirm with `git worktree list`

**Never merge the feature branch into main.**

## Why This Matters

Working in the wrong worktree causes:
- Commits landing on a branch another agent is actively using
- Overwriting changes the user explicitly isolated
- Corruption of parallel work streams

## Self-Check Before Any Work

Before writing a single file, ask yourself:

> "Did the user ask for a worktree? If yes — have I created it, confirmed it, and am I inside it?"

If the answer to any part is no — stop and create the worktree first.
