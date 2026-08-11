# PR Delivery

Use this workflow when the user explicitly wants one action to create a pull
request, review its diff in an isolated context, apply clear repairs, and watch
remote checks through a final reviewed revision.

## Flow

```text
committed clean feature branch
-> pr-delivery opens or reuses a draft PR
-> remote checks start
-> isolated read-only review
-> parent triages and repairs clear findings
-> validate, commit, push, and synchronize PR metadata
-> isolated delta review for every repair SHA
-> wait for all reviewer agents and retain a serialized completion manifest
-> pr-babysit watches the final reviewed SHA
-> watch, ready, or explicit merge
```

## Defaults

`/pr-delivery` defaults to `--on-green ready`: after the final reviewed SHA is
green, it may take the PR out of draft. It does not merge by default.

`/pr-babysit` defaults to `--on-green watch` when run directly. This avoids
changing a PR's public state when its watcher is invoked independently.

## Safety Gates

- The PR starts as a draft so remote CI can run before review and repair finish.
- A reviewer receives a compact context capsule and runs with enforced read-only
  capabilities, not merely a read-only prompt.
- `pr-babysit` starts only after every reviewer has returned and a matching
  serialized completion manifest records at least one completed reviewer for
  the final SHA. The manifest travels in the handoff capsule, not through a
  runtime-specific temporary file.
- The babysitter receives expected and reviewed SHAs and refuses to act on a
  different or unreviewed remote head.
- Every parent or babysitter repair creates a new SHA, must pass applicable
  quality checks, and requires isolated delta review before the PR can become
  ready or merge.
- Merge requires both `--on-green merge` and `--allow-merge`.

## Related Skills

- `pr-delivery`: public orchestrator.
- `pr`: draft creation, metadata synchronization, validation, and comment rules.
- `pr-babysit`: remote CI, conflicts, and comment triage for one reviewed SHA.
- `quality`: local validation before the final repair push and readiness.
- `gh-profile`: authenticated GitHub and remote Git routing.
- `publish-safe-links`: safe PR descriptions and comments.
