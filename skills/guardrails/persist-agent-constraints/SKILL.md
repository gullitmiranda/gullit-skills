---
name: persist-agent-constraints
description: Persists agent constraints (what not to do) in the project's canonical place for agent instructions. Use when the user states constraints, prohibitions, or things to avoid (e.g. nao faca, evite, don't, never, avoid, nao quero que, proibido).
---

# Persist Agent Constraints

When the user states **constraints** (prohibitions, restrictions, things to avoid — including corrections like "stop doing X"), persist them in the most relevant file so future sessions respect them.

## Hard Rules

- **One concern per bullet**: split long constraints into separate bullets.
- **No duplication**: scan the section and related sections before adding; refine an equivalent existing rule instead of duplicating.
- **Preserve file structure**: only add/update; do not remove or reorganize other sections.
- **Character hygiene**: no gremlin/control characters in written text.
- **Workspace authority**: when a constraint governs plans, notes, scratch, or their tracking, read `.agents/AGENTS.md` first when it exists.

## Workflow

1. **Parse** the constraint into one or more short, clear imperative bullet lines.
2. **Smart-route using the learn skill's logic** (see `learn/SKILL.md` Step 3):
   - Identify the constraint's topic (git, safety, quality, k8s, etc.), find the existing file that covers that topic, route to that file's constraints/safety section.
   - Examples: "don't push to main" -> `safety/SKILL.md` under Git Safety; "don't use kubectl delete" -> `k8s/SKILL.md` or `safety/SKILL.md`; "don't add emojis" -> `quality/SKILL.md` under Output hygiene; "don't auto-commit" -> `safety/SKILL.md` under Absolute Rules.
   - If no topical file matches, fall back to `.agents/AGENTS.md` for agent-workspace rules, `AGENTS.md` for cross-tool project rules, or the appropriate scope target per learn skill rules.
3. **Add or update the constraints section** in the target file:
   - Use `## Constraints` or `## Don't / Avoid`, or the file's existing equivalent (`## Absolute Rules`, `## Safety Checks`). If constraints naturally fit an existing section, add there instead of creating a new one.
   - Match the language and heading style of the rest of the target file.
4. **Cross-tool sync**: if the project has multiple instruction formats (`.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, `AGENTS.md`), update all that exist. See learn skill Step 5.
5. **Confirm**: report what was added, where (exact path and section).

## Section Format

```markdown
## Constraints

- Do not commit to main without a PR
- Do not use Linear for this project (use GitHub Issues)
- Do not add timelines or cronograms to plans
```
