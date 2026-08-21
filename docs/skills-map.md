# Skills Map

This map groups the repository's atomic skills by workflow role. Current source paths remain `skills/<name>/` until the installer can safely migrate existing installations to the approved nested source homes.

## Discovery and routing

Use these when the next step or the relevant context is unclear.

- `work-intake`: inspect context, classify artifacts, and select the smallest route.
- `workspace-status`: understand repository boundaries in multi-repository workspaces.
- [`grill-with-docs`](../skills/grill-with-docs/README.md): challenge a proposal against domain language and durable decisions.
- `agent-selection`: select the right runtime before substantial work.
- `context-capsule`: transfer the smallest useful context across agents or tools.

## Workspace and planning

Use these to establish the artifact contract or make implementation ready.

- `agent-workspace`: establish or migrate plans, notes, and scratch boundaries.
- `agent-notes`: record durable decisions, research, missions, and coordination knowledge.
- `work-plan`: create or refine one local implementation plan.
- `incremental-delivery`: coordinate multiple independent, reviewable deliveries.
- `model-selection`: compare complete runtime model configurations and defaults.

## Execution and closeout

Use these to implement and assess a ready contract.

- `build`: execute one ready local implementation plan.
- `incremental-delivery`: coordinate multi-increment implementation when needed.
- `work-closeout`: classify a plan or context and perform only confirmed closure actions.
- `quality`: apply checks and output hygiene.

## Guardrails

Use these whenever their boundary applies.

- `safety`, `git`, and `git-worktree`: repository state, branch, worktree, and destructive-operation safety.
- `data-boundary`: prevent private or context-specific information from leaking.
- `supply-chain-safety` and `js-supply-chain-safety`: secure package and tool installation; the stricter applicable rule wins.
- `publish-safe-links`: prevent local or unpublished paths from appearing in publishable text.
- `pr`, `pr-delivery`, and `pr-babysit`: pull-request lifecycle work when requested.

## Default compositions

Ambiguous feature work:

```text
work-intake
-> workspace-status
-> grill-with-docs when decisions need user input
-> work-plan
-> incremental-delivery when multiple independent deliveries are needed
-> agent-selection
-> git-worktree when isolation is needed
-> build
-> quality
-> pr when requested
-> work-closeout when the user wants plan assessment or closure
```

Existing ready plan:

```text
work-intake
-> agent-selection
-> git-worktree when needed
-> build
-> quality
-> work-closeout
```

Bug or regression:

```text
work-intake
-> establish a reproducible feedback loop
-> work-plan when the fix needs a contract
-> build
-> quality
```

Architecture work:

```text
work-intake
-> workspace-status
-> grill-with-docs
-> work-plan
-> incremental-delivery
-> agent-selection
-> build
-> quality
```
