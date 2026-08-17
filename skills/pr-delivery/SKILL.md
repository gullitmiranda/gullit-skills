---
name: pr-delivery
description: Create or reuse a draft PR early to start remote checks, review a fixed revision with guarded or strict boundaries, repair clear findings, and hand the reviewed revision to pr-babysit. Use only when the user explicitly requests this complete PR delivery flow.
disable-model-invocation: true
---

# PR Delivery

Use this skill as the explicit, end-to-end PR delivery action. It opens a draft
PR early so remote checks can run while a clean-context reviewer examines the
fixed diff. It does not make a PR mergeable until every review agent has
returned and the final head revision has been checked.

Apply `gh-profile` before every GitHub or remote Git operation, `pr` for PR
metadata and lifecycle rules, `quality` for validation, and `publish-safe-links`
before publishing PR text.

## Interface

```text
/pr-delivery [--base <branch>] [--spec <path-or-issue-url>] \
  [--review-mode auto|guarded|strict] \
  [--ready] [--merge] [--allow-merge]
```

Defaults:

- Base branch: the repository default branch.
- `--review-mode auto`: resolve to `strict` only when the runtime can verify an
  independently enforced no-mutation child boundary; otherwise resolve to
  `guarded`. Announce and record the resolved mode before spawning a reviewer.
  In native Zed, `auto` resolves to `guarded`.
- `--review-mode guarded`: force a clean-context reviewer with a no-mutation
  policy and parent-side integrity verification.
- `--review-mode strict`: require a runtime that technically enforces a
  separate read-only child boundary. If unavailable, stop rather than claim
  strict isolation.
- `--ready` (default): after all gates pass for the final reviewed revision,
  `pr-babysit` converts the draft to ready for review.
- `--merge`: after all gates pass, `pr-babysit` merges the PR. Implies
  `--ready`. Requires `--allow-merge`; it is never a default.

`--ready` and `--merge` are user-facing pass-throughs to `pr-babysit`. The
standalone `pr-babysit` default remains watch-only because monitoring a PR
directly must not change its public state by surprise.

## Authorization And Preconditions

An explicit `/pr-delivery` invocation authorizes:

- creating or updating the PR for the current branch;
- commits made solely to address findings discovered in this delivery run; and
- pushing the initial branch revision and those scoped repair commits.

It does not authorize committing unrelated unstaged work. Before publishing:

1. Confirm the target repository, feature branch, base branch, and GitHub
   profile.
2. Refuse `main` or `master` as the source branch.
3. Require a clean worktree and at least one committed change ahead of base.
4. Inspect the diff, commits, issue references, and PR template.
5. Build factual PR metadata. Do not claim local or remote validation that has
   not happened.
6. Run the pre-draft integrity gate from `pr`; full quality gates happen before
   the final repair push and readiness, not before the initial draft exists.

If the branch already has a draft PR, reuse it. If it has an open non-draft PR,
stop and ask the user rather than silently changing its review state. If a
pending auto-merge request is detected, do not make the PR ready without
explicit user direction.

## Delivery Protocol

### 1. Publish The Initial Draft

1. Push the committed branch.
2. Create a draft PR with the `pr draft` route, or synchronize the existing
   draft's title and body.
3. Record the PR URL, base SHA, and initial head SHA.
4. Keep the PR draft. Do not request reviewers, mark it ready, start
   `pr-babysit`, or merge at this stage.

The remote checks may now run in parallel with the local review. The draft body
may state that validation is in progress, but it must not use placeholders or
claim passing results without evidence.

### 2. Run A Fixed-Revision Review

Create a concise context capsule using the inputs in
[reviewer-prompt.md](reviewer-prompt.md). Pass the base SHA and head SHA
explicitly; the reviewer examines only that fixed diff and returns the
structured result in the template.

#### Resolve the review mode

For `auto`, select `strict` only from a verified runtime capability boundary,
not from a profile name or prompt. Otherwise select `guarded`. Record the
resolved mode in the reviewer capsule, completion manifest, and final report
before the reviewer starts.

#### Fixed-revision integrity gate

Before spawning any reviewer, verify that the local `HEAD` and remote PR head
both equal the fixed review head SHA. Also require a clean worktree and index,
and record a snapshot containing those values, the branch, and fixed base/head
SHAs. If either head is already different, return `stale-head` and stop.

After every reviewer returns, verify again that the local `HEAD` and remote PR
head both equal the fixed review head SHA, and that the worktree/index status
still equals the snapshot. If any check differs, return
`review-integrity-unknown`, stop, and do not create a manifest or start
`pr-babysit`. A concurrent actor can cause the same result; do not attribute it
without evidence.

#### `guarded` mode

Native Zed subagents inherit the parent's capabilities. Tell the reviewer not
to edit files, use write-capable tools, stage, commit, push, reset, checkout,
mutate branches, or mutate GitHub resources. Require a text-only report. This
is a policy guardrail, not technical isolation. The fixed-revision integrity
gate above detects local Git and PR-head changes, but cannot prove that no other
external mutation was attempted.

#### `strict` mode

Use this only when the calling runtime can technically remove the child's write
and GitHub mutation capabilities and the fixed-revision integrity gate can be
performed before and after the session. If either condition is unavailable,
stop after the draft PR with a clear explanation. A native Zed `spawn_agent`
child does not satisfy this mode. In Zed, a separate top-level thread is strict
only if its no-mutation capability boundary has been explicitly verified; a
named profile alone is not sufficient evidence.

Track every review session and wait for all of them to complete. Never start
`pr-babysit` concurrently with a reviewer. After a successful review set,
build the serialized completion manifest described in
[review-manifest.md](review-manifest.md), including the selected mode and the
successful integrity result. Do not build that manifest when any reviewer
failed, timed out, returned malformed evidence, returned a different SHA, or
left a user decision pending.

### 3. Triage Findings

The parent agent owns triage and all writes. Do not blindly implement every
suggestion.

| Finding | Action |
| --- | --- |
| High-confidence bug, regression, or clear security flaw with a small, testable fix that preserves the documented behavior | Fix autonomously. |
| Clear CI or lint issue introduced by the branch and solvable within the changed scope | Fix autonomously. |
| Ambiguous requirement, product behavior, public API, schema or data migration, permission model, dependency, rollout, or conflicting intent | Stop and ask the user. |
| Style preference, speculative refactor, or low-confidence observation without concrete impact | Do not change by default; report it as not applied. |
| Reviewer failure, malformed result, missing evidence, or timeout | Stop. Do not start babysitting. |

### 4. Publish And Review Every Repair Revision

For autonomous repairs:

1. Make only the minimal scoped changes.
2. Run the applicable targeted and project quality checks.
3. Commit focused repair changes with a conventional commit message.
4. Push the repair revision.
5. Use the continuous PR sync route in `pr` to refresh stale title, body,
   validation evidence, risks, and links.
6. Record the new final head SHA.
7. Run a new fixed-revision delta review in the selected mode from the
   previously reviewed SHA to the new final head SHA. Wait for every delta
   reviewer and replace the serialized
   review completion manifest only after they all succeed.

Repeat this repair and delta-review cycle when a reviewer finds another clear,
autonomous issue. Stop when a decision is needed, review evidence is invalid,
or the cycle no longer makes progress.

If there are no repairs, the initial reviewer already covers the initial head
SHA; build its serialized completion manifest after every reviewer returns
successfully.

### 5. Hand Off To `pr-babysit`

Call `pr-babysit` only after this barrier is true:

```text
all reviewer sessions completed
AND no user decision is pending
AND every autonomous repair is committed, validated, and pushed
AND remote PR head SHA equals the local final head SHA
AND final head SHA is the reviewed head SHA
AND a matching serialized completion manifest records at least one completed reviewer for that SHA
AND the manifest records the selected review mode and successful integrity verification
```

Invoke it with the fixed revision:

```text
/pr-babysit <pr-url> \
  --expected-head-sha <final-head-sha> \
  --reviewed-head-sha <final-head-sha> \
  --review-manifest-json '<serialized-manifest>' \
  [--ready] [--merge]
```

Pass `--merge` (with `--allow-merge`) through to `pr-babysit` only when the
user explicitly requested it on `/pr-delivery`.

If `pr-babysit` returns `needs-delta-review` after making a scoped repair,
first run the applicable targeted and project quality checks for its new head.
Then repeat the fixed-revision review in the selected mode only for the delta
from the previously reviewed SHA to its new head SHA. Wait for every reviewer,
build a matching replacement
serialized manifest, and call `pr-babysit` again with the new SHA as expected and
reviewed. Do not use `ready` or `merge` on an unreviewed revision.

Stop rather than loop indefinitely if the same failure recurs without progress,
a decision is needed, the PR head becomes stale, or a validation result is
unknown.

## Completion Report

Report:

- PR URL and source/base branches;
- initial and final reviewed head SHA;
- selected review mode, fixed-SHA integrity checks, reviewer sessions, and their outcome;
- autonomous fixes and validations actually run;
- current `pr-babysit` result; and
- any decision, CI failure, or merge blocker left for the user.

Arguments: $ARGUMENTS
