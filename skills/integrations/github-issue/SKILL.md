---
name: github-issue
description: Create or update GitHub issues with the mandatory minimal triage - type and area labels from the repo's existing label set, plus a complexity estimate - and no assignee, milestone, or project unless explicitly requested. Use when opening, drafting, or triaging an issue.
---

# GitHub Issue Triage

Every issue is classified before it is created. Labels come from the target repo's existing label set; nothing is invented and nobody is assigned by default.

## Hard Rules

- Never assign (`--assignee`) unless the user explicitly names the person doing the work, including "I'll do it myself".
- No milestone, project, iteration, or due date unless requested. GitHub-to-Linear sync creates the tracker record; never create a Linear issue directly.
- Use only labels that already exist in the target repo. If no label fits a dimension, leave it out and say so instead of inventing one.
- Search for an existing issue with the same scope before creating a duplicate.
- Route the account per `gh-profile` before writing, and verify the `author` after creating.
- Title and body are published artifacts: English by default, no local or unpublished paths (see `publish-safe-links`).
- When the type or area cannot be inferred from the request, ask one focused question rather than guessing.

## Triage Minimum

| Dimension | Requirement |
| --- | --- |
| Type | Exactly one type label (bug, feature/enhancement, docs, chore, refactor, perf, test), whichever exists in the repo |
| Area | Up to two area, component, or team labels supported by evidence; skip when the repo has no matching label |
| Priority/severity | Apply the repo's existing priority or severity label only when the request or evidence establishes it |
| Complexity | S, M, or L with a one-line justification; use the repo's complexity or size label when it exists, otherwise a `Complexity: <size> - <reason>` line in the body |

## Procedure

1. Read the repo's labels: `gh label list -R <owner/repo> -L 200`. Note which type, area, priority, and complexity labels exist.
2. Check for duplicates: `gh issue list -R <owner/repo> --state all --search "<keywords>"`.
3. Write the body with why, expected outcome, scope boundaries, and concrete evidence (paths, versions, reproduction steps). Add the `Complexity` line when no complexity label exists.
4. Create: `gh issue create -R <owner/repo> --title <title> --body-file <file> --label <type> --label <area>`.
5. Verify: `gh issue view <n> -R <owner/repo> --json labels,assignees,author`. Report the issue link, the applied labels, the complexity verdict, and that no assignee was set.
