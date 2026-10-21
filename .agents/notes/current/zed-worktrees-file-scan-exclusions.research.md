# Zed: Git Worktrees × `file_scan_exclusions`

**Status:** open problem, tracked upstream. Recorded 2026-10-21.

Durable record of the worktree × `file_scan_exclusions` bind in Zed: the
problem, what was verified on this date, and the upstream issues to re-check
later for improvements. All issue/PR states below are as of the research date.

## Problem

Three-way bind when working with git worktrees in Zed:

1. **No exclusions → memory blowup.** LSP/file watchers force-load ignored
   directories into the worktree snapshot with no bound (6.9 → 17 GB reported),
   and snapshot application stalls the main thread for 20 s+ on large trees.
   `file_scan_exclusions` is the only effective workaround today — and changing
   exclusions mid-session does not unload already-scanned entries; a Zed
   restart is required.
2. **With `file_scan_exclusions` → agent tools are blinded.** With
   `**/worktrees` excluded, agent native file tools refuse paths under it.
   Empirically verified: `read_file` inside an excluded path returns
   "Cannot read file because its path matches the global
   `file_scan_exclusions` setting". Enforcement is by design, not a bug.
3. **Worktree as workspace root → multi-root breaks.** Adding the worktree as
   an extra root — the only escape hatch that restores agent access — trips
   known multi-root × worktree bugs (below).

`file_scan_inclusions` is **not** an escape hatch: exclusions take precedence.
Inclusions only re-include gitignored paths, never excluded ones.

## Local setup at recording time

- User-level Zed `settings.json`: `file_scan_exclusions` includes
  `**/worktrees`; `file_scan_inclusions` includes `.env*`, `**/.agents/**`,
  `**/.cursor/**`, `**/.trunk/**`.
- Consequence: agents cannot read/edit worktree files unless the worktree is
  added as a workspace root, which destabilizes multi-root workspaces.

## Upstream references

### Feature requests / PRs that would fix this

- [zed-industries/zed#21018 - Separate `file_scan_exclusions` into distinct options for scan, search and tree exlusions](https://github.com/zed-industries/zed/issues/21018) — open since 2024-11, 94 👍 at research time, zero maintainer response in ~2 years. The issue to watch.
- [zed-industries/zed#65517 - Per surface file exclusions](https://github.com/zed-industries/zed/pull/65517) — open 2026-10-12, zero reviews, "Partially solves #21018". Adds `file_search_exclusions` / `file_finder_exclusions` via an `EntryExclusions` bitmask. Even if merged, it does NOT restore agent-tool access to excluded paths (no scan-only exclusion).
- [zed-industries/zed#45685 - Expose LSP's goto definition and find references to LLM agent](https://github.com/zed-industries/zed/pull/45685) — closed unmerged. Per research, its review documents agent-facing file tools checking `WorktreeSettings` (`file_scan_exclusions`, `private_files`) before opening buffers — the enforcement is deliberate.

### Agent-tool visibility, same family

- [zed-industries/zed#58713 - find_path skips files inside gitignored directories](https://github.com/zed-industries/zed/issues/58713) — closed; agent search honors ignore state.
- [zed-industries/zed#64440 - Add support for the `"..."` entry in `file_scan_inclusions`](https://github.com/zed-industries/zed/pull/64440) — merged 2026-09-18; testing notes confirm exclusions still take precedence over inclusions.

### Multi-root × worktree bugs (why worktree-as-root hurts)

- [zed-industries/zed#58302 - Multi-root workspace (multiple Project Panel roots) is incompatible with git worktrees](https://github.com/zed-industries/zed/issues/58302) — phantom roots, agent sessions lost after restart.
- [zed-industries/zed#62331 - git: Switching to an existing worktree in a multi-root project drops the other git root folders](https://github.com/zed-industries/zed/issues/62331) — reproducible.
- [zed-industries/zed#65675 - Saving a new buffer outside the project adds it as a workspace root, moving agent threads to a new sidebar group and triggering the ACP multi-root warning](https://github.com/zed-industries/zed/issues/65675) — filed 2026-10-15.
- [zed-industries/zed#54099 - external agent does not support multi root project! seriously?](https://github.com/zed-industries/zed/issues/54099) — not planned; ACP agents see only one root. [zed-industries/zed#65625 - agent: let the user choose which project folder is the agent's working directory in a multi-root workspace](https://github.com/zed-industries/zed/issues/65625) was closed as its duplicate.
- [zed-industries/zed#59411 - Stale workspace DB entries](https://github.com/zed-industries/zed/issues/59411) — stale entries hijack restart.
- [zed-industries/zed#54282 - Migrate project settings when removing folders from workspace](https://github.com/zed-industries/zed/pull/54282) — settings-loss-on-folder-removal fix, abandoned unmerged.

### Memory issues (why the exclusions stay)

- [zed-industries/zed#63693 - LSP file watchers on ignored directories force-load them into the worktree snapshot, following symlinks, with no bound and no watcher-scoped exclusion](https://github.com/zed-industries/zed/issues/63693) — 6.9 → 17 GB; exclusions + restart are the only workaround.
- [zed-industries/zed#62545 - Worktree snapshot application blocks the main thread for 20s+ on large node_modules trees (worktree.rs:1363), causing compositor ANR dialogs](https://github.com/zed-industries/zed/issues/62545)
- [zed-industries/zed#61385 - Sustained multi-GB memory growth during worktree rescans after filesystem watcher loses sync](https://github.com/zed-industries/zed/issues/61385)
- [zed-industries/zed#61702 - Remote: ACP thread replay retries unresolvable files indefinitely, exhausting memory](https://github.com/zed-industries/zed/issues/61702)
- [zed-industries/zed#63658 - macOS: project worktree stops receiving file/git changes after a hidden ancestor worktree (from an ACP tool-call directory location) is dropped - GlobalWatcher never re-watches descendants](https://github.com/zed-industries/zed/issues/63658)

## Workarounds in use

1. **Worktree as workspace root** — restores agent access; multi-root bugs
   above apply.
2. **Per-project exclusions** — for repos where agent work inside worktrees
   matters, move `**/worktrees` from user-level to project-level
   `.zed/settings.json`. Caveats: project arrays **replace** user arrays
   (re-list defaults such as `.git`, `.svn`, `node_modules`); exclusion
   changes require a Zed restart to take full effect.

## Re-check triggers

Re-verify upstream state when any of these fire:

- [zed-industries/zed#21018 - Separate `file_scan_exclusions` into distinct options for scan, search and tree exlusions](https://github.com/zed-industries/zed/issues/21018) gains maintainer response or merges → granular per-surface exclusions shipped.
- [zed-industries/zed#65517 - Per surface file exclusions](https://github.com/zed-industries/zed/pull/65517) merges → check whether agent tools can finally access excluded paths, or whether only search/finder surfaces split.
- [zed-industries/zed#63693](https://github.com/zed-industries/zed/issues/63693) / [#62545](https://github.com/zed-industries/zed/issues/62545) / [#61385](https://github.com/zed-industries/zed/issues/61385) get real fixes → memory pressure forcing the exclusions may drop.
- [zed-industries/zed#58302](https://github.com/zed-industries/zed/issues/58302) / [#62331](https://github.com/zed-industries/zed/issues/62331) / [#65675](https://github.com/zed-industries/zed/issues/65675) close → worktree-as-root stops breaking multi-root.
- A Zed release notes granular exclusions, watcher-scoped exclusions, or agent-tool visibility settings.

If any land, revisit the global `**/worktrees` exclusion and choose between
global vs per-project exclusions.
