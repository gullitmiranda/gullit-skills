---
name: pr-babysit
description: Watch one PR head, triage scoped conflicts, comments, and CI failures, and make it ready or merge only when the reviewed head SHA is green. Use after pr-delivery has completed every review session, or standalone to watch the current PR head.
disable-model-invocation: true
---

# PR Babysit

Keep one pull request revision moving toward a merge-ready state without acting
on a stale, unreviewed, or integrity-unknown head. This skill is versioned and
portable, and is guarded by explicit PR and commit identities.

Apply `gh-profile` before GitHub and remote Git operations. Apply `pr` when
synchronizing PR metadata or resolving review comments. Do not bypass branch
protection, required checks, or repository merge-queue policy.

## Interface

```text
/pr-babysit \
  --pr <url> \
  [--on-green watch|ready|merge] [--allow-merge]
```

Required arguments:

- `--pr`: the open PR URL.

`--on-green` defaults to `watch`. `ready` is allowed only when the expected and
reviewed SHAs match. `merge` additionally requires `--allow-merge`; it is never
a default.

The advanced internal arguments below exist for the `pr-delivery` handoff. They
are normally produced by that skill, not typed by the user:

- `--expected-head-sha <sha>`: the exact remote head this run may observe or
  repair. Defaults to the PR's current remote head, fetched at entry.
- `--reviewed-head-sha <sha>`: the latest head SHA completed by a review
  session. Required for `--on-green ready|merge`; when omitted, this run may
  only watch or repair.
- `--review-manifest-json '<serialized-manifest>'`: the serialized completion
  record created by `pr-delivery` as specified in
  `pr-delivery/review-manifest.md`. Required for `--on-green ready|merge`.

## Entry Gate

Before watching or changing anything:

1. Confirm the PR is open and belongs to the intended repository and branch.
2. Fetch its current head SHA, base SHA, draft state, merge state, required
   check status, and active unresolved threads. When `--expected-head-sha` was
   not provided, pin the fetched head as the expected SHA for this run.
3. If current head differs from the expected head SHA, return `stale-head`.
4. When a reviewed head SHA is known and differs from the expected head SHA,
   return `needs-delta-review`. A non-reviewed head cannot become ready or
   merge.
5. For `--on-green ready|merge`, parse and validate the review manifest. Its PR
   URL and expected/reviewed SHAs must match, completion must be `complete`,
   review mode must be `guarded` or `strict`, integrity must be verified from
   pre-review and post-review snapshots pinned to this SHA, and it must contain
   at least one reviewer session. Every session must have `status: reviewed`, a
   terminal successful result, and a `reviewed_head_sha` equal to this expected
   SHA. If the manifest is absent or invalid, return `blocked` without watching
   or changing the PR.
6. The serialized manifest is evidence that the parent completed all review
   sessions. This skill must never be started in parallel with them.

## Watch And Triage Loop

Observe only the current expected head. Re-check its SHA before every remote
mutation and after every CI polling interval.

### Merge Conflicts

Resolve a conflict only when the intended result is clear from the PR and base
branch. If intents conflict, abort the merge attempt and return
`needs-decision` with the conflicting files and intent question.

### Active Comments

Inspect active unresolved threads only. Read each comment body and the minimum
location and URL needed to act; do not dump unrelated GitHub payloads.

- Fix a valid, high-confidence bug or regression within this PR's scope.
- For a valid comment requiring a product, API, migration, security, or design
  decision, return `needs-decision`.
- For invalid or intentionally out-of-scope comments, reply with a short,
  factual rationale and resolve the thread only when repository policy permits.
- Follow the `pr` skill's targeted review-comment resolution rules.

### CI

Fix only failures caused by this PR and only with scoped changes. Never alter a
CI workflow or make unrelated code changes merely to make a check pass. For a
merge-blocking failure that appears unrelated, first check whether the branch
is behind base; merge or rebase only if the conflict resolution and resulting
intent are clear. Otherwise return `blocked` with the failure evidence.

## Mutation Barrier

Any source change, conflict resolution, base integration, commit, or push
creates a new head SHA. After such a mutation:

1. Run the applicable targeted and project quality checks before committing and
   pushing the scoped change. If a required check fails, return `blocked` with
   the validation evidence rather than pushing a known-bad revision.
2. Push the scoped change and fetch the new remote head SHA.
3. Synchronize PR metadata if the diff or validation evidence changed.
4. Return `needs-delta-review` with `previous_reviewed_head_sha`,
   `current_head_sha`, and the validation evidence.
5. Do not convert the PR to ready and do not merge.

`pr-delivery` must run a new fixed-revision review in its selected mode, wait
for every reviewer, verify fixed-SHA integrity before and after the review in
both modes, verify the technical child boundary additionally in `strict` mode,
build a matching serialized completion manifest, and call this skill again
using the new SHA as both expected and reviewed.

## Green Actions

Proceed only when all of the following hold for the same SHA:

- current remote head equals the expected head SHA;
- all required checks are successful;
- the PR is mergeable and has no unresolved blocking threads or conflicts;
- no watcher action created a newer revision; and
- no decision remains pending.

For `ready` and `merge`, additionally require that the expected head SHA equals
the reviewed head SHA and that the validated manifest records at least one
completed reviewer for this SHA.

Then apply `--on-green`:

| Mode | Action |
| --- | --- |
| `watch` | Report green status. Do not change draft state or merge. |
| `ready` | Convert a draft PR to ready for review. Before doing so, stop if an active auto-merge request or repository automation could merge the PR unexpectedly. |
| `merge` | Merge only with `--allow-merge`, after all prior conditions and repository protections are satisfied. Respect merge queues and never override protections. |

If checks are in progress, keep watching the same SHA. If they fail, triage the
failure under the CI rules. Stop and report when the failure cannot be safely
fixed within scope or when progress stops.

## Result Contract

Return one of:

- `green`: expected reviewed SHA is green; include the selected action.
- `needs-delta-review`: a mutation created a new head that needs a new review
  before readiness or merge.
- `needs-decision`: a user decision is required.
- `stale-head`: another actor changed the PR head.
- `blocked`: CI, conflict, policy, review-integrity, or external condition
  cannot be safely resolved.
- `timed-out`: checks did not settle within the active watcher limit.
- `merged`: only after explicit merge mode succeeds.

Always include the PR URL, current head SHA, reviewed head SHA (or `none` when
watching without a review manifest), review mode, check summary, changes made
during this run, and the next safe action.

Arguments: $ARGUMENTS
