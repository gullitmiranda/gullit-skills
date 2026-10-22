---
name: zed-thread-move
description: Move or import Zed agent threads between projects, including across different Zed installations/profiles. Use when the user asks to move a thread to a project, move all threads from one project to another, or import threads from an older Zed. Handles archived threads, count verification, schema differences, backups, and post-move auditing via a helper tool so you never hand-write SQL.
---
# Moving Zed agent threads between projects

Vendored from https://github.com/dandv/zed-skills (Apache-2.0, see LICENSE.md).
Local adaptation: macOS and Windows default-profile detection (via the sibling
`zed-threads` skill's `search.py`).

Zed stores threads across THREE SQLite databases per profile:

- `<profile>/threads/threads.db` — canonical thread store (the `threads` table)
- `<profile>/db/0-dev/db.sqlite` — dev-build sidebar cache (`sidebar_threads`)
- `<profile>/db/0-stable/db.sqlite` — stable-build sidebar cache (may be absent)

A thread's "project" is just its `folder_paths` value, duplicated across all
three DBs. Moving a thread = changing `folder_paths` everywhere consistently.
This is fiddly and easy to get wrong, so **always use the helper tool**
`scripts/move.py` rather than writing SQL yourself.

The tool path is in the skill's `<directory>` envelope: use
`<directory>/scripts/move.py`.

## The golden rule

**Never run `apply` without first running `plan` and getting explicit user
confirmation of the plan.** The `plan` phase is read-only and safe. The
`apply` phase writes to the databases.

## Workflow (follow exactly)

### Step 1 — Inspect the environment (read-only)

```
uv run <directory>/scripts/move.py env
```

`uv run` is preferred — it reads the script's PEP 723 metadata header and
pins the Python version. Plain `python3 <directory>/scripts/move.py …` also
works (stdlib only, no third-party deps).

This prints the detected profile, the DB inventory, and whether Zed is
running. Note the profile path. If autodetect fails, ask the user for the
Zed `--user-data-dir` and pass it with `--profile <path>` on every command.

Profile autodetection is delegated to the sibling `zed-threads` skill
(`../zed-threads/scripts/search.py --show-profiles`), which has the robust
`/proc`-based detector. The two skills are expected to live side by side; if
`search.py` is missing, autodetect is skipped and you must pass `--profile`.

### Step 2 — Build a plan (read-only)

Pick ONE of these selection modes based on the user's request:

**(a) Move ALL threads from a project** ("move everything from A to B"):
```
uv run <directory>/scripts/move.py plan \
  --from-folder "<SOURCE folder_paths>" \
  --dest "<DEST folder_paths>" \
  --expect-count <N> \
  --out /tmp/zed-move-plan.json
```
`--expect-count N` is the number the user expects (usually what they see in
the sidebar). The tool HARD-STOPS if the actual total differs — typically
because some threads are archived (hidden from the sidebar). If you don't
have a count from the user, omit `--expect-count`, but then you MUST show
them the full list (visible + archived) and confirm.

**(b) Move thread(s) by title** ("move thread 'XYZ' to B", possibly several):
```
uv run <directory>/scripts/move.py plan \
  --title "first thread title" \
  --title "second thread title" \
  --dest "<DEST folder_paths>" \
  --out /tmp/zed-move-plan.json
```
Repeat `--title` for each named thread. Threads may live in different source
projects — that's fine, the tool resolves each independently.

### Step 3 — Handle a STOP_AND_ASK

If `plan` prints `STOP_AND_ASK` on stderr and exits non-zero, **do not
proceed**. Relay the tool's message to the user and ask for clarification.
The tool stops in these cases:

- **No match** for a title → ask the user to re-check the name.
- **One similar (not exact) match** → show it, ask "did you mean this?"
- **Multiple similar matches** → list them, ask which one (or get the id).
- **Count mismatch** → e.g. user said 3 but the folder has 4 (1 archived).
  Explain the archived delta and ask whether to move all of them. To
  proceed after they confirm, re-run `plan` with `--expect-count` set to
  the TOTAL the tool reported (or omit it).

### Step 4 — Confirm the plan with the user

When `plan` succeeds it prints `PLAN OK` plus a per-thread list to stderr and
the machine-readable plan JSON to stdout (also saved to `--out`). Show the
user:
- how many threads, and which (titles), flagging any `[archived]`
- the source folder(s) and the destination folder
- whether it's a **cross-profile** import (`"cross_profile": true`)

Get an explicit "yes" before Step 5.

### Step 5 — Apply (writes to the DBs)

Output the "apply" command and tell the user to quit Zed, then run it:

```
uv run <directory>/scripts/move.py apply \
  --plan-file /tmp/zed-move-plan.json \
  --backup-dir "<DEST project>/zed-threads"
```

`apply` automatically:
1. Refuses if Zed is running, or if it can't determine whether Zed is
   running (e.g. the sibling `zed-threads` skill is missing) — fails safe
   by assuming Zed is running. Pass `--force` to override.
2. Backs up all destination DBs into `<backup-dir>/<YYYY-MM-DD_HH-MM>.zip`.
3. Quiesces the DBs (`wal_checkpoint(TRUNCATE)`).
4. Moves the threads — UPDATE for same-profile, INSERT for cross-profile.
5. Backfills `interacted_at` so moved threads don't show a misleading
   "last interacted = now" on the next click (pass `--no-backfill` to skip).
6. Audits: counts the moved threads at the destination in each DB.

Report the audit to the user. Every DB should show the expected count with
`[OK]`. If any shows `[MISMATCH]` (tool exits 5), surface it — do not retry
blindly; investigate or hand back to the user.

## Cross-profile import (older Zed → current Zed)

When importing from a different/older Zed installation, add
`--source-profile <OLD user-data-dir>` to the `plan` command. The dest
profile stays the autodetected (or `--profile`) current one.

Because the source profile's project layout may differ from the
destination's, **do NOT assume the source `folder_paths` is the right
destination**. Always ask the user which destination project each imported
thread should land in, and pass that as `--dest`. (If different threads need
different destinations, run one plan+apply per destination.)

## Key facts (so you can explain things to the user)

- **Archived threads are hidden from the sidebar.** A project that "looks
  like 3 threads" may have more. The tool counts the truth; trust it over
  the sidebar.
- **Subagent threads** (those with a `parent_id`) are intentionally excluded
  — they render nested inside their parent and never get their own sidebar
  row. The tool only operates on root threads.
- **0-stable may lag.** If the user runs only the dev build, the 0-stable
  sidebar can be out of date; the tool still writes it so a future stable
  launch is correct.
- **Backups are zips** at `<backup-dir>/<timestamp>.zip` containing all three
  DBs. To restore: unzip and copy `threads.db`, `0-dev_db.sqlite`,
  `0-stable_db.sqlite` back to their original locations in the profile.

## What you must NOT do

- Do not hand-write SQL against these databases.
- Do not run, or offer to run, the `apply` command yourself.
- Do not proceed past a `STOP_AND_ASK` without user input.
- Do not assume a destination folder on cross-profile imports — ask.
