# gullit-skills

Personal skills for AI coding agents, following the [Agent Skills](https://agentskills.io) open standard.

## Repository layout

```text
skills/                        # Cross-agent skills in installation-compatible source paths
  <skill-name>/SKILL.md

docs/                          # Workflow composition and runtime adapters
  skills-map.md
  workflows/
  tool-adapters/

.agents/                       # This repository's agent workspace contract
  AGENTS.md
  notes/                       # Tracked durable working knowledge
  plans/                       # Local ignored implementation plans
```

Skills remain in flat source paths while the installer work adds safe migration for existing installations. The public skill identities below are stable; the target nested source-home tree will be applied only when that migration is available.

## Agent workspace

`.agents/AGENTS.md` is the authority for agent working artifacts in this repository:

- `.agents/plans/` holds ignored local implementation plans.
- `.agents/notes/` holds tracked durable working knowledge.
- `.agents/scratch/` holds ignored disposable material.
- `.cursor/plans/` is a legacy local input that is migrated only with explicit user direction.

## Workflow entry points

The core workflow is self-contained and composes small skills instead of requiring third-party installs:

- `work-intake`: inspect context and select the smallest next route.
- `plan`: create or refine one ready local implementation plan.
- `build-plan`: execute one ready local implementation plan.
- `incremental-delivery`: coordinate multiple independent deliveries.
- `work-closeout`: assess a plan or work context and perform confirmed closeout actions.
- `agent-workspace`: establish or migrate the workspace contract.
- `agent-notes`: manage tracked notes and their lifecycle.
- `cursor-project-path-migration`: move a Cursor project path with reversible workspace-state recovery.

Legacy names such as `workflow-intake`, `engineering-workflow`, `work-context-cleanup`, `workflow`, `agents-standard`, and `project-path-migration` are compatibility entry points only. New workflows should use the public names above.

See [`docs/skills-map.md`](docs/skills-map.md) for the workflow map, [`docs/workflows/`](docs/workflows/) for examples, and [`docs/tool-adapters/`](docs/tool-adapters/) for runtime guidance.

## SKILL.md format

Each skill is a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: Short description of what the skill does and when to use it.
---

# My Skill

Instructions for the agent.
```

See the [Agent Skills specification](https://agentskills.io) for the full format reference.

## Install

Requires [ai-skills-cli](https://github.com/gullitmiranda/ai-skills-cli).

```bash
# Install all cross-agent skills
ai-skills add gullitmiranda/gullit-skills

# Install one workflow entry point
ai-skills add https://github.com/gullitmiranda/gullit-skills/tree/main/skills/work-intake

# Install the agent workspace contract
ai-skills add https://github.com/gullitmiranda/gullit-skills/tree/main/skills/agent-workspace

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
