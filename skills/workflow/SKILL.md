---
name: workflow
description: Language, terminal, workspace, branch, commit, PR, planning, and documentation workflow rules. Use when writing in English, committing, creating PRs, or creating plans in .cursor/plans/.
---

# Workflow Rules

Workflow rules for language, git, plans, and documentation in this workspace.

## Hard Rules

- Only commit when explicitly requested; never commit unstaged changes without explicit request.
- Never commit directly to main/master; all main branch changes go through PRs.
- NEVER commit files under `.cursor/plans/` — local-only and gitignored; committing them breaks the user's setup.
- NEVER include timelines, schedules, cronograms, or time estimates in plans.
- With Trunk hooks, run the final `git commit` with stdin closed (`</dev/null`) so the hook cannot hang on EOF. If still stuck or reporting daemon/GRPC errors, run `trunk daemon shutdown` once, then retry.

## Language

- Write all documentation, comments, code, commit messages, and PR titles/descriptions in English.

## Workspace & Multi-Repo

- Verify which repository an operation targets before running it; never assume a single git repo in a multi-repo workspace. Treat each repository as a separate git state.
- Temporary files go in `./tmp` or system tmp; never commit them.

## Branches & Commits

- Before creating a feature branch, fetch and fast-forward the local base branch so work starts from the latest `origin/main` or `origin/master`.
- Small, focused commits in conventional commit format.
- Reference issues when applicable: GitHub Issues by default; Linear only when explicitly referenced in the prompt or commits.

## Plans

- Unless explicitly asked otherwise, switch to Plan mode before creating or updating plan files so the originating chat is referenced.
- Save plans in `.cursor/plans/` with a `.plan.md` extension (e.g. `descriptive-name.plan.md`), using the native Cursor plan structure: `## Objective`, `## Tasks`, `## Dependencies`, `## Acceptance Criteria`, `## Notes`.
- Focus on what needs to be done, never when.

## Documentation

- Prefer linking to the GitHub repository URL instead of just mentioning the repo name.
- Do not include plan-only labels, deliverable IDs, or internal execution markers (e.g. `D04`, `PR 2`, spike numbering) in product/code documentation. Keep those in plans, PR descriptions, or issue tracker context.

## ZeroPath References

- Apply the `zeropath` skill whenever the task or draft mentions ZeroPath, `zeropath`, ZeroPath findings, or URLs under `https://zeropath.com/`.
- When referencing ZeroPath findings in any output, include the full URL as visible text: `https://zeropath.com/app/issues/<uuid>`. No UUID-only references, shortened links, hidden markdown labels, or vague labels like `ZeroPath 6.3`.
- Do not add ZeroPath information to unrelated PRs or documents; these rules apply only when ZeroPath is already part of the task, draft, commits, or linked evidence.
