#!/usr/bin/env bash
# Run every check. Pass --optional-scrub where no private term list exists (CI without the secret, contributors).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

scrub_args=()
[[ "${1:-}" == "--optional-scrub" ]] && scrub_args=(--optional)

scripts/scrub.sh "${scrub_args[@]+"${scrub_args[@]}"}"
python3 scripts/check_kit.py
