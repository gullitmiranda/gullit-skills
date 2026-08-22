# Agent workspace migration inventory

This inventory records the tracked references that must change for the agent workspace revamp. It is a migration record, not a runtime contract. Legacy paths and names in this note are historical references only.

## Classification

- **Compatibility read**: accept existing local input without making it a new target.
- **Local plan**: use `.agents/plans/` as the canonical ignored implementation-plan path.
- **Tracked note**: use `.agents/notes/{proposed,current,retired,archived}/` for durable lifecycle knowledge.
- **Remove**: retire the behavior or entry point after its replacement is available.

## Path and lifecycle references

| Source | Current behavior | Target outcome | Owner | Evidence |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Names the legacy local plan directory as the repository policy. | Local plan; defer all artifact policy to `.agents/AGENTS.md` and retain the legacy path only for explicit migration. | `agent-workspace` | Updated in this block. |
| `.gitignore` | Does not portably exclude legacy plans. | Compatibility read; ignore `.cursor/plans/` so local-plan handling does not depend on a developer-global ignore file. | `safety` | Updated in this block. |
| `.cursor/skills/plan-archive/SKILL.md` | Archives plans under the legacy local path through a separate Cursor skill. | Remove; fold confirmed local-plan archival into `work-closeout`. | `work-closeout` | Retire after replacement validation. |
| `README.md` | Advertises the Cursor-only archive skill and its install path. | Remove; describe the replacement skill and supported installation source after source-home migration is safe. | Documentation | Update with retired adapter. |
| `docs/tool-adapters/cursor.md` | Creates new local plans in the legacy directory. | Remove path instruction; the workspace authority owns plan location and migration. | `agent-workspace` | Updated after adapter review. |
| `docs/workflows/README.md` | Keeps plans local but names the legacy directory. | Local plan; retain the local-only rule with the canonical path. | `agent-workspace` | Update workflow guidance. |
| `skills/agents-standard/SKILL.md` | Treats plans as a tracked lifecycle tree and preserves legacy plans as local inputs. | Split into local plan, tracked note, and compatibility read rules. | `agent-workspace`, `agent-notes` | Rewrite required. |
| `skills/agents-standard/templates/agents-AGENTS.md` | Defines tracked plans, scratch plans, duplicated lifecycle state, and plan-contained decisions. | Split into local-plan and tracked-note layout. | `agent-workspace` | Rewrite required. |
| `skills/build-plan/SKILL.md` | Executes tracked plans with lifecycle transitions. | Remove tracked-plan transitions; execute one ready local plan. | `build-plan` | Rewrite required. |
| `skills/engineering-workflow/SKILL.md` | Keeps local plans at the legacy path. | Local plan; merge routing into `work-intake`. | `work-intake` | Retire after merge. |
| `skills/plan/SKILL.md` | Creates Cursor and Claude plans in the legacy path and prevents implicit promotion. | Local plan; create new plans at `.agents/plans/` while retaining legacy files as compatibility-only input. | `work-plan` | Rewrite required. |
| `skills/project-path-migration/SKILL.md` | Describes the legacy plan directory as repository content. | Local plan and tracked note; describe both new workspace locations and only mention the legacy path when a compatibility symlink exists. | `cursor-project-path-migration` | Update after rename gate. |
| `skills/publish-safe-links/SKILL.md` | Rejects legacy local plans from publishable output only. | Compatibility read; reject both legacy and canonical local plan paths. | `publish-safe-links` | Update required. |
| `skills/quality/SKILL.md` | Delegates publication safety while illustrating only the legacy plan path. | Compatibility read; delegate path enforcement to `publish-safe-links` without making local paths publishable. | `publish-safe-links` | Update required. |
| `skills/safety/SKILL.md` | Prevents commits under the legacy local plan path. | Local plan and compatibility read; prevent commits under both plan locations. | `safety` | Update required. |
| `skills/work-context-cleanup/SKILL.md` | Inspects legacy plans and delegates archival to `plan-archive`. | Local plan and remove; become `work-closeout` with a confirmed archive mode. | `work-closeout` | Rewrite required. |
| `skills/workflow-intake/SKILL.md` | Treats tracked plans and legacy local drafts as different plan types. | Split into tracked note and compatibility-read rules; route one ready local plan to `build-plan`. | `work-intake` | Rewrite required. |
| `skills/workflow-intake/output-template.md` | Exposes the previous tracked-plan lifecycle and old skill routes. | Tracked note only when the input is a note; local plans have no tracked lifecycle. | `work-intake` | Rewrite required. |
| `skills/workflow/SKILL.md` | Treats the legacy and agent plan directories as unrelated plan models. | Remove; distribute its unique rules to topical owners. | Topical owners | Retire after distribution. |

## Legacy skill disposition

| Current source | Target disposition | Active consumers to update | Gate |
| --- | --- | --- | --- |
| `skills/agents-standard/` | Rewrite as `agent-workspace`. | `build-plan` | The new shared artifact contract. |
| `skills/plan/` | Rewrite as `work-plan`. | `build-plan`, `workflow-intake`, `engineering-workflow`, skills map, templates | Revisit possible simplification after source-home migration. |
| `skills/workflow-intake/` | Merge with `engineering-workflow` as `work-intake`. | README, workflow docs, context docs, build skill | Leave one public workflow router. |
| `skills/engineering-workflow/` | Merge its useful route catalog into `work-intake`, then retire. | README, `build-plan`, `workflow-intake` | Core route must not require third-party skills. |
| `skills/build-plan/` | Retain the public name with the rewritten execution contract. | `workflow-intake` and template | Revisit possible simplification after source-home migration. |
| `skills/work-context-cleanup/` | Rewrite as `work-closeout`. | Indirect documentation and archive adapter | Absorb confirmed archive mode. |
| `skills/workflow/` | Retire after distributing unique rules. | None named; inspect rules contextually. | No duplicate broad router or policy owner. |
| `.cursor/skills/plan-archive/` | Retire after `work-closeout` validates confirmed archival. | README and prior closeout skill | No competing archive entry point. |
| `skills/project-path-migration/` | Rename to `cursor-project-path-migration` if its scope stays Cursor-specific. | None named | Source-home migration gate. |

## Source-home gate

The installed CLI can recursively discover nested skill directories. Complete the target source-home tree, then reinstall skills from a clean state before continuing the separate CLI rewrite. Legacy wrapper skills are not a compatibility mechanism. The rewritten CLI will later define vendored installation behavior and the final `skills.yaml` contract.

## Validation evidence

- Repository search covered tracked Markdown and configuration files for legacy plan paths, tracked-plan assumptions, archive ownership, legacy skill names, and target names.
- No `.cursor/plans/` artifact in this repository was moved or reclassified.
- `.agents/plans/agent-workspace-revamp.plan.md` remains ignored and local.
- Re-run the search after each rewrite block; historical references in this inventory are intentional and must not be treated as active behavior.
