# PR Delivery

Use this workflow when the user explicitly wants one action to create a pull
request, review its fixed diff with guarded or strict boundaries, apply clear
repairs, and watch remote checks through a final reviewed revision.

## Flow

```text
committed clean feature branch
-> pr-delivery opens or reuses a draft PR
-> remote checks start
-> guarded fixed-revision review, or strict review when the runtime supports it
-> parent triages and repairs clear findings
-> validate, commit, push, and synchronize PR metadata
-> guarded or strict delta review for every repair SHA
-> wait for all reviewer agents and retain a serialized completion manifest
-> pr-babysit watches the final reviewed SHA
-> watch, ready, or explicit merge
```

## Defaults

`/pr-delivery` defaults to `--review-mode auto` and `--ready`. `auto`
selects `strict` only when the runtime proves a separate no-mutation child
boundary; otherwise it selects `guarded` and reports that resolution. In native
Zed, it resolves to `guarded`. After the final reviewed SHA is green, the flow
may take the PR out of draft. It does not merge by default.

`/pr-babysit` is watch-only by default when run directly. This avoids
changing a PR's public state when its watcher is invoked independently.

## Safety Gates

- The PR starts as a draft so remote CI can run before review and repair finish.
- Before and after every review, the parent verifies that local `HEAD` and the
  remote PR head both equal the fixed review SHA and that the clean worktree and
  index status are unchanged.
- In `auto`, the resolved mode is recorded before the review. When it resolves
  to `guarded`, a reviewer receives a compact context capsule and explicit
  no-mutation instructions. This is a policy guardrail, not technical
  isolation.
- `strict` mode is available only when the runtime can enforce a separate child
  capability boundary as well as the fixed-SHA integrity gate. Native Zed
  subagents inherit the parent profile, so strict mode stops rather than
  claiming isolation.
- `pr-babysit` starts only after every reviewer has returned and a matching
  serialized completion manifest records at least one completed reviewer for
  the final SHA. The manifest travels in the handoff capsule, not through a
  runtime-specific temporary file.
- The babysitter receives expected and reviewed SHAs and refuses to act on a
  different or unreviewed remote head.
- Every parent or babysitter repair creates a new SHA, must pass applicable
  quality checks, and requires fixed-revision delta review before the PR can become
  ready or merge.
- Merge requires the explicit `--merge` flag.

## Related Skills

- `pr-delivery`: public orchestrator.
- `pr`: draft creation, metadata synchronization, validation, and comment rules.
- `pr-babysit`: remote CI, conflicts, and comment triage for one reviewed SHA.
- `quality`: local validation before the final repair push and readiness.
- `gh-profile`: authenticated GitHub and remote Git routing.
- `publish-safe-links`: safe PR descriptions and comments.
