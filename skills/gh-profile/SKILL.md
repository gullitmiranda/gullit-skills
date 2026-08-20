---
name: gh-profile
description: Route authenticated GitHub CLI access by repository owner and workspace context. Use whenever reading or managing GitHub resources, before gh commands, and before remote git operations.
---

# GitHub CLI Profile Routing

GitHub access uses the authenticated `gh` CLI. A `gh` wrapper on PATH
(`~/.local/bin/gh`) automatically routes each call to the correct account —
by explicit repo owner in args, then by cwd — injecting a fresh keyring token
per invocation. An editor login is not GitHub CLI authentication.

## Hard Rules

- Never use `gh auth switch` — the wrapper routes per call; switching mutates global keyring state and races with parallel agents. This also applies when recovering from a wrong-account mistake: fix routing context, not global state.
- Do not set `GH_TOKEN`/`GITHUB_TOKEN` manually for account selection; a preset token makes the wrapper pass through unchanged.
- Fail closed when the account for a resource is ambiguous; ask the user, do not guess.
- Do not expose tokens, credentials, or private resource contents in logs or published text.
- Keep real account names and organization mappings in private machine config (dotfiles `config.yaml`), not in a public skill.

## Tool Selection

- Prefer `gh` for GitHub resources, especially when a resource may be private or internal. Use generic HTTP fetching only for resources confirmed public.
- If an unauthenticated request returns `401`, `403`, or `404`, retry through `gh` before concluding that the resource is unavailable.

## Procedure

1. Call `gh` normally — the wrapper resolves the account from the repo owner in the args or the cwd. Include `-R owner/repo` when operating outside the repo's directory.
2. For `git fetch`/`pull`/`push`, the per-directory git credential helper selects the same account; no extra step needed.
3. On unexpected auth failures, run `gh auth status` (never injected by the wrapper) to inspect keyring accounts.

## Publishing / Write Actions

Reads are low-risk under any account; **writes are attributed to an author** and are hard to undo cleanly (a comment can be deleted, but notifications already went out). Before any write — `gh issue create`, `gh pr create`, `gh issue/pr comment`, discussion comments, reviews, label/milestone changes:

1. **Confirm the authoring account with the user** when the target repo's owner/context does not clearly map to the account the user intends to publish under (e.g. personal vs. work identity on a third-party repo).
2. **Verify the resolved account before sending**: run a routed read in the same context first (e.g. `gh repo view owner/repo` with the same `-R`/cwd) and confirm the wrapper routes to the intended account. If it resolves to the wrong account, stop and ask — do not "fix" it with `gh auth switch` or by exporting tokens.
3. **After publishing, check the author** of the created resource (the `author.login` field on the issue/PR/comment). If it went out under the wrong account, tell the user immediately; delete and repost only with their approval — never paper over it silently.

## Account Setup

When authenticating a new account, include the `workflow` scope when the account will manage workflow files:

```sh
gh auth login --scopes workflow
gh auth refresh --scopes workflow
```
