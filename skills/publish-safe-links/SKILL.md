---
name: publish-safe-links
description: Verify that file links and path references in published content (PR bodies, issue bodies, GitHub/Linear/Slack comments, READMEs, release notes, versioned docs) resolve for any reader. Use before submitting any text that will be read outside the agent session, especially when the rough draft mentions file paths, plans, research docs, or worktree paths.
---

# Publish-Safe Links

Prevent links and path references in **publishable content** from pointing at
local-only, gitignored, or unpushed files that a reader cannot access.

## When to apply

Apply this skill BEFORE submitting any of:

- `gh pr create` / `gh pr edit` / `gh pr comment` body
- `gh issue create` / `gh issue edit` / `gh issue comment` body
- Linear MCP tool calls that create or update issue/comment bodies
- Slack MCP tool calls that post messages or replies
- Edits to versioned docs, READMEs, CHANGELOGs, ADRs, release notes
- Any other text that will be read by someone outside the current agent session

Skip for:

- Agent-private context: planning docs under `.cursor/plans/`, internal research
  under `.factory/`, scratch notes, agent transcripts. These are read only by the
  agent and can freely reference local paths.
- The chat reply itself (the user can resolve any path they see).

## Core principle

Two categories of content with different rules:

| Category              | Examples                                  | Link rule                            |
| --------------------- | ----------------------------------------- | ------------------------------------ |
| Agent-private context | `.cursor/plans/*`, `.factory/*`, scratch  | Local paths OK                       |
| Publishable content   | PR/issue body, comments, docs, Slack/Linear | Every link must resolve for any reader |

If unsure, treat as publishable.

## Always-prohibited path patterns

These paths NEVER appear as links in publishable content, with no verification
needed:

- `.cursor/plans/` — local-only plan files
- `.cursor/skills/` (when not part of the published repo)
- `.factory/` — internal research and scratch
- `wt-*/` — local git worktrees
- `agent-transcripts/` — chat history
- `/Users/...` or `~/...` — absolute machine paths
- `terminals/` from Cursor projects state

If the rough draft references one of these, either:

1. Remove the link and describe the content inline ("tracked in local plan",
   "see internal research"), OR
2. Replace with a public equivalent (a tracked design doc, an issue, etc.)

## Verification procedure for any other path

For every relative path or filename that appears in the publishable draft, run
the three checks below from the relevant repo root:

```bash
# 1. Is it tracked in git?
git ls-files --error-unmatch <path>
# Exit 0 = tracked. Exit 1 = NOT tracked, do not link.

# 2. Is it gitignored?
git check-ignore -v <path>
# Exit 0 (with output) = ignored, do not link.

# 3. Is it pushed?
git log origin/<base-branch>..HEAD -- <path>
# Empty output = pushed (safe). Any commits listed = local-only changes;
# either push first or do not link to the unpublished state.
```

A path passes only when (1) succeeds, (2) does NOT match, and (3) is empty.

## Replacement patterns

When a link cannot be used as-is:

| Situation                              | Replacement                                                                  |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| Code reference in a public repo        | GitHub permalink: `https://github.com/<org>/<repo>/blob/<SHA>/<path>#L12-L34` (immune to renames) |
| Local plan / research / scratch        | Describe inline: "tracked in local plan (not published)"                     |
| File committed locally but not pushed  | Push first, then link; otherwise describe without link                       |
| Cross-repo path inside a monorepo      | Use the standalone repo's URL, not the submodule path                        |
| Path inside a submodule                | Path relative to the submodule root (per AGENTS.md), not prefixed with submodule name |

## Cross-repo and submodule context

- When writing in a PR/issue of repo `cloudwalk/X`, do not link as if reader is
  inside the monorepo (e.g., do not write `cw-infra-monorepo/X/...`). Use paths
  relative to the standalone repo, or full GitHub URLs.
- Inside a submodule's docs (e.g., `endurance-iac/`, `resources-provisioning/`),
  use paths relative to the submodule root. Do not prefix with the submodule
  directory name (per the `cw-infra-monorepo/AGENTS.md` rule).

## Allowed exceptions

- **Local-only plans linked in chat replies** — fine, the user reads them.
- **Internal Linear/Slack channels visible only to the team** — even there,
  prefer not to link to gitignored paths because teammates on a different
  machine cannot resolve them. Describe inline instead.
- **PR body referencing a file in the same PR** — OK as long as the path is
  tracked AND the PR has been pushed (otherwise the link 404s on github.com
  until push lands).

## Pre-publish checklist

Before invoking the publishing tool, run mentally:

- [ ] No `.cursor/plans/`, `.factory/`, `wt-*/`, `agent-transcripts/`,
      `/Users/`, `~/` references in the draft
- [ ] Every relative path passes `git ls-files --error-unmatch`
- [ ] No path matches `git check-ignore`
- [ ] All referenced files are pushed (`git log origin/<base>..HEAD -- <path>`
      is empty), OR the publish step pushes before submitting
- [ ] Cross-repo links use standalone repo URLs, not monorepo paths
- [ ] Submodule paths are relative to the submodule root

If any item fails, fix the draft before publishing.
