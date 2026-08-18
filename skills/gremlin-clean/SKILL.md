---
name: gremlin-clean
description: Strip gremlin/invisible Unicode characters from files. Corrective cleanup of
existing files — `quality` governs not generating them; `deslop` cleans up
visible AI slop in prose and comments. Use when linters report no-irregular-whitespace or when you suspect invisible characters in AI-generated text.
---

# Gremlin Clean

Strip gremlin/invisible Unicode characters from files. Corrective cleanup of
existing files — `quality` governs not generating them; `deslop` cleans up
visible AI slop in prose and comments.

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

## What It Does NOT Do

The script intentionally leaves typographic dashes (U+2013 en dash, U+2014 em
dash) untouched — they are valid Unicode in legitimate prose. If the user
reports them as gremlins (common in AI-generated Markdown tables or range
notation in infrastructure code), replace them manually:

```bash
python3 -c "
import sys; p = sys.argv[1]
open(p,'w').write(open(p).read().replace('\u2014','-').replace('\u2013','-'))
" <file>
```
