# gullit-skills

Personal skills for AI coding agents, following the [Agent Skills](https://agentskills.io) open standard.

## Directory Structure

```
skills/                        # Cross-agent skills (installed by all agents)
  <skill-name>/SKILL.md
  gh-profile-template/SKILL.md # Reusable template — copy and fill in placeholders

.cursor/skills/                # Cursor-specific skills
  plan-archive/SKILL.md

.claude/skills/                # Claude Code-specific skills
.agents/skills/                # Other agent-specific skills
```

- `skills/` contains skills that work across any agent runtime.
- Skills with a `-template` suffix are reusable templates with placeholders. Copy to your own skills repo, rename, and fill in the values.
- `.<agent>/skills/` contains skills scoped to a specific agent (Cursor, Claude, Codex, etc.).

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
