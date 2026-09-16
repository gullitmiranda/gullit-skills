# Agent Instructions

## Git Workflow

- This is a personal repository owned by `gullitmiranda`.
- Do not open pull requests for this repository by default.
- When the user asks to publish committed changes here, push directly to `main` unless the user explicitly asks for a PR or a separate review branch.

## Agent workspace

- `.agents/AGENTS.md` is the authority for agent working artifacts, including their location, lifecycle, and tracking.
- Local implementation plans live only under `.agents/plans/` (ignored, never committed). `.cursor/plans` may be a compatibility symlink to that tree; do not create a second real plan directory, and do not create or repair the symlink without explicit user direction.
