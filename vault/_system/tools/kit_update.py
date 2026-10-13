#!/usr/bin/env python3
"""Update this vault to a new AI Kickstart release without losing anything you wrote.

Reads:    this vault, the new kit you name (--kit: the downloaded zip or its unpacked folder) and,
          ideally, the kit version this vault came from (--old: same forms)
Writes:   only with --apply: adds files that are new in the kit, and replaces kit files you never
          changed. Never touches your own files (profile, plan, indexes, answers, AGENTS.md), files
          you edited, or files you deleted. Never deletes anything.
Network:  none
Secrets:  none
Used by:  skill `kit-update`
Run:      python3 _system/tools/kit_update.py --kit <new zip or folder> --old <old zip or folder> [--apply] [--diff] [--json]
Exit:     0 nothing left to do · 1 there is something to apply or look at · 2 usage error

What each file gets (the same rules as the companion app):
    update     a kit file you never changed, and the release changed it: replaced with --apply
    add        new in this release: created with --apply
    conflict   a kit file you edited, and the release changed it too: you choose (keep yours, take the
               new one, or have your AI merge the two). Never changed by this tool
    merge      one of your own files (plan, profile, indexes…) that the release changed: your AI
               brings the new parts in by hand. Never changed by this tool
    removed    you deleted it: stays deleted
    retired    the release no longer ships it: stays in your vault, it's yours now
    unchanged  nothing to do

Without --old the tool can't tell your edits from the kit's changes, so every kit file that differs
shows up as a conflict. Old releases are on https://github.com/liqweed/ai-kickstart/releases; the
version this vault came from is in _system/kickstart/kit-version.md (vaults from before v1.4 don't
have it: look for the zip name you first downloaded, e.g. ai-kickstart-v1.2.zip).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import difflib
import hashlib
import os
import re
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

import vaultlib as vl

# Files the person's AI is told to edit, or that hold the person's own answers. Keep this list
# identical to PERSON_OWNED in packages/core/src/update.ts (scripts/check_kit.py compares them).
PERSON_OWNED = [
    re.compile(r"^AGENTS\.md$"),
    re.compile(r"^_system/HARNESS-PLAN\.md$"),
    re.compile(r"^_system/index\.md$"),
    re.compile(r"^_system/profile/(?!README\.md$)[^/]+\.md$"),
    re.compile(r"^_system/kickstart/answers/"),
    re.compile(r"^_system/tools/README\.md$"),
    re.compile(r"(^|/)_index\.md$"),
]
ACTIONS = ["update", "add", "conflict", "merge", "removed", "retired", "unchanged"]
SKIP_PARTS = {"__pycache__", ".DS_Store"}
VERSION_NOTE = "_system/kickstart/kit-version.md"


def kind_of(path: str) -> str:
    return "person" if any(p.search(path) for p in PERSON_OWNED) else "kit"


def fingerprint(data: bytes) -> str:
    """Hash text with line endings normalised, so a CRLF-only change still counts as untouched."""
    try:
        data = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    except UnicodeDecodeError:
        pass
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _wanted(parts: List[str]) -> bool:
    return not any(p.startswith(".") or p in SKIP_PARTS for p in parts)


def load_kit(source: Path) -> Dict[str, bytes]:
    """The vault files of a kit: from a release zip, an unpacked kit folder, or its vault/ folder."""
    files: Dict[str, bytes] = {}
    if source.is_file() and zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as z:
            names = [n for n in z.namelist() if not n.endswith("/")]
            roots = sorted({m.group(0) for m in (re.match(r"^(?:[^/]+/)?vault/", n) for n in names) if m}, key=len)
            if not roots:
                raise ValueError(f"{source.name} has no vault/ folder. Is it an AI Kickstart zip?")
            for n in names:
                if n.startswith(roots[0]):
                    rel = n[len(roots[0]):]
                    if rel and _wanted(rel.split("/")):
                        files[rel] = z.read(n)
        return files
    if not source.is_dir():
        raise ValueError(f"{source} is neither a folder nor a zip file.")
    root = source / "vault" if (source / "vault" / "AGENTS.md").is_file() else source
    if not (root / "AGENTS.md").is_file():
        raise ValueError(f"{source} doesn't look like an AI Kickstart kit (no AGENTS.md, no vault/ folder).")
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and _wanted(rel.split("/")):
            files[rel] = p.read_bytes()
    return files


def kit_version(files: Dict[str, bytes]) -> str:
    m = re.search(rb"^kit_version:\s*\"?([0-9.]+)", files.get(VERSION_NOTE, b""), re.M)
    return m.group(1).decode() if m else "unknown"


def plan(vault: Path, new: Dict[str, bytes], old: Optional[Dict[str, bytes]]) -> List[Dict[str, str]]:
    """Sort every file into an action. Mirrors planUpdate() in packages/core/src/update.ts."""
    baseline = {p: fingerprint(b) for p, b in (old or {}).items()}
    rows: List[Dict[str, str]] = []
    for path in sorted(new):
        target = vault / path
        now = fingerprint(target.read_bytes()) if target.is_file() else None
        was, nxt, kind = baseline.get(path), fingerprint(new[path]), kind_of(path)
        if now is None:
            action = "add" if was is None else "removed"
        elif now == nxt or was == nxt:
            action = "unchanged"
        elif kind == "person":
            action = "merge"
        elif was is None:
            action = "conflict"
        else:
            action = "update" if now == was else "conflict"
        rows.append({"path": path, "kind": kind, "action": action})
    for path in sorted(set(baseline) - set(new)):
        if (vault / path).is_file():
            rows.append({"path": path, "kind": kind_of(path), "action": "retired"})
    return rows


def kit_diff(path: str, new: Dict[str, bytes], old: Optional[Dict[str, bytes]], vault: Path) -> str:
    """What the release changed in one file (old kit → new kit), or yours → new kit without --old."""
    def lines(data: Optional[bytes]) -> List[str]:
        return [] if data is None else data.decode("utf-8", errors="replace").replace("\r\n", "\n").splitlines(keepends=True)
    if old is not None:
        a, label = old.get(path), "kit as you got it"
    else:
        target = vault / path
        a, label = (target.read_bytes() if target.is_file() else None), "your vault"
    changed = [l for l in difflib.ndiff(lines(a), lines(new.get(path))) if l[:2] in ("- ", "+ ")]
    if not changed:
        return ""
    return f"--- {label}: {path}\n+++ new kit: {path}\n" + "".join(l[0] + l[2:] if l.endswith("\n") else l[0] + l[2:] + "\n" for l in changed)


def write_bytes_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def apply(vault: Path, rows: List[Dict[str, str]], new: Dict[str, bytes], limit: int) -> List[str]:
    """Add new files and replace untouched kit files. Nothing else, ever."""
    todo = [r["path"] for r in rows if r["action"] in ("update", "add")]
    if len(todo) > limit:
        raise ValueError(f"{len(todo)} files to write, more than --max {limit}. Check the dry run, then raise --max.")
    for path in todo:
        write_bytes_atomic(vault / path, new[path])
    return todo


WHAT = {
    "update": "Kit files you never changed: replaced with the new version",
    "add": "New in this release: added",
    "conflict": "Kit files you edited that the release also changed: choose keep yours, take new, or merge",
    "merge": "Your own files the release changed: your AI brings the new parts in by hand (never overwritten)",
    "removed": "Files you deleted: left deleted",
    "retired": "No longer in the kit: left in your vault, they're yours now",
}


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--kit", required=True, help="the new kit: its zip, its unpacked folder, or that folder's vault/")
    ap.add_argument("--old", help="the kit version this vault came from (same forms). Strongly recommended")
    ap.add_argument("--apply", action="store_true", help="add new files and replace untouched kit files (default: dry run)")
    ap.add_argument("--max", type=int, default=300, help="refuse to write more files than this (default 300)")
    ap.add_argument("--diff", action="store_true", help="also show what the release changed in each conflict and merge file")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault = vl.resolve_vault(args.vault)
    try:
        new = load_kit(Path(args.kit).expanduser())
        old = load_kit(Path(args.old).expanduser()) if args.old else None
    except (ValueError, OSError, zipfile.BadZipFile) as e:
        print(f"kit_update: {e}", file=sys.stderr)
        return 2
    rows = plan(vault, new, old)
    written: List[str] = []
    if args.apply:
        try:
            written = apply(vault, rows, new, args.max)
        except ValueError as e:
            print(f"kit_update: {e}", file=sys.stderr)
            return 2
        rows = plan(vault, new, old)
    count = {a: sum(r["action"] == a for r in rows) for a in ACTIONS}
    attention = [r for r in rows if r["action"] in ("conflict", "merge")]
    versions = {"vault": kit_version(old) if old else "unknown (no --old)", "new": kit_version(new)}
    diffs = {r["path"]: kit_diff(r["path"], new, old, vault) for r in attention} if args.diff else {}
    if args.json:
        vl.print_json({"tool": "kit_update", "versions": versions, "applied": args.apply, "written": written,
                       "count": count, "files": [r for r in rows if r["action"] != "unchanged"], "diffs": diffs})
    else:
        mode = "applied" if args.apply else "dry run, nothing written"
        print(f"# Kit update: {versions['vault']} → {versions['new']} ({mode})\n")
        if old is None:
            print("Without --old, every kit file that differs is listed as a conflict. Add --old for a clean plan.\n")
        if written:
            print(f"Wrote {len(written)} file(s): new ones added, untouched kit files replaced.\n")
        for action in ACTIONS[:-1]:
            items = [r for r in rows if r["action"] == action]
            if items:
                print(f"## {action} ({len(items)})\n{WHAT[action]}.\n")
                for r in items:
                    print(f"- `{r['path']}`")
                print()
        for path, text in diffs.items():
            print(f"## What the release changed in `{path}`\n\n```diff\n{text or '(no text difference)'}```\n")
        print(f"Unchanged: {count['unchanged']} file(s).")
        if not args.apply and (count["update"] or count["add"]):
            print("Next: run again with --apply to add and replace the files above. Nothing else is touched.")
    pending = count["update"] + count["add"] + count["conflict"] + count["merge"]
    return 1 if pending else 0


if __name__ == "__main__":
    sys.exit(main())
