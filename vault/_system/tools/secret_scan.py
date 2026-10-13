#!/usr/bin/env python3
"""Find things that should never be in the vault: passwords, API keys, card and bank account numbers.

Reads:    text files in the vault (or the files you name)
Writes:   nothing
Network:  none
Secrets:  never prints a full match; findings are masked (first 4 characters + length)
Used by:  skills `vault-maintenance`, `tool-builder`; optional git pre-commit hook
Run:      python3 _system/tools/secret_scan.py [FILE ...] [--json]
Exit:     0 nothing found · 1 findings · 2 usage error

Extra patterns (e.g. a national ID format) go in config/secret-scan.md frontmatter:
    extra_patterns: ["\\b\\d{3}-\\d{2}-\\d{4}\\b"]
    allow: ["the exact text of a false positive"]
To silence one line, add <!-- secret-scan: ignore --> to it.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import re
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import vaultlib as vl

TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".base", ".canvas", ".py", ".sh", ".ps1",
             ".ini", ".toml", ".env", ".cfg", ".conf", ".html", ".xml", ".ics"}
IGNORE_MARK = "secret-scan: ignore"


def luhn_ok(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0


def card_ok(match: str) -> bool:
    digits = re.sub(r"[ -]", "", match)
    return 13 <= len(digits) <= 19 and digits[0] in "3456" and luhn_ok(digits) and len(set(digits)) > 2


def iban_ok(match: str) -> bool:
    s = re.sub(r"\s", "", match).upper()
    if not 15 <= len(s) <= 34:
        return False
    moved = s[4:] + s[:4]
    try:
        return int("".join(str(int(c, 36)) for c in moved)) % 97 == 1
    except ValueError:
        return False


def password_ok(match: str) -> bool:
    """'password: hunter2' yes; 'password: in the password manager' no."""
    value = re.split(r"[:=]", match, maxsplit=1)[1].strip().strip("\"'`*")
    if len(value) < 6 or " " in value:
        return False
    if value.lower() in {"<redacted>", "redacted", "none", "n/a", "unknown", "manager", "todo", "xxxxxx", "******"}:
        return False
    return not re.fullmatch(r"[*x•.\-_]+", value, re.I) and not value.startswith(("[[", "<", "{{", "("))


Rule = Tuple[str, "re.Pattern[str]", Optional[Callable[[str], bool]]]

RULES: List[Rule] = [
    ("private key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"), None),
    ("API key (OpenAI-style)", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_\-]{20,}"), None),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})"), None),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), None),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), None),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"), None),
    ("Stripe key", re.compile(r"\b[rs]k_live_[A-Za-z0-9]{20,}"), None),
    ("web token (JWT)", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), None),
    ("password or secret", re.compile(
        r"(?i)\b(?:password|passwd|passcode|pwd|pin code|pincode|secret|api[ _-]?key|access[ _-]?token|wachtwoord|passwort|mot de passe|contraseña)\b\s*[:=]\s*\S+"),
     password_ok),
    ("card number", re.compile(r"\b(?:\d[ -]?){12,18}\d\b"), card_ok),
    ("bank account (IBAN)", re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]){11,30}\b"), iban_ok),
]


def mask(s: str) -> str:
    s = s.strip()
    return f"{s[:4]}… ({len(s)} chars)"


def scan_text(text: str, rules: List[Rule], allow: List[str]) -> List[Dict[str, object]]:
    found = []
    for n, line in enumerate(text.splitlines(), 1):
        if IGNORE_MARK in line:
            continue
        for kind, rx, check in rules:
            for m in rx.finditer(line):
                hit = m.group(0)
                if any(a and a in line for a in allow):
                    continue
                if check and not check(hit):
                    continue
                found.append({"line": n, "kind": kind, "preview": mask(hit)})
    return found


def build_rules(config: Dict[str, object]) -> List[Rule]:
    rules = list(RULES)
    for i, pat in enumerate(vl.as_list(config.get("extra_patterns"))):
        try:
            rules.append((f"custom pattern {i + 1}", re.compile(pat), None))
        except re.error as e:
            raise SystemExit(f"error: config/secret-scan.md extra_patterns #{i + 1} is not a valid pattern: {e}")
    return rules


def display_path(vault: Path, p: Path) -> str:
    """Vault-relative when possible (also through symlinks such as macOS /var -> /private/var)."""
    for base, target in ((vault, p), (vault.resolve(), p.resolve())):
        try:
            return vl.rel(base, target)
        except ValueError:
            continue
    return str(p)


def scan_vault(vault: Path, files: Optional[List[Path]] = None, config: Optional[Dict[str, object]] = None) -> List[Dict[str, object]]:
    config = vl.load_config(vault, "secret-scan") if config is None else config
    rules, allow = build_rules(config), vl.as_list(config.get("allow"))
    paths = files if files is not None else list(vl.iter_files(vault, TEXT_EXTS))
    results = []
    for p in paths:
        if not p.is_file():
            continue
        if p.name == "secret_scan.py":
            continue  # this file describes the patterns it looks for
        for f in scan_text(vl.read_text(p), rules, allow):
            f["file"] = display_path(vault, p)
            results.append(f)
    return results


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="only scan these files (default: the whole vault)")
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault = vl.resolve_vault(args.vault)
    files = [Path(f).resolve() for f in args.files] if args.files else None
    results = scan_vault(vault, files)
    if args.json:
        vl.print_json({"tool": "secret_scan", "findings": results})
    elif not results:
        print("secret_scan: nothing found.")
    else:
        print(f"secret_scan: {len(results)} possible secret(s). Move them to a password manager, then delete them here.\n")
        for f in results:
            print(f"- {f['file']}:{f['line']}  {f['kind']}  {f['preview']}")
    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main())
