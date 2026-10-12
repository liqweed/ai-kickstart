#!/usr/bin/env bash
# Build the shareable zip: dist/ai-kickstart-v<VERSION>.zip
# Contains only what a friend needs (README, LICENSE, START-HERE.html, guide/, vault/), not the maintainer scaffolding.
# Usage: scripts/build.sh [--optional-scrub]
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

scripts/check.sh "$@"

version="$(tr -d '[:space:]' < VERSION)"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

mkdir -p "$stage/ai-kickstart" dist
cp -R README.md LICENSE START-HERE.html guide vault "$stage/ai-kickstart/"
find "$stage" -name '.DS_Store' -delete

out="dist/ai-kickstart-v${version}.zip"
rm -f "$out"
(cd "$stage" && zip -rq "$OLDPWD/$out" ai-kickstart)
echo "build: $out ($(du -h "$out" | cut -f1), $(unzip -l "$out" | tail -1 | awk '{print $2}') files)"
