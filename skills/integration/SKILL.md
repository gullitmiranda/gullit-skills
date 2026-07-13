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

- Use the repository's configured issue-tracker CLI as the primary integration path.
- Use MCP or direct APIs only when the supported CLI cannot perform the operation.
- Preserve issue identifiers and links when they are explicitly part of the task.
- Do not invent issue references, teams, projects, labels, or statuses.
- Keep organization-specific defaults in a private profile or specialized skill.

## Trunk and Tooling

- When fixing lint or format issues in a Trunk-enabled repository, run the repository's documented Trunk check/fix workflow first.
- Prefer each tool's native configuration and ignore mechanisms over integration-specific overrides.
- Keep integration configuration minimal and compatible with direct tool invocation.

## MCP Servers

- Configure MCP servers in the repository or user-level configuration expected by the host.
- Verify server connectivity before relying on an MCP-only workflow.
- Prefer deterministic CLI/API operations when an MCP server is unavailable or unstable.
- Do not send secrets or unnecessary private context to external MCP servers.

## External APIs

- Use secure transport and the provider's supported authentication mechanism.
- Store credentials outside repositories and logs.
- Validate status codes, response schemas, rate limits, retries, and cancellation behavior.
- Log actionable metadata without logging secrets, private payloads, or sensitive personal data.
- Make provider-specific routing and privacy assumptions explicit before sending data.

## Multi-Repository Workspaces

- Identify repository boundaries before running commands.
- Run each integration command from the intended repository.
- Keep source, cache, and generated outputs distinct.
- Validate cross-repository links and paths before publishing them.
