# gullit-skills

Personal skills for AI coding agents, following the [Agent Skills](https://agentskills.io) open standard.

## Directory Structure

```
skills/                        # Cross-agent skills (installed by all agents)
  <skill-name>/SKILL.md
  gh-profile-template/SKILL.md # Reusable template — copy and fill in placeholders

docs/                          # Workflow docs and tool adapters
  skills-map.md
  workflows/
  tool-adapters/

.cursor/skills/                # Cursor-specific skills
  plan-archive/SKILL.md

.claude/skills/                # Claude Code-specific skills
.agents/skills/                # Other agent-specific skills
```

- `skills/` contains skills that work across any agent runtime.
- `docs/` contains workflow composition docs, context transfer guidance, and tool adapters.
- Skills with a `-template` suffix are reusable templates with placeholders. Copy to your own skills repo, rename, and fill in the values.
- `.<agent>/skills/` contains skills scoped to a specific agent (Cursor, Claude, Codex, etc.).

## Workflow Entry Points

This repo keeps atomic skills independent and documents how to compose them into
larger engineering workflows.

- [`docs/skills-map.md`](docs/skills-map.md): phase-based map of personal and external skills.
- [`docs/workflows/`](docs/workflows/): example flows for features, bugs, architecture work, existing plans, and parallel workstreams.
- [`docs/context-management.md`](docs/context-management.md): portable context capsule protocol.
- [`docs/agent-selection.md`](docs/agent-selection.md): when to use main chat, subagents, forks, IDE agents, or terminal/ACP/Pi-style agents.
- [`docs/tool-adapters/`](docs/tool-adapters/): Cursor, Zed, terminal-agent, and Pi-extension adapters.
- [`docs/references.md`](docs/references.md): external references that shaped the workflow design.

Core orchestration skills:

- `engineering-workflow`: choose the workflow and compose atomic skills.
- `agent-selection`: recommend the right agent/runtime for the next phase.
- `context-capsule`: create portable handoff context for subagents, forks, Zed threads, terminal agents, or later resume.

## SKILL.md Format

Each skill is a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: Short description of what the skill does and when to use it.
---

# My Skill

Instructions for the agent...
```

See the [agentskills.io](https://agentskills.io) spec for the full format reference.

## Install

Requires [ai-skills-cli](https://github.com/gullitmiranda/ai-skills-cli).

```bash
# Install all cross-agent skills
ai-skills add gullitmiranda/gullit-skills

# Install a single skill
ai-skills add https://github.com/gullitmiranda/gullit-skills/tree/main/skills/git

# Install Cursor-specific skills
ai-skills add https://github.com/gullitmiranda/gullit-skills/tree/main/.cursor/skills/plan-archive

# Pin to a specific ref
ai-skills add gullitmiranda/gullit-skills --ref v1.0.0
```

<details>
<summary>Don't have <code>ai-skills</code> yet?</summary>

```bash
curl -fsSL https://raw.githubusercontent.com/gullitmiranda/ai-skills-cli/main/scripts/install | bash
```

Or review the script before running:

```bash
curl -fsSL https://raw.githubusercontent.com/gullitmiranda/ai-skills-cli/main/scripts/install -o /tmp/ai-skills-install.sh && \
  less /tmp/ai-skills-install.sh && \
  read -p "Execute? [y/N] " -n 1 -r && echo && \
  [[ $REPLY =~ ^[Yy]$ ]] && bash /tmp/ai-skills-install.sh
```

</details>
