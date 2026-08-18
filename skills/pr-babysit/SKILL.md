---
name: pr-babysit
description: Watch PR heads, triage scoped conflicts, comments, and CI failures, and make each PR ready or merge it only when the reviewed head SHA is green. Use after pr-delivery has completed every review session, or standalone to watch current PR heads.
disable-model-invocation: true
---

# PR Babysit

Keep pull request revisions moving toward merge-ready without acting on a stale, unreviewed, or integrity-unknown head.

Apply `gh-profile` before GitHub and remote Git operations. Apply `pr` when synchronizing PR metadata or resolving review comments. Do not bypass branch protection, required checks, or repository merge-queue policy (except via `--admin`, below).

## Interface

```text
/pr-babysit <pr-url> [<pr-url> ...] [--ready] [--merge] [--solo] [--admin]
```

- `<pr-url>`: one or more open PR URLs; each is watched and triaged independently with its own result.
- `--ready`: when green, convert from draft to ready for review.
- `--merge`: when green, merge. Implies `--ready` (convert first, keep watching the same SHA — some required checks only run once ready — and merge only after they succeed). Never a default.
- `--solo`: user is sole reviewer (solo repository). Waives only the human-review gate (review manifest); every other condition still applies. Report `solo` as review mode in the result so the bypass is auditable.
- `--admin`: merge with `gh pr merge --admin`, bypassing branch protection (required reviews, required checks). Only valid with `--merge`; requires admin permission. Use only when the user is sole maintainer and protection cannot be satisfied otherwise (e.g. org-level required review with no other reviewer). Report `admin` in the result.

`--ready` and `--merge` are cumulative steps, not exclusive modes; with neither, the run only watches and repairs. They are allowed only when expected and reviewed SHAs match (in practice a `pr-delivery` handoff) or when `--solo` was passed. Watching multiple PRs without manifests and without `--solo` is watch-only for all of them.

Internal arguments for the `pr-delivery` handoff (normally produced by that skill, single-PR invocation only):

- `--expected-head-sha <sha>`: exact remote head this run may observe or repair. Defaults to the PR's current remote head, fetched at entry.
- `--reviewed-head-sha <sha>`: latest head SHA completed by a review session. Required for `--ready`/`--merge` unless `--solo`.
- `--review-manifest-json '<serialized-manifest>'`: completion record created by `pr-delivery` per `pr-delivery/review-manifest.md`. Required for `--ready`/`--merge` unless `--solo`.
- `--on-green watch|ready|merge`: legacy alias (`ready` → `--ready`, `merge` → `--ready --merge`). Prefer the flags.

## Entry Gate

For each PR, before watching or changing anything:

1. Confirm the PR is open and belongs to the intended repository and branch.
2. Fetch current head SHA, base SHA, draft state, merge state, required check status, and active unresolved threads. When `--expected-head-sha` was not provided, pin the fetched head as expected.
3. If current head differs from expected, return `stale-head`.
4. If a reviewed head SHA is known and differs from expected, return `needs-delta-review`. A non-reviewed head cannot become ready or merge.
5. For `--ready`/`--merge` without `--solo`, validate the review manifest: PR URL and expected/reviewed SHAs match; completion is `complete`; review mode is `guarded` or `strict`; integrity verified from pre- and post-review snapshots pinned to this SHA; at least one reviewer session, each with `status: reviewed`, a terminal successful result, and `reviewed_head_sha` equal to the expected SHA. Absent or invalid manifest → `blocked` without watching or changing the PR. With `--solo`, skip and record review mode `solo`.
6. The serialized manifest is evidence the parent completed all review sessions. This skill must never be started in parallel with them.

## Watch And Triage Loop

Observe only the current expected head. Re-check its SHA before every remote mutation and after every CI polling interval.

One invocation owns exactly one head SHA. Draft→ready conversion does not end the run (SHA unchanged). Any scoped fix that creates a new SHA ends this run's authority to ready or merge: return `needs-delta-review`; `pr-delivery` reviews the delta; only a new invocation pinned to the new SHA may proceed.

### Merge Conflicts

Resolve only when the intended result is clear from the PR and base branch. If intents conflict, abort and return `needs-decision` with the conflicting files and intent question.

### Active Comments

Inspect active unresolved threads only; read each comment body and the minimum location/URL needed to act.

- Fix valid, high-confidence bugs or regressions within this PR's scope.
- Valid comment requiring a product, API, migration, security, or design decision → `needs-decision`.
- Invalid or intentionally out-of-scope comments: reply with a short factual rationale; resolve the thread only when repository policy permits.
- Follow the `pr` skill's targeted review-comment resolution rules.

### CI

Fix only failures caused by this PR, only with scoped changes. Never alter a CI workflow or make unrelated changes to make a check pass. For a merge-blocking failure that appears unrelated, first check whether the branch is behind base; merge or rebase only if conflict resolution and intent are clear. Otherwise return `blocked` with the failure evidence.

## Mutation Barrier

Any source change, conflict resolution, base integration, commit, or push creates a new head SHA. After such a mutation:

1. Run applicable targeted and project quality checks before committing and pushing. If a required check fails, return `blocked` with the evidence rather than pushing a known-bad revision.
2. Push and fetch the new remote head SHA.
3. Synchronize PR metadata if the diff or validation evidence changed.
4. Return `needs-delta-review` with `previous_reviewed_head_sha`, `current_head_sha`, and the validation evidence.
5. Do not convert to ready and do not merge.

`pr-delivery` must then run a new fixed-revision review in its selected mode, wait for every reviewer, verify fixed-SHA integrity before and after review in both modes (plus the technical child boundary in `strict`), build a matching serialized manifest, and call this skill again with the new SHA as both expected and reviewed.

## Green Actions

Proceed only when all hold for the same SHA: current remote head equals expected; all required checks successful; PR mergeable with no unresolved blocking threads or conflicts; no watcher action created a newer revision; no decision pending. For `--ready`/`--merge`, additionally require expected == reviewed with a validated manifest recording at least one completed reviewer for this SHA, or `--solo`.

Then apply in order:

1. `--ready`: convert draft to ready. Stop first if an active auto-merge request or repository automation could merge unexpectedly. After converting, keep watching the same SHA (some checks only start once a PR leaves draft).
2. `--merge`: merge only after all prior conditions and repository protections are satisfied, including checks that started after ready conversion. Respect merge queues; never override protections. With `--admin`, use `gh pr merge --admin` and report `admin` in the result.

If checks are in progress, keep watching the same SHA. If they fail, triage under the CI rules. Stop and report when the failure cannot be safely fixed within scope or progress stops.

## Result Contract

Return one of:

- `green`: expected reviewed SHA is green; include the requested steps.
- `needs-delta-review`: a mutation created a new head needing review before readiness or merge.
- `needs-decision`: a user decision is required.
- `stale-head`: another actor changed the PR head.
- `blocked`: CI, conflict, policy, review-integrity, or external condition cannot be safely resolved.
- `timed-out`: checks did not settle within the active watcher limit.
- `merged`: only after explicit merge mode succeeds.

Always include PR URL, current head SHA, reviewed head SHA (or `none`), review mode, check summary, changes made, and next safe action. Multiple PRs: one result per PR.

Arguments: $ARGUMENTS
