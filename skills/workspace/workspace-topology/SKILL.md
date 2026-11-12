---
name: workspace-topology
description: Resolve clone/worktree destinations across a personal multi-context code directory using hierarchical WORKSPACE.md rules. Use before cloning a repository, choosing a worktree path, opening a set of repos as a workspace (Cursor/Zed multi-root/pseudo-project), when a repo may belong to one of several context directories, or when moving an existing clone between contexts.
---

# Workspace Topology

Resolve where a repo should live by reading `WORKSPACE.md` files that document
the user's personal directory contexts. `WORKSPACE.md` is local (outside any
git repo); per-repo rules stay in `AGENTS.md`.

## Hard Rules

- Never clone into a directory reserved for worktrees, even temporarily.
- Never infer context from the GitHub org or repo name alone.
- Never commit `WORKSPACE.md` files that live outside repositories.
- Never relocate or `git worktree move` existing worktrees to match a
  documented pattern without explicit instruction.
- Do not create `WORKSPACE.md` inside cloned repos — that is `AGENTS.md`'s job.
- Do not centralize worktrees into one root; each repo keeps its configured
  placement (GIT_DIR, conditionals, hooks).

Editor workspaces (Cursor `.code-workspace`, Zed multi-root) are views over
the tree, not the source of truth.

## Procedure

1. **Find applicable rules.** Walk up from the candidate destination,
   collecting every `WORKSPACE.md`. Apply outermost-first; nearer files
   override or extend.
2. **Classify the repo.** Map `owner/repo` to a context only when an applicable
   `WORKSPACE.md` explicitly says so. Do not infer from the remote owner name.
3. **Verify the destination.** It must not sit inside a location marked as
   reserved for worktrees, and must match the repo's classification when a
   rule exists.
4. **Ask when ambiguous.** If no `WORKSPACE.md` applies or the applicable file
   is silent, ask the user before cloning. Include the proposed destination.

For worktrees: check `WORKSPACE.md` and the repo's `AGENTS.md` for a worktree
convention before falling back to the `git-worktree` skill's default.

For opening a workspace (Cursor/Zed): read the relevant `WORKSPACE.md` first
so the workspace mirrors the tree instead of guessing.

## Template

See [WORKSPACE-template.md](WORKSPACE-template.md) for the minimal
`WORKSPACE.md` format. Nested files only record deviations from ancestors.

## Moving an Existing Clone

When a repo's correct context changes, move the existing clone instead of
cloning again: history, worktrees, local config, and hooks move with it.

1. Confirm the tree state first (`git status`, `git worktree list`, unpushed
   commits). Do not move a clone holding work you cannot recover.
2. Move the directory to the destination resolved by the rules above.
3. Update every `WORKSPACE.md` that names the repo or the old path: the old
   context, the new context, and their common ancestors.
4. Re-verify identity in the new path: `user.email`, conditional includes
   (`includeIf gitdir`) still keyed on the old path, and credential routing
   (see `gh-profile`).
5. Re-verify access from the new path before starting work.

A `WORKSPACE.md` may declare a documented exception allowing worktrees of
another context's canonical clone inside one stable directory of the
consuming workspace (for example `worktrees/`). That exception covers
worktrees only and must be written down before the worktree is created.
