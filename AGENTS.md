# Agent Instructions

## Git Workflow

- This is a personal repository owned by `gullitmiranda`.
- Do not open pull requests for this repository by default.
- When the user asks to publish committed changes here, push directly to `main` unless the user explicitly asks for a PR or a separate review branch.

## Agent workspace

- `.agents/AGENTS.md` is the authority for agent working artifacts, including their location, lifecycle, and tracking.
- Local implementation plans in `.agents/plans/` are ignored and never committed. `.cursor/plans/` is a legacy local input; do not move it or create its compatibility symlink without explicit user direction.
