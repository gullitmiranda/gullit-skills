#!/usr/bin/env python3
"""
Strip gremlin/invisible Unicode characters from text files.
Replaces irregular spaces with U+0020, removes zero-width and control chars.
Usage: strip-gremlins.py [file ...]   (or stdin if no args).
"""

import sys
from pathlib import Path

BINARY_EXTENSIONS = frozenset(
    {
        ".db",
        ".sqlite",
        ".sqlite3",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".ico",
        ".webp",
        ".svg",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".zip",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".7z",
        ".rar",
        ".woff",
        ".woff2",
        ".ttf",
        ".otf",
        ".eot",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".o",
        ".a",
        ".pyc",
        ".pyo",
        ".class",
        ".jar",
        ".war",
        ".bin",
        ".dat",
        ".iso",
        ".img",
        ".mp3",
        ".mp4",
        ".wav",
        ".avi",
        ".mov",
        ".mkv",
        ".flac",
        ".ogg",
        ".wasm",
        ".pb",
        ".tfrecord",
        ".parquet",
        ".avro",
        ".lock",
    }
)

# Space-like: replace with normal space (U+0020)
SPACE_LIKE = (
    "\u00a0"  # NBSP
    "\u1680"  # Ogham space
    "\u180e"  # Mongolian vowel separator
    "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a"  # en quad..hair space
    "\u202f"  # Narrow no-break space
    "\u205f"  # Medium mathematical space
    "\u3000"  # Ideographic space
    "\ufeff"  # BOM
)

# Zero-width / control / separators: remove
REMOVE = (
    "\u00ad"  # Soft hyphen
    "\u200b\u200c\u200d\u2060\u2063"  # ZWSP, ZWNJ, ZWJ, word joiner, invisible separator
    "\u2028\u2029"  # Line separator, paragraph separator
    + "".join(
        chr(c) for c in range(0x20) if c not in (9, 10, 13)
    )  # Control except tab, LF, CR
    + "\u007f"  # DEL
)

TRANSLATE_TO_SPACE = str.maketrans({c: " " for c in SPACE_LIKE})
TRANSLATE_REMOVE = str.maketrans({c: "" for c in REMOVE})


def clean(s: str) -> str:
    s = s.translate(TRANSLATE_TO_SPACE)
    s = s.translate(TRANSLATE_REMOVE)
    return s


def main() -> None:
    if len(sys.argv) < 2:
        sys.stdout.write(clean(sys.stdin.read()))
        return

    for path in sys.argv[1:]:
        p = Path(path)
        if not p.exists():
            print(f"strip-gremlins: skip (not found): {path}", file=sys.stderr)
            continue
        if not p.is_file():
            print(f"strip-gremlins: skip (not a file): {path}", file=sys.stderr)
            continue
        if p.suffix.lower() in BINARY_EXTENSIONS:
            print(f"strip-gremlins: skip (binary): {path}", file=sys.stderr)
            continue
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"strip-gremlins: skip (read error): {path} — {e}", file=sys.stderr)
            continue
        out = clean(raw)
        if out != raw:
            p.write_text(out, encoding="utf-8", newline="")
            print(f"strip-gremlins: cleaned {path}")
        else:
            print(f"strip-gremlins: no change {path}")


if __name__ == "__main__":
    main()
