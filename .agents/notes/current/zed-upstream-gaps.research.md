# Zed: Upstream Gap Map (Cursor-parity pain points)

**Status:** open gaps, partially tracked upstream. Recorded 2026-10-22, extended same day.

Durable record of the Zed-vs-Cursor agent/conversation UX gaps felt locally,
what exists upstream as of the research date, and where a contribution would
land. All issue/PR/discussion states are as of 2026-10-22, verified live via
`gh` against `zed-industries/zed` (read-only). Prior local records cover
adjacent pain: [zed-worktrees-file-scan-exclusions.research.md](./zed-worktrees-file-scan-exclusions.research.md)
(multi-root x worktree bugs) and `../plans/zed-workflow-migration.plan.md`
(thread-identity decisions; thread title is not a stable identity).

Relevant code today: legacy `crates/assistant` is gone. Current crates:
`agent` (thread store, SQLite), `agent_ui` (panel, `threads_archive_view.rs`,
`agent_panel.rs`), `sidebar` (Threads Sidebar + thread switcher),
`settings_content` (agent settings UI), `gpui` (platform layer).

## Gap map (as of 2026-10-22)

| # | Gap | Upstream anchor | Status / today | Contribution route |
|---|-----|-----------------|-----------------|--------------------|
| 1 | Search across thread content | [#58676](https://github.com/zed-industries/zed/issues/58676) — roadmap "Planned" | Title-based searches only | Fix [#61761](https://github.com/zed-industries/zed/issues/61761) first; FTS design needs staff buy-in |
| 2 | Thread management via commands/agent | scattered; no single anchor | new/rename/archive shipped; move missing; no slash commands | Move-thread action; dandv skill as stopgap |
| 3 | Recency-first view / configurable grouping | [discussion #58374](https://github.com/zed-industries/zed/discussions/58374), 26 upvotes | Recency sort within project groups only; no config | Settings; discuss first |
| 4 | Pin threads | discussion #58374 | Not implemented | Schema + action + ordering; coordinate in #58374 |
| 5 | Root/worktree mgmt via commands, agents, CLI | Net-new; bugs [#58302](https://github.com/zed-industries/zed/issues/58302)/[#62331](https://github.com/zed-industries/zed/issues/62331)/[#65260](https://github.com/zed-industries/zed/issues/65260)/[#65851](https://github.com/zed-industries/zed/issues/65851) | `workspace::AddFolderToProject` / `RemoveFromProject` exist; no agent tool; no CLI flags | Discussion first; agent tool and CLI flags share the root-management seam |
| 6 | Native OS notifications | [#63482](https://github.com/zed-industries/zed/pull/63482) (terminal-only, open); [#61189](https://github.com/zed-industries/zed/pull/61189) API merged, idle | In-app popup + sound | Hook agent completion to the platform API |
| 7 | Hide execution details, focus on final answer | [discussion #58333](https://github.com/zed-industries/zed/discussions/58333) 70 upvotes; [discussion #58314](https://github.com/zed-industries/zed/discussions/58314) 19 upvotes | Settings cover native cards/thinking only | **Phase 2 of #58314 is the local desire** |
| 8 | Context bloat (Zed consumes far more than Cursor) | [#59401](https://github.com/zed-industries/zed/issues/59401), open | Compaction + terminal 16 KB cap shipped; grep/read_file untruncated | Truncation at assembly; code-first |

Fork-first development strategy and reference-PR inventory:
[zed-contribution-fork-strategy.decision.md](./zed-contribution-fork-strategy.decision.md).

## 1. Search across conversation content (e.g. find the thread about a PR)

**Today:** all three existing searches are title-based only:

- Threads Sidebar filter ("Search threads...", `crates/sidebar/src/sidebar.rs`)
- Thread History ("Search all threads...", `cmd-g`, `threads_archive_view.rs` —
  matches title or project folder name)
- In-thread search (`cmd-f`, `agent::ToggleSearch`, current thread contents)

**Upstream:** [zed-industries/zed#58676 - Search across thread history](https://github.com/zed-industries/zed/issues/58676)
— open, 12 upvotes, `area:ai`, listed as **Planned** on zed.dev/roadmap.
Originated as [discussion #39338](https://github.com/zed-industries/zed/discussions/39338).
Known blocker (documented in issue): thread payloads are **zstd-compressed JSON
blobs** in SQLite (`threads.db`, table `threads(id, summary, updated_at,
data_type, data)`, `crates/agent/src/db.rs`), read per-id — cross-thread
content search needs either decompress-scan or a new indexable text column
maintained at save time (FTS). That storage decision is the crux and needs
staff buy-in before coding.

**Interim workaround:** dandv's comment on #58676 (2026-07) links a
community skill that searches the thread SQLite database(s) directly,
read-only, auto-detecting all Zed profiles — https://github.com/dandv/zed-skills.
Usable locally until core search lands.

**Decision — copy, do not install as-is (2026-10-22).** The repo hosts two
skills, Apache-2.0: `zed-threads` (this one) and `zed-thread-move` (rewrites
`folder_paths` across `threads.db` + sidebar cache DBs to move threads between
projects — a stopgap for gap 2, but it writes to live SQLite DBs: use only
with Zed closed and backups; the upstream move-thread action is the real
fix). `zed-threads` has **no macOS support**: profile autodetection is
`/proc`-based and the computed default is `~/.local/share/zed`, while the real
macOS path is `~/Library/Application Support/Zed/threads/threads.db`; the
`--db` / `--profile` / `$ZED_THREADS_DB` overrides make manual use possible
today. Vendor an adapted copy into the personal skills repo with attribution
to dandv, adding macOS path detection; revisit if upstream lands core search.

Related bug: [zed-industries/zed#61761 - Agent panel: thread search ignores manually renamed thread titles](https://github.com/zed-industries/zed/issues/61761)
— open, `state:reproducible`, `severity:S2`; rename -> full quit -> reopen
reproduces it. Well-scoped contribution candidate.

## 2. Managing threads via commands / from inside a conversation

**Shipped already** (may not be obvious):

- New thread: `agent::NewThread` (`cmd-n`), `agent::ToggleNewThreadMenu`,
  `agents_sidebar::NewThreadInGroup`.
- Rename: `agent::RenameSelectedThread`, click-the-title editing, "Regenerate
  Thread Title" in options menu. Persistence was fixed
  ([#50431](https://github.com/zed-industries/zed/issues/50431), completed) and
  ACP rename shipped ([#56205](https://github.com/zed-industries/zed/issues/56205),
  completed).
- Archive/delete: `agent::ArchiveSelectedThread` (`shift-backspace`),
  `agent::RemoveSelectedThread` (`cmd-shift-backspace`).
- Export/import: `agent::OpenActiveThreadAsMarkdown`,
  `agent::CopyThreadToClipboard` / `LoadThreadFromClipboard`,
  `agent::ImportThreadsFromOtherChannels`.

**Still missing:**

- **Move thread between projects** — no command. Only mechanism: the
  `ProjectPickerModal` restore-destination shown when unarchiving a thread with
  no project paths. Generalize `ThreadMetadata.worktree_paths` mutation
  (`crates/agent_ui/src/thread_metadata_store.rs`) using
  `ProjectPickerDelegate::update_working_directories_and_unarchive` as the
  pattern. Related bugs:
  [#64899](https://github.com/zed-industries/zed/issues/64899) (threads
  re-homed to active project on worktree events),
  [#65675](https://github.com/zed-industries/zed/issues/65675) (buffer outside
  project becomes root, moves threads).
- **Built-in slash commands to manage the thread** (`/rename` etc.) — net-new;
  today slash commands are only user-defined skills (`PromptLocalCommand`).

## 3. Threads grouped/sorted by recency instead of by workspace

**Today:** sidebar groups threads by project group (`ProjectGroupKey`), and
within each group already sorts by recency (`thread_display_time` =
`interacted_at ?? updated_at`, descending). Thread History groups by time
buckets (Today/...), sorted by `created_at ?? updated_at`. No configurable
grouping/sort mode (`ThreadsSidebarSettingsContent` only has `auto_open`,
`position`, `default_width`).

**Upstream:** [discussion #58374 - Agent Threads Sidebar: support pinned threads or configurable sort order](https://github.com/zed-industries/zed/discussions/58374)
— open, 26 upvotes, the canonical request. Issues #58249 and #62207 were
closed only because they were converted into that discussion. Maintainer
signal: "Making threads draggable is on our list" (macraig, 2026-06);
latest pushback (oskari, 2026-10) that drag-sort is not a substitute for
pinning. Also [discussion #61989](https://github.com/zed-industries/zed/discussions/61989)
(filtering/grouping options for history). Note
[#50854](https://github.com/zed-industries/zed/issues/50854) (global history)
was **not planned** — per-project scoping is deliberate, so a "flat recency
view" proposal should coexist with scoping, not remove it.

## 4. Pinning threads

**Not implemented.** `ThreadMetadata` has no `pinned` field (fields: `title`,
`title_override`, `updated_at`, `created_at`, `interacted_at`, `worktree_paths`,
`remote_connection`, `archived`). Tracked in the same
[discussion #58374](https://github.com/zed-industries/zed/discussions/58374)
(26 upvotes — highest-demand gap of the six). Implementation would add
`pinned`/`pin_order` to the SQLite schema + `ThreadMetadata` (migration),
a `PinSelectedThread` action in the `actions!(agent, ...)` list, pinned-first
ordering in `sidebar.rs::rebuild_contents` / `threads_archive_view.rs::update_items`.

## 5. Add/remove worktrees in multi-root via commands and agents

**Commands exist today; the agent surface is the gap:**

- Add: `workspace::AddFolderToProject` (`cmd-shift-a`), handler
  `Workspace::add_folder_to_project` (`crates/workspace/src/workspace.rs`) —
  but hardwired to an OS file picker. Programmatic seam underneath is public:
  `Project::create_worktree` / `find_or_create_worktree`
  (`crates/project/src/project.rs`).
- Remove: `project_panel::RemoveFromProject` — selection-driven; no
  path-parameterized variant. `Project::remove_worktree` is public.
- **No agent tool for root management exists** (`crates/agent/src/tools/`),
  and **no upstream issue/PR requests one** (discussions search was
  inconclusive — GraphQL search errored). Net-new proposal; under
  CONTRIBUTING.md's "discuss first" rule this should start as a Discussion.
- Workaround today: `zed --add <path>` via the terminal tool, with known bugs
  ([#29130](https://github.com/zed-industries/zed/issues/29130),
  [#59917](https://github.com/zed-industries/zed/issues/59917)).
- Adjacent open PRs to coordinate with:
  [#65886](https://github.com/zed-industries/zed/pull/65886) (sidebar: add
  project folders + drag-and-drop reordering),
  [#62817](https://github.com/zed-industries/zed/pull/62817) (preserve folder
  order), [#64877](https://github.com/zed-industries/zed/pull/64877)
  (workspace scoping for spawn_agent).
- Worktree-picker bugs matching locally-felt pain: switching to an existing
  worktree in multi-root drops the other roots
  ([#62331](https://github.com/zed-industries/zed/issues/62331), open,
  `.contrib/good non-first issue`); branch picker offers branches already
  checked out in another worktree
  ([#65260](https://github.com/zed-industries/zed/issues/65260), open);
  removing a worktree from the picker leaves the project orphaned
  ([#65851](https://github.com/zed-industries/zed/issues/65851), open, S1).
- Risk surface: the multi-root x worktree bugs tracked in the worktrees note
  (#58302, #62331, #65675).

**CLI gap (felt locally 2026-10-22):** the `zed` CLI today offers only
`-n/--new`, `-a/--add`, `-e/--existing` (plus `--foreground`, `--wait`,
`--user-data-dir`, stdin via `-`) — no way to list, remove, or reorder
workspace roots from the CLI, and no upstream issue requests it (searched
2026-10-22; only `--add` bugs
[#29130](https://github.com/zed-industries/zed/issues/29130) /
[#59917](https://github.com/zed-industries/zed/issues/59917)). Net-new flags
(`zed --remove <path>`, listing, etc.) would ride the same IPC path as
`--add` (`crates/cli/src/main.rs`) and share the root-management seam with
the agent tool — propose both together via Discussion.

## 6. Native OS notifications

**Today:** agent finish/waiting notifications are a **Zed-rendered popup
window + sound** (`crates/agent_ui/src/ui/agent_notification.rs`, fired from
`conversation_view.rs::show_notification`; `Sound::AgentDone`), with settings
`agent.notify_when_agent_waiting` (`PrimaryScreen`/`AllScreens`/`Never`) and
`agent.play_sound_when_agent_done`. Broken on Linux/Wayland where OS
notifications would work: [#43803](https://github.com/zed-industries/zed/issues/43803),
[#40656](https://github.com/zed-industries/zed/issues/40656).

**The platform API already exists and is idle:**
[#61189](https://github.com/zed-industries/zed/pull/61189) (merged 2026-07)
added `Platform::show_system_notification` / `dismiss_system_notification` /
`on_system_notification_response` plus `SystemNotification`, implemented on
all three desktop platforms (macOS UNUserNotificationCenter, Windows, Linux
notify-rust/D-Bus). **No app-layer consumer exists** (verified by greps of
current `main`). Stacked follow-up:
[#61194](https://github.com/zed-industries/zed/pull/61194).

**In flight:** [#63482](https://github.com/zed-industries/zed/pull/63482) adds
a system-notification option for **terminal** threads only; the agent-thread
equivalent is not taken. Contributing this is small and well-scoped: hook
`show_notification` (and mirror #63482's settings shape) to
`Platform::show_system_notification` with a `View` action.

## 7. Hide execution details; focus on the final answer (turn-level collapse)

**Partial relief exists today via settings:** `agent.expand_edit_card: false`,
`agent.expand_terminal_card: false`, `thinking_display: "always_collapsed"`
(plus `show_turn_stats`). These cover native edit/terminal cards and thinking
blocks — **not** ACP/external-agent transcript blocks, and there is no
turn-level grouping (no "Worked for Xs" equivalent). No settings-only
workaround exists for ACP transcript blocks.

**Upstream (both deliberately parked in Discussions):**

- [discussion #58333 - Allow ACP/tool/code transcript blocks to be collapsed by default](https://github.com/zed-industries/zed/discussions/58333)
  — open, **70 upvotes, the highest-demand gap recorded in this note**.
  Asks for collapse-by-default verbose transcript/code blocks with
  identifiable collapsed headers, building on the existing
  `expand_edit_card` / `expand_terminal_card` / `thinking_display`
  primitives.
- [discussion #58314 - expand a turn live while the agent works, then collapse it into Thinking / Commands / Edits sections when done](https://github.com/zed-industries/zed/discussions/58314)
  — open, 19 upvotes. The Codex/Cursor-style pattern: full transcript while
  live, then the finished turn collapses into collapsible sections plus the
  final message. Commenter h3har notes codex-acp already emits
  `final_answer` vs `commentary` message metadata, which would make the
  auto-collapse achievable for external Codex at least.
- [zed-industries/zed#64272 - Agent panel: turn-level workflow auto-collapse (Codex style)](https://github.com/zed-industries/zed/issues/64272)
  was closed as a duplicate of both discussions.
- Related smaller item: [#65643](https://github.com/zed-industries/zed/issues/65643)
  (clamp/summarize long commands in terminal tool-call cards) — closed.

**Implementation surface:** agent panel rendering (`agent_ui` conversation
view / `AcpThreadView`); builds on the existing card-expand settings; should
apply to external ACP agents, which render in the same view.

**Local desire (2026-10-22):** specifically **Phase 2** of discussion #58314 —
the settled-turn collapse (finished turn reads as collapsible
Thinking / Commands / Edits sections plus the final message), keeping the
live expanded transcript during work. Phase 1 as-is is fine; the
auto-collapse-on-completion is the wanted part.

## 8. Context bloat: Zed consumes far more context than Cursor

- Upstream: [#59401 - Large tool outputs (grep/read_file) are sent without truncation, overflowing the model context](https://github.com/zed-industries/zed/issues/59401)
  — open. Evidence from a real thread: 13.3 MB uncompressed thread JSON,
  99.7% raw tool output; a single grep returned 5.2M chars.
- **Already fixed** (staff yeskunall, since ~1.6.3, on `main`/preview):
  automatic compaction on by default (triggers ~90% of the context window),
  cumulative token usage tracked, terminal tool output capped (~16 KB),
  context overflow surfaced as a distinct `MaxTokens` stop reason.
- **Still broken:** grep/read_file outputs are untruncated (reproduced on
  1.19.2, 2026-09); screenshots stay in history across turns and blow total
  input size (2026-10-15 comment); some users prefer opt-in output controls
  over auto-truncation (dan-oak, 2026-10-07).
- Contribution angle: truncate non-terminal tool outputs at assembly,
  mirroring the terminal cap — staff explicitly called this "the remaining
gap". Anchored, code-first candidate.

## Upstream trajectory and contributing reality

- The agent panel is one of the most active areas: ~30 agent-panel PRs merged
  since Apr 2026, roughly half from outside the org roster; community PRs
  merged in 3 days to 3 months (e.g. #63660 terminal-thread rename, 9 days).
- Triage is fast (community bot labels in seconds; staff triage within hours
  to days), but fast triage != fast feature acceptance.
- **Roadmap** ([zed.dev/roadmap](https://zed.dev/roadmap)): "Search across
  thread history" (#58676) is **Planned** — pushing on an open door, but
  comment first to align on the storage approach. Pin/sort-order is
  deliberately parked in discussion #58374; folders likewise (issue #58318
  was converted to a discussion within hours).
- CONTRIBUTING.md hard rules: max 3 open PRs; **discuss features before
  coding** (no staff-confirmed issue -> open a Discussion, not a PR); CLA
  required; tests mandatory; UI changes need the UI/UX checklist +
  screenshots/video; one PR = one thing; no autonomous-agent PRs; AI
  assistance must be disclosed and human-understood.
- Company context: frontier investment shifting to Delta, but the editor's
  agent stack remains in active in-house maintenance.

**Recommended contribution entry points (cheapest first):**

1. Fix [#61761](https://github.com/zed-industries/zed/issues/61761) — renamed
   titles ignored by thread search; S2, reproducible, small scope.
2. System notifications for agent threads — platform API merged and idle;
   mirror #63482; motivating bugs #43803/#40656.
3. Comment on #58676 proposing the FTS/storage approach; needs staff buy-in
   on the zstd-blob schema question.
4. Agent root-management tool — net-new; start with a Discussion, coordinate
   with #65886/#62817/#64877.
5. Pin threads — coordinate in discussion #58374 first (drag-reorder already
   "on their list").
6. grep/read_file output truncation (#59401) — staff-named remaining gap,
   anchored issue, code-first.

## Re-check triggers

- #58676 moves beyond "Planned" or gains an implementation PR.
- #59401 gains an implementation PR (non-terminal tool output truncation).
- Discussion #58374 gains a maintainer plan for pinning / sort modes.
- Discussions #58333 / #58314 gain maintainer plans for transcript collapse
  or turn-level collapse.
- #63482 merges -> check whether agent-thread system notifications followed.
- Any release notes about system notifications, thread grouping settings, or
  agent workspace-root tools.
- Upstream changes to `ThreadMetadata` schema (new fields) or
  `crates/agent/src/db.rs` (indexable text column) — signals someone started
  content search.

## Caveats

- GitHub Discussions could not be searched systematically (GraphQL search
  API parse errors); individual discussions were verified by direct lookup.
  A pre-existing discussion requesting agent-callable root management may
  exist.
- The repo-root `CHANGELOG.md` is gone (404 via API); releases are documented
  on zed.dev and were not fetched page-by-page.
- Negative claims ("no consumer", "no request") rest on direct greps of
  current `main` plus a 2026-08-22 local clone snapshot.
- Notification behavior on agent *error* (as opposed to completion/waiting)
  was not verified; no evidence of error-triggered notifications was found.
