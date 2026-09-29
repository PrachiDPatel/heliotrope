#!/usr/bin/env bash
# check-secrets.sh — secret/PII scan for Heliotrope merge reviews.
# Usage: ./scripts/check-secrets.sh [git-rev-range]
#   No arg  -> scans staged changes + tracked files.
#   "main...HEAD" -> scans the branch diff (coordinator merge review).
# Exit 0 = clean, 1 = findings.
set -u
cd "$(dirname "$0")/.."

PATTERNS="scripts/secret-patterns.txt"
RANGE="${1:-}"
FAIL=0

# Build a clean patterns file (strip comments/blank lines, and the slack-token line
# has a stray trailing space issue avoided by using fixed patterns below).
TMP_PATTERNS="$(mktemp)"
grep -vE '^\s*(#|$)' "$PATTERNS" | sed 's/[[:space:]]*$//' | grep -v 'xox\[bap\]- $' > "$TMP_PATTERNS"
printf 'xox[bap]-[A-Za-z0-9-]{10,}\n' >> "$TMP_PATTERNS"

if [ -n "$RANGE" ]; then
  LABEL="diff $RANGE"
  DIFF_TEXT=$(git diff "$RANGE" -- . ':!scripts/secret-patterns.txt' ':!scripts/check-secrets.sh')
else
  LABEL="staged"
  DIFF_TEXT=$(git diff --cached -- . ':!scripts/secret-patterns.txt' ':!scripts/check-secrets.sh')
fi
HITS=$(printf '%s\n' "$DIFF_TEXT" | grep -E -n -f "$TMP_PATTERNS" || true)
if [ -n "$HITS" ]; then
  echo "FAIL [$LABEL] pattern hits:"; echo "$HITS"; FAIL=1
else
  echo "ok [$LABEL] no pattern hits"
fi

# Tracked files that should never be in git.
BAD_TRACKED=$(git ls-files | grep -Ei '\.(pem|key|p12|pfx|sqlite3?|db)$|seed\.local|\.env$|\.dev\.vars|(^|/)test-results/|(^|/)playwright-report/' || true)
if [ -n "$BAD_TRACKED" ]; then
  echo "FAIL [tracked] sensitive paths in git:"; echo "$BAD_TRACKED"; FAIL=1
else
  echo "ok [tracked] no sensitive paths tracked"
fi

# .gitignore still ignores the sensitive names (protections not weakened).
for p in .env .dev.vars .wrangler/state key.pem data.sqlite test-results/x; do
  git check-ignore -q "$p" || { echo "FAIL [gitignore] not ignored: $p"; FAIL=1; }
done
echo "ok [gitignore] sensitive names ignored"

rm -f "$TMP_PATTERNS"
[ "$FAIL" -eq 0 ] && echo "PASS: clean" || echo "FAIL: findings above"
exit "$FAIL"
