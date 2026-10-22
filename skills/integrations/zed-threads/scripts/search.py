#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["zstandard"]
# ///
"""Search Zed agent threads for keywords or regex.

Run with `uv run scripts/search.py …` to auto-install deps via PEP 723.
Or run with plain `python3` — the script falls back to the `zstd` CLI
if the `zstandard` package isn't installed.
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

try:
    import zstandard as _zstd
    _dctx = _zstd.ZstdDecompressor()
    def decompress(blob: bytes) -> bytes:
        return _dctx.stream_reader(blob).read()
except ImportError:
    def decompress(blob: bytes) -> bytes:
        r = subprocess.run(
            ["zstd", "-d", "--stdout"], input=blob, capture_output=True, check=True
        )
        return r.stdout


# Lower number = higher display priority within a thread.
KIND_ORDER: dict[str, int] = {
    "user": 0,
    "mention": 1,
    "summary": 2,
    "agent": 3,
    # tool:* — sort alphabetically among themselves, after everything else.
}

# BM25-style field boost weights (higher = more relevant).
# Used only with --rank.
KIND_BOOST: dict[str, float] = {
    "user": 3.0,
    "mention": 2.5,
    "summary": 2.0,
    "agent": 1.0,
    # tool:* — default 0.3
}


def _kind_sort_key(kind: str) -> tuple[int, str]:
    """Return a sort key so matches sort: user > mention > summary > agent > tool:*."""
    if kind.startswith("tool:"):
        return (4, kind)
    return (KIND_ORDER.get(kind, 99), kind)


def _kind_boost(kind: str) -> float:
    """Return the BM25-style field boost weight for a given kind."""
    if kind in KIND_BOOST:
        return KIND_BOOST[kind]
    if kind.startswith("tool:"):
        return 0.3
    return 0.5  # unknown kinds


def iter_searchable_text(thread_json: dict):
    """Yield (kind, text) tuples for each searchable span in a thread.

    Includes: user Text/Mention, agent Text, agent ToolUse (name + input JSON).
    Excludes: agent Thinking, user Image, tool_results.
    """
    for msg in thread_json.get("messages", []):
        if not isinstance(msg, dict):
            continue
        for role, body in msg.items():
            if not isinstance(body, dict):
                continue
            for block in body.get("content", []):
                if not isinstance(block, dict):
                    continue
                for kind, val in block.items():
                    if role == "User" and kind == "Text" and isinstance(val, str):
                        yield ("user", val)
                    elif role == "User" and kind == "Mention" and isinstance(val, dict):
                        c = val.get("content")
                        if isinstance(c, str):
                            yield ("mention", c)
                    elif role == "Agent" and kind == "Text" and isinstance(val, str):
                        yield ("agent", val)
                    elif role == "Agent" and kind == "ToolUse" and isinstance(val, dict):
                        name = val.get("name", "")
                        inp = val.get("input", val.get("raw_input", ""))
                        inp_str = inp if isinstance(inp, str) else json.dumps(inp)
                        yield (f"tool:{name}", inp_str)


def make_snippet(text: str, pattern: re.Pattern, context_len: int) -> str:
    """Extract a snippet around the first match of `pattern` in `text`.

    The total snippet length (including the match itself) is at least 60 chars
    when the source text permits, regardless of how low `context_len` is.
    """
    m = pattern.search(text)
    if not m:
        return ""
    MIN_TOTAL = 60
    # Ensure enough context on each side so the total snippet (match +
    # context on both ends) reaches MIN_TOTAL, but don't exceed text bounds.
    match_len = m.end() - m.start()
    needed_per_side = max(context_len, (MIN_TOTAL - match_len + 1) // 2)
    start = max(0, m.start() - needed_per_side)
    end = min(len(text), m.end() + needed_per_side)
    snippet = text[start:end].replace("\n", " ").replace("\r", " ")
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def _is_zed_executable(argv0: str) -> bool:
    """True only if argv[0] looks like the Zed editor binary itself.

    The `--user-data-dir` flag is NOT Zed-specific: every Electron/CEF/Chromium
    app (Obsidian, WebStorm's jcef_helper, VS Code, etc.) accepts it too. So we
    must key on the executable, not the flag, or we pick up unrelated apps'
    data dirs as bogus "Zed profiles".
    """
    base = Path(argv0).name.lower()
    # Exact editor binary names. (`./zed`, `/usr/bin/zed`, `Zed`, `zed-editor`.)
    return base in ("zed", "zed-editor", "zed-preview", "zed-nightly")


def _looks_like_chromium_child(parts: list[str]) -> bool:
    """True for Electron/CEF/Chromium helper subprocesses.

    These carry `--type=renderer|utility|gpu-process|zygote|...` and frequently
    a `--user-data-dir`, but are never the Zed editor. Reject them outright.
    """
    return any(a.startswith("--type=") for a in parts)


def detect_running_zed_processes():
    """Return list of (has_explicit, dir_or_None, cmdline) per running Zed process.

    Uses /proc (full cmdline, Linux) primary; falls back to ps.
    Supports --user-data-dir DIR and --user-data-dir=DIR.
    `cmdline` is the full command line string (for display, e.g. "is Zed
    running?" checks).

    Only processes whose executable (argv[0]) is actually the Zed binary are
    considered; this avoids matching other apps that happen to accept a
    `--user-data-dir` flag (Obsidian, jcef_helper, VS Code, ...).
    """
    results = []
    # /proc primary (robust, no truncation, linux)
    try:
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                raw = (entry / "cmdline").read_bytes()
                parts = [p.decode("utf-8", "replace") for p in raw.split(b"\0") if p]
                if not parts:
                    continue
                # Must be the Zed editor binary, and not a Chromium helper child.
                if not _is_zed_executable(parts[0]) or _looks_like_chromium_child(parts):
                    continue
                cmdline_str = " ".join(parts)
                m = re.search(r"--user-data-dir[=\s]+(\S+)", cmdline_str)
                if m:
                    results.append((True, m.group(1), cmdline_str))
                else:
                    results.append((False, None, cmdline_str))
            except Exception:
                continue
    except Exception:
        pass

    if results:
        return results

    # ps fallback
    try:
        out = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            parts = line.split()
            if not parts:
                continue
            if not _is_zed_executable(parts[0]) or _looks_like_chromium_child(parts):
                continue
            m = re.search(r"--user-data-dir[=\s]+(\S+)", line)
            if m:
                results.append((True, m.group(1), line))
            else:
                results.append((False, None, line))
    except Exception:
        pass
    return results


def get_default_profile() -> Path:
    """Return the default Zed user-data dir per platform.

    Prefers a candidate that already has threads/threads.db if present.
    """
    home = Path.home()
    cands: list[Path] = []
    if sys.platform == "darwin":
        cands.append(home / "Library" / "Application Support" / "Zed")
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            cands.append(Path(appdata) / "Zed")
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        cands.append(Path(xdg).expanduser() / "zed")
    cands.append(home / ".local/share" / "zed")
    cands.append(home / ".var/app/dev.zed.Zed/data" / "zed")
    for c in cands:
        if (c / "threads" / "threads.db").exists():
            return c
    return cands[0] if cands else (home / ".local/share" / "zed")


def get_active_profiles() -> list[Path]:
    """Return deduped list of active profile dirs.

    - Every distinct --user-data-dir from running zed procs.
    - Plus the default profile IFF at least one zed proc was seen without the flag
      (or if no zed procs at all, still return default so the tool remains useful).
    Order: explicit first, then default.
    """
    procs = detect_running_zed_processes()
    profiles: list[Path] = []
    default_p = get_default_profile()
    saw_default_runner = False
    for has_flag, val, _cmdline in procs:
        if has_flag and val:
            p = Path(val).expanduser()
            if p not in profiles:
                profiles.append(p)
        else:
            saw_default_runner = True
    if saw_default_runner or not procs:
        if default_p not in profiles:
            profiles.append(default_p)
    if not profiles:
        profiles.append(default_p)
    return profiles


def resolve_threads_dbs(args) -> list[Path]:
    """Return list of threads.db Paths according to precedence.

    Explicit --db / $ZED_THREADS_DB / --profile / $ZED_USER_DATA_DIR => single entry (len==1).
    Otherwise: one or more from get_active_profiles().
    """
    if args.db:
        return [Path(args.db).expanduser()]
    if os.environ.get("ZED_THREADS_DB"):
        return [Path(os.environ["ZED_THREADS_DB"]).expanduser()]
    prof = getattr(args, "profile", None) or os.environ.get("ZED_USER_DATA_DIR")
    if prof:
        return [Path(prof).expanduser() / "threads" / "threads.db"]
    # auto
    return [p / "threads" / "threads.db" for p in get_active_profiles()]


def search(db_path: Path, pattern: re.Pattern, limit: int, since: str | None,
           folder: str | None, context_len: int, matches_per_thread: int,
           rank: bool = False):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = conn.cursor()

    sql = "SELECT id, summary, updated_at, folder_paths, data FROM threads"
    where, params = [], []
    if since:
        where.append("updated_at >= ?")
        params.append(since)
    if folder:
        where.append("folder_paths LIKE ?")
        params.append(f"%{folder}%")
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY updated_at DESC"

    cur.execute(sql, params)

    results = []
    for tid, summary, updated_at, folder_paths, data in cur:
        try:
            obj = json.loads(decompress(data))
        except Exception as e:
            print(f"warn: skip {tid}: {e}", file=sys.stderr)
            continue

        matches = []
        kind_counts: dict[str, int] = {}  # only populated when rank=True
        # Summary is also searchable.
        for kind, text in [("summary", summary or "")] + list(iter_searchable_text(obj)):
            if pattern.search(text):
                matches.append((kind, make_snippet(text, pattern, context_len)))
                if rank:
                    kind_counts[kind] = kind_counts.get(kind, 0) + 1
                if matches_per_thread and len(matches) >= matches_per_thread:
                    break

        if matches:
            matches.sort(key=lambda m: _kind_sort_key(m[0]))
            entry: dict = {
                "id": tid,
                "summary": summary,
                "updated_at": updated_at,
                "folder_paths": folder_paths,
                "matches": matches,
            }
            if rank:
                score = sum(count * _kind_boost(k) for k, count in kind_counts.items())
                entry["_score"] = score
            results.append(entry)
            if not rank and len(results) >= limit:
                break

    if rank:
        # Sort by score desc, then by recency for ties.
        results.sort(key=lambda r: (r.get("_score", 0), r["updated_at"]), reverse=True)
        results = results[:limit]

    return results


def main():
    p = argparse.ArgumentParser(description="Search Zed agent threads.")
    p.add_argument("query", nargs="?", default=None,
                   help="keyword or substring to search for (optional if --show-profiles)")
    p.add_argument("--db", default=None,
                   help="path to threads.db (highest precedence; forces single-profile search even if multiple Zed instances active)")
    p.add_argument("--profile", "--user-data-dir", dest="profile", default=None,
                   help="Zed user-data-dir (profile root containing threads/); forces single-db at <profile>/threads/threads.db. Also honored via $ZED_USER_DATA_DIR. (autodetects otherwise)")
    p.add_argument("--show-profiles", action="store_true",
                   help="print the profile directory (or directories) that would be searched, one per line (or JSON array with --json), then exit 0. QUERY not required.")
    p.add_argument("--running", action="store_true",
                   help="print the command line of each running Zed editor process, one per line (or JSON array with --json), then exit. Exit 0 if any are running, 1 if none. QUERY not required.")
    p.add_argument("--limit", type=int, default=50, help="max threads to return (default: 50)")
    p.add_argument("--since", help="only threads with updated_at >= this (e.g. 2026-05-01)")
    p.add_argument("--folder", help="filter by folder_paths substring")
    p.add_argument("--case-sensitive", action="store_true", help="case-sensitive match (default: insensitive)")
    p.add_argument("--regex", action="store_true", help="treat query as a Python regex (default: literal substring)")
    p.add_argument("--context", type=int, default=80, help="chars of context around match (default: 80)")
    p.add_argument("--matches-per-thread", type=int, default=3,
                   help="max snippets shown per thread (0 = unlimited, default: 3)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    p.add_argument("--ids-only", action="store_true", help="print only matching thread IDs, one per line")
    p.add_argument("--rank", action="store_true", help="rank results by relevance (BM25-style field boosts) instead of recency")
    args = p.parse_args()

    if args.show_profiles:
        prof = getattr(args, "profile", None) or os.environ.get("ZED_USER_DATA_DIR")
        if prof:
            profs = [Path(prof).expanduser()]
        else:
            profs = get_active_profiles()
        # If --db was the only override, derive a profile dir from it for display (best effort)
        if not prof and args.db:
            dbp = Path(args.db).expanduser()
            if dbp.name == "threads.db" and dbp.parent.name == "threads":
                profs = [dbp.parent.parent]
        if args.json:
            json.dump([str(p) for p in profs], sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            for p in profs:
                print(p)
        return

    if args.running:
        # Reuse the guarded /proc detector so callers don't reinvent a
        # drift-prone `pgrep` pattern. (zed-thread-move relies on this.)
        cmdlines = [cmd for _flag, _dir, cmd in detect_running_zed_processes()]
        if args.json:
            json.dump(cmdlines, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            for c in cmdlines:
                print(c)
        sys.exit(0 if cmdlines else 1)

    if not args.query:
        print("error: query is empty (use --show-profiles to list autodetected profile(s) without a query)", file=sys.stderr)
        sys.exit(2)

    flags = 0 if args.case_sensitive else re.IGNORECASE
    pattern_src = args.query if args.regex else re.escape(args.query)
    try:
        pattern = re.compile(pattern_src, flags)
    except re.error as e:
        print(f"error: invalid regex: {e}", file=sys.stderr)
        sys.exit(2)

    db_paths = resolve_threads_dbs(args)

    # Surface what we are searching (always, quiet for single auto)
    explicit_single = bool(
        args.db
        or os.environ.get("ZED_THREADS_DB")
        or getattr(args, "profile", None)
        or os.environ.get("ZED_USER_DATA_DIR")
    )
    if not explicit_single:
        active = get_active_profiles()
        if len(active) > 1:
            print(f"zed-threads: considering {len(active)} profiles:", file=sys.stderr)
            for pp in active:
                print(f"  {pp}", file=sys.stderr)
        else:
            print(f"using profile: {active[0] if active else '?'}", file=sys.stderr)

    all_results = []
    for dbp in db_paths:
        if not dbp.exists():
            if len(db_paths) > 1:
                prof_dir = dbp.parent.parent
                print(f"warn: skipping missing db for profile {prof_dir}: {dbp}", file=sys.stderr)
                continue
            else:
                print(f"error: db not found: {dbp}", file=sys.stderr)
                sys.exit(2)

        res = search(
            db_path=dbp,
            pattern=pattern,
            limit=args.limit,
            since=args.since,
            folder=args.folder,
            context_len=args.context,
            matches_per_thread=args.matches_per_thread,
            rank=args.rank,
        )
        for r in res:
            if len(db_paths) > 1:
                r["profile"] = str(dbp.parent.parent)
            all_results.append(r)
        if len(all_results) >= args.limit:
            break

    # When multiple profiles are searched they often hold overlapping/copied
    # threads (same thread `id`). Dedup by id, keeping the first occurrence
    # (explicit profiles are searched first, so they win).
    if len(db_paths) > 1:
        seen_ids = set()
        deduped = []
        for r in all_results:
            if r["id"] in seen_ids:
                continue
            seen_ids.add(r["id"])
            deduped.append(r)
        all_results = deduped

    results = all_results

    if args.ids_only:
        for r in results:
            print(r["id"])
        return

    if args.json:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if not results:
        print("no matches")
        return

    # Text output: prefix with "profile: ..." header on change (only present in true multi case)
    current_profile = None
    for r in results:
        prof = r.get("profile")
        if prof is not None and prof != current_profile:
            if current_profile is not None:
                print()
            print(f"profile: {prof}")
            current_profile = prof
        print(f"{r['id']}  {r['updated_at']}  {r['folder_paths'] or '-'}")
        if args.rank:
            print(f"  score: {r.get('_score', 0):.1f}  {r['summary']}")
        else:
            print(f"  {r['summary']}")
        for kind, snippet in r["matches"]:
            print(f"  [{kind}] {snippet}")
        print()
    print(f"-- {len(results)} thread(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
