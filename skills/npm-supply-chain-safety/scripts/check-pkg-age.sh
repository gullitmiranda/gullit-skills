#!/usr/bin/env bash
# check-pkg-age.sh — minimum-release-age guard for npm packages
#
# Usage:
#   check-pkg-age.sh <package>[@version]
#   check-pkg-age.sh @tanstack/react-router 1.169.1
#   check-pkg-age.sh react-router@latest
#
# Exit codes:
#   0 = LOW risk (>= 7 days old)
#   1 = MEDIUM risk (< 7 days, >= 24h)
#   2 = HIGH risk (< 24h)
#   3 = ERROR (could not determine age)

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

# Parse args: supports "pkg version" or "pkg@version"
if [[ "$#" -eq 2 ]]; then
  PKG="$1"
  VERSION="$2"
elif [[ "$#" -eq 1 ]]; then
  if [[ "$1" == *"@"* && "$1" != @* ]]; then
    # e.g. react-router@1.0.0
    PKG="${1%@*}"
    VERSION="${1##*@}"
  elif [[ "$1" == @*"@"* ]]; then
    # e.g. @tanstack/react-router@1.0.0 (scoped pkg with version)
    PKG="${1%@*}"
    VERSION="${1##*@}"
  else
    PKG="$1"
    VERSION="latest"
  fi
else
  echo "Usage: $0 <package>[@version]"
  echo "       $0 <package> <version>"
  exit 3
fi

# Resolve 'latest' to actual version
if [[ "$VERSION" == "latest" || "$VERSION" == "*" ]]; then
  VERSION=$(npm view "${PKG}" version 2>/dev/null || echo "")
  if [[ -z "$VERSION" ]]; then
    echo -e "${RED}ERROR${NC}: could not resolve latest version for ${PKG}" >&2
    exit 3
  fi
fi

echo -e "${BOLD}Checking publish age for ${PKG}@${VERSION}${NC}"

# Get the publish timestamp for this specific version
# Note: npm view's dot-notation can't handle version numbers with dots,
# so we fetch the full time object as JSON and extract via jq.
PUBLISHED=$(npm view "${PKG}@${VERSION}" --json 2>/dev/null | jq -r --arg v "${VERSION}" '.time[$v] // empty' 2>/dev/null || echo "")

if [[ -z "$PUBLISHED" ]]; then
  echo -e "${RED}ERROR${NC}: could not determine publish date — package or version may not exist" >&2
  exit 3
fi

NOW=$(date -u +%s)

# Parse date — supports both macOS (BSD) and Linux (GNU)
if date -j > /dev/null 2>&1; then
  # macOS/BSD date
  PUB=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${PUBLISHED:0:19}" "+%s" 2>/dev/null || echo "")
else
  # GNU date (Linux)
  PUB=$(date -d "${PUBLISHED}" +%s 2>/dev/null || echo "")
fi

if [[ -z "$PUB" ]]; then
  echo -e "${RED}ERROR${NC}: could not parse publish date: ${PUBLISHED}" >&2
  exit 3
fi

AGE_SECONDS=$(( NOW - PUB ))
AGE_HOURS=$(( AGE_SECONDS / 3600 ))
AGE_DAYS=$(( AGE_HOURS / 24 ))

echo "Published: ${PUBLISHED}"
echo "Age:       ${AGE_DAYS}d ${AGE_HOURS}h"

if [[ "$AGE_HOURS" -lt 24 ]]; then
  echo -e "Risk:      ${RED}${BOLD}HIGH${NC} — published less than 24h ago"
  echo "Action:    DO NOT install. Wait at least 24-72h and verify with: socket npm install ${PKG}@${VERSION}"
  exit 2
elif [[ "$AGE_DAYS" -lt 7 ]]; then
  echo -e "Risk:      ${YELLOW}${BOLD}MEDIUM${NC} — published less than 7 days ago"
  echo "Action:    Run socket check first: socket npm install ${PKG}@${VERSION}"
  exit 1
else
  echo -e "Risk:      ${GREEN}${BOLD}LOW${NC} — ${AGE_DAYS} days old"
  exit 0
fi
