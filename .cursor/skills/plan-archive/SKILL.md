---
name: plan-archive
description: Archive outdated or superseded plans into .cursor/plans/.archived/ with consistent handling. Use when the user asks to archive, retire, or supersede a plan.
---

# Plan Archive

Archive plans instead of deleting them. Plans are historical artifacts worth preserving.

## When to Archive

- User explicitly asks to archive, retire, or supersede a plan
- A plan is replaced by a newer version

**Never** archive without explicit user request.

## Procedure

1. Ensure the archive directory exists:

```bash
mkdir -p .cursor/plans/.archived/
```

2. Move the plan file, preserving the original filename:

```bash
mv .cursor/plans/<plan-file>.plan.md .cursor/plans/.archived/<plan-file>.plan.md
```

3. Do **not** modify the archived plan content. Keep it intact as historical reference.

## Superseded Plans

When a replacement plan exists, pick **one** of these approaches:

- **Option A** — Add a reference line inside the archived plan's YAML frontmatter (before the closing `---`):

```yaml
superseded_by: <replacement-plan-file>.plan.md
```

- **Option B** — Document the relationship in the replacement plan's frontmatter:

```yaml
supersedes: <archived-plan-file>.plan.md
```

Either option is acceptable. Prefer whichever the user requests; default to Option A.

## Rules

- **Never delete plans** — always archive
- Preserve complete file content including frontmatter
- Only archive when explicitly requested by the user
- Report what was archived and where after completion
