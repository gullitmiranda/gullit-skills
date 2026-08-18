---
name: gh-profile
description: Route authenticated GitHub CLI access by repository owner and workspace context. Use whenever reading or managing GitHub resources, before gh commands, and before remote git operations.
---

# GitHub CLI Profile Routing

Use the authenticated GitHub CLI path for GitHub resources and select the account from a configured local profile map. An editor login is not GitHub CLI authentication.

## Hard Rules

- Never assume that Cursor, Zed, or another editor login supplies GitHub authentication to tools.
- Do not use `GH_TOKEN` or `GITHUB_TOKEN` for profile selection; environment tokens can override the keyring account selected by `gh auth switch`.
- Keep real account names, organization mappings, and work-specific paths in a private machine or workspace configuration. Do not hardcode them in a public skill.
- Fail closed when the expected account is ambiguous; ask the user, do not guess.
- Do not expose tokens, credentials, or private resource contents in logs or published text.

## Tool Selection

- Treat GitHub URLs, repositories, files, pull requests, issues, releases, workflows, and API resources as GitHub operations; prefer `gh`, especially when a resource may be private or internal. Use generic HTTP fetching only for resources confirmed public and accessible without authentication.
- Prefer `gh api repos/<owner>/<repo>/contents/<path>` for repository files, or local `git` when the repository is already cloned.
- If an unauthenticated request returns `401`, `403`, or `404`, retry through the configured `gh` profile before concluding that the resource is unavailable.

## Procedure

Before every GitHub CLI or remote Git operation:

1. Resolve the expected account, in precedence order:
   - Explicit repository owner from a GitHub URL or `OWNER/REPO` reference.
   - Workspace path mapping from the local profile configuration.
   - Ask the user when ambiguous; do not guess.
2. Check configured accounts without environment-token overrides:

   ```sh
   env -u GH_TOKEN -u GITHUB_TOKEN gh auth status
   ```

3. Switch when necessary:

   ```sh
   env -u GH_TOKEN -u GITHUB_TOKEN gh auth switch --user <expected-user>
   ```

4. Run the intended command with the same clean environment:

   ```sh
   env -u GH_TOKEN -u GITHUB_TOKEN gh <command>
   ```

For `git fetch`, `git pull`, and `git push`, ensure the repository-specific credential configuration selects the same account before running the command.

## Environment

- Do not evaluate a project environment file in the shell used for routed GitHub commands when it exports a GitHub token.
- Load non-GitHub environment variables only in the command that needs them.
- Prefer explicit owner routing over the current working directory.

## Account Setup

When authenticating a new account, include the `workflow` scope when the account will manage workflow files:

```sh
gh auth login --scopes workflow
gh auth refresh --scopes workflow
```
