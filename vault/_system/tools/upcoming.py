#!/usr/bin/env python3
"""What's coming up: due tasks, birthdays, anniversaries, renewals and deadlines from your notes.

Reads:    every note: open tasks with a due date, and date fields in frontmatter
Writes:   nothing
Network:  none
Secrets:  none
Used by:  skills `daily-briefing`, `weekly-review`, `people`
Run:      python3 _system/tools/upcoming.py [--days 14] [--json]
Exit:     0 always (2 on a usage error)

Due dates on tasks, any of these styles:
    - [ ] Renew passport 📅 2026-11-30          (Obsidian Tasks plugin)
    - [ ] Renew passport due: 2026-11-30
    - [ ] Renew passport [due:: 2026-11-30]     (Dataview)
    - [ ] Renew passport ⏳ 2026-11-20           (scheduled: shown as "planned")
Yearly dates in frontmatter (YYYY-MM-DD or MM-DD): birthday, anniversary
One-off dates in frontmatter (YYYY-MM-DD): due, deadline, renewal, expires, review_by, next_service
Add your own field names in config/upcoming.md: yearly_fields: [nameday] · date_fields: [warranty_until]
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Dict, List, Optional

import vaultlib as vl

YEARLY_FIELDS = ["birthday", "anniversary"]
DATE_FIELDS = ["due", "deadline", "renewal", "expires", "review_by", "next_service"]
DUE_RES = [
    ("due", re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")),
    ("due", re.compile(r"\[due::\s*(\d{4}-\d{2}-\d{2})\]", re.I)),
    ("due", re.compile(r"(?<![\w\[])due:\s*(\d{4}-\d{2}-\d{2})", re.I)),
    ("due", re.compile(r"@due\((\d{4}-\d{2}-\d{2})\)", re.I)),
    ("planned", re.compile(r"⏳\s*(\d{4}-\d{2}-\d{2})")),
]
CLEAN_RE = re.compile(r"\s*(?:[📅⏳🛫➕✅]\s*\d{4}-\d{2}-\d{2}|\[\w+::[^\]]*\]|(?<![\w\[])due:\s*\d{4}-\d{2}-\d{2}|@due\([^)]*\)|[🔺⏫🔼🔽⏬🔁])")


def collect(vault: Path, today: dt.date, days: int, include_overdue: bool = True,
            config: Optional[Dict[str, object]] = None) -> List[Dict[str, object]]:
    config = vl.load_config(vault, "upcoming") if config is None else config
    yearly = YEARLY_FIELDS + vl.as_list(config.get("yearly_fields"))
    once = DATE_FIELDS + vl.as_list(config.get("date_fields"))
    horizon = today + dt.timedelta(days=days)
    items: List[Dict[str, object]] = []

    def keep(d: dt.date) -> bool:
        return d <= horizon and (d >= today or include_overdue)

    for path in vl.iter_notes(vault):
        r = vl.rel(vault, path)
        if vl.is_system_exempt(r) or r.startswith("99-archive/"):
            continue
        text = vl.read_text(path)
        fm = vl.parse_frontmatter(text)
        title = path.stem
        if fm.present and not fm.problems and str(fm.data.get("status") or "") not in ("done", "archive"):
            for key in yearly:
                md = vl.parse_month_day(fm.data.get(key))
                if not md:
                    continue
                year, month, day = md
                when = vl.next_occurrence(month, day, today)
                if when <= horizon:
                    what = f"{title}: {key}"
                    if year:
                        what += f" ({when.year - year})"
                    items.append({"date": when.isoformat(), "kind": key, "text": what, "file": r, "line": None})
            for key in once:
                d = vl.parse_date(fm.data.get(key))
                if d and keep(d):
                    items.append({"date": d.isoformat(), "kind": key, "text": f"{title}: {key}", "file": r, "line": None})
        body = text[fm.end_offset:] if fm.present and not fm.problems else text
        offset = text[: len(text) - len(body)].count("\n")
        for task in vl.tasks(body):
            if task.status not in (" ", "/"):
                continue
            for kind, rx in DUE_RES:
                m = rx.search(task.text)
                if not m:
                    continue
                d = vl.parse_date(m.group(1))
                if d and keep(d):
                    clean = CLEAN_RE.sub("", task.text).strip()
                    items.append({"date": d.isoformat(), "kind": kind, "text": clean, "file": r, "line": task.line + offset})
                break
    items.sort(key=lambda i: (str(i["date"]), str(i["file"]), i["line"] or 0))
    return items


def render(items: List[Dict[str, object]], today: dt.date, days: int) -> str:
    if not items:
        return f"upcoming: nothing due in the next {days} days."
    groups: Dict[str, List[str]] = {"Overdue": [], "Today": [], "Tomorrow": [], f"Next {days} days": []}
    for i in items:
        d = dt.date.fromisoformat(str(i["date"]))
        delta = (d - today).days
        label = "Overdue" if delta < 0 else "Today" if delta == 0 else "Tomorrow" if delta == 1 else f"Next {days} days"
        when = f"{d.strftime('%a')} {d.isoformat()}"
        if delta < 0:
            when += f" ({-delta}d late)"
        kind = " _(planned)_" if i["kind"] == "planned" else ""
        groups[label].append(f"- {when} — {i['text']}{kind} · {vl.note_link(str(i['file']))}")
    out = []
    for label, lines in groups.items():
        if lines:
            out += [f"## {label}", *lines, ""]
    return "\n".join(out).rstrip()


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--days", type=int, default=14, help="how far ahead to look (default 14)")
    ap.add_argument("--no-overdue", action="store_true", help="leave out overdue items")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    if args.days < 0:
        ap.error("--days must be 0 or more")
    vault, today = vl.resolve_vault(args.vault), vl.parse_today(args.today)
    items = collect(vault, today, args.days, not args.no_overdue)
    if args.json:
        vl.print_json({"tool": "upcoming", "today": today.isoformat(), "days": args.days, "items": items})
    else:
        print(render(items, today, args.days))
    return 0


if __name__ == "__main__":
    sys.exit(main())
