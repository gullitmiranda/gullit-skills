---
name: persist-agent-constraints
description: Persists agent constraints (what not to do) in the project's canonical place for agent instructions. Use when the user states constraints, prohibitions, or things to avoid (e.g. nao faca, evite, don't, never, avoid, nao quero que, proibido).
---

# Persist Agent Constraints

When the user states **constraints** (prohibitions, restrictions, things to avoid),
persist them in the most relevant file so future sessions respect them.

## When to Apply

Apply when the user:

- Says what **not** to do (e.g. "nao faca X", "don't do Y", "never Z")
- Adds **restrictions** or **prohibitions** (e.g. "evite", "avoid", "nao quero que", "proibido")
- Corrects behavior by stating what to **avoid** or **stop doing**

## Workflow

1. **Parse** the constraint into one or more short, clear bullet lines (imperative).

2. **Smart-route using the learn skill's logic** (see `learn/SKILL.md` Step 3):
   - Identify the constraint's topic (git, safety, quality, k8s, etc.)
   - Find the existing file that covers that topic
   - Route to that file's constraints/safety section

   Common routing examples:
   - "don't push to main" -> `safety/SKILL.md` under Git Safety
   - "don't use kubectl delete" -> `k8s/SKILL.md` or `safety/SKILL.md`
   - "don't add emojis" -> `quality/SKILL.md` under Output hygiene
   - "don't auto-commit" -> `safety/SKILL.md` under Absolute Rules

   If no topical file matches, fall back to `AGENTS.md` (project scope)
   or the constraint's appropriate scope target per learn skill rules.

3. **Add or update the constraints section** in the target file:
   - Use `## Constraints` or `## Don't / Avoid` as section heading (or the file's existing equivalent like `## Absolute Rules`, `## Safety Checks`)
   - If the target file already has a section where constraints naturally fit (e.g., safety rules, prohibited operations), add there instead of creating a new section
   - One bullet per constraint, concise and actionable
   - De-duplicate: if an equivalent rule already exists, refine instead of duplicating

4. **Cross-tool sync**: If the project has multiple instruction formats
   (`.claude/skills/`, `.cursor/skills/`, `AGENTS.md`), update all that exist.
   See learn skill Step 5.

5. **Confirm**: Report what was added, where (exact path and section).

## Section Format

When creating a new constraints section:

```markdown
## Constraints

- Do not commit to main without a PR
- Do not use Linear for this project (use GitHub Issues)
- Do not add timelines or cronograms to plans
```

Match the language and heading style of the rest of the target file.

## Rules

- **One concern per bullet**: Split long constraints into separate bullets
- **No duplication**: Scan the section and related sections before adding
- **Preserve file structure**: Only add/update; do not remove or reorganize other sections
- **Character hygiene**: No gremlin/control characters in written text
