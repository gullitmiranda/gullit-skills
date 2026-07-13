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

- Prefer using `work` instead of organization- or employer-specific abbreviations in directory and namespace naming when the value is not a fixed identifier.

## Link formatting

- When referencing any external resource, include a clickable URL whenever possible; compact raw URLs are welcome and often preferred over label-only references, and bare numbers or abbreviations should only be used when no URL is available.

## Git commit destinations

- In the user's **personal** GitHub repos (owner `gullitmiranda`, e.g. `~/code/gullit/...`), committing/pushing directly to `main` is allowed without explicit per-task confirmation. The safety skill's "never commit to main/master" rule applies to shared or organizational repos, not personal ones. Still keep commits well-scoped and reversible.

## PR Review Comments

- When the user asks to resolve PR review comments from automated review agents, handle each targeted comment individually by replying in GitHub or updating the PR, whichever best resolves it, and then mark the thread/comment as resolved before finishing.
