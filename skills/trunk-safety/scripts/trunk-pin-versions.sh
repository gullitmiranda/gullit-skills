#!/usr/bin/env bash
set -euo pipefail

TRUNK_YAML=".trunk/trunk.yaml"

if [[ ! -f "$TRUNK_YAML" ]]; then
  echo "ERROR: $TRUNK_YAML not found. Run 'trunk init' first." >&2
  exit 1
fi

echo "=== Pinning versions in $TRUNK_YAML ==="
echo ""

cp "$TRUNK_YAML" "${TRUNK_YAML}.bak"

# Match lines like "    - tool@1.2.3" that don't already end with "!"
# Handles versions with dots, hyphens, and alphanumerics (e.g., 3.2.513, 1.0.0-beta.1)
if sed --version 2>/dev/null | grep -q GNU; then
  # GNU sed (Linux)
  sed -i -E 's/(- [a-zA-Z0-9_-]+@[0-9][0-9a-zA-Z._-]*)$/\1!/' "$TRUNK_YAML"
else
  # BSD sed (macOS)
  sed -i '' -E 's/(- [a-zA-Z0-9_-]+@[0-9][0-9a-zA-Z._-]*)$/\1!/' "$TRUNK_YAML"
fi

echo "Changes:"
diff "${TRUNK_YAML}.bak" "$TRUNK_YAML" || true
echo ""

pinned=$(grep -cE '@[0-9][0-9a-zA-Z._-]*!' "$TRUNK_YAML" || echo "0")
echo "Pinned $pinned version(s) with '!' suffix."

rm -f "${TRUNK_YAML}.bak"
echo "Done."
