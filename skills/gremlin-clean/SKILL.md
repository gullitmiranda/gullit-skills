---
name: gremlin-clean
description: Strip gremlin/invisible Unicode characters from files. Use when linters report no-irregular-whitespace or when you suspect invisible characters in AI-generated text.
---

# Gremlin Clean

Strip gremlin/invisible Unicode characters from files.

## When to Use

- Linter reports `no-irregular-whitespace` or similar
- Invisible characters suspected in AI-generated text
- File content looks correct but tooling fails on hidden characters

## Procedure

1. **Target**: use the path(s) provided by the user, or the currently focused/last-edited file
2. **Run**: `python3 <skill-dir>/scripts/strip-gremlins.py <path> [path ...]`
3. **Report**: state which files were cleaned or had no change

## What It Does

- Replaces irregular space-like characters (NBSP, en/em spaces, ideographic space, etc.) with standard U+0020
- Removes zero-width characters (ZWSP, ZWNJ, ZWJ, word joiner, invisible separator)
- Removes control characters (except tab, LF, CR)
- Removes line/paragraph separators
- Skips binary files automatically
