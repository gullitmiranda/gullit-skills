# gullit-skills

Common personal skills for AI coding agents.

## Structure

Skills follow the filesystem convention for discovery:

- Single skill: `SKILL.md` at root
- Multiple skills: `<skill-name>/SKILL.md`
- Agent-specific: `.cursor/skills/...`, `.claude/skills/...`
- Common across agents: `.ai-agents/skills/...`

## Install

```bash
# Install all skills from this repo
ai-skills add https://github.com/gullitmiranda/gullit-skills

# Install a single skill
ai-skills add https://github.com/gullitmiranda/gullit-skills/tree/main/skills/my-skill
```
