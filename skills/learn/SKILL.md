---
name: learn
description: Persist learned rules with smart routing to topical files across tools. Use when the user runs /learn or asks you to remember a preference or project convention.
---

# Learn (Smart-Routed Memory)

Persist "learned" instructions by routing them to the file where they will
actually be loaded in context, not a catch-all. Agents load skills/rules by
topic relevance; a rule in the wrong file is a rule that gets ignored.

## Step 1 - Parse the instruction

- `rule`: one bullet, imperative, concise
- `topic`: the rule's domain (git, quality, safety, workflow, k8s, documentation, etc.)
- `appliesTo` (optional): path or glob, only when explicitly specified
- `scope`: default `project`

Explicit syntax: `scope=user|project|local: <rule>`,
`applies-to=<path-or-glob>: <rule>` (combinable).

## Step 2 - Determine scope

| Signal | Scope |
| ------ | ----- |
| "for all my projects" / "global" / about assistant behavior or personal preferences | `user` |
| "only for me in this repo" / "local" / "do not commit" | `local` |
| About this repo's conventions, stack, or tooling | `project` |
| Ambiguous | Ask: "scope: project / local / user?" |

Heuristics: assistant behavior or personal style -> `user` (e.g. "only push
when requested", "nao faca commits na main sem eu pedir"); repo
conventions/stack -> `project` ("in this repo we use pnpm"); personal AND
repo-specific -> `local`.

## Step 3 - Smart route to best file

Do NOT blindly append to a catch-all file.

### 3a. Candidate files by scope

**scope = user:**

| Priority | Location | Notes |
| -------- | -------- | ----- |
| 1 | Topical SKILL.md in `~/.claude/skills/`, `~/.cursor/skills/`, `~/.codex/skills/` | Best topical match wins |
| 2 | `~/.claude/CLAUDE.md` | Claude Code user-level |
| 3 | `~/.codex/AGENTS.md` | Codex user-level |
| Fallback | `~/.cursor/skills/user-preferences/SKILL.md` | Only if no topical match |

**scope = project:**

| Priority | Location | Notes |
| -------- | -------- | ----- |
| 1 | Topical SKILL.md in `.claude/skills/`, `.cursor/skills/` | Best topical match wins |
| 2 | `.cursor/rules/*.mdc` | Cursor rules (glob-based) |
| 3 | `./AGENTS.md` | Cross-tool |
| 4 | `./CLAUDE.md` or `.claude/CLAUDE.md` | Claude Code project-level |
| Fallback | `./AGENTS.md` under a new topical section | Only if no topical match |

**scope = local:** `./AGENTS.local.md`, else `./CLAUDE.local.md`.

### 3b. Match rule topic to candidates

Read each candidate's frontmatter `description` (SKILL.md), `description`/`globs`
(.mdc), or heading structure. Strong signals: description mentions the topic;
a section heading matches. Moderate: file already contains related rules. Pick
the highest-scoring file; on ties prefer the more specific one (e.g.
`git/SKILL.md` over `workflow/SKILL.md` for a branching rule).

### 3c. Topic-to-file quick reference

| Rule topic | Likely target file |
| ---------- | ------------------ |
| Git commits, branches, push, merge, rebase, worktree | `git/SKILL.md` or `safety/SKILL.md` |
| Code style, linting, formatting, conventional commits | `quality/SKILL.md` |
| PR creation, review, merge strategy | `pr/SKILL.md` |
| Dangerous operations, destructive commands, permissions | `safety/SKILL.md` |
| Language, documentation style, planning format | `workflow/SKILL.md` |
| Kubernetes operations | `k8s/SKILL.md` |
| GitHub Issues, MCP, external integrations | `integration/SKILL.md` or topical skill |
| Agent behavior constraints (don't do X) | Delegate to `persist-agent-constraints` skill |
| File-specific rules (applies to certain paths/globs) | `.cursor/rules/*.mdc` |

### 3d. New file vs. fallback

Create a new topical file when the rule is a recurring topic likely to get more
rules, or 2+ unrelated rules would fit the same new topic. Otherwise use the
fallback, under a descriptive section heading (e.g. `## Documentation`), never
a generic "Learned preferences" bucket.

## Step 4 - Write with de-duplication

1. Read the target file; if an equivalent rule exists, refine it instead of duplicating.
2. Append under the section matching the rule's sub-topic, else the most relevant existing section, else a new section with a clear heading.
3. Write the rule as a single bullet (imperative, concise).

Format specifics:

- **SKILL.md:** append bullet under the matching section.
- **Cursor rules (.mdc):** if `appliesTo` is specified, set/update `globs`:
  ```yaml
  ---
  description: Rules for API routes
  globs: ["src/api/**/*.ts"]
  alwaysApply: false
  ---
  ```
- **AGENTS.md:** append under `## Always apply` or create a contextual section.

## Step 5 - Cross-tool sync

If the project already has instruction files for multiple tools, write the rule
to ALL applicable existing formats: topical SKILL.md (`.claude/skills/` or
`.cursor/skills/`), matching `.cursor/rules/*.mdc`, `CLAUDE.md`, `AGENTS.md`.
Do NOT create new tool-specific directories just for sync.

## Step 6 - Gitignore update (local scope only)

- Read global excludes: `git config --get core.excludesfile`
- If empty, use `~/.config/git/ignore` (create if missing)
- Append `AGENTS.local.md` and `CLAUDE.local.md` if not present
- Do NOT change git config

## Step 7 - Confirm

Report what was saved, where (exact file path and section), which scope, and
all files updated if cross-tool sync happened.

## File templates (when creating new files)

`AGENTS.md`:

```markdown
# AGENTS

## Always apply (project)

## Contextual (project)
```

`AGENTS.local.md`:

```markdown
# AGENTS (local)

## Always apply (local)

## Contextual (local)
```

`.claude/CLAUDE.md` (shim):

```markdown
# Claude instructions

Read and follow `AGENTS.md` as the canonical project rules.

If `AGENTS.local.md` exists, treat it as personal (local) preferences.
```

## Anti-patterns (what NOT to do)

- **Never** dump all rules into a single catch-all file regardless of topic
- **Never** write a git rule to `user-preferences/SKILL.md` when `git/SKILL.md` exists
- **Never** ignore existing topical files and always use `AGENTS.md`
- **Never** create a new file when an existing file already covers the topic
- **Never** duplicate a rule that already exists in the target file
