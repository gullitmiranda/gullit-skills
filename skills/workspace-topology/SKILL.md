---
name: workspace-topology
description: Resolve clone/worktree destinations across a personal multi-context code directory using hierarchical WORKSPACE.md rules. Use before cloning a repository, choosing a worktree path, opening a set of repos as a workspace (Cursor/Zed multi-root/pseudo-project), or when a repo may belong to one of several context directories.
---

# Workspace Topology

## Purpose

Prevent repositories from being cloned into the wrong directory when the user's
home has multiple context folders (personal, OSS, employer, employer
sub-contexts). Reduce the failure mode of "cloned into the nearest worktree area"
or "cloned into whatever directory happened to be current".

This skill does not dictate a single global layout. It teaches agents how to read
the user's local `WORKSPACE.md` convention, inherit rules hierarchically, and ask
before cloning when the target context is ambiguous.

## Core conventions

- A **`WORKSPACE.md`** file documents an organizational directory (a "context" or
  scope). It is local and personal: outside any git repository by default, so
  personal directory preferences do not leak into shared repos.
- `WORKSPACE.md` files compose **recursively**. A more nested file only records
  deviations from its nearest ancestor. If `~/code/WORKSPACE.md` covers the
  default pattern, only create `~/code/employer/WORKSPACE.md` when that scope
  needs its own rule.
- Repository-level instructions stay in **`AGENTS.md`** inside the repo. That is
  where shared, versioned, repo-intrinsic rules live (build, test, monorepo
  worktree patterns, etc.). A repo's `AGENTS.md` may reference `WORKSPACE.md`
  by path but must not duplicate global topology rules.
- Do **not** centralize worktrees into one root. Each repo keeps its worktree
  placement as configured (GIT_DIR, per-repo conditionals, hooks). The skill's
  job is to *know where worktrees are*, not to relocate them.
- Workspaces in the editor (Cursor `.code-workspace`, Zed pseudo-project /
  multi-root) are *views* over the directory tree, not the source of truth.
  The tree layout itself, defined by `WORKSPACE.md` files, is canonical.

## Before cloning a repository

1. Identify the candidate destination:
   - If the user provided an explicit path, use it verbatim.
   - If the user named a context (e.g. "clone into platform"), resolve via the
     matching `WORKSPACE.md` ancestors.
   - If neither, map the remote `owner/repo` to a context only when the
     relevant `WORKSPACE.md` explicitly says so. Do not infer context from the
     remote owner name alone.
2. Walk up from the candidate destination, collecting every `WORKSPACE.md` up
   to and including the root of the user's code directory. Apply rules
   outermost-first; nearer files override or extend.
3. Before running `git clone`, verify:
   - The final destination does not sit inside any location marked as reserved
     for worktrees by an applicable `WORKSPACE.md`.
   - The destination context matches the repo's classification when a rule
     exists.
4. If no ancestor `WORKSPACE.md` applies, or the applicable file is silent on
   where this repo belongs, **ask the user** before cloning. Include the
   proposed destination in the question.
5. After cloning, confirm the resulting path to the user.

## Before creating a worktree

1. Read any `WORKSPACE.md` files that apply to the repo's directory, plus the
   repo's own `AGENTS.md` if present. Check for an explicit worktree
   convention (path pattern, naming scheme).
2. If both documents are silent, fall back to the `git-worktree` skill's
   default convention for deriving the path.
3. Never clone a fresh repository into a directory reserved for worktrees —
   even temporarily. A worktree directory is not a place for primary clones.

## Before opening a workspace

- When the user asks to open a context (or build a Cursor/Zed workspace from
  it), read the relevant `WORKSPACE.md` first. It declares the intended
  root(s), so the workspace mirrors the tree instead of guessing.
- Treat each repository inside the workspace as its own git state; do not
  apply repo-level operations across roots without confirmation.

## Minimal `WORKSPACE.md` template

```markdown
# Workspace: <name>

## Scope
- One-line description of what belongs here.

## Roots
- Canonical clones live at: <relative path>
- Linked worktrees live at: <relative path or per-repo pattern>

## Reserved locations
- Directories that must never receive new clones.

## Clone rules
- e.g. "repos in <owner>/<org> go here by default"
- e.g. "ask before cloning anything not in that set"

## When ambiguous
- Ask the user; do not guess.
```

Keep it short. A more nested `WORKSPACE.md` only contains fields that differ
from its ancestors.

## Data boundary

- Never commit `WORKSPACE.md` files that live outside repositories; they
  describe personal layout.
- A repo's `AGENTS.md` may mention that a `WORKSPACE.md` convention exists, but
  must not enumerate personal directories (employer paths, context names) in a
  public repo. If the repo is private and the maintainer chooses to include
  its own context block, that is their decision — not this skill's default.
- If the user asks to publish a `WORKSPACE.md` example, redact personal paths.

## Anti-patterns

- Do not infer context from the GitHub org or repo name when no `WORKSPACE.md`
  rule says so.
- Do not create `WORKSPACE.md` files inside cloned repos unless the user
  explicitly wants per-repo local notes — that is `AGENTS.md`'s job.
- Do not rewrite worktree paths to match a global pattern just because a new
  convention was documented; existing repos keep their current layout.
- Do not "helpfully" move or `git worktree move` existing worktrees to match
  a documented template without explicit instruction.
