#!/usr/bin/env bash
set -euo pipefail

# check-advisories.sh
# Queries OSV.dev and GitHub Advisory Database for vulnerabilities
# affecting trunk tools. Flags items not yet in compromised-versions.md.
#
# Usage:
#   check-advisories.sh              # report only
#   check-advisories.sh --update     # report + update "Last updated" date

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
COMPROMISED_FILE="$SKILL_DIR/references/compromised-versions.md"
TODAY=$(date -u +%Y-%m-%d)

UPDATE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --update)  UPDATE=true; shift ;;
    --help|-h)
      echo "Usage: $(basename "$0") [--update] [--help]"
      echo ""
      echo "Check OSV.dev and GitHub Advisory Database for vulnerabilities"
      echo "affecting trunk tools. Flags items not in compromised-versions.md."
      echo ""
      echo "  --update   Update 'Last updated' date in compromised-versions.md"
      echo "  --help     Show this message"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Dependencies ──────────────────────────────────────────────

for dep in curl jq; do
  command -v "$dep" &>/dev/null || { echo "ERROR: $dep is required" >&2; exit 1; }
done

HAS_GH=false
command -v gh &>/dev/null && HAS_GH=true

# ── Tool Registry ────────────────────────────────────────────
# Format: name|osv_ecosystem|osv_package|gh_advisory_ecosystem
#
# OSV ecosystems: PyPI, npm, Go, crates.io, NuGet, Packagist, ...
# GH  ecosystems: pip, npm, go, rust, nuget, composer, ...
#
# Leave fields empty when the tool has no package registry presence.
# To add a tool: append a line following the same format.

TOOLS=(
  "checkov|PyPI|checkov|pip"
  "markdownlint|npm|markdownlint-cli|npm"
  "prettier|npm|prettier|npm"
  "shellcheck|||"
  "shfmt|Go|mvdan.cc/sh|go"
  "taplo|crates.io|taplo|rust"
  "trufflehog|Go|github.com/trufflesecurity/trufflehog|go"
  "yamllint|PyPI|yamllint|pip"
  "trivy|Go|github.com/aquasecurity/trivy|go"
)

SUPPLY_CHAIN_RE="malware|supply.chain|backdoor|compromis|malicious|credential.steal|exfiltrat|trojan"

# ── Known IDs (already documented) ───────────────────────────

KNOWN_IDS=$(grep -oE '(CVE-[0-9]+-[0-9]+|GHSA-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+)' \
  "$COMPROMISED_FILE" 2>/dev/null | sort -u || true)

is_known() { echo "$KNOWN_IDS" | grep -qxF "$1" 2>/dev/null; }

# ── Query helpers ─────────────────────────────────────────────

osv_query() {
  local eco=$1 pkg=$2
  [[ -z "$eco" || -z "$pkg" ]] && return
  curl -sf --max-time 15 -X POST "https://api.osv.dev/v1/query" \
    -H "Content-Type: application/json" \
    -d "{\"package\":{\"name\":\"${pkg}\",\"ecosystem\":\"${eco}\"}}" 2>/dev/null || true
}

gh_query() {
  local eco=$1 pkg=$2
  [[ "$HAS_GH" != true || -z "$eco" || -z "$pkg" ]] && return
  gh api "/advisories" -f ecosystem="$eco" -f affects="$pkg" -f per_page=100 2>/dev/null || true
}

# ── Main ──────────────────────────────────────────────────────

echo "=== Trunk Tool Advisory Check ==="
echo "Date: $TODAY"
echo "Source: OSV.dev$(${HAS_GH} && echo ", GitHub Advisory Database" || echo "")"
$HAS_GH || echo "Note: gh CLI not available — GitHub checks skipped"
echo ""

total_new=0

for entry in "${TOOLS[@]}"; do
  IFS='|' read -r name osv_eco osv_pkg gh_eco <<< "$entry"
  printf "  %-15s " "$name"
  findings=()

  # ── OSV.dev ──
  if [[ -n "$osv_eco" ]]; then
    json=$(osv_query "$osv_eco" "$osv_pkg")
    if [[ -n "$json" ]]; then
      while IFS=$'\t' read -r vid vsummary; do
        [[ -z "$vid" ]] && continue
        is_known "$vid" && continue

        # skip if any alias is already documented
        skip=false
        while IFS= read -r alias; do
          is_known "$alias" && { skip=true; break; }
        done < <(echo "$json" | jq -r ".vulns[] | select(.id==\"$vid\") | .aliases[]?" 2>/dev/null)
        $skip && continue

        tag=""
        echo "$vsummary" | grep -qiE "$SUPPLY_CHAIN_RE" && tag="⚠ SUPPLY-CHAIN "
        findings+=("${tag}[osv] ${vid}: ${vsummary}")
      done < <(echo "$json" | jq -r '.vulns[]? | [.id, .summary] | @tsv' 2>/dev/null)
    fi
  fi

  # ── GitHub Advisory Database ──
  if [[ -n "$gh_eco" && -n "$osv_pkg" && "$HAS_GH" == true ]]; then
    json=$(gh_query "$gh_eco" "$osv_pkg")
    if [[ -n "$json" ]]; then
      while IFS=$'\t' read -r ghsa_id gsummary gseverity gtype; do
        [[ -z "$ghsa_id" ]] && continue
        is_known "$ghsa_id" && continue

        tag=""
        [[ "$gtype" == "malware" ]] && tag="⚠ MALWARE "
        [[ "$gseverity" == "critical" ]] && tag="${tag}CRITICAL "
        findings+=("${tag}[gh] ${ghsa_id} (${gseverity}): ${gsummary}")
      done < <(echo "$json" | jq -r '.[]? | [.ghsa_id, .summary, .severity, .type] | @tsv' 2>/dev/null)
    fi
  fi

  count=${#findings[@]}
  if [[ $count -eq 0 ]]; then
    echo "✓ clean"
  else
    echo "⚠ ${count} new"
    for f in "${findings[@]}"; do echo "      $f"; done
    total_new=$((total_new + count))
  fi
done

echo ""
echo "── Summary ─────────────────────────"
echo "Tools checked : ${#TOOLS[@]}"
echo "New advisories: $total_new"

if [[ $total_new -gt 0 ]]; then
  echo ""
  echo "Items marked ⚠ SUPPLY-CHAIN or ⚠ MALWARE need immediate attention."
  echo "Review and add confirmed threats to:"
  echo "  $COMPROMISED_FILE"
fi

if [[ "$UPDATE" == true ]]; then
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/^Last updated:.*/Last updated: $TODAY/" "$COMPROMISED_FILE"
  else
    sed -i "s/^Last updated:.*/Last updated: $TODAY/" "$COMPROMISED_FILE"
  fi
  echo ""
  echo "Updated 'Last updated' → $TODAY in compromised-versions.md"
fi

echo ""
echo "Done."
