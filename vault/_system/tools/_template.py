#!/usr/bin/env python3
"""<One line: what this tool does, in plain words.>

Reads:    <which notes/files/folders, or "the CSV file you name">
Writes:   nothing            <- or: "only with --apply: <exactly what>"
Network:  none               <- or: "<host> (read-only, <why>)" — needs the owner's OK (TOOLS-CONTRACT §3)
Secrets:  none               <- or: "<NAME> from an environment variable or the OS keychain; never printed"
Used by:  skill `<skill-name>`
Run:      python3 _system/tools/<name>.py [--json]
Exit:     0 success · 1 something to report / nothing done · 2 usage error

Copy this file to _system/tools/<name>.py (or _system/skills/<skill>/scripts/<name>.py), replace every
<…>, delete what you don't need, add a test in tests/, register it in _system/tools/README.md, then run
python3 _system/tools/selftest.py. The rules are in _system/TOOLS-CONTRACT.md.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # no __pycache__ folders in the vault

import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Find _system/tools/vaultlib.py from here, so this works in _system/tools/ and in a skill's scripts/ folder.
sys.path.insert(0, str(next(p / "_system" / "tools" for p in Path(__file__).resolve().parents
                            if (p / "_system" / "tools" / "vaultlib.py").is_file())))
import vaultlib as vl  # noqa: E402


def run(vault: Path, today, apply: bool = False) -> List[Dict[str, object]]:
    """The actual work: pure, testable, no printing. Return a list of results."""
    results: List[Dict[str, object]] = []
    for path in vl.iter_notes(vault):
        r = vl.rel(vault, path)
        if vl.is_system_exempt(r):
            continue
        # … look at the note, append what you find …
    return results


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD")
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run)")  # writers only
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault, today = vl.resolve_vault(args.vault), vl.parse_today(args.today)
    results = run(vault, today, args.apply)
    if args.json:
        vl.print_json({"tool": "<name>", "results": results})
    elif not results:
        print("<name>: nothing to report.")
    else:
        for r in results:
            print(f"- {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
