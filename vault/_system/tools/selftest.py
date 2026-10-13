#!/usr/bin/env python3
"""Check that the vault tools work on this computer: runs every tool test and the contract checks.

Reads:    the tools and their tests (in temporary folders, not your notes)
Writes:   nothing in the vault (tests use throwaway folders)
Network:  none
Secrets:  none
Used by:  harness step P0.6, skills `tool-builder` and `vault-maintenance`
Run:      python3 _system/tools/selftest.py [-v]
Exit:     0 all good · 1 something failed
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import platform
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
VAULT = TOOLS.parents[1]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    if sys.version_info < (3, 9):
        print(f"selftest: Python {platform.python_version()} is too old. The tools need Python 3.9 or newer.")
        return 1
    verbose = 2 if "-v" in sys.argv[1:] else 1
    loader = unittest.TestLoader()
    suite = loader.discover(str(TOOLS / "tests"), pattern="test_*.py", top_level_dir=str(TOOLS / "tests"))
    for scripts in sorted(VAULT.glob("_system/skills/*/scripts")):
        if any(scripts.glob("test_*.py")):
            suite.addTests(loader.discover(str(scripts), pattern="test_*.py", top_level_dir=str(scripts)))
    print(f"selftest: Python {platform.python_version()} on {platform.system()}, {suite.countTestCases()} tests")
    result = unittest.TextTestRunner(verbosity=verbose, stream=sys.stdout).run(suite)
    if result.wasSuccessful():
        print("selftest: OK. The tools work on this computer.")
        return 0
    print("selftest: FAILED. Show this output to your AI and ask it to fix the tool (skill: tool-builder).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
