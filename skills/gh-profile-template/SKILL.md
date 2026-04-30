---
name: gh-profile
description: >
  Route GitHub CLI (gh) profile/auth based on workspace path. ALWAYS use before
  any gh command or git push/pull to a remote. ~/code/cw/ → gullit-cw,
  ~/code/gullit/ and ~/code/oss/ → gullitmiranda.
---

# GitHub CLI Profile Routing

## MANDATORY — Run before every `gh` command or `git push/pull`

Different workspace paths use different GitHub accounts. The wrong account will cause 403 errors on push/pull.

## Routing Rules

| Workspace path prefix | GitHub user      |
|-----------------------|------------------|
| `~/code/cw/`          | `gullit-cw`      |
| `~/code/gullit/`      | `gullitmiranda`  |
| `~/code/oss/`         | `gullitmiranda`  |
| `~/.ai-skills/`       | `gullitmiranda`  |
| `~/.factory/`         | `gullitmiranda`  |

## Procedure

1. Check which account is active:
   ```sh
   gh auth status
   ```
2. If it does not match the expected user for the current path, switch:
   ```sh
   gh auth switch --user <expected-user>
   ```
3. For work repos (`~/code/cw/`), load env vars if needed:
   ```sh
   eval "$(mise env)"
   ```
4. Then run the intended command.

## Initial Account Setup

When logging in to an account for the first time, always include the `workflow` scope:

```sh
gh auth login --scopes workflow
```

This ensures the token can push changes to `.github/workflows/` files. Without this scope, GitHub rejects those pushes even if you have repo access.

If an existing account is missing the scope, refresh it once:

```sh
gh auth refresh --scopes workflow
```

The scope persists across automatic token refreshes. It is only lost on full re-login (`gh auth logout` + `gh auth login`).

## Rules

- **Never** rely on `GH_TOKEN` from `mise.toml` for profile selection — always use `gh auth switch`.
- `eval "$(mise env)"` is only for loading other env vars (API keys, tokens), not for profile switching.
- When in doubt about which account to use, check `gh auth status` first.
- Always use `--scopes workflow` when running `gh auth login` for any account.
