---
name: tech-debt
description: Register technical debt in the project's canonical tech debt file without taking follow-up action. Use when the user asks to log, note, capture, register, or save a tech debt for later.
---

# Tech Debt

Record technical debt for later without trying to fix, plan, triage, or execute anything else.

## When to Apply

Apply when the user:

- asks to register or log a tech debt
- says something should be noted for later
- wants to capture a debt without acting on it now
- runs `/tech-debt`

## Core Rule

This workflow is **record-only**.

Do not:

- change application code to address the debt
- create issues, plans, tasks, or PRs unless explicitly requested
- start an investigation beyond what is needed to write a clear entry
- commit or push anything unless explicitly requested

## Target File

Use `TECH_DEBTS.md` at the current project's root as the canonical file.

- If it does not exist, create it.
- If the project already has a clear equivalent file such as `docs/TECH_DEBTS.md` or `TECHNICAL_DEBT.md`, prefer the existing canonical file instead of creating a second registry.
- If unsure which file is canonical, ask once. Otherwise default to `TECH_DEBTS.md`.

## Entry Format

Add each new item at the top of `## Open`, so the newest debts stay easiest to find.

Use this template:

```markdown
### <short debt title>

- Date: YYYY-MM-DD
- Scope: <project area, service, path, or module>
- Problem: <what is wrong or missing today>
- Impact: <risk, maintenance cost, or limitation>
- Trigger: <what surfaced this debt now>
- Suggested direction: <optional, high-level only>
```

Rules:

- Use one `###` heading per debt item.
- Keep the title short and searchable.
- Use the user's language when possible.
- Omit `Suggested direction` when there is no useful hint.
- If the user provided paths, symbols, ticket IDs, or links, include them in `Scope` or `Problem`.
- Keep each bullet concise and scannable.
- Do not invent implementation details.

## File Template

If the file does not exist, create it with:

```markdown
# Tech Debts

Project-level register of technical debt items captured for later follow-up.

## Open

## Resolved
```

## Workflow

1. Parse the user's message into a concise debt entry.
2. Determine the current project's canonical tech debt file.
3. Create the file if needed.
4. Insert the new item at the top of `## Open`.
5. Confirm what was recorded and where.

## Confirmation Style

Report:

- the recorded title
- the target file path
- that no further action was taken

## Anti-Patterns

- Do not fix the debt during registration
- Do not create backlog items automatically
- Do not expand the scope into a refactor plan
- Do not move or rewrite existing debt entries unless the user asks
