#!/usr/bin/env python3
"""Add missing frontmatter (tags, type, status, created, updated, summary) to notes, without touching what's there.

Reads:    notes in the vault (or under --path)
Writes:   only with --apply: adds missing frontmatter fields to notes; never changes or removes existing values
Network:  none
Secrets:  none
Used by:  skill `vault-maintenance` (after importing notes from another app, or tidying an older vault)
Run:      python3 _system/tools/fix_frontmatter.py [--path 01-life] [--apply] [--max 50]
Exit:     0 nothing to do or done · 1 proposals waiting (dry run) or notes skipped · 2 usage error

A dry run (the default) only shows what would change. Guesses come from the folder:
01-life/people/ → type: person, 03-projects/ideas/ → status: someday, and so on. `summary` is
left empty on purpose: a one-line summary needs judgment, so the AI (or you) writes it afterwards.
Dates come from the file's own dates. Inbox notes are left alone unless you pass --include-inbox.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import vaultlib as vl

AREA_TAGS = {"01-life": "life", "02-work": "work", "03-projects": "projects", "04-learning": "learning",
             "05-planning": "planning", "06-reference": "reference", "07-briefings": "briefing",
             "99-archive": "archive", "config": "system", "_inbox": "inbox"}
TYPE_BY_PREFIX = [("01-life/people/", "person"), ("03-projects/ideas/", "idea"), ("03-projects/", "project"),
                  ("05-planning/", "review"), ("06-reference/connections/", "connection"), ("06-reference/", "reference"),
                  ("07-briefings/", "briefing"), ("_system/kickstart/answers/", "log")]
STATUS_BY_PREFIX = [("99-archive/", "archive"), ("03-projects/archive/", "done"), ("03-projects/ideas/", "someday"),
                    ("05-planning/", "done"), ("07-briefings/", "done")]
ORDER = ["tags", "type", "status", "created", "updated", "summary"]


def guess(vault: Path, path: Path) -> Dict[str, str]:
    r = vl.rel(vault, path)
    parts = r.split("/")[:-1]
    tags = []
    if parts:
        tags.append(AREA_TAGS.get(parts[0], parts[0].lstrip("_0123456789-").lower() or "note"))
        if len(parts) > 1 and parts[0] in ("01-life", "04-learning", "02-work"):
            tags.append(parts[1].lower().replace(" ", "-"))
    if r.lower().endswith("_index.md"):
        tags.append("navigation")
    typ = "navigation" if r.lower().endswith("_index.md") else next((t for p, t in TYPE_BY_PREFIX if r.startswith(p)), "note")
    status = next((s for p, s in STATUS_BY_PREFIX if r.startswith(p)), "active")
    created = vl.file_date(path, "birth")
    updated = max(vl.file_date(path), created)
    return {"tags": "[" + ", ".join(dict.fromkeys(tags)) + "]", "type": typ, "status": status,
            "created": created.isoformat(), "updated": updated.isoformat(), "summary": ""}


def plan_note(vault: Path, path: Path) -> Tuple[Optional[str], List[str], Optional[str]]:
    """Return (new text or None, list of added 'key: value' lines, reason it was skipped)."""
    text = vl.read_raw(path)
    nl = "\r\n" if "\r\n" in text else "\n"
    fm = vl.parse_frontmatter(text)
    if fm.problems:
        return None, [], "frontmatter can't be read safely: " + "; ".join(fm.problems)
    g = guess(vault, path)
    if not fm.present:
        added = [f"{k}: {g[k]}".rstrip() for k in ORDER]
        return "---" + nl + nl.join(added) + nl + "---" + nl + nl + text.lstrip("\r\n"), added, None
    missing = [k for k in ORDER if k not in fm.data and not (k == "summary" and "description" in fm.data)]
    if not missing:
        return None, [], None
    added = [f"{k}: {g[k]}".rstrip() for k in missing]
    head = text[: fm.end_offset]
    close = head.rstrip("\r\n").rfind("\n") + 1  # start of the closing --- line
    new_head = head[:close] + nl.join(added) + nl + head[close:]
    return new_head + text[fm.end_offset:], added, None


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--path", help="only notes under this vault-relative folder or file")
    ap.add_argument("--include-inbox", action="store_true", help="also fix notes in _inbox/")
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run, show only)")
    ap.add_argument("--max", type=int, default=50, help="change at most this many notes per run (0 = no limit; default 50)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault = vl.resolve_vault(args.vault)
    prefix = args.path.replace("\\", "/").strip("/") if args.path else None

    proposals, skipped = [], []
    for path in vl.iter_notes(vault):
        r = vl.rel(vault, path)
        if vl.is_system_exempt(r) or (r.startswith("_inbox/") and not args.include_inbox):
            continue
        if prefix and not (r == prefix or r.startswith(prefix + "/")):
            continue
        new, added, reason = plan_note(vault, path)
        if reason:
            skipped.append({"file": r, "reason": reason})
        elif new is not None:
            proposals.append({"file": r, "added": added, "_path": path, "_new": new})

    limited = proposals[: args.max] if args.max else proposals
    written = 0
    if args.apply:
        for p in limited:
            vl.write_atomic(p["_path"], p["_new"])  # type: ignore[arg-type]
            written += 1

    if args.json:
        vl.print_json({"tool": "fix_frontmatter", "applied": args.apply, "written": written,
                       "proposals": [{"file": p["file"], "added": p["added"]} for p in limited],
                       "not_shown": len(proposals) - len(limited), "skipped": skipped})
    else:
        if not proposals and not skipped:
            print("fix_frontmatter: every note already has its frontmatter.")
        verb = "Added" if args.apply else "Would add"
        for p in limited:
            print(f"- {p['file']}: {verb.lower()} " + " · ".join(p["added"]))
        if len(proposals) > len(limited):
            print(f"- … {len(proposals) - len(limited)} more (run again, or raise --max)")
        for s in skipped:
            print(f"- SKIPPED {s['file']}: {s['reason']}")
        if proposals:
            print()
            if args.apply:
                print(f"fix_frontmatter: updated {written} note(s). Now write a one-line `summary` for each.")
            else:
                print(f"fix_frontmatter: {len(proposals)} note(s) need fields. Dry run: nothing written. Add --apply to write.")
    if args.apply:
        return 1 if skipped else 0
    return 1 if proposals or skipped else 0


if __name__ == "__main__":
    sys.exit(main())
