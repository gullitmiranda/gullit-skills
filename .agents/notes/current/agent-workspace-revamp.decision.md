# Agent workspace revamp

Status: underway

This decision record defines the target artifact model for the next revision of the agent workspace standard. It is not an implementation plan.

## Purpose

Separate executable implementation contracts from durable working knowledge. The previous model overloaded `plan` to mean missions, research, decisions, executable work, and local task drafts. That ambiguity made lifecycle and archival rules unreliable.

## Decisions

### Artifact roles

- `.agents/plans/` is the canonical local home for implementation plans. A migrated `.cursor/plans` path may remain as a local compatibility symlink to it.
- `.agents/notes/` contains tracked working knowledge: missions, proposals, research, decisions, and other material that can guide future work.
- `.agents/scratch/` contains local, disposable material that has no preservation or lifecycle expectation.
- `docs/` contains project documentation intended to be canonical for readers of the repository.

Target layout:

```text
.agents/
  AGENTS.md
  .gitignore
  plans/                         # local and gitignored
    example.plan.md
    .archived/                   # local, frozen historical plans
  notes/                         # tracked
    proposed/
    current/
    retired/
    archived/
  scratch/                       # local and gitignored
```

Folders appear only when their first artifact requires them. Archived artifacts are frozen.

### Implementation plans

An implementation plan is a contract of execution that is sufficiently resolved for an agent to carry it out without making relevant product, scope, or architecture decisions.

Before implementation, the executing agent must verify that the plan defines its objective, scope, approach, constraints, and validation sufficiently. If a relevant decision remains open, the agent must propose a plan refinement or request clarification before implementation. It may proceed by making that decision only when the user explicitly authorizes that autonomy.

Local implementation decisions that do not alter the agreed contract, scope, or architecture remain the executor's normal responsibility.

`*.plan.md` is reserved exclusively for implementation plans and must never appear inside `.agents/notes/`. There is no separate `work plan` artifact: `work plan`, `implementation plan`, and an execution-ready plan describe the same concept in this model. The public skill name is an invocation and runtime-compatibility decision, not a second artifact type.

### Notes

Notes are not execution contracts. They capture context, intent, findings, decisions, coordination, and other knowledge that can guide later work.

Notes may use descriptive kind suffixes when useful, such as:

```text
*.mission.md
*.proposal.md
*.research.md
*.decision.md
```

These suffixes are conventions, not a closed schema. Notes do not require folders by kind.

A note lifecycle represents relevance and preservation, not whether implementation work is happening:

```text
proposed -> current -> retired -> archived
```

`current` means that a note remains authoritative or relevant. `active` is not a note lifecycle state because it commonly implies work in progress, which does not hold for an accepted decision or completed research that still guides work.

`Status` is distinct from lifecycle when a note needs it. It may express a type-specific working state, such as `accepted` for a decision, `underway` for a mission, or `complete` for research. `Outcome` may record a terminal result such as `implemented`, `rejected`, `superseded`, `abandoned`, or `invalidated`. Neither field replaces lifecycle.

### Note visibility and frozen states

A note's lifecycle is represented only by its folder. Do not duplicate it in frontmatter or the body: moving the file is the lifecycle transition, and the path is sufficient for people and tooling to determine its state.

`Status` and `Outcome` are optional, type-specific metadata that appear visibly in the body immediately after the title:

```markdown
# Passkey enrollment decision

Status: accepted
Outcome: implemented
```

Frontmatter may be added for tool-specific metadata that cannot be derived from the path or visible content, but it must not duplicate lifecycle information.

`retired` and `archived` notes are frozen by default. An agent must create a successor note rather than routinely edit either state. This is a behavioral preservation rule, not an irreversible filesystem lock: the user may explicitly authorize a migration, cleanup, correction, or reactivation when changing a frozen record is warranted.

### Closing implementation plans

After implementation, a plan has one of three destinations:

1. Discard it when it contains no useful future context.
2. Move it unchanged to `.agents/plans/.archived/` when local execution history is useful.
3. Distill durable knowledge into a note or project documentation.

Distillation captures decisions, constraints, findings, outcomes, and follow-up work. It does not promote the entire operational checklist, transient commands, or incidental editing order into tracked notes.

### Work closeout (proposal)

Plan closure is distinct from implementation. A plan may be implemented while awaiting review, validation, deployment, or an explicit decision to retain it as active context.

The existing `work-context-cleanup` already performs the needed evidence-gathering and plan classification. Rather than add competing skills such as `after-build`, `plan-status`, or `plan-cleanup`, evolve it into a clearer public closeout skill, tentatively named `work-closeout`.

`work-closeout` should support a focused plan-closeout mode as well as current-context and broader workspace modes. It inspects the plan, implementation evidence, validation, review state, and remaining work; classifies the result; and recommends the smallest next action. It must not archive, discard, or distill a plan without clear user intent or confirmation.

### Migration principles

Migration is per repository and opt-in. No legacy artifact is moved, reclassified, promoted, or committed unless the user explicitly directs it.

Moving local legacy plans from `.cursor/plans/` to the canonical `.agents/plans/` is mechanical, not semantic: preserve the file contents, filenames, and `.archived/` history. Create a local compatibility symlink from `.cursor/plans` to `../.agents/plans` so existing paths and legacy tooling continue to resolve. The symlink is not a second plan location, must remain untracked, and new instructions and skills must target `.agents/plans/`.

This mechanical move applies only when the target path is unoccupied. A repository that already has the previous tracked `.agents/plans/` tree must first receive an explicitly approved semantic migration of that content; do not merge the two structures implicitly.

Only tracked artifacts created under the previous standard need semantic reclassification. Missions, research, decisions, and other working knowledge become notes; each existing slice must be evaluated individually to determine whether it is an implementation-ready plan or a note. This reclassification is never automatic.

Existing `docs/` content remains independent of the workspace migration. It changes only when a repository explicitly chooses to revise, promote, or link its canonical documentation.

### Skill dependencies and workflow navigation

Skill identity, workflow position, consumer dependency, and source-directory placement are separate concerns:

- A skill has one atomic responsibility and a clear, scope-specific name.
- A workflow describes the ordered use of skills to reach an outcome.
- A consuming project or personal setup declares the skills it needs as dependencies in `skills.yaml`.
- Source-directory placement is a navigational home for maintainers, not a restriction on which workflows may use the skill.

A workflow must not require separately installed third-party skills to complete its core path. External material is copied or adapted into an owned skill only when justified. Workflow documentation composes atomic skills; it must not duplicate their instructions or create one large orchestration skill responsible for every phase.

`guardrails` is the preferred source home for cross-cutting skills that impose policy, safety, quality, or behavioral limits. It includes user preferences and writing-quality guidance as well as safety controls; do not create a separate `standards` home. Git safety, worktree isolation, and GitHub identity routing are active guardrails and belong there too.

The engineering workflow has one public entry point: merge `workflow-intake` and `engineering-workflow` into `work-intake`. Retire the separately triggerable `engineering-workflow` skill; keep its useful routing catalog as an internal section or reference of `work-intake` so a user never chooses between competing routers.

The revised skill set should distinguish these responsibilities:

- interpreting, installing, and migrating the agent workspace model;
- creating and refining implementation plans;
- managing notes and their lifecycle;
- routing work through a workflow;
- selecting an execution runtime and transferring context when needed;
- executing a ready implementation plan; and
- closing or archiving a local plan.

Choose a nested source layout that is easy to navigate. The current installer can discover nested skills; complete the source tree, then reinstall skills from a clean state. The rewritten CLI will later define vendored installation behavior.

### Target source-home tree

This is the target tree. `->` marks a required rename, merge, or retirement during implementation.

```text
skills/
  engineering/
    discovery/
      grill-with-docs/
      workflow-intake/             -> work-intake/
      engineering-workflow/        -> merge into work-intake/

    workflow/
      agent-selection/
      context-capsule/

    planning/
      plan/                        -> work-plan/

    execution/
      build-plan/                  # retain pending post-migration naming review
      incremental-delivery/        # retain; slim duplicated guardrail rules
      work-context-cleanup/        -> work-closeout/

    delivery/
      pr/
      pr-delivery/
      pr-babysit/

    maintenance/
      tech-debt/

  workspace/
    agents-standard/               -> agent-workspace/
    agent-notes/
    workspace-status/
    workspace-topology/
    project-path-migration/        -> cursor-project-path-migration/
    agent-runtime/
      model-selection/

  guardrails/
    user-preferences/
    quality/
    safety/
    git/
    git-worktree/
    gh-profile/
    data-boundary/
    supply-chain-safety/
    js-supply-chain-safety/        # specialization; stricter rule wins
    trunk-safety/
    persist-agent-constraints/
    publish-safe-links/
    skill-writing/
    deslop/
    gremlin-clean/

  integrations/
    integration/
    zeropath/

  reporting/
    activity-report/

  personal/
    daily-notes/
    learn/

retire/
  workflow/                        -> distribute unique rules to topical owners
  plan-archive/                    -> work-closeout archive mode
```

The tree deliberately places skills in one primary home only. Workflows and consumer `skills.yaml` dependencies may compose skills across these homes. `engineering/discovery/` is justified by the pre-planning role of `work-intake` and `grill-with-docs`; `engineering/execution/` distinguishes plan execution and multi-increment coordination from plan authoring; `reporting/` is justified by the cross-system evidence-reconciliation responsibility of `activity-report`. `engineering/maintenance/` and `integrations/` remain distinct homes because each names a stable primary responsibility.

### Dependency manifest boundary

A consuming project or personal setup may declare actual skill dependencies in `skills.yaml`. Workflow documents describe when and how selected skills are used.

The future dependency shape may resemble:

```yaml
version: 1

dependencies:
  - source: <source specifier accepted by npx skills>
    include:
      - <skill-name>
    exclude:
      - <skill-name>
```

`include` and `exclude` are optional. Do not use this manifest for upstream provenance, copied material, or inspiration: `docs/references.md` is the canonical reference record. Do not validate or depend on this shape as a stable installer contract. The rewritten CLI will later install skills as vendored copies, so its final schema and behavior remain owned by the separate `ai-skills-cli` work.

### External sources and provenance

External repositories are sources of ideas or upstream material, not required runtime dependencies for a workflow's core path. When an external skill is needed, copy or adapt it into an owned skill repository only after verifying its license and required attribution or notice obligations.

`docs/references.md` is the canonical provenance record. For every copied or materially adapted external artifact, it must record:

- the upstream URL and immutable revision or release;
- the applicable license and retained notices;
- the upstream artifact and local destination;
- whether it was copied, adapted, or only inspired local work;
- the substantive local divergences; and
- the intended upstream-review or update policy.

A high-level idea needs only a reference entry. Do not present an external skill as an installed prerequisite when the owned workflow contains the required behavior.

## Implementation prerequisites

### Shared artifact-contract rewrite

Treat `agent-workspace`, `work-plan`, `work-intake`, `build-plan`, and `work-closeout` as a coordinated semantic rewrite, not a set of independent renames. Their common contract is:

- implementation plans are local `.agents/plans/` artifacts that are discarded, archived locally, or distilled after use;
- tracked lifecycle artifacts are `.agents/notes/{proposed,current,retired,archived}`;
- `.cursor/plans/` is compatibility input only and never a new canonical target.

`agent-notes` is a distinct recurring skill for creating, updating, retiring, archiving, superseding, and distilling notes. `agent-workspace` owns setup, migration, and explanation of the artifact model.

`incremental-delivery` remains a distinct execution skill for coordinating multiple independent deliveries. Extract its reusable safety, validation, branch, and publication rules to the appropriate guardrails rather than absorbing the entire skill into `work-plan`.

`work-closeout` includes an archive mode with explicit user confirmation. Retire `plan-archive` after moving its required behavior and updating callers.

### Path and reference migration map

Before changing any skill path, create a reference inventory for every use of `.cursor/plans/` and the previous tracked `.agents/plans/` model. Classify each use as:

- compatibility-only read;
- canonical `.agents/plans/` local-plan path;
- canonical `.agents/notes/` tracked-note path; or
- removed behavior.

Update `publish-safe-links` to block local `.agents/plans/` references in publishable output.

### Post-migration naming review

After the target source-home tree is complete and skills have been reinstalled from it, evaluate whether the public names `work-plan` and `build-plan` should become simpler. Treat this as a separate follow-up decision informed by verified runtime behavior and user needs.

Do not add runtime-command invocation or collision guidance to durable documentation as part of this revamp.

### Deferred dependency-model work

Dependencies are listed in `skills.yaml`. Its schema, installer behavior, and provenance format are deliberately outside this revamp and will be defined by the separate `ai-skills-cli` design work. Consult that definition at implementation time.

- Exact `ai-skills-cli` implementation and command surface.
- Exact `skills.yaml` schema and vendored-install behavior.
- Which external artifacts to copy or adapt, after license review.
- Revision of `docs/references.md` from its current externally-installed dependency framing to the provenance model defined there.

Complete the target source-home tree, reinstall skills from a clean state, then use that updated skill set to finish the CLI work.

## Alternatives considered

### Keep one lifecycle tree under `.agents/plans/`

Rejected. It makes executable plans indistinguishable from missions, research, decisions, and local work artifacts, recreating the archival problem that prompted this revamp.

### Treat every standalone task plan as tracked lifecycle content

Rejected. Short-lived execution plans are useful locally but do not necessarily deserve repository history or required lifecycle metadata.

### Promote completed plans wholesale into notes

Rejected. Completed plans contain operational details that decay quickly. Durable knowledge should be distilled instead.

### Require a fixed taxonomy for all note types

Rejected. A small set of conventional suffixes improves navigation without forcing every useful note into a closed classification.
