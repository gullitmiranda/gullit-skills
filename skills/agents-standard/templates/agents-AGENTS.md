# `.agents/AGENTS.md` template

Adapt to the project during setup; do not copy blindly. Remove sections the project does not need (e.g. docs taxonomy if the project has no consumer docs). Keep it short — standing rules, not tutorials.

```markdown
# Agent Workspace Structure

Agent working artifacts: plans, decision notes, scratch. Project documentation lives in `docs/`.

## Layout

    .agents/
      AGENTS.md          # this file — the format and its rules
      .gitignore         # scratch exclusions (scratch/, plans/scratch/)
      plans/             # tracked: missions, slices, promoted tasks, decision notes
        proposed/        # under discussion, backlog
        active/          # in execution (plans) or in effect (decision notes)
        implemented/     # final: delivered / in force
        rejected/        # final: considered and declined
        archived/        # frozen; never authority on the present
        scratch/         # gitignored: ephemeral task plans — no format required
      scratch/           # gitignored: non-plan ephemera (research, spikes)

Create folders when the first artifact needs them.

## Artifact types (filename suffix declares granularity)

| Suffix | Artifact | todos | parent: |
|---|---|---|---|
| `.mission.plan.md` | roadmap macro; coarse todos + final review | yes | never |
| `.slice.plan.md` | executable cut of a mission | yes | required → mission |
| `.plan.md` | standalone task — lives in `plans/scratch/` only | yes | optional |
| `.md` | decision note — no todos | no | no (links in body) |

## Lifecycle

Status is encoded twice and must agree: the folder AND a `Status:` line in the file.

- `proposed → active`: work starts. `active → implemented | rejected`: terminal.
- `implemented → archived`: only when the rationale no longer guides future work. Archived files are frozen.
- `rejected` keeps the reason; delete when it no longer prevents re-litigating a tempting mistake.
- `plans/scratch/` has no lifecycle and no format obligations.

## Required format (outside scratch)

- `Status:` line immediately after the title, matching the folder.
- `## Alternatives considered` — genuine alternatives and why they lost; if none, say so.
- Cross-references via relative markdown links, never bare filenames.

## Promotion (location is the state)

- Task → slice: rename to `.slice.plan.md` and move from `plans/scratch/` into the tree in the same change.
- Research → durable: move from `.agents/scratch/` to `docs/research/` when it will be re-consulted, grounds a decision, or was expensive to produce.
- When a slice closes, update the parent mission's todos in the same change.

## Git policy

- `plans/` (minus `plans/scratch/`) is tracked; missions, slices, and decision notes are always committed.
- Nothing ephemeral is committed; a standalone task never enters the tracked tree.
```
