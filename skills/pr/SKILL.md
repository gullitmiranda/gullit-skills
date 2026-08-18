---
name: pr
description: Pull request lifecycle - create and update PRs with gh CLI, validate quality gates, keep PR metadata aligned with the current diff, and mark ready for review. Use when creating a PR, updating an existing PR after new changes, running quality checks, or marking PR ready for review.
---
# Pull Request Management

## Rules

- Always use `gh` CLI for GitHub operations.
- Generate conventional commit format titles: `<type>(<scope>): <summary>`, under 72 chars.
- Treat PR title, description, linked issues, and test plan as living metadata that must match the current branch diff. Re-check and update after any material change.
- Keep PR title and body grounded in `git diff <base>...HEAD`, not only commit message wording.
- Before creating or updating a PR, check for existing related PRs/issues with overlapping scope and cross-reference when it helps reviewers.
- Issues are created on GitHub (native sync sends them to Linear), but Linear has the richer integration — especially status changes. When linking an issue, check the GitHub issue for its synced Linear ID (the sync adds it to the issue) and link BOTH: the GitHub issue (auto-close on merge) and the Linear issue (status tracking). Use Linear alone only when a Linear URL/ID was given with no GitHub counterpart. Never invent an ID.
- Never claim tests/checks passed unless they were actually executed in the current session.
- Always include URLs when reporting GitHub PR/issue references; markdown links or compact raw URLs are fine, never bare `#123`.
- Apply the `zeropath` skill only for PRs that already mention ZeroPath in the prompt, commits, diff, PR body, comments, or linked evidence. Do not add ZeroPath sections to unrelated PRs.
- If the current branch belongs to a `gh stack` stack (check `gh stack view --json`), delegate stack operations (submit, sync, merge, navigation) to the `gh-stack` skill; never use `gh pr merge` on a stacked PR — use `gh stack merge <target> --yes`.
- Run quality checks before a standard PR is marked ready; `/pr draft` may open an early draft after an integrity preflight so remote checks can start.

## PR Information Quality Contract

Every PR body should contain, when applicable:

1. **Why**: concise problem/context statement
2. **What changed**: grouped bullets by area/component
3. **Risk & impact**: user impact, operational risk, migrations, breaking changes
4. **Validation**: exact commands executed and short outcomes
5. **Rollout/Backout**: only when deployment risk is non-trivial
6. **Linked issues**: GitHub Issue references supported by branch context, plus the synced Linear ID when the issue has one (see Rules)

Hard rules:

- No placeholders like "TODO", "N/A", or template hints in the final body.
- No "tests passed" without command evidence.
- Remove stale sections when scope changes; do not append contradictory notes.
- Prefer short factual bullets over marketing text.

## Routes

### `/pr` — Create Pull Request

1. Pre-flight: on a feature branch (not main/master), commits ahead of base, branch pushed, `gh` authenticated. If uncommitted changes exist, use `/commit` first.
2. Analyze `git log <base>..HEAD` and `git diff <base>...HEAD`; identify change type, scope, and issue references.
3. Build the body from `.github/pull_request_template.md` if present, else the Quality Contract above. Test Plan lists only commands actually run. If the PR addresses ZeroPath findings, include each as a complete visible URL, e.g. `Addresses ZeroPath finding: https://zeropath.com/app/issues/<uuid>`.
4. `gh pr create` with heredoc body; return the PR URL as a markdown link.

### `/pr draft` — Early Draft PR

Use only when a parent workflow (e.g. `pr-delivery`) needs remote checks running before final local validation.

1. Run the integrity preflight (branch, commits, push, auth, diff/title/body/issues, `publish-safe-links` on the body).
2. Create or reuse a **draft** PR. Do not request reviewers, mark ready, or enable merging.
3. State that checks are in progress; never claim they passed.
4. Defer full quality gates to the final reviewed revision; `/pr` and `/pr ready` still require them.

### Continuous PR Sync — after any material change

1. Check for an existing open PR with `gh pr view`; if none, follow the create flow.
2. Compare PR title/body against the current diff, commits, and executed validations for drift (scope, bullets, test plan, risks, linked issues, draft/ready status).
3. If drift exists, update immediately with `gh pr edit --title ... --body-file ...`. Remove stale claims rather than piling on corrections. Keep ZeroPath references as complete visible URLs; never claim ZeroPath confirmed resolution without CLI or user-supplied evidence.
4. Do not end a PR-related task while metadata is known stale; mention the sync in the final response.

### Review Comment Resolution

- Inspect every targeted unresolved thread/comment, not a subset. For automated review agents, address each targeted comment individually.
- For ZeroPath comments, use the `zeropath` skill and prefer CLI-backed evidence. Include finding URLs as complete visible URLs. Do not say a finding is resolved unless the CLI or user-supplied evidence confirms it; otherwise say the change addresses the pattern and is awaiting re-scan.
- Mark each addressed GitHub thread as resolved before finishing. Do not report the task complete while any targeted bot comment remains unresolved. If a comment cannot be safely resolved without user input, stop and ask.

#### Severity triage (especially for bot reviewers)

Bot reviewers — particularly `elrond-cw[bot]` — over-flag stylistic nits and push back on intentional design decisions. Do **not** mechanically "fix" every comment. Triage first:

1. **Critical / relevant — fix the code.** Real bugs, security issues, regressions, broken builds, wrong API usage, missing required fields, breaking-change risk, incorrect business logic, data-loss risk, broken user-facing docs.
2. **Important quality — fix or reply with explicit rationale.** Maintainability concerns with real impact (missing error handling on a hot path, racey concurrency, leaky abstractions, untested edge case the diff introduces). Fix when cheap; otherwise reply with rationale and resolve.
3. **Trivial nits — won't-fix by default.** Pure preference/style with no functional impact. Reply briefly why, mark resolved.
4. **Bot undoing an intentional decision — always won't-fix.** When the PR description, commit message, plan, linked issue, or prior chat makes intent explicit and the bot suggests reverting it, reply pointing at where the intent is documented, then resolve.

When uncertain whether something is critical vs. nit, ask the user — do not silently downgrade a real concern.

Won't-fix replies: short, neutral, grounded in documented intent. Example:

```text
Won't fix — intentional. <one-line rationale, e.g. "this is the migration
target documented in the PR description / linked issue / plan #N">.
```

Do not argue with the bot, list pros/cons, or promise follow-ups that are not real.

### `/pr check` / `/pr validate` / `/pr review` — Validation

1. Run the project's quality gates (see below) and verify they pass.
2. Get PR details with `gh pr view`; if none exists, suggest `/pr`.
3. Validate title format, body completeness against the Quality Contract, and that the body still matches the current diff.
4. Check metadata (assignee, labels, reviewers, milestone if applicable) and CI/CD check status; report failing checks with reasons.

### `/pr ready` — Mark Ready for Review

1. Confirm the PR exists, is draft, and is not merged/closed.
2. **Quality validation is `pr-delivery`'s job.** If this PR came from a
   `pr-delivery` run, its fixed-revision review already covered this — do not
   re-run a parallel gate. If not, delegate the full review to `pr-delivery`
   rather than running an ad-hoc validation here.
3. Verify required checks pass and no merge conflicts exist.
4. Request reviewers (CODEOWNERS, changed-file patterns, prior reviewers) and assign the author.
5. Remove draft status. Do not apply status labels — draft→ready is the native GitHub signal; repo-specific labels belong to that repo's own rules.

## Quality Gates

Find quality commands from `CONTRIBUTING.md` (root or `.github/`), else `README.md`, else auto-detect from project config files (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, etc.). Run tests, lint/format, build, and security checks as applicable.

## Issue Tracking

Issues live on GitHub by default and sync to Linear. When an issue has a synced Linear ID (check the issue body/comments), link both: `Closes [#123: Title](github-url)` for auto-close plus the Linear link for status tracking. Linear alone only when a Linear URL/ID was provided without a GitHub issue. Never invent an ID; do not fabricate links.

Use full markdown URLs with closing keywords so GitHub auto-closes on merge:

```markdown
Closes [#123: Issue Title](https://github.com/<owner>/<repo>/issues/123)
```

Fetch unknown titles with `gh issue view 123 --json number,title,url` (or `linearis issues read TEAM-123` for a Linear ID). Check the GitHub issue for a synced Linear identifier and include both links when present.

## Safety

- Never create a PR from main/master, without committed changes, or without pushing the branch first.
- Never push to main/master directly.
- Run an integrity preflight before every PR creation; run full quality checks before marking a PR ready or mergeable.

## Arguments

- `/pr` — Create pull request (optional: title override, base branch)
- `/pr draft` — Create or reuse a draft PR after integrity preflight; intended for `pr-delivery`
- `/pr check|validate|review` — Run quality checks and validation
- `/pr ready` — Mark PR ready for review (optional: reviewers, priority)
