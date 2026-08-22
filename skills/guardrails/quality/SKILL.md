---
name: quality
description: Quality gates, native file-edit safety, commit and PR standards, and output character hygiene. Use when writing code, editing files, committing, creating PRs, generating text, or when the user runs /gremlin-clean.
---

# Quality Rules

This skill is preventive — it governs what you generate. To clean up existing
AI-generated text, use `deslop`; to strip gremlin characters from existing
files, use `gremlin-clean`.

## Output / Character Hygiene (Gremlin Characters)

**MANDATORY:** All generated text — code, comments, docs, user-facing messages — must be free of gremlin characters (invisible/problematic Unicode). They cause rendering issues, lint errors (e.g. `no-irregular-whitespace`), and parsing errors. Models sometimes emit them despite instructions.

Use only **U+0020** (space) and **LF/CRLF**. Avoid:

- **Zero-width**: U+200B (ZWSP), U+200C (ZWNJ), U+200D (ZWJ), U+2060 (word joiner), U+2063 (invisible separator)
- **Non-breaking / other spaces**: U+00A0 (NBSP), U+1680, U+180E, U+2000–U+200A, U+202F, U+205F, U+3000 (ideographic space), U+FEFF (BOM)
- **Line/paragraph**: U+2028, U+2029
- **Other**: U+00AD (soft hyphen), control characters (U+0000–U+001F, U+007F), directional formatting

When pasting or referencing external text, rewrite it as clean text instead of copying raw content that may contain gremlins.

**/gremlin-clean:** follow the `gremlin-clean` skill: run its bundled `scripts/strip-gremlins.py` on the target file(s) and report. The script skips binary files (`.db`, `.sqlite`, images, archives, fonts, compiled files, etc.).

## File Operations

- Use the harness's native file tools (`edit_file`, `write_file`, `save_file`, `move_path`, `copy_path`, `delete_path`, `create_directory`) when available for file operations inside project roots.
- Do not edit files via shell (`sed -i`, `python3 << EOF`, heredocs, `cat >`, `mv`, `cp`) inside project roots.
- Shell file edits are allowed only outside all project roots (for example, an unadded worktree or `~/.agents/skills/`); state the exception before using them.

## Commit Standards

- Conventional commit format: `<type>(<scope>): <description>`; types: feat, fix, chore, docs, style, refactor, test
- Present tense, imperative mood; concise but descriptive
- Write commit messages in the default artifact language defined by `user-preferences`.
- Issue references: GitHub Issues by default (`#123` / `owner/repo#123`); Linear `TEAM-123` only when explicitly referenced

## Lint and format fix workflow (Trunk)

1. Run `trunk check --fix` first to auto-fix everything Trunk can fix.
2. Address remaining issues manually.
3. Re-run `trunk check` to confirm.

Do not manually fix what Trunk can fix.

## Quality Gates

### Pre-commit

- Tests pass, linting passes, build succeeds, security scans pass
- No sensitive data in commits

### Draft PR Opening

A draft PR may be opened early by `pr-delivery` to start remote checks before isolated review and final local validation finish. Before doing so, verify the source branch, committed diff, PR metadata, and publishable links. Keep the PR draft and do not claim unexecuted validation as passing.

### Ready Or Merge

Before a PR is marked ready or merged:

- All applicable quality gates pass; code review requirements met
- Documentation updated when needed; tests cover new functionality
- The final remote head must be the reviewed revision
- For ZeroPath-related changes, include relevant local validation and use the `zeropath` skill for any ZeroPath scan or finding-status evidence

## Pull Request Standards

- Write PR titles and descriptions in the default artifact language defined by `user-preferences`; use conventional commit format for PR titles
- Reference issues when applicable: GitHub Issues by default; Linear only when explicitly referenced in commits or prompt
- When referencing PRs or issues, always use full GitHub URLs (e.g., `https://github.com/org/repo/pull/123`), never shorthand like `repo #123` or `repo#number`
- When a PR references ZeroPath, include known findings as complete visible URLs like `https://zeropath.com/app/issues/<uuid>` and do not add ZeroPath content to unrelated PRs
- Do not claim "ZeroPath confirmed resolved" unless confirmed by the ZeroPath CLI or explicit ZeroPath evidence supplied by the user; otherwise say the change addresses the finding pattern and is awaiting re-scan
- **Before publishing any text with file paths or links** (PR body, issue body, comments, Slack/Linear messages, versioned docs), follow the `publish-safe-links` skill to avoid linking to gitignored, untracked, or unpushed files such as `.agents/plans/`, `.cursor/plans/`, `.factory/`, `wt-*/`, or absolute machine paths
