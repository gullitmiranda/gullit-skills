# Skills Map

This map groups personal and external skills by workflow phase. It is a
navigation aid: atomic skills stay installable from `skills/<name>/`, while
workflow docs describe how to compose them.

## Phases

### Discovery

Use these when the goal, domain language, or relevant code area is still fuzzy.

- `workflow-intake`: analyze available context and recommend how to start or resume before implementation.
- `workspace-status`: understand repository boundaries in multi-repo workspaces.
- [`grill-with-docs`](../skills/grill-with-docs/README.md): challenge a plan against the domain model, update `CONTEXT.md`, and capture durable decisions.
- `zoom-out` from `mattpocock/skills`: build a higher-level map of an unfamiliar code area.
- `prototype` from `mattpocock/skills`: answer a design question with throwaway logic or UI code.

### Planning

Use these when the work needs structure before implementation.

- `plan`: create or update tool-appropriate local plans.
- `incremental-delivery`: split large work into testable, reviewable increments.
- `to-prd` from `mattpocock/skills`: turn agreed context into a PRD in the project issue tracker.
- `to-issues` from `mattpocock/skills`: break a PRD or plan into vertical-slice issues.
- `agent-selection`: choose the right runtime before substantial work starts.

### Isolation

Use these before parallel or risky implementation.

- `git-worktree`: enforce isolated worktrees when requested.
- `git`: apply safe branch, commit, and reset workflows.
- `safety`: apply command, workspace, git, and destructive-operation safety rules.
- `data-boundary`: prevent work-only information from leaking into personal or public repositories.

### Execution

Use these to implement changes with tight feedback loops.

- `tdd` from `mattpocock/skills`: implement one behavior at a time with red-green-refactor.
- `diagnose` from `mattpocock/skills`: debug with a reproducible feedback loop before hypothesizing.
- `quality`: apply code, documentation, testing, performance, and security standards.
- `npm-supply-chain-safety`: protect npm install and dependency changes.
- `trunk-safety`: protect Trunk setup and upgrades.

### Architecture

Use these when design friction, testability, or module depth matters.

- `improve-codebase-architecture` from `mattpocock/skills`: identify deepening opportunities informed by domain docs and ADRs.
- [`grill-with-docs`](../skills/grill-with-docs/README.md): resolve terminology and durable trade-offs discovered during architecture work.
- `tech-debt`: record deferred technical debt without starting follow-up work.

### Validation And Review

Use these before handing work to a reviewer or maintainer.

- `quality`: run appropriate checks and keep generated text clean.
- `pr`: create, update, and validate pull requests.
- `publish-safe-links`: verify published links and file references before posting externally.
- `zeropath`: handle ZeroPath-specific findings and evidence when relevant.

### Context Management

Use these when parallel work, context pressure, or tool switching would otherwise
pollute the main conversation.

- `workflow-intake`: decide whether to continue in the current thread or route work to another runtime.
- `context-capsule`: create a portable summary for subagents, forks, Zed threads, terminal agents, or future resumes.
- `agent-selection`: decide whether the next step belongs in the main chat, subagent, fork, IDE agent, or terminal/ACP/Pi-style agent.
- `handoff` from `mattpocock/skills`: compact a session when context window pressure is the main problem.
- Pi-style transcript tools such as `copy-all`: use only when exact conversational history matters.

## Default Composition

For ambiguous feature work:

```text
workflow-intake when starting from unknown state
-> workspace-status
-> zoom-out or grill-with-docs
-> plan or to-prd
-> incremental-delivery or to-issues
-> agent-selection
-> git-worktree when isolation is needed
-> tdd
-> quality
-> pr
```

For hard bugs:

```text
workspace-status
-> diagnose
-> tdd for regression coverage when appropriate
-> quality
-> pr
```

For architecture work:

```text
workspace-status
-> zoom-out
-> improve-codebase-architecture
-> grill-with-docs for durable decisions
-> incremental-delivery
-> agent-selection
```
