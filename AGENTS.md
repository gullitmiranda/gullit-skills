# Agent Instructions

## Git Workflow

- This is a personal repository owned by `gullitmiranda`.
- Do not open pull requests for this repository by default.
- When the user asks to publish committed changes here, push directly to `main` unless the user explicitly asks for a PR or a separate review branch.

## Agent workspace

- `.agents/AGENTS.md` is the authority for agent working artifacts, including their location, lifecycle, and tracking.
- `.agents/plans` and `.cursor/plans` are the same ignored local plan tree: one real directory, the other a relative symlink, either direction. In Cursor, create and edit plans through `.cursor/plans`. Do not ask which path to use. Do not create a second real plan directory.
