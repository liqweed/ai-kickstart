"""Contract tests: every tool in the vault follows _system/TOOLS-CONTRACT.md.

Covers the shared tools in _system/tools/ and every skill script in _system/skills/*/scripts/.
New tools are picked up automatically, so a tool that breaks a rule fails the self-test.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import ast
import re
import subprocess
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
VAULT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))

import secret_scan  # noqa: E402

HEADER_FIELDS = ["Reads:", "Writes:", "Network:", "Secrets:", "Used by:", "Run:"]
NETWORK_MODULES = {"urllib.request", "http.client", "socket", "requests", "httpx", "aiohttp", "ftplib", "smtplib", "urllib3"}
LIBRARY_FILES = {"vaultlib.py", "selftest.py"}


def tool_files():
    shared = [p for p in sorted(TOOLS.glob("*.py")) if not p.name.startswith("_") and p.name not in LIBRARY_FILES]
    skill = [p for p in sorted(VAULT.glob("_system/skills/*/scripts/*.py"))
             if not p.name.startswith(("_", "test_"))]
    return shared + skill


def header(path: Path) -> str:
    return ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""


def field(doc: str, name: str) -> str:
    m = re.search(rf"^{re.escape(name)}\s*(.+)$", doc, re.M)
    return m.group(1).strip() if m else ""


class TestContract(unittest.TestCase):
    def test_there_are_tools(self) -> None:
        self.assertTrue(tool_files(), "no tools found")

    def test_header_block(self) -> None:
        for p in tool_files():
            with self.subTest(tool=p.name):
                doc = header(p)
                self.assertTrue(doc, "no docstring (TOOLS-CONTRACT §2)")
                for f in HEADER_FIELDS:
                    self.assertTrue(field(doc, f), f"header field {f} missing or empty (TOOLS-CONTRACT §2)")

    def test_python_39_syntax(self) -> None:
        for p in tool_files() + [TOOLS / "vaultlib.py"]:
            with self.subTest(tool=p.name):
                ast.parse(p.read_text(encoding="utf-8"), feature_version=(3, 9))

    def test_writers_default_to_dry_run(self) -> None:
        for p in tool_files():
            with self.subTest(tool=p.name):
                writes = field(header(p), "Writes:").lower()
                if writes.startswith("nothing"):
                    continue
                self.assertIn("--apply", writes, "a tool that writes must say 'only with --apply' (TOOLS-CONTRACT §3)")
                self.assertIn('"--apply"', p.read_text(encoding="utf-8"), "declares --apply but has no --apply option")

    def test_network_is_declared(self) -> None:
        for p in tool_files() + [TOOLS / "vaultlib.py"]:
            with self.subTest(tool=p.name):
                tree = ast.parse(p.read_text(encoding="utf-8"))
                imported = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported |= {a.name for a in node.names}
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported |= {node.module} | {f"{node.module}.{a.name}" for a in node.names}
                uses_net = bool(imported & NETWORK_MODULES)
                declared = field(header(p), "Network:").lower()
                if uses_net:
                    self.assertFalse(declared.startswith("none"), "imports a network module but says 'Network: none' (§3)")

    def test_no_personal_paths_or_secrets(self) -> None:
        for p in tool_files() + [TOOLS / "vaultlib.py"]:
            with self.subTest(tool=p.name):
                text = p.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"(/[U]sers/|/home/|[A-Z]:\\\\[U]sers\\\\)\w", text), "hard-coded personal path (§2, §4)")
        found = secret_scan.scan_vault(VAULT, files=tool_files(), config={})
        self.assertEqual(found, [], "a tool file contains something that looks like a secret (§4)")

    def test_registered(self) -> None:
        registry = (TOOLS / "README.md").read_text(encoding="utf-8")
        for p in tool_files():
            with self.subTest(tool=p.name):
                self.assertIn(f"`{p.name}`", registry, "not listed in _system/tools/README.md (§5)")

    def test_help_runs(self) -> None:
        for p in tool_files():
            with self.subTest(tool=p.name):
                r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True, encoding="utf-8", timeout=60)
                self.assertEqual(r.returncode, 0, r.stderr[-500:])
                self.assertTrue(r.stdout.strip())


if __name__ == "__main__":
    unittest.main()
