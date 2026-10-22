#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""zed-thread-move: safely move/import Zed agent threads between projects.

Two phases:
  plan    read-only: discover threads, verify counts, print a JSON plan
  apply   execute a plan JSON produced by `plan` (backup + atomic writes + audit)

See SKILL.md for the recipe a calling agent should follow.
"""
import argparse
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

# Lowest-common-denominator sidebar columns (present in every observed Zed
# migration version). title_override exists in newer 0-dev but NOT older
# 0-stable, so it is deliberately excluded from inserts.
SIDEBAR_LCD_COLS = [
    "thread_id", "session_id", "agent_id", "title", "updated_at", "created_at",
    "folder_paths", "folder_paths_order", "archived",
    "main_worktree_paths", "main_worktree_paths_order",
    "remote_connection", "interacted_at",
]


# Profile autodetection is owned by the sibling `zed-threads` skill, which has
# the robust implementation (/proc cmdline parsing + guards against other apps
# that also accept --user-data-dir). These two skills always ship together, so
# we shell out to its `search.py --show-profiles` rather than duplicating that
# logic here. See ../../zed-threads/scripts/search.py.
SEARCH_PY = (Path(__file__).resolve().parent.parent.parent
             / "zed-threads" / "scripts" / "search.py")


def detect_active_profile():
    """Return the autodetected Zed profile dir (str), or None.

    Delegates to zed-threads's `search.py --show-profiles --json`, which returns
    one or more active profile dirs (most-relevant first). We take the first.
    """
    if not SEARCH_PY.exists():
        print(f"WARN: cannot find sibling detector: {SEARCH_PY}", file=sys.stderr)
        return None
    try:
        out = subprocess.run(
            [sys.executable, str(SEARCH_PY), "--show-profiles", "--json"],
            capture_output=True, text=True, check=True).stdout
        profiles = json.loads(out)
    except Exception as e:
        print(f"WARN: profile autodetect via search.py failed: {e}", file=sys.stderr)
        return None
    return profiles[0] if profiles else None


def profile_paths(profile):
    """Return existing DB paths for a profile. 0-stable is optional."""
    base = Path(profile)
    candidates = {
        "threads": base / "threads" / "threads.db",
        "dev": base / "db" / "0-dev" / "db.sqlite",
        "stable": base / "db" / "0-stable" / "db.sqlite",
    }
    return {k: v for k, v in candidates.items() if v.exists()}


def connect_ro(path):
    # NEVER use immutable=1: it ignores the WAL of a running Zed and returns
    # stale main-file state.
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_columns(path, table):
    conn = connect_ro(path)
    try:
        return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
    finally:
        conn.close()


def zed_running():
    """Return matching process lines if Zed appears to be running.

    Delegates to zed-threads's `search.py --running`, which uses the guarded
    /proc detector (correctly matches a `.../zed` binary, not just
    `/zed-editor` or `./zed`). Fails safe: if the detector is unavailable or
    errors, assumes Zed IS running rather than silently skipping the guard
    against writing to a live DB.
    """
    if not SEARCH_PY.exists():
        print(f"WARN: cannot find sibling detector: {SEARCH_PY}", file=sys.stderr)
        return [f"detector unavailable ({SEARCH_PY} not found) - assuming Zed "
                "may be running; quit Zed and retry, or pass --profile explicitly"]
    try:
        out = subprocess.run(
            [sys.executable, str(SEARCH_PY), "--running", "--json"],
            capture_output=True, text=True).stdout
        return json.loads(out) if out.strip() else []
    except Exception as e:
        print(f"WARN: zed-running check via search.py failed: {e}", file=sys.stderr)
        return [f"detector failed ({e}) - assuming Zed may be running; quit "
                "Zed and retry"]


# --------------------------------------------------------------------------
# Thread resolution
# --------------------------------------------------------------------------

def all_threads(threads_db):
    """Every root thread (parent_id NULL) with its sidebar archived flag."""
    conn = connect_ro(threads_db)
    try:
        rows = conn.execute(
            "SELECT id, summary, folder_paths, parent_id, updated_at "
            "FROM threads WHERE parent_id IS NULL OR parent_id=''"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def archived_map(dev_db):
    """session_id -> archived flag, from the 0-dev sidebar (the live one)."""
    if dev_db is None:
        return {}
    conn = connect_ro(dev_db)
    try:
        return {r["session_id"]: r["archived"]
                for r in conn.execute(
                    "SELECT session_id, archived FROM sidebar_threads")}
    finally:
        conn.close()


def threads_in_folder(threads_db, folder):
    """Root threads whose folder_paths exactly equals `folder`."""
    return [t for t in all_threads(threads_db) if t["folder_paths"] == folder]


def match_threads_by_title(threads_db, query):
    """Case-insensitive substring match against summary. Returns (exact, fuzzy).

    exact: summary equals query (case-insensitive)
    fuzzy: summary contains query as a substring (case-insensitive)
    """
    q = query.strip().lower()
    exact, fuzzy = [], []
    for t in all_threads(threads_db):
        s = (t["summary"] or "").lower()
        if s == q:
            exact.append(t)
        elif q in s:
            fuzzy.append(t)
    return exact, fuzzy


# --------------------------------------------------------------------------
# Plan building
# --------------------------------------------------------------------------

class PlanError(Exception):
    """Raised when the agent must stop and ask the user for clarification."""


def build_plan(dest_profile, source_profile, dest_folder,
               from_folder=None, titles=None, expect_count=None):
    """Resolve which threads to move and return a plan dict.

    Raises PlanError (with a human-readable message) when the agent must
    stop and ask the user. The calling agent should surface that message
    verbatim and NOT proceed.
    """
    titles = titles or []
    src_dbs = profile_paths(source_profile)
    dst_dbs = profile_paths(dest_profile)
    if "threads" not in src_dbs:
        raise PlanError(f"source profile has no threads.db: {source_profile}")
    if "threads" not in dst_dbs:
        raise PlanError(f"dest profile has no threads.db: {dest_profile}")

    src_threads_db = src_dbs["threads"]
    arch = archived_map(src_dbs.get("dev"))

    selected = []
    if from_folder is not None:
        selected = threads_in_folder(src_threads_db, from_folder)
        if not selected:
            raise PlanError(
                f"No threads found in source folder {from_folder!r}. "
                f"Check the exact folder_paths value (run `env` / list folders).")
    else:
        for query in titles:
            exact, fuzzy = match_threads_by_title(src_threads_db, query)
            if len(exact) == 1 and not fuzzy:
                # Unambiguous: exactly one exact match, no other near-matches.
                selected.append(exact[0])
            elif len(exact) == 1 and fuzzy:
                # An exact match exists, but so do other substring matches.
                # For short/ambiguous queries this is risky - surface all and
                # let the user disambiguate (they may have meant a longer one).
                raise PlanError(
                    f"{query!r} exactly matches one thread, but {len(fuzzy)} "
                    "other thread(s) also contain that text:\n"
                    "  EXACT:\n" + _fmt_matches(exact)
                    + "\n  ALSO CONTAINING:\n" + _fmt_matches(fuzzy)
                    + "\nConfirm which one (or pass a more specific title).")
            elif len(exact) > 1:
                raise PlanError(_ambiguous_msg(query, exact, "exact"))
            elif len(fuzzy) == 1:
                # one near-match: confirm with user, don't assume
                raise PlanError(
                    f"No thread titled exactly {query!r}. One similar match:\n"
                    + _fmt_matches(fuzzy)
                    + "\nConfirm this is the intended thread before moving.")
            elif len(fuzzy) > 1:
                raise PlanError(_ambiguous_msg(query, fuzzy, "similar"))
            else:
                raise PlanError(
                    f"No thread matches {query!r} (no exact or similar title). "
                    f"Ask the user to re-check the title.")

    # Deduplicate by id (a title query could overlap a folder selection)
    by_id = {t["id"]: t for t in selected}
    selected = list(by_id.values())

    # Count verification (hard stop). expect_count is the user's VISIBLE
    # (non-archived) count - that's what they see in the sidebar. But a
    # folder/title selection moves ALL matched threads, including archived
    # ones the user can't see. So we hard-stop whenever the TOTAL to be
    # moved differs from what the user expects, and explain the archived
    # delta. This is the "/code/sandboxes looks like 3 but is really 4"
    # case: the user must consciously accept moving the hidden one too.
    archived_sel = [t for t in selected if arch.get(t["id"], 0)]
    visible_sel = [t for t in selected if not arch.get(t["id"], 0)]
    if expect_count is not None and len(selected) != expect_count:
        raise PlanError(
            f"COUNT MISMATCH (hard stop). You expected {expect_count} "
            f"thread(s); the selection actually contains {len(selected)} "
            f"({len(visible_sel)} visible + {len(archived_sel)} archived). "
            f"Archived threads are hidden from the sidebar, which is likely "
            f"why your count looked short.\n"
            + _fmt_matches(selected, arch)
            + "\nConfirm with the user whether to move all of them "
            "(re-run plan with --expect-count set to the TOTAL, or drop it).")

    source_folders = sorted({(t["folder_paths"] or "(none)") for t in selected})
    return {
        "dest_profile": str(dest_profile),
        "source_profile": str(source_profile),
        "cross_profile": str(dest_profile) != str(source_profile),
        "dest_folder": dest_folder,
        "source_folders": source_folders,
        "thread_ids": [t["id"] for t in selected],
        "threads": [
            {"id": t["id"], "summary": t["summary"],
             "from": t["folder_paths"] or "(none)",
             "archived": bool(arch.get(t["id"], 0))}
            for t in selected
        ],
        "counts": {"visible": len(visible_sel),
                   "archived": len(archived_sel),
                   "total": len(selected)},
    }


def _fmt_matches(threads, arch=None):
    lines = []
    for t in threads:
        flag = ""
        if arch is not None:
            flag = " [archived]" if arch.get(t["id"], 0) else ""
        folder = t["folder_paths"] or "(none)"
        lines.append(f"  {t['id'][:8]}  {folder}  {t['summary']}{flag}")
    return "\n".join(lines)


def _ambiguous_msg(query, threads, kind):
    return (f"AMBIGUOUS: {len(threads)} {kind} matches for {query!r}:\n"
            + _fmt_matches(threads)
            + "\nAsk the user which one (or pass the exact thread id).")


# --------------------------------------------------------------------------
# Apply (write phase)
# --------------------------------------------------------------------------

def backup_zip(dbs, backup_dir):
    """Zip all DBs into <backup_dir>/<YYYY-MM-DD_HH-MM>.zip. Returns the path."""
    import shutil
    import tempfile
    from datetime import datetime
    if shutil.which("zip") is None:
        raise RuntimeError("'zip' not found (install: sudo apt install zip)")
    bdir = Path(backup_dir)
    bdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_path = bdir / f"{stamp}.zip"
    if zip_path.exists():
        raise RuntimeError(f"backup already exists: {zip_path} "
                           "(wait a minute or remove it)")
    tmp = Path(tempfile.mkdtemp())
    try:
        names = {"threads": "threads.db", "dev": "0-dev_db.sqlite",
                 "stable": "0-stable_db.sqlite"}
        staged = []
        for key, path in dbs.items():
            dest = tmp / names[key]
            shutil.copy2(path, dest)
            staged.append(dest.name)
        subprocess.run(["zip", "-q", str(zip_path), *staged],
                       cwd=tmp, check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return zip_path


def quiesce(path):
    conn = sqlite3.connect(str(path))
    try:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        conn.close()


def apply_plan(plan, backup_dir, backfill_interacted=True, force=False):
    """Execute a plan dict. Returns an audit dict. Refuses if Zed is running,
    unless force is True."""
    running = zed_running()
    if running and not force:
        raise RuntimeError("Zed is running - quit it first, or pass --force. "
                           "Matched:\n" + "\n".join(running))

    dest_profile = plan["dest_profile"]
    source_profile = plan["source_profile"]
    dest_folder = plan["dest_folder"]
    thread_ids = plan["thread_ids"]
    cross = plan["cross_profile"]

    dst = profile_paths(dest_profile)
    src = profile_paths(source_profile)

    # 1. Backup destination DBs.
    zip_path = backup_zip(dst, backup_dir)

    # 2. Quiesce destination DBs.
    for p in dst.values():
        quiesce(p)

    # 3. Mutate.
    if cross:
        _apply_cross_profile(src, dst, dest_folder, thread_ids, backfill_interacted)
    else:
        _apply_same_profile(dst, dest_folder, thread_ids, backfill_interacted)

    # 4. Audit.
    audit = _audit(dst, dest_folder, thread_ids)
    audit["backup"] = str(zip_path)
    return audit


def _id_list_sql(thread_ids):
    """Return a safely-quoted SQL IN-list for thread/session ids (UUIDs)."""
    # IDs are Zed UUIDs (hex + hyphen); validate to be safe then inline.
    safe = []
    for tid in thread_ids:
        if not re.fullmatch(r"[0-9a-fA-F-]{36}", tid):
            raise RuntimeError(f"refusing unexpected thread id: {tid!r}")
        safe.append(f"'{tid}'")
    return "(" + ",".join(safe) + ")"


def _apply_same_profile(dst, dest_folder, thread_ids, backfill):
    """Same-profile move: set folder_paths in threads.db + both sidebars.

    For sidebars we UPDATE existing rows AND INSERT any missing ones
    (synthesized from threads.db). Missing rows happen when a thread was
    only ever opened in one build (e.g. dev), so the other build's sidebar
    (e.g. 0-stable) never created a row for it. Without the INSERT, the
    audit would show a count short of expected for that sidebar.
    """
    idlist = _id_list_sql(thread_ids)
    df = dest_folder.replace("'", "''")
    threads_db = str(dst["threads"]).replace("'", "''")
    cols = ", ".join(SIDEBAR_LCD_COLS)

    conn = sqlite3.connect(str(dst["threads"]))
    try:
        conn.execute("BEGIN")
        conn.execute(
            f"UPDATE threads SET folder_paths='{df}', folder_paths_order='0' "
            f"WHERE id IN {idlist}")
        conn.commit()
    finally:
        conn.close()

    for key in ("dev", "stable"):
        if key not in dst:
            continue
        conn = sqlite3.connect(str(dst[key]))
        try:
            conn.execute("BEGIN")
            # Move rows that already exist in this sidebar.
            conn.execute(
                f"UPDATE sidebar_threads SET folder_paths='{df}', "
                f"folder_paths_order='0', main_worktree_paths='{df}', "
                f"main_worktree_paths_order='0' WHERE session_id IN {idlist}")
            # Insert any selected threads missing from this sidebar,
            # synthesized from threads.db.
            conn.execute(f"ATTACH '{threads_db}' AS st")
            conn.execute(
                f"INSERT INTO sidebar_threads ({cols}) "
                "SELECT randomblob(16), t.id, NULL, t.summary, "
                f"t.updated_at, t.created_at, '{df}', '0', 0, '{df}', '0', "
                "NULL, t.updated_at FROM st.threads t "
                f"WHERE t.id IN {idlist} "
                "AND NOT EXISTS (SELECT 1 FROM sidebar_threads d "
                "WHERE d.session_id=t.id)")
            if backfill:
                conn.execute(
                    "UPDATE sidebar_threads SET interacted_at=updated_at "
                    "WHERE (interacted_at IS NULL OR interacted_at='') "
                    f"AND session_id IN {idlist}")
            conn.commit()
            conn.execute("DETACH st")
        finally:
            conn.close()


def _apply_cross_profile(src, dst, dest_folder, thread_ids, backfill):
    """Cross-profile import: copy thread rows + synthesize sidebar rows.

    Uses LCD sidebar columns (no title_override). Idempotent: INSERT OR
    IGNORE on threads (PK=id), WHERE NOT EXISTS on sidebars (PK is a fresh
    randomblob, so dedupe on session_id instead).
    """
    idlist = _id_list_sql(thread_ids)
    df = dest_folder.replace("'", "''")
    src_threads = str(src["threads"]).replace("'", "''")

    # 1. Copy thread rows into dest threads.db, overriding folder_paths.
    conn = sqlite3.connect(str(dst["threads"]))
    try:
        conn.execute("BEGIN")
        conn.execute(f"ATTACH '{src_threads}' AS src")
        conn.execute(
            "INSERT OR IGNORE INTO threads "
            "(id, summary, updated_at, data_type, data, parent_id, "
            " folder_paths, folder_paths_order, created_at) "
            f"SELECT id, summary, updated_at, data_type, data, parent_id, "
            f"'{df}', '0', created_at FROM src.threads WHERE id IN {idlist}")
        conn.commit()
        conn.execute("DETACH src")
    finally:
        conn.close()

    # 2. Sidebar rows. If the source has a 0-dev sidebar, copy its rows
    #    (LCD cols); else synthesize from threads.db. Insert into every
    #    dest sidebar.
    src_dev = src.get("dev")
    cols = ", ".join(SIDEBAR_LCD_COLS)
    for key in ("dev", "stable"):
        if key not in dst:
            continue
        conn = sqlite3.connect(str(dst[key]))
        try:
            conn.execute("BEGIN")
            if src_dev is not None:
                src_dev_s = str(src_dev).replace("'", "''")
                conn.execute(f"ATTACH '{src_dev_s}' AS sdev")
                conn.execute(
                    f"INSERT INTO sidebar_threads ({cols}) "
                    "SELECT randomblob(16), s.session_id, s.agent_id, s.title, "
                    "s.updated_at, s.created_at, "
                    f"'{df}', '0', s.archived, '{df}', '0', "
                    "s.remote_connection, "
                    "COALESCE(NULLIF(s.interacted_at,''), s.updated_at) "
                    "FROM sdev.sidebar_threads s "
                    f"WHERE s.session_id IN {idlist} "
                    "AND NOT EXISTS (SELECT 1 FROM sidebar_threads d "
                    "WHERE d.session_id=s.session_id)")
                conn.commit()
                conn.execute("DETACH sdev")
            else:
                src_threads_s = src_threads
                conn.execute(f"ATTACH '{src_threads_s}' AS st")
                conn.execute(
                    f"INSERT INTO sidebar_threads ({cols}) "
                    "SELECT randomblob(16), t.id, NULL, t.summary, "
                    f"t.updated_at, t.created_at, '{df}', '0', 0, '{df}', '0', "
                    "NULL, t.updated_at FROM st.threads t "
                    f"WHERE t.id IN {idlist} "
                    "AND NOT EXISTS (SELECT 1 FROM sidebar_threads d "
                    "WHERE d.session_id=t.id)")
                conn.commit()
                conn.execute("DETACH st")
        finally:
            conn.close()


def _audit(dst, dest_folder, thread_ids):
    """Return per-DB counts of the moved threads at the dest folder."""
    idlist = _id_list_sql(thread_ids)
    df = dest_folder.replace("'", "''")
    result = {"dest_folder": dest_folder, "per_db": {}, "moved": []}
    # threads.db: counts + titles of what actually landed at the dest.
    conn = connect_ro(dst["threads"])
    try:
        rows = conn.execute(
            f"SELECT id, summary FROM threads "
            f"WHERE id IN {idlist} AND folder_paths='{df}' "
            "ORDER BY updated_at DESC").fetchall()
        result["moved"] = [{"id": r["id"], "summary": r["summary"]} for r in rows]
        result["per_db"]["threads"] = len(rows)
    finally:
        conn.close()
    for key in ("dev", "stable"):
        if key not in dst:
            continue
        conn = connect_ro(dst[key])
        try:
            n = conn.execute(
                f"SELECT COUNT(*) FROM sidebar_threads "
                f"WHERE session_id IN {idlist} AND folder_paths='{df}'"
            ).fetchone()[0]
            result["per_db"][key] = n
        finally:
            conn.close()
    result["expected"] = len(thread_ids)
    return result


def main():
    parser = argparse.ArgumentParser(prog="zed-thread-move")
    parser.add_argument("--profile", help="Zed user-data-dir (default: autodetect)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("env", help="print detected profile + DB inventory")

    # plan: resolve threads to move and emit a JSON plan (read-only).
    p_plan = sub.add_parser("plan", help="read-only: build a move plan")
    p_plan.add_argument("--dest", required=True,
                        help="destination folder_paths (e.g. /3t/e/prg/sandboxes)")
    g = p_plan.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-folder",
                   help="move ALL threads in this source folder_paths")
    g.add_argument("--title", action="append", default=[],
                   help="match a thread by title (repeatable for multiple)")
    p_plan.add_argument("--expect-count", type=int,
                        help="user's claimed visible (non-archived) count; "
                             "hard-stops on mismatch")
    p_plan.add_argument("--source-profile",
                        help="cross-profile import: OLD Zed user-data-dir to pull "
                             "threads FROM (default: same as --profile)")
    p_plan.add_argument("--out", help="write plan JSON to this path")

    # apply: execute a plan JSON (write phase).
    p_apply = sub.add_parser("apply", help="execute a plan JSON (writes!)")
    p_apply.add_argument("--plan-file", required=True,
                         help="path to a plan JSON produced by `plan --out`")
    p_apply.add_argument("--backup-dir", required=True,
                         help="directory for the timestamped backup zip")
    p_apply.add_argument("--no-backfill", action="store_true",
                         help="skip the interacted_at backfill")
    p_apply.add_argument("--force", action="store_true",
                         help="apply even if Zed appears to be running "
                              "(or the running-check couldn't be performed)")

    args = parser.parse_args()
    profile = args.profile or detect_active_profile()
    if not profile:
        print("FATAL: could not detect Zed profile; pass --profile", file=sys.stderr)
        return 2

    if args.cmd == "env":
        dbs = profile_paths(profile)
        print(f"profile: {profile}")
        for k, v in dbs.items():
            cols = table_columns(v, "sidebar_threads" if k != "threads" else "threads")
            print(f"  {k:7} {v}  ({len(cols)} cols)")
        running = zed_running()
        print(f"zed_running: {bool(running)}")
        return 0

    if args.cmd == "plan":
        source_profile = args.source_profile or profile
        try:
            plan = build_plan(
                dest_profile=profile,
                source_profile=source_profile,
                dest_folder=args.dest,
                from_folder=args.from_folder,
                titles=args.title,
                expect_count=args.expect_count,
            )
        except PlanError as e:
            print("STOP_AND_ASK", file=sys.stderr)
            print(str(e), file=sys.stderr)
            return 3

        text = json.dumps(plan, indent=2)
        if args.out:
            Path(args.out).write_text(text)
        # Human summary to stderr; machine JSON to stdout.
        c = plan["counts"]
        print(f"PLAN OK: move {c['total']} thread(s) "
              f"({c['visible']} visible + {c['archived']} archived)",
              file=sys.stderr)
        print(f"  from: {', '.join(plan['source_folders'])}", file=sys.stderr)
        print(f"  to:   {plan['dest_folder']}", file=sys.stderr)
        print(f"  cross-profile: {plan['cross_profile']}", file=sys.stderr)
        for t in plan["threads"]:
            flag = " [archived]" if t["archived"] else ""
            print(f"    {t['id'][:8]}  {t['summary']}{flag}", file=sys.stderr)
        if args.out:
            print(f"  plan written to {args.out}", file=sys.stderr)
        print(text)
        return 0

    if args.cmd == "apply":
        plan = json.loads(Path(args.plan_file).read_text())
        try:
            audit = apply_plan(plan, args.backup_dir,
                               backfill_interacted=not args.no_backfill,
                               force=args.force)
        except RuntimeError as e:
            print("APPLY FAILED:", e, file=sys.stderr)
            return 4
        exp = audit["expected"]
        ok = all(v == exp for v in audit["per_db"].values())
        print(f"APPLIED. backup: {audit['backup']}", file=sys.stderr)
        print(f"  dest: {audit['dest_folder']}  expected {exp} per DB",
              file=sys.stderr)
        for t in audit["moved"]:
            print(f"    - {t['summary']}", file=sys.stderr)
        for k, v in audit["per_db"].items():
            mark = "OK" if v == exp else "MISMATCH"
            print(f"    {k:7} {v}  [{mark}]", file=sys.stderr)
        print(json.dumps(audit, indent=2))
        return 0 if ok else 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
