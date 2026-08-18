---
name: integration
description: General rules for GitHub, issue trackers, Trunk, MCP servers, and external APIs. Use when an engineering task crosses a repository or service boundary.
---

# Integration Rules

## GitHub

- Treat GitHub URLs and repository references as authenticated GitHub operations.
- Prefer `gh` for repository files, pull requests, issues, releases, workflows, and API resources.
- Apply the `gh-profile` skill before every `gh` command or remote git operation.
- Use generic HTTP fetching only for resources confirmed to be public.
- Never assume that an editor login provides CLI authentication.
- Do not publish private resource contents, tokens, prompts, or credentials.

## Issue Trackers

- Prefer repository-attached issues (e.g. GitHub issues) as the canonical record for project-scoped work; use team trackers for cross-repo or team-level work.
- Use the repository's configured issue-tracker CLI as the primary path; use MCP or direct APIs only when the CLI cannot perform the operation.
- Preserve issue identifiers and links when they are explicitly part of the task.
- Do not invent issue references, teams, projects, labels, or statuses.
- Keep organization-specific defaults in a private profile or specialized skill.

## Trunk and Tooling

- When fixing lint or format issues in a Trunk-enabled repository, run the repository's documented Trunk check/fix workflow first.
- Prefer each tool's native configuration and ignore mechanisms over integration-specific overrides.

## MCP Servers

- Prefer deterministic CLI/API operations when an MCP server is unavailable or unstable.
- Do not send secrets or unnecessary private context to external MCP servers.

## External APIs

- Store credentials outside repositories and logs.
- Validate status codes, response schemas, rate limits, retries, and cancellation behavior.
- Log actionable metadata without logging secrets, private payloads, or sensitive personal data.
- Make provider-specific routing and privacy assumptions explicit before sending data.

## Multi-Repository Workspaces

- Identify repository boundaries and navigate to the correct repo before running any command.
- Validate cross-repository links and paths before publishing them.
