---
name: user-preferences
description: guma's personal assistant behavior preferences across all projects (user-level). Use when interacting with the user in any repo for general assistant behavior not covered by topical skills.
---

# User Preferences (User-Level)

Miscellaneous personal preferences that do not belong in a topical skill file.
Before adding rules here, check if a topical skill already covers the domain
(git, quality, safety, workflow, k8s, etc.) and add there instead.

## Tool defaults

- When the user mentions "skill", default to creating/editing in `.claude/skills/` instead of `.cursor/rules/`, unless explicitly instructed otherwise.

## Shell environment (Cursor IDE)

- The Cursor shell does NOT run `mise activate` hooks. Environment variables set by mise (e.g., `GH_TOKEN`) are NOT automatically loaded when running commands.
- Before running `gh` CLI or any command that depends on mise-managed env vars in work repos (`~/Code/work/*`), prefix with `eval "$(mise env)"` to load the correct environment.
- Example: `cd /path/to/repo && eval "$(mise env)" && gh pr create ...`

## Naming preferences

- Prefer using `work` instead of `cw` or `cloudwalk` in directory and namespace naming when the value is not a fixed identifier.

## Git commit destinations

- In the user's **personal** GitHub repos (owner `gullitmiranda`, e.g. `~/code/gullit/...`), committing/pushing directly to `main` is allowed without explicit per-task confirmation. The safety skill's "never commit to main/master" rule applies to **work** repos (CloudWalk/cw, OSS, shared), not personal ones. Still keep commits well-scoped and reversible.

## Skill source vs. ai-skills CLI cache

Skills installed by `ai-skills` are clones under `~/.ai-skills/repos/<profile>/<owner>/<repo>/`. Agent-visible directories like `~/.claude/skills/<name>`, `~/.cursor/skills-cursor/<name>`, `~/.codex/skills/<name>` are **symlinks** that resolve into that cache. Editing through the symlink writes to the cache.

**The cache is NOT a working repo.** It is a tool-managed clone — safe to be reset, re-cloned, or moved by `ai-skills update` / `ai-skills doctor`. Commits/pushes from the cache can also mutate the upstream in unintended ways.

Before editing or committing anything that came in via a skill symlink:

1. Resolve the symlink: `readlink -f <path>` (or `pwd -P` after `cd`).
2. If the resolved path is under `~/.ai-skills/repos/`, **stop**. Either:
   - Edit in the registered source clone (see mapping below), or
   - Use `ai-skills publish <repo>` (when implemented) to send local changes upstream from the cache.
3. After editing in the source clone, run `ai-skills update <repo>` to refresh the cache so the agent-visible symlinks see the new content.

### Source repo mapping

| Skill repo | Source clone (working repo) |
|---|---|
| `gullitmiranda/gullit-skills` | `~/code/gullit/gullit-skills/` |
| `gullitmiranda/ai-skills-cli` | `~/code/gullit/ai-skills-cli/` |

Add new entries here as new source clones are registered.

## PR Review Comments

- When the user asks to resolve PR review comments from `cloudwalk-review-agent[bot]` or `enrond-cw[bot]`, handle each targeted comment individually by replying in GitHub or updating the PR, whichever best resolves it, and then mark the thread/comment as resolved before finishing.
