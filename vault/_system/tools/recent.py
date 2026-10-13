#!/usr/bin/env python3
"""What changed lately: notes created or updated, and tasks completed, in the last N days.

Reads:    every note (frontmatter dates, completed tasks, file modification times)
Writes:   nothing
Network:  none
Secrets:  none
Used by:  skills `weekly-review` (look back), `vault-maintenance`
Run:      python3 _system/tools/recent.py [--days 7] [--json]
Exit:     0 always (2 on a usage error)

Dates come from the note's `created` / `updated` frontmatter. Notes without them fall back to the
file's modification time (marked "file date"). Completed tasks count when they carry a completion
date: "- [x] Call the plumber ✅ 2026-10-09" (Obsidian Tasks) or "[completion:: 2026-10-09]".
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

DONE_RES = [re.compile(r"✅\s*(\d{4}-\d{2}-\d{2})"), re.compile(r"\[completion::\s*(\d{4}-\d{2}-\d{2})\]", re.I)]
CLEAN_RE = re.compile(r"\s*(?:[📅⏳🛫➕✅]\s*\d{4}-\d{2}-\d{2}|\[\w+::[^\]]*\]|[🔺⏫🔼🔽⏬🔁])")


def collect(vault: Path, today: dt.date, days: int) -> Dict[str, List[Dict[str, object]]]:
    since = today - dt.timedelta(days=days)
    created, updated, done = [], [], []
    for path in vl.iter_notes(vault):
        r = vl.rel(vault, path)
        if vl.is_system_exempt(r):
            continue
        text = vl.read_text(path)
        fm = vl.parse_frontmatter(text)
        data = fm.data if fm.present and not fm.problems else {}
        summary = str(data.get("summary") or "")
        c, u = vl.parse_date(data.get("created")), vl.parse_date(data.get("updated"))
        source = "frontmatter"
        if not c and not u:
            u, source = vl.file_date(path), "file date"
        entry = {"file": r, "summary": summary, "source": source}
        if c and since < c <= today:
            created.append({**entry, "date": c.isoformat()})
        elif u and since < u <= today:
            updated.append({**entry, "date": u.isoformat()})
        for task in vl.tasks(text):
            if task.status != "x":
                continue
            for rx in DONE_RES:
                m = rx.search(task.text)
                d = vl.parse_date(m.group(1)) if m else None
                if d and since < d <= today:
                    done.append({"file": r, "date": d.isoformat(), "text": CLEAN_RE.sub("", task.text).strip()})
                    break
    for lst in (created, updated, done):
        lst.sort(key=lambda e: (str(e["date"]), str(e["file"])), reverse=True)
    return {"created": created, "updated": updated, "completed_tasks": done}


def render(result: Dict[str, List[Dict[str, object]]], days: int) -> str:
    total = sum(len(v) for v in result.values())
    if not total:
        return f"recent: nothing changed in the last {days} days."
    out = [f"recent: last {days} days — {len(result['created'])} new, {len(result['updated'])} updated, "
           f"{len(result['completed_tasks'])} tasks done", ""]
    for key, title in (("created", "New notes"), ("updated", "Updated notes")):
        if not result[key]:
            continue
        out.append(f"## {title}")
        groups: Dict[str, List[str]] = defaultdict(list)
        for e in result[key]:
            area = str(e["file"]).split("/")[0] if "/" in str(e["file"]) else "(vault root)"
            note = f" — {e['summary']}" if e["summary"] else ""
            flag = " _(file date)_" if e["source"] == "file date" else ""
            groups[area].append(f"  - {e['date']} {vl.note_link(str(e['file']))}{note}{flag}")
        for area in sorted(groups):
            out.append(f"- **{area}**")
            out += groups[area]
        out.append("")
    if result["completed_tasks"]:
        out.append("## Tasks done")
        out += [f"- {e['date']} {e['text']} · {vl.note_link(str(e['file']))}" for e in result["completed_tasks"]]
    return "\n".join(out).rstrip()


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--days", type=int, default=7, help="how far back to look (default 7)")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    if args.days < 1:
        ap.error("--days must be 1 or more")
    vault, today = vl.resolve_vault(args.vault), vl.parse_today(args.today)
    result = collect(vault, today, args.days)
    if args.json:
        vl.print_json({"tool": "recent", "today": today.isoformat(), "days": args.days, **result})
    else:
        print(render(result, args.days))
    return 0


if __name__ == "__main__":
    sys.exit(main())
