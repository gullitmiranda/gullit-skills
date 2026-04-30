---
name: learn
description: Persist learned rules with smart routing to topical files across tools. Use when the user runs /learn or asks you to remember a preference or project convention.
---

# Learn (Smart-Routed Memory)

Persist "learned" instructions by routing them to the file where they will
actually be loaded in context, not a catch-all. Works across Cursor, Claude Code,
Codex, and other agents that read standard instruction files.

## Core Principle

**Route to where the rule will be read.** A git rule must land in the git skill,
not a generic preferences file. Agents load skills/rules by topic relevance; a
rule in the wrong file is a rule that gets ignored.

## Step 1 - Parse the instruction

Extract from the user's message:

- `rule`: one bullet, imperative, concise
- `topic`: what domain does this rule belong to (git, quality, safety, workflow, k8s, documentation, etc.)
- `appliesTo` (optional): path or glob pattern (only when explicitly specified)
- `scope`: default `project` (see Step 2)

### Explicit syntax (when the user specifies)

- `scope=user: <rule>`
- `scope=project: <rule>`
- `scope=local: <rule>`
- `applies-to=<path-or-glob>: <rule>` (combinable: `scope=project applies-to=backend/: ...`)

## Step 2 - Determine scope

| Signal                                                                                                | Scope                                 |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------- |
| "for all my projects" / "global" / "always for me" / about assistant behavior or personal preferences | `user`                                |
| "only for me in this repo" / "local" / "do not commit"                                                | `local`                               |
| About this repo's conventions, stack, or tooling                                                      | `project`                             |
| Ambiguous                                                                                             | Ask: "scope: project / local / user?" |

### Heuristic upgrade (avoid wrong default)

- Rule about assistant behavior or personal style -> `user`
  - EN: "only push when requested", "ask before committing", "be concise", "avoid emojis"
  - PT-BR: "sempre respeite quando eu mandar usar uma git worktree", "nao faca commits na main sem eu pedir"
- Rule about a specific repo's conventions/stack -> `project`
  - "in this repo we use pnpm", "our CI uses trunk"
- Rule personal AND repo-specific -> `local`

## Step 3 - Smart route to best file

This is the critical step. Do NOT blindly append to a catch-all file.

### 3a. Build candidate file list

Scan the instruction file locations that the current scope can write to:

**scope = user:**

| Priority | Location                                                                                                    | Format                   |
| -------- | ----------------------------------------------------------------------------------------------------------- | ------------------------ |
| 1        | Topical SKILL.md in any user-level skills dir: `~/.claude/skills/`, `~/.cursor/skills/`, `~/.codex/skills/` | Best topical match wins  |
| 2        | `~/.claude/CLAUDE.md`                                                                                       | Claude Code user-level   |
| 3        | `~/.codex/AGENTS.md`                                                                                        | Codex user-level         |
| Fallback | `~/.cursor/skills/user-preferences/SKILL.md`                                                                | Only if no topical match |

**scope = project:**

| Priority | Location                                                                      | Format                           |
| -------- | ----------------------------------------------------------------------------- | -------------------------------- |
| 1        | Topical SKILL.md in project skills dirs: `.claude/skills/`, `.cursor/skills/` | Best topical match wins          |
| 2        | `.cursor/rules/*.mdc`                                                         | Cursor rules (glob-based)        |
| 3        | `./AGENTS.md`                                                                 | Cross-tool (Codex, Claude, etc.) |
| 4        | `./CLAUDE.md` or `.claude/CLAUDE.md`                                          | Claude Code project-level        |
| Fallback | `./AGENTS.md` under a new topical section                                     | Only if no topical match         |

**scope = local:**

| Priority | Location            | Format            |
| -------- | ------------------- | ----------------- |
| 1        | `./AGENTS.local.md` | Cross-tool local  |
| 2        | `./CLAUDE.local.md` | Claude Code local |

### 3b. Match rule topic to candidate files

For each candidate file that exists, read its frontmatter `description`
(for SKILL.md) or `description`/`globs` (for .mdc) or heading structure.

**Score the match:**

- Does the file's description mention the rule's topic? (strong signal)
- Does the file have a section heading related to the rule? (strong signal)
- Does the file already contain similar or related rules? (moderate signal)

**Pick the highest-scoring file.** If multiple files score equally, prefer the
one that is more specific (e.g., `git/SKILL.md` over `workflow/SKILL.md` for
a branching rule).

### 3c. Topic-to-file quick reference (common mappings)

This table helps the agent route without scanning when the mapping is obvious:

| Rule topic                                              | Likely target file                            |
| ------------------------------------------------------- | --------------------------------------------- |
| Git commits, branches, push, merge, rebase, worktree    | `git/SKILL.md` or `safety/SKILL.md`           |
| Code style, linting, formatting, conventional commits   | `quality/SKILL.md`                            |
| PR creation, review, merge strategy                     | `pr/SKILL.md`                                 |
| Dangerous operations, destructive commands, permissions | `safety/SKILL.md`                             |
| Language, documentation style, planning format          | `workflow/SKILL.md`                           |
| Kubernetes operations                                   | `k8s/SKILL.md`                                |
| GitHub Issues, MCP, external integrations               | `integration/SKILL.md` or topical skill       |
| Agent behavior constraints (don't do X)                 | Delegate to `persist-agent-constraints` skill |
| File-specific rules (applies to certain paths/globs)    | `.cursor/rules/*.mdc`                         |

If the rule's topic does not match any existing file, consider whether it
warrants a new topical file or belongs in the catch-all.

### 3d. When to create a new file vs. use fallback

**Create a new topical file** when:

- The rule represents a recurring topic that will likely get more rules
- There are already 2+ unrelated rules that would fit the same new topic

**Use the fallback** (user-preferences or AGENTS.md) when:

- The rule is truly unique/miscellaneous
- It does not fit any existing or logical new topic grouping

When using the fallback, add the rule under a descriptive section heading
(not a generic "Learned preferences" bucket). E.g., `## Documentation`,
`## Editor behavior`, etc.

## Step 4 - Write with de-duplication

1. Read the target file
2. Check if an equivalent rule already exists -> refine instead of duplicating
3. Find the appropriate section:
   - If the file has a section matching the rule's sub-topic, append there
   - If not, append to the most relevant existing section
   - As a last resort, create a new section with a clear heading
4. Write the rule as a single bullet (imperative, concise)

### Format-specific writing

**SKILL.md files:** Append bullet under the matching section.

**Cursor rules (.mdc):** If `appliesTo` is specified, set/update the `globs` field:

```yaml
---
description: Rules for API routes
globs: ["src/api/**/*.ts"]
alwaysApply: false
---
```

**AGENTS.md:** Append under `## Always apply` or create a contextual section.

## Step 5 - Cross-tool sync (when multiple formats exist)

If the project has instruction files for multiple tools, write the rule to ALL
applicable formats so it takes effect regardless of which tool is used.

Check which of these exist and update each:

1. `.claude/skills/` or `.cursor/skills/` -> write to the topical SKILL.md
2. `.cursor/rules/` -> write to the matching .mdc rule file
3. `CLAUDE.md` -> append to the relevant section
4. `AGENTS.md` -> append to the matching section

**Do NOT create new tool-specific directories** just for cross-tool sync.
Only sync to formats that already exist in the project.

## Step 6 - Gitignore update (local scope only)

- Read global excludes: `git config --get core.excludesfile`
- If empty, use `~/.config/git/ignore` (create if missing)
- Append `AGENTS.local.md` and `CLAUDE.local.md` if not present
- Do NOT change git config

## Step 7 - Confirm

Report:

- What was saved (the rule text)
- Where (exact file path and section)
- Which scope
- If cross-tool sync happened, list all files updated

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
