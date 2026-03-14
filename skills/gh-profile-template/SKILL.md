---
name: gh-profile
description: >
  Template: Route GitHub CLI (gh) profile/auth based on workspace path.
  Use before running any gh command to ensure the correct GitHub account is active.
  Copy this skill and fill in the placeholders for your environment.
---

# GitHub CLI Profile Routing (Template)

> **This is a reusable template.** Copy it to your skills repo and replace
> all `<placeholder>` values with your actual paths and GitHub usernames.

## Purpose

Different workspace paths belong to different GitHub accounts. Before running any `gh` CLI command, the agent must ensure the correct profile is active.

## Routing Rules

Determine the expected GitHub user from the current working directory:

| Workspace path prefix   | GitHub user       |
|--------------------------|-------------------|
| `~/Code/<personal>/`     | `<personal-user>` |
| `~/Code/oss/`            | `<personal-user>` |
| `~/.dotfiles`            | `<personal-user>` |
| `~/Code/<work>/`         | `<work-user>`     |

Paths are matched by prefix after expanding `~` to `$HOME`.
Add or remove rows to match your directory layout.

## Procedure (before every `gh` command)

1. Resolve the current working directory to one of the routing rules above.
2. Run `gh auth status` to check which user is currently active.
3. If the active user does not match the expected user, switch first:

   ```sh
   gh auth switch --user <expected-user>
   ```

4. Then proceed with the intended `gh` command.

## Environment Variables

- **Never** rely on the `GH_TOKEN` environment variable set in `mise.toml` for profile selection. Profile routing must always use `gh auth switch`.
- Still run `eval "$(mise env)"` when needed for **other** environment variables in work repos (e.g., API keys, service tokens), but do not use it as a substitute for profile switching.

## Example

```sh
# 1. Check current profile
gh auth status
# active account: <wrong-user>

# 2. Switch to the expected profile
gh auth switch --user <expected-user>

# 3. (work repos only) Load env vars if needed
eval "$(mise env)"

# 4. Run the actual command
gh pr create --fill
```
