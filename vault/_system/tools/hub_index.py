#!/usr/bin/env python3
"""Keep hub notes (_index.md) current: rewrite the list of notes between the auto-index markers.

Reads:    every _index.md, and the notes in its folder (names + `summary` frontmatter)
Writes:   only with --apply: the text between <!-- auto-index:start --> and <!-- auto-index:end -->
          in hub notes. Everything outside the markers is never touched.
Network:  none
Secrets:  none
Used by:  skill `vault-maintenance`; any skill that adds notes to a folder with a hub
Run:      python3 _system/tools/hub_index.py [--apply] [--json]
Exit:     0 all hubs current (or updated with --apply) · 1 hubs would change (dry run) · 2 usage error

Put the markers in any _index.md where you want an automatic list:

    <!-- auto-index:start -->
    <!-- auto-index:end -->

Options go inside the start marker, e.g. <!-- auto-index:start group=relationship depth=2 sort=updated -->
    group=<field>   group notes under headings by a frontmatter field (e.g. relationship, status)
    depth=2         also list the notes inside each subfolder (default 1: subfolders get a count)
    sort=updated    newest first (default: by name)
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import difflib
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import vaultlib as vl

START_RE = re.compile(r"<!--\s*auto-index:start([^>]*?)-->")
END_RE = re.compile(r"<!--\s*auto-index:end\s*-->")


def options(raw: str) -> Dict[str, str]:
    return dict(re.findall(r"(\w+)=([\w\-]+)", raw))


def note_info(vault: Path, path: Path) -> Dict[str, str]:
    fm = vl.parse_frontmatter(vl.read_text(path))
    data = fm.data if fm.present and not fm.problems else {}
    return {"rel": vl.rel(vault, path), "name": path.stem, "summary": str(data.get("summary") or "").strip(),
            "updated": str(data.get("updated") or ""), "data": data}  # type: ignore[dict-item]


def notes_in(vault: Path, folder: Path) -> List[Dict[str, str]]:
    return [note_info(vault, p) for p in sorted(folder.glob("*.md")) if p.name not in ("_index.md",) and not p.name.startswith(".")]


def subfolders(folder: Path) -> List[Path]:
    return [d for d in sorted(folder.iterdir()) if d.is_dir() and not d.name.startswith(".") and d.name not in vl.SKIP_DIRS]


def count_notes(folder: Path) -> int:
    return sum(1 for p in folder.rglob("*.md") if p.name != "_index.md" and not any(part.startswith(".") for part in p.parts))


def line_for(n: Dict[str, str], indent: str = "") -> str:
    summary = f" — {n['summary']}" if n["summary"] else ""
    return f"{indent}- {vl.note_link(n['rel'])}{summary}"


def sort_notes(notes: List[Dict[str, str]], how: str) -> List[Dict[str, str]]:
    if how == "updated":
        return sorted(notes, key=lambda n: (n["updated"], n["name"].lower()), reverse=True)
    return sorted(notes, key=lambda n: n["name"].lower())


def generate(vault: Path, hub: Path, opts: Dict[str, str]) -> str:
    folder, how = hub.parent, opts.get("sort", "name")
    depth = int(opts.get("depth", "1")) if opts.get("depth", "1").isdigit() else 1
    notes = sort_notes(notes_in(vault, folder), how)
    lines: List[str] = []
    group = opts.get("group")
    if group:
        buckets: Dict[str, List[Dict[str, str]]] = {}
        for n in notes:
            val = n["data"].get(group) if isinstance(n["data"], dict) else ""  # type: ignore[union-attr]
            key = (", ".join(val) if isinstance(val, list) else str(val or "")).strip() or "Other"
            buckets.setdefault(key[:1].upper() + key[1:], []).append(n)
        for key in sorted(buckets, key=lambda k: (k == "Other", k.lower())):
            lines += ["", f"### {key}"] + [line_for(n) for n in buckets[key]]
        lines = lines[1:]
    else:
        lines += [line_for(n) for n in notes]
    for sub in subfolders(folder):
        count = count_notes(sub)
        if not count:
            continue
        sub_hub = sub / "_index.md"
        label = f"[[{vl.rel(vault, sub_hub)[:-3]}|{sub.name}/]]" if sub_hub.is_file() else f"{sub.name}/"
        lines.append(f"- **{label}** — {count} note{'s' if count != 1 else ''}")
        if depth >= 2:
            lines += [line_for(n, "  ") for n in sort_notes(notes_in(vault, sub), how)]
    return "\n".join(lines) if lines else "_(Nothing here yet.)_"


def plan_hub(vault: Path, hub: Path) -> Tuple[Optional[str], Optional[str]]:
    """Return (new text if it changes, problem if the markers are broken)."""
    text = vl.read_raw(hub)
    start = START_RE.search(text)
    if not start:
        return None, None
    end = END_RE.search(text, start.end())
    if not end:
        return None, "has auto-index:start but no auto-index:end"
    if START_RE.search(text, start.end()):
        return None, "has more than one auto-index block (only one per hub)"
    nl = "\r\n" if "\r\n" in text else "\n"
    body = generate(vault, hub, options(start.group(1))).replace("\n", nl)
    new = text[: start.end()] + nl + body + nl + text[end.start():]
    return (new if new != text else None), None


def main(argv: Optional[List[str]] = None) -> int:
    vl.setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", help="vault folder (default: the vault these tools live in)")
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run, show only)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    vault = vl.resolve_vault(args.vault)

    changes, problems, hubs = [], [], 0
    for hub in vl.iter_notes(vault):
        if hub.name != "_index.md":
            continue
        new, problem = plan_hub(vault, hub)
        r = vl.rel(vault, hub)
        if problem:
            problems.append({"file": r, "problem": problem})
            continue
        if START_RE.search(vl.read_text(hub)):
            hubs += 1
        if new is not None:
            old = vl.read_raw(hub)
            changed = [l for l in difflib.ndiff(old.splitlines(), new.splitlines()) if l[:2] in ("- ", "+ ")]
            diff = f"--- {r}\n" + "\n".join(changed) + "\n"
            changes.append({"file": r, "diff": diff, "_path": hub, "_new": new})
            if args.apply:
                vl.write_atomic(hub, new)

    if args.json:
        vl.print_json({"tool": "hub_index", "applied": args.apply, "hubs_with_markers": hubs,
                       "changes": [{"file": c["file"], "diff": c["diff"]} for c in changes], "problems": problems})
    else:
        for c in changes:
            print(c["diff"] if not args.apply else f"- updated {c['file']}")
        for p in problems:
            print(f"- PROBLEM {p['file']}: {p['problem']}")
        if not changes and not problems:
            print(f"hub_index: all {hubs} hub(s) with auto-index markers are current.")
        elif changes and not args.apply:
            print(f"hub_index: {len(changes)} hub(s) would change. Dry run: nothing written. Add --apply to write.")
        elif changes:
            print(f"hub_index: updated {len(changes)} hub(s).")
    if problems:
        return 1
    return 1 if changes and not args.apply else 0


if __name__ == "__main__":
    sys.exit(main())
