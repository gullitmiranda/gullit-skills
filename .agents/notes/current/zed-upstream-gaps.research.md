# Zed: Upstream Gap Map (Cursor-parity pain points)

**Status:** open gaps, partially tracked upstream. Recorded 2026-10-22, extended same day (gap 9 added 2026-10-22), extended 2026-11-06 (gap 10 from the terminal-deadline check; gaps 11-12 for thread identity/deeplinks and global thread search).

Durable record of the Zed-vs-Cursor agent/conversation UX gaps felt locally,
what exists upstream as of the research date, and where a contribution would
land. All issue/PR/discussion states are as of 2026-10-22 unless a section says
otherwise, verified live via `gh` against `zed-industries/zed` (read-only); gaps 10-12 were
verified again on 2026-11-06. Prior local records cover
adjacent pain: [zed-worktrees-file-scan-exclusions.research.md](./zed-worktrees-file-scan-exclusions.research.md)
(multi-root x worktree bugs) and `../plans/zed-workflow-migration.plan.md`
(thread-identity decisions; thread title is not a stable identity).

Relevant code today: legacy `crates/assistant` is gone. Current crates:
`agent` (thread store, SQLite), `agent_ui` (panel, `threads_archive_view.rs`,
`agent_panel.rs`), `sidebar` (Threads Sidebar + thread switcher),
`settings_content` (agent settings UI), `gpui` (platform layer).

## Gap map (original inventory 2026-10-22; terminal execution, thread identity, and global search added 2026-11-06)

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
| 9 | Inline think tags from chat-completions reasoning models | [#47559](https://github.com/zed-industries/zed/issues/47559) closed 2026-08-28 without a fix; [#50989](https://github.com/zed-industries/zed/issues/50989) open | No tag parser on the openai_compatible path; tags leak into UI, titles, summaries | Revive [#54252](https://github.com/zed-industries/zed/pull/54252), closed unmerged |
| 10 | Enforced terminal deadlines without killing intentional services | [v1.27.0 terminal tool](https://github.com/zed-industries/zed/blob/c84af5b99cbc366d675064e52b23664a015b6e35/crates/agent/src/tools/terminal_tool.rs) | Explicit timeout works; omitted timeout is unbounded in the inspected implementation | Runtime deadline policy plus a separate persistent-session lifecycle; instructions alone are not enforcement |
| 11 | Thread identity: copy a thread ID and a link/deeplink to the thread | [discussion #66184](https://github.com/zed-industries/zed/discussions/66184) proposes `zed://agent/thread/<session_id>`; no copy action exists | `zed://` routes exist for `agent`, `agent?prompt=`, `file`, `git/commit/<sha>`, settings, skills; no route opens an existing local thread, and no menu/command copies an ID or link (`agent::CopyThreadToClipboard` exports markdown) | Comment on #66184; add the URL route plus a copy action riding the existing open-by-id seam |
| 12 | Global thread search across all projects | [#58676](https://github.com/zed-industries/zed/issues/58676) (content search, Planned) combined with [#50854](https://github.com/zed-industries/zed/issues/50854) (global history, NOT_PLANNED) | Every search surface is title-based and project-scoped by design; Cursor's single cross-project search has no equivalent | Same storage decision as gap 1; frame global scope as an additive follow-up to #58676 |

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

**Local observation (2026-11-11):** `zed -n <workspace> <child paths...>` kept
only `<workspace>` as an open root; the extra paths were not added. The
workable pattern was to open the parent directory as the single root and place
the child repos inside it, which makes per-task root changes unnecessary. This
does not contradict the CLI gap above: it is a layout workaround, and
programmatic add/remove/reorder remains unimplemented.

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

## 9. Inline think tags from chat-completions reasoning models

**Local trigger (2026-10-22):** after enabling the thinking toggle on GLM-5.x
lanes behind an OpenAI-compatible gateway, raw inline-reasoning delimiters
(angle-bracketed `think` / `/think`, the GLM-family CoT markers — the exact
bytes are intentionally not written here: the serving transport corrupts
them inside agent tool calls, see below) started
showing up in the agent panel transcript, and one thread's auto-generated
title stored the model's reasoning verbatim (tags included). The local thread
DB scan found dozens of tags in historical agent messages that never
discussed tags. Same-flavor reports upstream: [#50989](https://github.com/zed-industries/zed/issues/50989)
(commit messages with tags via LM Studio, open) and closed ones #52392,
#45316, #41318, #34852, #23778, #30233.

**Root cause (verified in source at v1.25.2):** there is no think-tag parser
anywhere on the chat-completions path. `ChatCompletionEventMapper`
(`crates/language_model_core/src/chat_completion.rs:424`) only turns
`delta.reasoning_content` into thinking events; `content` is never tag-parsed,
so tags arriving in `content` render as ordinary markdown (HTML block or
literal text). Titles (`thread.rs:5036`) and compaction consume raw text with
no stripping, and `AgentMessage::to_markdown` (`thread.rs:610-625`) actively
re-emits literal tag wrappers around thinking when serializing history for
compaction — the prompt itself teaches the model to keep producing the tags.

**Wire-level confirmation (same day):** against the gateway, GLM-5.x with
`reasoning_effort: "none"` returns chain-of-thought inline in `content`
delimited by the tags (the model family cannot disable reasoning); with an
explicit on-value it returns proper `reasoning_content` and clean `content`.
So the leak appears whenever a request shape reaches the worker with
reasoning off/unmapped — including auxiliary calls — and Zed has no
fallback parsing for it. A serving-side transform also mangles tag literals
inside request payloads (tool results arrive at the model corrupted), which
makes the bug self-masking: reporting it through the agent corrupts the
report.

**Upstream:** [#47559 - openai_compatible doesn't support inline think tags](https://github.com/zed-industries/zed/issues/47559)
(the issue title spells the literal delimiter) — closed 2026-08-28 with no
fix landing; the implementation PR [#54252 - Fix thinking block handling for OpenAI-compatible providers](https://github.com/zed-industries/zed/pull/54252)
was closed unmerged on 2026-04-24, and no maintainer opposition is recorded —
it looks dropped rather than rejected, so a revival PR that rebases #54252
(parse think tags in the chat-completions mapper, strip them from
titles/compaction) is a well-anchored contribution candidate; #50989 stays
open as fresh evidence the gap is live. Interim local mitigations already
applied: `interleaved_reasoning: true` on all chat-completions reasoning
entries and never sending effort `none` to GLM lanes.

**Framing for upstream (2026-10-23):** classify as a feature request, argue
it with bug-grade impact. The OpenAI-compat spec does not define where
reasoning goes, so Zed is technically spec-clean — but every mature client
in the ecosystem handles inline reasoning (pi-ai encodes per-family
`thinkingFormat`; Claude Code sits on a bridge that returns separate
thinking blocks), while vLLM/Ollama/OpenRouter serve R1/Qwen/GLM workers
that emit inline tags all day. The strong upstream argument is not "my
gateway emitted tags" (answer: fix your server) but "a robust OpenAI-
compatible client must tolerate the servers the ecosystem actually runs".
Two-tier contribution:

1. Full reasoning segregation in the chat-completions mapper (parse inline
   tags into thinking events, rebase #54252) — medium size.
2. Defensive-only: strip known tag delimiters in the title and compaction
   prompts so CoT can never land in a thread title — small, nearly
   uncontroversial, removes the most visible symptoms alone.

**Related findings (2026-10-23, verified in source on `main`):**

- Title and thread-context summary generation are routable per-model today:
  `agent.thread_summary_model` (exists in v1.25.2), consumed via
  `thread_summary_model -> default_fast_model -> default_model` fallback in
  `crates/language_model/src/registry.rs`; `build_thread_title_request`
  (`crates/agent/src/thread.rs`) and the `ThreadContextSummarization` intent
  both use the summarization model. Local mitigation: point it at a lane with
  a real thinking-off switch (e.g. kimi-k3 with thinking disabled), same
  pattern as the existing `agent.compaction_model` override. This fixes
  garbage titles and broken per-interaction summary messages without any
  upstream change.
- Verified NOT a bug (2026-11-03, source at `main` and `v1.25.2`): the
  automatic title path (SessionInfoUpdate -> TitleUpdated ->
  `handle_conversation_event` in `thread_metadata_store.rs`) preserves
  `title_override` explicitly; `set_generated_title` clearing the override is
  reachable only through the explicit "Regenerate Thread Title" action
  (plus the title-failure retry button), is intentional, and is pinned by
  `test_store_set_generated_title_clears_title_override`. The local
  symptom was most likely a click on that retry button (shown whenever
  title generation fails — plausible with garbage titles from the think-tag
  leak). No upstream issue exists for "rename later reverts" (searched ~10
  phrasings) because the automatic path does not have the bug. Kept as a
  possible tiny hardening PR: `set_generated_title` has no doc comment
  warning that automatic title syncs must go through `save`/
  `handle_conversation_event` — a wiring that would regress the override
  was proposed and closed unmerged in #63980.

**Related finding (2026-10-28, verified in source on `main`):**
`agent.compaction_model` only honors `provider`/`model`. Its
`enable_thinking`/`effort` fields are ignored: `build_compaction_request`
(`crates/agent/src/thread.rs`) builds the request with `..Default::default()`,
so `thinking_allowed` is `false` and `thinking_effort` is `None`. For an
`openai_compatible` model entry with `reasoning_effort` set,
`supports_none_reasoning_effort` (`crates/language_models/src/provider/open_ai_compatible.rs`)
returns true, and `into_open_ai_response` (`crates/open_ai/src/completion.rs`)
then sends `reasoning.effort: "none"`. Models that reject `none` (some newer
OpenAI reasoning models only accept `low` and up) fail every compaction with
a 400. The same mapping hits title/summary requests. Local mitigation: point
`compaction_model` at a model that accepts `none`, or rewrite `none` at a
proxy. Upstream fix candidates: honor the selection's thinking/effort in
`build_compaction_request`, or add a per-model opt-out for `none` in
`openai_compatible` capabilities. Not filed yet.

## 10. Terminal deadlines and intentional process lifetimes

**Verified 2026-11-06:** source inspection used upstream `v1.27.0`, commit
`c84af5b99cbc366d675064e52b23664a015b6e35`. The locally inspected CLI reported
`Zed 1.27.0`, build `20261104.154313`; that alone does not establish which
binary serves every active conversation.

- `timeout_ms` is optional. The inspected terminal tool declares no default or
  ceiling; with no timeout supplied, it waits for completion or explicit
  cancellation. The timeout branch marks the operation as timed out and calls
  `terminal.kill`: [schema](https://github.com/zed-industries/zed/blob/c84af5b99cbc366d675064e52b23664a015b6e35/crates/agent/src/tools/terminal_tool.rs#L51-L85),
  [execution](https://github.com/zed-industries/zed/blob/c84af5b99cbc366d675064e52b23664a015b6e35/crates/agent/src/tools/terminal_tool.rs#L995-L1038).
- Unix PTY cleanup targets the foreground process group and the child shell.
  This is not a guarantee for every descendant, detached session, platform,
  or non-PTY path: [terminal cleanup](https://github.com/zed-industries/zed/blob/c84af5b99cbc366d675064e52b23664a015b6e35/crates/terminal/src/terminal.rs#L3110-L3128),
  [process-group signaling](https://github.com/zed-industries/zed/blob/c84af5b99cbc366d675064e52b23664a015b6e35/crates/terminal/src/pty_info.rs#L149-L174).
- The tool's instruction to supply timeouts and avoid indefinite servers is
  model guidance, not a mandatory deadline. No supported global deadline
  setting or argument-rewriting pre-tool hook was identified in this
  investigation. [Instructions](https://zed.dev/docs/ai/instructions) and
  [tool permission regexes](https://zed.dev/docs/ai/tool-permissions) do not
  themselves implement a runtime deadline.

**Applied policy mitigation:** the `quality` skill owns the Command Execution
contract; the Zed instruction bootstrap and Git/PR workflows load it. Finite
operations require explicit budgets, native waits replace avoidable sleep
polling, and timeout starts diagnosis rather than an unchanged retry. Service
lifetimes remain separate from startup/readiness/status deadlines. Stopping
an observation must not implicitly stop a service or cancel remote CI.

**Runtime smoke checks:** native terminal calls with `timeout_ms: 1000`
returned timeout results with captured output. An instrumented, self-expiring
60-second parent/child fixture was absent 6.319 seconds after start, before
its own expiry. This verifies the tested process group only, not arbitrary
process trees. No persistent service or remote workflow was started.

**Remaining enforcement work:** a runtime default/ceiling for finite tool
operations and a supported persistent-session lifecycle require harness work;
these were not implemented by editing instructions. Regression coverage must
include a bounded native CI watch, diagnosis after timeout, owned-process
cleanup, and a persistent service surviving a timed-out status observation.
The CI-watch and persistent-service cases were not exercised in this check.

## 11. Thread identity: copy a thread ID and a link/deeplink to the thread

**Today:** threads are addressable only from inside the app. Zed's `zed://` scheme already has
several routes -- `zed://agent` opens the Agent Panel (#34862, merged), `zed://agent?prompt=...`
opens a new thread with a prefilled prompt (#47959, merged), plus `zed://file`,
`zed://git/commit/<sha>`, settings and skills routes -- but no route opens a thread that already
exists locally. There is also no command, keybinding, or thread-options entry that copies a
thread's ID or a link to it; `agent::CopyThreadToClipboard` serializes the whole thread as
markdown for re-import, which is not a reference.

**Seam already in code:** thread sharing ([PR #46140](https://github.com/zed-industries/zed/pull/46140),
merged 2026-01-06, staff-only ship) opens a shared thread by session id through
`AgentPanel::open_thread`. So "open by id" exists; what is missing is the URL route and the
user-facing copy affordances.

**Upstream:** [discussion #66184 - Agent: open an existing agent thread from a URL (`zed://agent/thread/<session_id>`)](https://github.com/zed-industries/zed/discussions/66184)
-- open since 2026-10-26, 2 upvotes, 1 comment (2026-10-27, someone who wants to jump from a tool
that lists running agent sessions). It proposes focusing the window that owns the thread
(connecting to a remote host first when needed) and showing the thread in the Agent Panel, for
Zed Agent and ACP threads alike. Its stated use cases match the local need: links from
notes/issues/PRs, scripts and monitors that report "agent finished", launchers (Raycast/Alfred),
and handoffs. No copy-affordance issue or discussion exists (searched 2026-11-06); #66184 is the
right thread to attach it to.

**Local desire:**
- two thread-options entries: copy the thread ID (session id) and copy
  `zed://agent/thread/<session_id>`, both pasteable into issues, notes, and PR bodies.
- the deeplink route itself, so a reference resolved anywhere (terminal, browser, Slack, another
  editor) lands on the right thread instead of the project's last-opened thread.

**Caveats to settle in the proposal:** `session_id` vs the `thread_id` primary key (still churning,
see [#64470](https://github.com/zed-industries/zed/issues/64470)), behavior when the owning project
is closed or the host is remote, and whether a copied link should embed the window identity.
The copy action is small and can land first; the route is the part that needs maintainer sign-off.

## 12. Global thread search across all projects

**Today:** both thread search surfaces are title-based and scoped: the Threads Sidebar filter
matches within a project group, and Thread History (`cmd-g`) matches title or project folder name
in per-time-bucket lists. Scope is per project deliberately (see gap 3).

**Upstream:**
- [#58676 - Search across thread history](https://github.com/zed-industries/zed/issues/58676)
  remains the only open request for content search: open, 15 upvotes, 9 hearts, last updated
  2026-09-18, **Planned** on the roadmap. Storage decision in gap 1 gates it.
- [#50854](https://github.com/zed-industries/zed/issues/50854) (history across all workspaces) was
  closed as **NOT_PLANNED**; per-project scoping is intentional, so a global surface has to be
  additive rather than a replacement.
- No issue or discussion requests a single cross-project search surface explicitly (searched
  2026-11-06); filtering/grouping asks live in discussions
  [#58374](https://github.com/zed-industries/zed/discussions/58374) and
  [#61989](https://github.com/zed-industries/zed/discussions/61989).

**Local desire (Cursor inspiration):** one search surface over every thread in every project --
title and content -- with a jump to the thread, instead of guessing the project window first and
then filtering by title. This is #58676 plus a scope switch (current project / all projects), so it
should be proposed as a follow-up to #58676 rather than as a separate storage problem. Copies of
threads living in other Zed profiles remain out of scope for core; the local `zed-threads` skill
covers that case today.

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
7. Revive #54252 as the fix for closed-unfixed #47559 (inline think-tag
   parsing for openai_compatible) — the old PR was dropped with no recorded
   opposition; pair it with stripping tags from titles/compaction.
8. Thread copy-link / deeplink (gap 11) — smallest visible win; comment on
   #66184 to align on `session_id` vs `thread_id`, then add the copy action on
   top of the `AgentPanel::open_thread` seam.

## Re-check triggers

- Terminal tool defaults, global deadline settings, pre-execution hooks, or
  managed background-session support change; re-check timeout and service
  lifecycle semantics separately.
- #58676 moves beyond "Planned" or gains an implementation PR.
- The chat-completions mapper (`crates/language_model_core/src/chat_completion.rs`)
  gains a think-tag parser, or someone revives #54252 / files a successor to
  the closed #47559.
- #59401 gains an implementation PR (non-terminal tool output truncation).
- Discussion #58374 gains a maintainer plan for pinning / sort modes.
- Discussions #58333 / #58314 gain maintainer plans for transcript collapse
  or turn-level collapse.
- #63482 merges -> check whether agent-thread system notifications followed.
- Any release notes about system notifications, thread grouping settings, or
  agent workspace-root tools.
- Discussion #66184 gains a maintainer response or an implementation PR
  (`zed://agent/thread/<session_id>`).
- A "copy thread id" / "copy thread link" action appears in the thread options
  menu, or `agent::CopyThread` starts emitting a URL.
- Thread search gains a scope switch or a global/all-projects surface (beyond
  the per-project Thread History buckets).
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
