---
name: zed-threads
description: Search the user's Zed agent threads by keyword or regex. Use when the user references a prior Zed conversation, asks "what did we discuss about X in Zed", wants to find a thread by remembered command/topic, or asks to grep their Zed agent history. Autodetects the threads.db location on Linux, macOS, and Windows (respecting $XDG_DATA_HOME, the platform default data dir, --user-data-dir of running Zed instances, and $ZED_USER_DATA_DIR / --profile). Supports searching multiple active Zed profiles at once when detected. Overridable via --db / $ZED_THREADS_DB. Decompresses zstd message blobs.
TODO: update schema to v1.4.0
---

# Zed thread search

Vendored from https://github.com/dandv/zed-skills (Apache-2.0, see LICENSE.md).
Local adaptation: macOS and Windows default-profile detection.

Zed stores agent threads in a SQLite DB at `<profile>/threads/threads.db` (where `<profile>` is the user-data directory). Default profile: on Linux `$XDG_DATA_HOME/zed` (or `~/.local/share/zed`), on macOS `~/Library/Application Support/Zed`, on Windows `%APPDATA%\Zed`. If Zed is launched with `--user-data-dir DIR`, its threads live at `DIR/threads/threads.db`.

Each thread's messages are JSON blobs compressed with zstd, so you can't `LIKE` over them — use `scripts/search.py` to do the decompress-and-grep.

The script autodetects active profiles by inspecting running Zed processes (for `--user-data-dir`) plus the computed default. When >1 active profile is detected it searches *all* of them and tags results with the originating profile directory.

## Invocation

```
uv run scripts/search.py [QUERY] [--db PATH] [--profile DIR] [--show-profiles]
                                [--since DATE] [--folder STR]
                                [--limit N] [--matches-per-thread N]
                                [--case-sensitive] [--regex] [--context N]
                                [--json] [--ids-only] [--rank]
```

`uv run` is preferred — it reads the script's PEP 723 metadata header and installs `zstandard` automatically. Plain `python3 scripts/search.py …` also works; if `zstandard` isn't installed, the script falls back to shelling out to the `zstd` CLI.

`--show-profiles` prints the profile dir(s) that would be searched (one per line, or JSON with `--json`) and exits without needing QUERY. Useful for inspecting autodetection.

The DB path resolves as follows (explicit flags/env always force single-profile mode):

1. `--db PATH` (or `$ZED_THREADS_DB`)
2. `--profile DIR` (or `$ZED_USER_DATA_DIR`) → `<DIR>/threads/threads.db`
3. Autodetected active profiles (see below). If exactly one → single db. If >1 → search all of them.
4. Computed default (platform-specific: `$XDG_DATA_HOME/zed`, `~/.local/share/zed`, `~/Library/Application Support/Zed`, or `%APPDATA%\Zed`, preferring a candidate where `threads/threads.db` exists)

When multiple profiles are searched, text output prefixes groups with `profile: /path/to/profile` and JSON results include a `"profile"` field containing the profile directory (not the `threads.db` filename).

## What's searched vs skipped

| Searched (ranked from most to least relevant)                       | Skipped                                 |
|---------------------------------------------------------------------|-----------------------------------------|
| Thread `summary` column                                             |                                         |
| User text messages                                                  |                                         |
| User `@mention` content (rules, files, threads pulled into context) | User `Image` blocks                     |
| Agent text replies                                                  | Agent `Thinking` blocks                 |
| Tool calls — name + JSON-stringified input args                     | Tool **results** (output of tool calls) |

Snippets are always at least 60 characters when the source text permits, regardless of `--context`.

This intentionally finds threads by *what was said* and *what was done* (commands run, files edited), but not by tool output noise or the model's internal thinking.

## `--rank`: relevance scoring

When `--rank` is passed, results are sorted by relevance instead of recency (newest first). Each thread gets a BM25-style score computed as:

```
score = Σ (match_count_per_kind × kind_weight)
```

| Kind     | Weight |
|----------|--------|
| `user`   | 3.0    |
| `mention`| 2.5    |
| `summary`| 2.0    |
| `agent`  | 1.0    |
| `tool:*` | 0.3    |

A thread where the user explicitly typed the query gets a higher score than one where the query only appears in tool invocations or agent responses. Ties are broken by recency (newer first).

Text output shows `score: N.N` before the summary. JSON output includes a `"_score"` field. `--rank` scans **all** matching threads (not just the first `--limit` from chronological order), so it is slower on large databases.

## Output

By default, results are returned grouped by thread, in reverse chronological order (newest first):

```
<thread-id>  <updated_at>  <folder_paths>
  <summary>
  [user]   …snippet around match…
  [tool:terminal]  …snippet…
```

When the script autodetects multiple active Zed profiles it searches all of them. Text output then prefixes each group with a `profile: /path/to/profile/dir` header (the directory containing `threads/`, not `threads.db` itself). `--json` results include a top-level `"profile"` string on each thread object. `--ids-only` is unchanged (plain IDs).

Use `--json` for structured output, `--ids-only` to pipe IDs to another command.

Use `--show-profiles` (no QUERY needed) to just list the profile dir(s) the script would search right now.

## Examples

Find threads that mention a topic:
```
python3 scripts/search.py "cpuset"
```

Recent threads only, narrow by working directory:
```
python3 scripts/search.py "migration" --since 2026-04-01 --folder $HOME/my-project
```

Just the IDs, e.g. to feed another tool:
```
python3 scripts/search.py "TODO" --ids-only --limit 20
```

Wider snippets when you need more context:
```
uv run scripts/search.py "FOREIGN KEY" --context 200 --matches-per-thread 5
```

Regex (Python `re` syntax):
```
uv run scripts/search.py "cpus(et|\.max)" --regex
uv run scripts/search.py "TODO\(\w+\)" --regex --case-sensitive
```

Rank by relevance instead of recency:
```
uv run scripts/search.py "libreoffice" --rank --limit 10
```

## Requirements

- `python3` ≥ 3.10 (uses stdlib `sqlite3`, `json`, `re`)
- **Either** `uv` on `$PATH` (recommended — handles `zstandard` install via the PEP 723 header) **or** one of:
  - `pip install zstandard` (Python decompression, no system deps)
  - `zstd` CLI on `$PATH` (the script shells out as a fallback)
- Read access to the threads DB. The script opens it `mode=ro`, so it's safe to run while Zed is open — SQLite's WAL mode is designed for concurrent readers.
- (Optional) `--show-profiles` works without a query and without touching any DB contents.

## Schema reference

Single table `threads`:

| column               | type    | notes                                                  |
|----------------------|---------|--------------------------------------------------------|
| `id`                 | TEXT PK | thread UUID                                            |
| `summary`            | TEXT    | human-readable title shown in Zed's thread list        |
| `updated_at`         | TEXT    | ISO-8601 with nanos + tz                               |
| `data_type`          | TEXT    | always `"zstd"` in observed data                       |
| `data`               | BLOB    | zstd-compressed JSON `{"title":..., "messages":[...]}` |
| `parent_id`          | TEXT    | nullable, links forked threads                         |
| `worktree_branch`    | TEXT    | git branch when thread started                         |
| `folder_paths`       | TEXT    | working directory(ies) for the thread                  |
| `folder_paths_order` | TEXT    | display order                                          |
| `created_at`         | TEXT    | ISO-8601                                               |

Decompressed message JSON (observed variants):

```jsonc
{
  "title": "...",
  "messages": [
    { "User":  { "id": "...", "content": [
        {"Text": "..."},
        {"Mention": {"uri": {...}, "content": "..."}},
        {"Image": {...}}
    ]}},
    { "Agent": { "content": [
        {"Thinking": {"text": "...", "signature": "..."}},
        {"Text": "..."},
        {"ToolUse": {"name": "...", "input": {...}, "raw_input": "...", ...}}
    ], "tool_results": {"<tool_use_id>": {...}} }},
    "Resume"  // sentinel, not a dict
  ]
}
```
