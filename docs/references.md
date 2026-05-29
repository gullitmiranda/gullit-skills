# References

These repositories influenced the workflow design in this repo. They are
references, not dependencies. Do not vendor their code or assume their exact
tooling is present.

## Matt Pocock Skills

Repository: <https://github.com/mattpocock/skills>

Useful ideas:

- Small composable skills instead of one large process.
- `grill-with-docs` for alignment, domain language, `CONTEXT.md`, and ADRs.
- `tdd` for red-green-refactor in vertical slices.
- `diagnose` for feedback-loop-first debugging.
- `to-prd` and `to-issues` for turning discussion into trackable work.
- `handoff` for context compaction when a conversation needs to continue later.

How this repo uses the ideas:

- Treat Matt's skills as externally installed skills.
- Document how to compose them with personal skills such as `plan`,
  `incremental-delivery`, `git-worktree`, `quality`, and `pr`.
- Keep personal orchestration skills thin so the atomic skills remain reusable.

## Davis Pi Setup

Repository: <https://github.com/davis7dotsh/my-pi-setup>

Useful ideas:

- `copy-all` shows when exact transcript transfer is useful.
- `diff` tracks files changed by an agent run and makes review easier.
- `usage` turns session logs into cost and usage reports.
- `tps-tracker` adds lightweight runtime feedback.
- Simple command wrappers can turn repeated prompts into reusable tool actions.

How this repo uses the ideas:

- Treat transcript copying as an exceptional transfer mode, not the default.
- Prefer context capsules for normal handoff and tool switching.
- Document Pi-style utilities as adapter ideas for future automation.

## Dmmulroy Pi Dotfiles

Repository: <https://github.com/dmmulroy/.dotfiles/tree/main/home/.pi>

Useful ideas:

- A Pi workspace can combine skills, extensions, settings, MCP adapters, themes,
  and secret cloaking.
- Extension packages can live in a workspace with strict TypeScript checks.
- Tooling can support skill discovery, skill toggling, todos, MCP, and output
  protection.
- Dotfiles can make an agent environment reproducible across machines.

How this repo uses the ideas:

- Keep this repository focused on portable skills and docs.
- Put tool-specific details under `docs/tool-adapters/`.
- Consider future Pi or terminal-agent extensions only after the workflow docs
  prove useful in practice.

## Local Design Choice

The local strategy is:

```text
portable workflow docs
-> small orchestration skills
-> atomic reusable skills
-> optional tool-specific adapters
```

This keeps the workflow understandable in Cursor, Zed, terminal agents, and
future ACP-compatible tools without coupling the core skills to one runtime.
