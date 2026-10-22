# Zed contribution: fork-first strategy

**Status:** decided 2026-10-22. Gap inventory and upstream anchors live in
[zed-upstream-gaps.research.md](./zed-upstream-gaps.research.md).

## Decision

Develop the candidate features locally in a fork of `zed-industries/zed`
first, to test and validate in daily driving, then organize the work into
deliverable PRs. Two motivators:

1. **Validation before review.** UX changes are exactly the kind of thing that
   needs real daily-driving evidence; upstream's UI/UX checklist for PRs
   requires screenshots/video anyway, so the local build produces that
   material as a side effect.
2. **Leverage existing PRs and partial implementations** as reference, even
   where they are not mergeable as-is:

   - **Notifications:** [#61189](https://github.com/zed-industries/zed/pull/61189)
     (merged platform API — `Platform::show_system_notification`, tri-platform,
     currently with no app-layer consumer),
     [#61194](https://github.com/zed-industries/zed/pull/61194) (stacked
     follow-up), [#63482](https://github.com/zed-industries/zed/pull/63482)
     (terminal-thread system notifications, open — reference for the settings
     shape to mirror for agent threads).
   - **Root management:** [#65886](https://github.com/zed-industries/zed/pull/65886)
     (sidebar: add project folders + drag-and-drop reordering),
     [#62817](https://github.com/zed-industries/zed/pull/62817) (preserve folder
     order), [#64877](https://github.com/zed-industries/zed/pull/64877)
     (workspace scoping for spawn_agent), and the CLI `--add` IPC path in
     `crates/cli/src/main.rs` for the CLI flags idea.
   - **Turn collapse:** existing settings primitives (`agent.expand_edit_card`,
     `agent.expand_terminal_card`, `thinking_display`) are the base to build on;
     codex-acp emits `final_answer` vs `commentary` message metadata, useful for
     the Phase 2 auto-collapse of [discussion #58314](https://github.com/zed-industries/zed/discussions/58314).
   - **Content search:** no implementation PRs; dandv's `zed-threads` skill
     (vendored copy planned, see the gap note) is the decompress-scan design
     reference for #58676.
   - **Context bloat:** #59401 fixes already on `main` (auto-compaction,
     terminal 16 KB cap) — build non-terminal truncation on the same seam.

## Constraints (from upstream CONTRIBUTING.md and observed triage)

- **Code-first** where a staff-anchored issue exists:
  [#61761](https://github.com/zed-industries/zed/issues/61761),
  agent-thread system notifications,
  [#59401](https://github.com/zed-industries/zed/issues/59401) truncation.
- **Discussion-first** for the parked features:
  [discussion #58374](https://github.com/zed-industries/zed/discussions/58374)
  (pin/sort), [discussion #58333](https://github.com/zed-industries/zed/discussions/58333) /
  [discussion #58314](https://github.com/zed-industries/zed/discussions/58314)
  (collapse), agent root-management tool and CLI flags (no anchor at all).
  Prototype locally, but engage the discussion early with screenshots/video
  from the local build.
- One feature per branch, rebased often — the agent area moves fast
  (~30 merged PRs since Apr 2026).
- Max 3 open PRs; AI assistance must be disclosed and human-understood; no
  autonomous-agent PRs.

## Suggested sequencing

1. Vendored `zed-threads` skill with macOS path detection (local relief, no
   upstream dependency).
2. Collapse settings locally + engage discussions #58333/#58314 (Phase 2 is
   the desired outcome).
3. Agent-thread system notifications (small scope; API idle; #63482 as
   settings reference).
4. Fix #61761.
5. Non-terminal tool output truncation (#59401 remaining gap).
6. Root management (agent tool + CLI flags) via Discussion.
