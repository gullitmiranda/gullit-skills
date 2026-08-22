---
name: tech-debt
description: Register technical debt in the project's canonical tech debt file without taking follow-up action. Use when the user asks to log, note, capture, register, or save a tech debt for later.
---

# Tech Debt

Record technical debt for later. This workflow is **record-only**.

## Hard Rules

- Do not change application code to address the debt.
- Do not create issues, plans, tasks, or PRs unless explicitly requested.
- Do not investigate beyond what is needed to write a clear entry.
- Do not commit or push unless explicitly requested.
- Do not move or rewrite existing debt entries unless the user asks.

## Target File

Canonical file: `TECH_DEBTS.md` at the current project's root.

- If the project already has a clear equivalent (`docs/TECH_DEBTS.md`, `TECHNICAL_DEBT.md`), prefer it over creating a second registry.
- If unsure which file is canonical, ask once. Otherwise default to `TECH_DEBTS.md`.
- If it does not exist, create it with:

```markdown
# Tech Debts

Project-level register of technical debt items captured for later follow-up.

## Open

## Resolved
```

## Entry Format

Add each new item at the top of `## Open` (newest first):

```markdown
### <short debt title>

- Date: YYYY-MM-DD
- Scope: <project area, service, path, or module>
- Problem: <what is wrong or missing today>
- Impact: <risk, maintenance cost, or limitation>
- Trigger: <what surfaced this debt now>
- Suggested direction: <optional, high-level only>
```

- One `###` heading per debt; short, searchable title; use the user's language.
- Omit `Suggested direction` when there is no useful hint.
- Include user-provided paths, symbols, ticket IDs, or links in `Scope` or `Problem`.
- Do not invent implementation details.

## Workflow

1. Parse the user's message into a concise debt entry.
2. Resolve the canonical file (create if needed).
3. Insert at the top of `## Open`.
4. Confirm: recorded title, target file path, and that no further action was taken.
