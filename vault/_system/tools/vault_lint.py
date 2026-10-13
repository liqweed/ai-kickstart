#!/usr/bin/env python3
"""Vault health check: broken links, missing frontmatter, orphans, duplicates, a stale index, an old inbox, secrets.

Reads:    every note in the vault, _system/index.md, config/vault-lint.md (optional settings)
Writes:   nothing
Network:  none
Secrets:  findings from secret_scan are masked
Used by:  skill `vault-maintenance` (monthly), `weekly-review` (inbox age)
Run:      python3 _system/tools/vault_lint.py [--only CHECK,...] [--json] [--strict]
Exit:     0 no errors (warnings and tips are fine) · 1 errors found (or warnings with --strict) · 2 usage error

Settings (all optional) go in config/vault-lint.md frontmatter:
    inbox_days: 14          # inbox notes older than this are flagged
    stale_days: 120         # "active" notes not updated for this long are flagged
    ignore: ["04-learning/imported/"]   # path prefixes to skip entirely
    types: [recipe]         # extra allowed values for `type`
    statuses: [paused]      # extra allowed values for `status`
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import datetime as dt
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import vaultlib as vl
import secret_scan

REQUIRED = ["tags", "type", "status", "created", "updated", "summary"]
TYPES = {"note", "project", "reference", "meeting", "idea", "plan", "log", "decision", "person",
         "review", "briefing", "navigation", "source", "connection"}
STATUSES = {"active", "review", "someday", "done", "archive"}

# Dated series and capture areas: no "orphan" warnings (contract §4).
SERIES_PREFIXES = ("07-briefings/", "05-planning/weekly/", "05-planning/monthly/", "_system/kickstart/answers/",
                   "_inbox/", "99-archive/", "config/")

SEVERITY = {
    "frontmatter-invalid": "error", "broken-link": "error", "secret": "error",
    "frontmatter-missing": "warning", "field-missing": "warning", "field-invalid": "warning",
    "duplicate-name": "warning", "index-drift": "warning", "inbox-age": "warning",
    "orphan": "tip", "stale-active": "tip", "empty-note": "tip", "unused-attachment": "tip",
}
CHECKS = list(SEVERITY)
HELP = {
    "frontmatter-invalid": "Fix the YAML block at the top of the note (it must open and close with ---).",
    "broken-link": "Point the link at an existing note, create the note, or remove the brackets.",
    "secret": "Move it to a password manager and delete it from the vault.",
    "frontmatter-missing": "Add frontmatter (fix_frontmatter.py can draft it).",
    "field-missing": "Add the missing fields (contract §3). `summary` needs a human-quality sentence.",
    "field-invalid": "Use an allowed value or a YYYY-MM-DD date.",
    "duplicate-name": "Two notes with the same name confuse links and the AI. Merge them or rename one.",
    "index-drift": "Mention the folder in _system/index.md (contract §5), or fix the path.",
    "inbox-age": "Sort these in the weekly review: file, turn into a task, or delete (ask first).",
    "orphan": "Link the note from a parent (a hub, project or related note), or archive it.",
    "stale-active": "Still active? Update it, or set status to done/someday/archive.",
    "empty-note": "Fill it in or delete it (ask first).",
    "unused-attachment": "Not linked from any note. Link it, or delete it (ask first).",
}


class Note:
    def __init__(self, vault: Path, path: Path):
        self.path = path
        self.rel = vl.rel(vault, path)
        self.text = vl.read_text(path)
        self.fm = vl.parse_frontmatter(self.text)
        self.body = self.text[self.fm.end_offset:] if self.fm.present and not self.fm.problems else self.text
        self.links = vl.wikilinks(self.body if self.fm.present else self.text)
        self.mdlinks = vl.markdown_links(self.body)
        self.exempt = vl.is_system_exempt(self.rel)


def lint(vault: Path, today: dt.date, only: Optional[List[str]] = None, config: Optional[Dict[str, object]] = None) -> List[Dict[str, object]]:
    config = vl.load_config(vault, "vault-lint") if config is None else config
    inbox_days = int(str(config.get("inbox_days") or 14))
    stale_days = int(str(config.get("stale_days") or 120))
    ignore = tuple(vl.as_list(config.get("ignore")))
    types = TYPES | set(vl.as_list(config.get("types")))
    statuses = STATUSES | set(vl.as_list(config.get("statuses")))
    want = set(only or CHECKS)
    out: List[Dict[str, object]] = []

    def add(check: str, file: str, detail: str, line: Optional[int] = None) -> None:
        if check in want:
            out.append({"check": check, "severity": SEVERITY[check], "file": file, "line": line, "detail": detail})

    notes = [Note(vault, p) for p in vl.iter_notes(vault)]
    notes = [n for n in notes if not (ignore and n.rel.startswith(ignore))]
    resolver = vl.LinkResolver(vault)
    incoming: Dict[str, int] = defaultdict(int)
    linked_files = set()

    for n in notes:
        for link in n.links:
            target = resolver.resolve(link.target)
            if target:
                if target != n.rel:
                    incoming[target] += 1
                linked_files.add(target)
            elif not n.exempt:
                add("broken-link", n.rel, f"[[{link.target}]] has no matching note or file", link.line)
        for url in n.mdlinks:
            cand = (n.path.parent / url).resolve()
            try:
                linked_files.add(vl.rel(vault, cand))
            except ValueError:
                pass
            hit = resolver.resolve(url)
            if hit:
                linked_files.add(hit)

    for n in notes:
        if n.exempt:
            continue
        fm, data = n.fm, n.fm.data
        in_inbox = n.rel.startswith("_inbox/")
        if fm.problems:
            for p in fm.problems:
                add("frontmatter-invalid", n.rel, p)
        elif not fm.present:
            if not in_inbox:
                add("frontmatter-missing", n.rel, "no frontmatter")
        else:
            missing = [k for k in REQUIRED if k not in data and not (k == "summary" and "description" in data)]
            if missing:
                add("field-missing", n.rel, "missing: " + ", ".join(missing))
            elif not str(data.get("summary") or "").strip():
                add("field-missing", n.rel, "summary is empty")
            t, s = str(data.get("type") or ""), str(data.get("status") or "")
            if t and t not in types:
                add("field-invalid", n.rel, f"type '{t}' is not one of: {', '.join(sorted(types))}")
            if s and s not in statuses:
                add("field-invalid", n.rel, f"status '{s}' is not one of: {', '.join(sorted(statuses))}")
            created, updated = vl.parse_date(data.get("created")), vl.parse_date(data.get("updated"))
            for key, val in (("created", created), ("updated", updated)):
                if key in data and data[key] not in ("", None) and val is None:
                    add("field-invalid", n.rel, f"{key} '{data[key]}' is not YYYY-MM-DD")
            if created and updated and updated < created:
                add("field-invalid", n.rel, "updated is earlier than created")
            if s == "active" and updated and (today - updated).days > stale_days and not n.rel.startswith("_system/kickstart/"):
                add("stale-active", n.rel, f"active, last updated {updated} ({(today - updated).days} days ago)")

        if in_inbox and n.path.name.lower() != "readme.md":
            born = vl.parse_date(data.get("created")) if fm.present else None
            born = born or vl.file_date(n.path, "birth")
            age = (today - born).days
            if age > inbox_days:
                add("inbox-age", n.rel, f"in the inbox for {age} days")

        is_hub = n.path.name in ("_index.md", "README.md", "index.md")
        if not is_hub and not n.rel.startswith(SERIES_PREFIXES) and not n.rel.startswith("_system/"):
            if incoming.get(n.rel, 0) == 0 and not n.links:
                add("orphan", n.rel, "no links in or out")

        body = re.sub(r"^#+ .*$", "", vl.strip_code(n.body), flags=re.M)
        if len(re.sub(r"\s", "", body)) < 20 and not is_hub and not in_inbox:
            add("empty-note", n.rel, "almost no content")

    by_key: Dict[str, List[str]] = defaultdict(list)
    for n in notes:
        if n.exempt or n.path.name in ("_index.md", "README.md", "SKILL.md", "index.md"):
            continue
        key = re.sub(r"[\W_]+", "", n.path.stem.lower())
        if key:
            by_key[key].append(n.rel)
    for key, rels in by_key.items():
        if len(rels) > 1:
            for r in rels:
                add("duplicate-name", r, "same name as: " + ", ".join(x for x in rels if x != r))

    check_index(vault, notes, add)

    if "unused-attachment" in want:
        for p in vl.iter_files(vault, vl.ATTACHMENT_EXTS):
            r = vl.rel(vault, p)
            if r.startswith(("_system/", "99-archive/")) or (ignore and r.startswith(ignore)):
                continue
            if r not in linked_files:
                add("unused-attachment", r, "not linked from any note")

    if "secret" in want:
        for f in secret_scan.scan_vault(vault):
            if ignore and str(f["file"]).startswith(ignore):
                continue
            add("secret", str(f["file"]), f"{f['kind']}: {f['preview']}", int(f["line"]))

    order = {"error": 0, "warning": 1, "tip": 2}
    out.sort(key=lambda f: (order[str(f["severity"])], CHECKS.index(str(f["check"])), str(f["file"]), f["line"] or 0))
    return out


def check_index(vault: Path, notes: List[Note], add) -> None:
    """Every folder that holds notes is mentioned in _system/index.md, and paths it names exist."""
    index = vault / "_system" / "index.md"
    if not index.is_file():
        add("index-drift", "_system/index.md", "the vault index is missing")
        return
    text = vl.read_text(index).lower()
    folders = set()
    for n in notes:
        parts = n.rel.split("/")[:-1]
        if not parts or parts[0].startswith("_system") or parts[0] in ("99-archive",):
            continue
        for depth in range(1, min(len(parts), 2) + 1):
            folders.add("/".join(parts[:depth]))
        if len(parts) >= 3 and parts[0] == "03-projects" and parts[1] == "active":
            folders.add("/".join(parts[:3]))
    for f in sorted(folders):
        name = f.split("/")[-1].lower()
        if f.lower() + "/" in text or f.lower() in text or f"`{name}/`" in text or f"{name}/" in text:
            continue
        add("index-drift", "_system/index.md", f"folder '{f}/' holds notes but isn't mentioned")
    tops = {p.name for p in vault.iterdir() if p.is_dir() and not p.name.startswith(".")}
    for m in re.finditer(r"`([^`\n]+)`", vl.read_text(index)):
        path = m.group(1).strip().rstrip("/")
        first = path.split("/")[0]
        looks_like_vault_path = first in tops or re.match(r"^(\d\d-[\w-]+|_[a-z]+|config)$", first)
        if "/" not in path or not looks_like_vault_path or re.search(r"[<>*{}]|YYYY|\.\.\.|…", path):
            continue
        if not (vault / path).exists():
            add("index-drift", "_system/index.md", f"mentions `{path}`, which doesn't exist")


def render(findings: List[Dict[str, object]], max_per_check: int) -> str:
    if not findings:
        return "vault_lint: all clear. Nothing to fix."
    counts = defaultdict(int)
    for f in findings:
        counts[f["severity"]] += 1
    lines = [f"vault_lint: {counts['error']} error(s), {counts['warning']} warning(s), {counts['tip']} tip(s)", ""]
    by_check: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for f in findings:
        by_check[str(f["check"])].append(f)
    for check, items in by_check.items():
        lines.append(f"## {check} ({SEVERITY[check]}, {len(items)})")
        lines.append(f"_{HELP[check]}_")
        for f in items[:max_per_check] if max_per_check else items:
            where = f"{f['file']}:{f['line']}" if f["line"] else str(f["file"])
            lines.append(f"- {where} — {f['detail']}")
        if max_per_check and len(items) > max_per_check:
            lines.append(f"- … and {len(items) - max_per_check} more (use --max 0 to see all)")
        lines.append("")
    return "\n".join(lines).rstrip()


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--only", help="comma-separated checks: " + ", ".join(CHECKS))
    ap.add_argument("--skip", help="comma-separated checks to leave out")
    ap.add_argument("--max", type=int, default=15, help="findings shown per check (0 = all; default 15)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault = vl.resolve_vault(args.vault)
    only = [c.strip() for c in args.only.split(",")] if args.only else list(CHECKS)
    if args.skip:
        only = [c for c in only if c not in {s.strip() for s in args.skip.split(",")}]
    unknown = [c for c in only if c not in SEVERITY]
    if unknown:
        print(f"error: unknown check(s): {', '.join(unknown)}. Choose from: {', '.join(CHECKS)}", file=sys.stderr)
        return 2
    findings = lint(vault, vl.parse_today(args.today), only)
    if args.json:
        vl.print_json({"tool": "vault_lint", "findings": findings})
    else:
        print(render(findings, args.max))
    errors = sum(1 for f in findings if f["severity"] == "error")
    warnings = sum(1 for f in findings if f["severity"] == "warning")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
