---
name: workspace-topology
description: Resolve clone/worktree destinations across a personal multi-context code directory using hierarchical WORKSPACE.md rules. Use before cloning a repository, choosing a worktree path, opening a set of repos as a workspace (Cursor/Zed multi-root/pseudo-project), or when a repo may belong to one of several context directories.
---

# Workspace Topology

Resolve where a repo should live by reading `WORKSPACE.md` files that document
the user's personal directory contexts. `WORKSPACE.md` is local (outside any
git repo); per-repo rules stay in `AGENTS.md`.

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

## Hard Rules

- Never clone into a directory reserved for worktrees, even temporarily.
- Never infer context from the GitHub org or repo name alone.
- Never commit `WORKSPACE.md` files that live outside repositories.
- Never relocate or `git worktree move` existing worktrees to match a
  documented pattern without explicit instruction.
- Do not create `WORKSPACE.md` inside cloned repos — that is `AGENTS.md`'s job.
- Do not centralize worktrees into one root; each repo keeps its configured
  placement (GIT_DIR, conditionals, hooks).

## Template

See [WORKSPACE-template.md](WORKSPACE-template.md) for the minimal
`WORKSPACE.md` format. Nested files only record deviations from ancestors.
