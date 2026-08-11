---
name: pr-babysit
description: Discover and watch the PR for the current branch or an explicit PR, triage scoped conflicts, comments, and CI failures, and make it ready or merge only when the current revision is safe.
disable-model-invocation: true
---

# PR Babysit

Keep one pull request moving toward review or merge readiness without acting on a stale head. The skill works for PRs created by any workflow.

Apply gh-profile before GitHub and remote Git operations. Apply pr when synchronizing PR metadata or resolving review comments. Do not bypass branch protection, required checks, or repository merge-queue policy.

## Invocation

Preferred invocation:

    /pr-babysit

Optional inputs:

    --pr <url>
    --on-green watch|ready|merge
    --allow-merge

The default on-green mode is ready. An explicit PR URL overrides discovery.

## PR discovery

1. When --pr is supplied, use that PR.
2. When --pr is absent, discover the open PR for the current checked-out branch.
3. When no branch PR exists, inspect the repository for one clearly related open PR only when context identifies it unambiguously.
4. When no PR or multiple plausible PRs exist, return needs-decision with the candidate URLs. Never require the user to provide a SHA manually.
5. Fetch the current head SHA, base SHA, draft state, merge state, required check status, active unresolved threads, and auto-merge state.

## Watch and triage loop

Watch the current remote head. Re-check its SHA before every remote mutation and after every CI polling interval.

### Merge conflicts

Resolve a conflict only when the intended result is clear from the PR and base branch. If intents conflict, return needs-decision with the conflicting files and intent question.

### Active comments

Inspect active unresolved threads only. Read each comment body and the minimum location and URL needed to act.

- Fix a valid, high-confidence bug or regression within the PR scope.
- For a valid comment requiring a product, API, migration, security, or design decision, return needs-decision.
- For invalid or intentionally out-of-scope comments, reply with a short factual rationale and resolve the thread only when repository policy permits.
- Follow the pr skill targeted review-comment rules.

### CI

Fix only failures caused by this PR and only with scoped changes. Never alter a CI workflow or make unrelated code changes merely to make a check pass. For a merge-blocking failure that appears unrelated, first check whether the branch is behind base. Integrate base only if the resulting intent is clear; otherwise return blocked with the failure evidence.

## Mutation barrier

Any source change, conflict resolution, base integration, commit, or push creates a new head SHA.

1. Run applicable targeted and project quality checks before committing and pushing the scoped change.
2. Push the scoped change and fetch the new remote head SHA.
3. Synchronize PR metadata if the diff or validation evidence changed.
4. Resume watching the new head and wait for its checks to settle.
5. Do not merge the new head until required reviews and repository protections are satisfied.

## Green actions

Proceed only when all required checks are successful, the PR is mergeable, no unresolved blocking thread or conflict exists, and no watcher action created a newer revision.

| Mode | Action |
| --- | --- |
| watch | Report green status. Do not change draft state or merge. |
| ready | Convert a draft PR to ready for review. A completed review is not required because ready starts the review phase. Before doing so, stop if an active auto-merge request or repository automation could merge unexpectedly. |
| merge | Merge only with allow-merge, after repository-required approvals, review requirements, and protections are satisfied. |

## Result contract

Return one of:

- green: current head is green; include the selected action.
- needs-decision: a PR cannot be discovered uniquely, a conflict intent is unclear, or a product or design decision is required.
- stale-head: another actor changed the PR head during the run.
- blocked: CI, conflict, policy, or external condition cannot be safely resolved.
- timed-out: checks did not settle within the active watcher limit.
- merged: only after explicit merge mode succeeds.

Always include the PR URL, current head SHA, check summary, changes made during this run, and the next safe action.
