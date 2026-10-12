#!/usr/bin/env bash
# Privacy scrub: fail if any repo file contains a term from the maintainer's PRIVATE term list.
#
# The term list never lives in this repo (it contains exactly the names it protects).
#   Local:  ~/.config/ai-kickstart/scrub-terms.txt  (override with AI_KICKSTART_SCRUB_TERMS=<path>)
#   CI:     SCRUB_PATTERN env var (from a repository secret), one ERE with terms joined by "|"
#
# Usage: scripts/scrub.sh [--optional]
#   --optional  exit 0 with a warning when no term list is available (used in CI and for contributors)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

optional=false
[[ "${1:-}" == "--optional" ]] && optional=true

terms_file="${AI_KICKSTART_SCRUB_TERMS:-$HOME/.config/ai-kickstart/scrub-terms.txt}"
if [[ -n "${SCRUB_PATTERN:-}" ]]; then
  pattern="$SCRUB_PATTERN"
elif [[ -f "$terms_file" ]]; then
  pattern="$(grep -vE '^[[:space:]]*(#|$)' "$terms_file" | paste -sd'|' -)"
else
  if $optional; then
    echo "scrub: WARNING no term list ($terms_file) and no SCRUB_PATTERN; skipped." >&2
    exit 0
  fi
  echo "scrub: no term list at $terms_file and no SCRUB_PATTERN set." >&2
  exit 2
fi

# Normalise: newlines/CRs become alternations, empty alternatives are dropped.
# (A secret pasted via pbcopy ends with a newline; GNU grep treats that as an extra
#  empty pattern that matches every line.)
pattern="$(printf '%s' "$pattern" | tr '\r\n' '||' | sed -E 's/\|+/|/g; s/^\|//; s/\|$//')"
if [[ -z "$pattern" ]] || printf '\n' | grep -qiE -- "$pattern"; then
  echo "scrub: the term pattern is empty or matches empty text (an empty alternative?); refusing to run." >&2
  exit 2
fi

# Tracked + untracked-but-not-ignored files. LICENSE is third-party legal text; pnpm-lock.yaml is
# generated from npm package names (a package name can collide with a term without saying anything about anyone).
files=()
while IFS= read -r f; do
  [[ -f "$f" && "$f" != "LICENSE" && "$f" != "pnpm-lock.yaml" ]] && files+=("$f")
done < <(git ls-files -co --exclude-standard)

fail=0
if hits="$(grep -nIiE -- "$pattern" "${files[@]}")"; then
  echo "scrub: personal/employer terms found:" >&2
  echo "$hits" >&2
  fail=1
fi

# The author's surname is allowed only in the credit lines.
allowed_credit='^(README\.md|CONTRIBUTING\.md|guide/[^/]+\.html|design/[^/]+/[^/]+\.md|design/([^/]+-)?prototype/[^/]+\.html|site/src/layouts/Base\.astro|site/src/pages/index\.astro|scripts/scrub\.sh)$'
for f in "${files[@]}"; do
  if [[ ! "$f" =~ $allowed_credit ]] && grep -qI "Radnitz" "$f"; then
    echo "scrub: credit name outside allowed files: $f" >&2
    fail=1
  fi
done

if [[ $fail -eq 0 ]]; then
  echo "scrub: OK (${#files[@]} files)"
fi
exit $fail
