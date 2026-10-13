"""Shared helpers for the vault tools. Not a tool itself: the tools import it.

Reads:    vault notes (Markdown), only when a tool asks
Writes:   nothing (write_atomic is called only by tools running with --apply)
Network:  none
Secrets:  none

Standard library only, Python 3.9+, macOS / Windows / Linux.
The frontmatter parser understands the simple YAML this vault uses (key: value,
[inline, lists], block lists, quoted strings). It is not a full YAML parser:
anything nested is kept as raw text, never guessed at.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

# Folders no tool ever walks into. Hidden folders (".obsidian", ".git", ".trash") are skipped too.
SKIP_DIRS = {"node_modules", "__pycache__", ".venv", "venv"}

# Notes that are not "content" and so don't follow the note rules (frontmatter, links).
SYSTEM_EXEMPT_PREFIXES = ("_system/skills/", "_system/tools/", "_system/templates/")
SYSTEM_EXEMPT_FILES = {"AGENTS.md", "CLAUDE.md"}

NOTE_EXT = ".md"
ATTACHMENT_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".heic", ".avif",
    ".pdf", ".mp3", ".m4a", ".wav", ".ogg", ".webm", ".mp4", ".mov",
    ".csv", ".xlsx", ".docx", ".pptx", ".canvas", ".base",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- setup

def setup_stdout() -> None:
    """Print UTF-8 everywhere (Windows consoles default to a legacy code page)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


def default_vault() -> Path:
    """The vault this copy of the tools lives in: <vault>/_system/tools/vaultlib.py."""
    return Path(__file__).resolve().parents[2]


def resolve_vault(arg: Optional[str]) -> Path:
    vault = Path(arg).expanduser().resolve() if arg else default_vault()
    if not vault.is_dir():
        raise SystemExit(f"error: vault folder not found: {vault}")
    return vault


def parse_today(arg: Optional[str]) -> _dt.date:
    """--today YYYY-MM-DD makes output reproducible (tests, re-running last week's review)."""
    if not arg:
        return _dt.date.today()
    try:
        return _dt.date.fromisoformat(arg)
    except ValueError:
        raise SystemExit(f"error: --today must be YYYY-MM-DD, got {arg!r}")


# --------------------------------------------------------------------------- walking

def rel(vault: Path, path: Path) -> str:
    """Vault-relative path with forward slashes on every OS."""
    return path.relative_to(vault).as_posix()


def iter_files(vault: Path, exts: Optional[Iterable[str]] = None) -> Iterator[Path]:
    wanted = {e.lower() for e in exts} if exts else None
    for root, dirs, files in os.walk(vault):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS)
        for name in sorted(files):
            if name.startswith("."):
                continue
            p = Path(root) / name
            if wanted is None or p.suffix.lower() in wanted:
                yield p


def iter_notes(vault: Path) -> Iterator[Path]:
    return iter_files(vault, {NOTE_EXT})


def is_system_exempt(relpath: str) -> bool:
    return relpath in SYSTEM_EXEMPT_FILES or relpath.startswith(SYSTEM_EXEMPT_PREFIXES)


def read_text(path: Path) -> str:
    """Note text with line endings normalised to \\n (for reading)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[1:] if text.startswith("﻿") else text


def read_raw(path: Path) -> str:
    """Note text exactly as stored, Windows line endings included (for tools that write it back)."""
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        text = f.read()
    return text[1:] if text.startswith("﻿") else text


def write_atomic(path: Path, text: str) -> None:
    """Write via a temporary file and rename, so a crash never leaves half a note."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def file_date(path: Path, kind: str = "mtime") -> _dt.date:
    st = path.stat()
    ts = getattr(st, "st_birthtime", None) if kind == "birth" else None
    return _dt.date.fromtimestamp(ts if ts else st.st_mtime)


# --------------------------------------------------------------------------- frontmatter

@dataclass
class Frontmatter:
    present: bool = False
    data: Dict[str, object] = field(default_factory=dict)
    problems: List[str] = field(default_factory=list)
    raw: str = ""          # the text between the --- lines
    end_offset: int = 0    # index in the note text where the body starts


def _scalar(value: str) -> object:
    v = value.strip()
    if v == "" or v in ("~", "null", "Null", "NULL"):
        return ""
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [str(_scalar(x)) for x in _split_inline_list(inner)]
    return v


def _split_inline_list(inner: str) -> List[str]:
    out, buf, quote = [], "", ""
    for ch in inner:
        if quote:
            buf += ch
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == ",":
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [x.strip() for x in out if x.strip()]


KEY_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_\- .]*?)\s*:(?:\s+(.*)|\s*)$")


def parse_frontmatter(text: str) -> Frontmatter:
    """Read the YAML block at the very top of a note, if there is one."""
    fm = Frontmatter()
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        return fm
    lines = text.splitlines(keepends=True)
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") in ("---", "..."):
            end = i
            break
    fm.present = True
    if end is None:
        fm.problems.append("frontmatter starts with --- but never closes")
        return fm
    fm.raw = "".join(lines[1:end])
    fm.end_offset = sum(len(l) for l in lines[: end + 1])
    key = None
    for n, line in enumerate(lines[1:end], 2):
        s = line.rstrip("\r\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        if s[0] in " \t":
            stripped = s.strip()
            if key is not None and stripped.startswith("- "):
                cur = fm.data.get(key)
                if not isinstance(cur, list):
                    cur = [] if cur in ("", None) else [str(cur)]
                cur.append(str(_scalar(stripped[2:])))
                fm.data[key] = cur
            elif key is not None:
                prev = fm.data.get(key)
                fm.data[key] = (str(prev) + "\n" if prev not in ("", None) else "") + stripped
            continue
        if s.startswith("- ") and key is not None:
            cur = fm.data.get(key)
            if not isinstance(cur, list):
                cur = [] if cur in ("", None) else [str(cur)]
            cur.append(str(_scalar(s[2:])))
            fm.data[key] = cur
            continue
        m = KEY_RE.match(s)
        if not m:
            fm.problems.append(f"line {n}: not 'key: value' ({s[:60]!r})")
            key = None
            continue
        key = m.group(1).strip()
        if key in fm.data:
            fm.problems.append(f"line {n}: key '{key}' appears twice")
        fm.data[key] = _scalar(m.group(2) or "")
    return fm


def as_list(value: object) -> List[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [p.strip() for p in str(value).split(",") if p.strip()]


def parse_date(value: object) -> Optional[_dt.date]:
    """YYYY-MM-DD, or a datetime starting with it. Returns None for anything else."""
    if isinstance(value, list) or value in (None, ""):
        return None
    s = str(value).strip()[:10]
    if not DATE_RE.match(s):
        return None
    try:
        return _dt.date.fromisoformat(s)
    except ValueError:
        return None


def parse_month_day(value: object) -> Optional[Tuple[Optional[int], int, int]]:
    """Birthday-style dates: 'YYYY-MM-DD' or 'MM-DD' -> (year or None, month, day)."""
    if isinstance(value, list) or value in (None, ""):
        return None
    s = str(value).strip()
    m = re.match(r"^(?:(\d{4})-)?(\d{2})-(\d{2})$", s)
    if not m:
        return None
    year = int(m.group(1)) if m.group(1) else None
    month, day = int(m.group(2)), int(m.group(3))
    try:
        _dt.date(2000, month, day)  # leap year: allows 02-29
    except ValueError:
        return None
    return year, month, day


def next_occurrence(month: int, day: int, today: _dt.date) -> _dt.date:
    """Next date (today or later) for a yearly event. 29 Feb falls on 28 Feb in other years."""
    for year in (today.year, today.year + 1):
        try:
            d = _dt.date(year, month, day)
        except ValueError:
            d = _dt.date(year, 2, 28)
        if d >= today:
            return d
    raise AssertionError("unreachable")


# --------------------------------------------------------------------------- note body helpers

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def strip_code(text: str) -> str:
    """Blank out fenced code blocks, inline code and HTML comments, keeping line numbers."""
    text = COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence:
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence):
                fence = None
            out.append("")
            continue
        if m:
            fence = m.group(2)
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(out)


WIKILINK_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
MDLINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass
class Link:
    target: str     # the note or file name, without #heading / |alias
    line: int
    embed: bool


def wikilinks(text: str) -> List[Link]:
    """[[Target]], [[Target|alias]], [[Target#Heading]], ![[embed]]. Ignores code and comments.
    In tables, Obsidian writes the alias pipe as \\| ; that's handled too."""
    links = []
    for n, line in enumerate(strip_code(text).split("\n"), 1):
        for m in WIKILINK_RE.finditer(line):
            inner = m.group(2).replace("\\|", "|")
            target = inner.split("|", 1)[0]
            target = re.split(r"#|\^", target, maxsplit=1)[0].strip().rstrip("\\").strip()
            if target:
                links.append(Link(target, n, m.group(1) == "!"))
    return links


def markdown_links(text: str) -> List[str]:
    """Targets of [label](relative/path) links, external URLs left out."""
    out = []
    for m in MDLINK_RE.finditer(strip_code(text)):
        url = m.group(1)
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("#"):
            continue
        from urllib.parse import unquote
        out.append(unquote(url.split("#", 1)[0]))
    return out


TASK_RE = re.compile(r"^(\s*)[-*+] \[(.)\] (.*)$")


@dataclass
class Task:
    status: str     # " " open, "x" done, "/" in progress, "-" cancelled, ">" deferred, "?" question
    text: str
    line: int


def tasks(text: str) -> List[Task]:
    out = []
    for n, line in enumerate(strip_code(text).split("\n"), 1):
        m = TASK_RE.match(line)
        if m:
            out.append(Task(m.group(2).lower(), m.group(3).strip(), n))
    return out


# --------------------------------------------------------------------------- link resolution

class LinkResolver:
    """Resolve wikilinks the way Obsidian does: by file name anywhere in the vault,
    or by path when the link contains a slash. Case-insensitive."""

    def __init__(self, vault: Path):
        self.vault = vault
        self.by_name: Dict[str, List[str]] = {}
        self.by_path: Dict[str, str] = {}
        for p in iter_files(vault):
            r = rel(vault, p)
            ext = p.suffix.lower()
            keys = [r.lower()]
            if ext == NOTE_EXT:
                keys.append(r[: -len(NOTE_EXT)].lower())
            for k in keys:
                self.by_path[k] = r
            names = [p.name.lower()]
            if ext == NOTE_EXT:
                names.append(p.stem.lower())
            for nm in names:
                self.by_name.setdefault(nm, []).append(r)

    def resolve(self, target: str) -> Optional[str]:
        t = target.strip().replace("\\", "/").lstrip("/").lower()
        if not t:
            return None
        if t in self.by_path:
            return self.by_path[t]
        if "/" in t:
            for k, r in self.by_path.items():
                if k.endswith("/" + t):
                    return r
            return None
        hits = self.by_name.get(t)
        return hits[0] if hits else None


# --------------------------------------------------------------------------- output

def print_json(obj: object) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def note_link(relpath: str) -> str:
    """An Obsidian link to a note, by path so it's never ambiguous."""
    target = relpath[: -len(NOTE_EXT)] if relpath.endswith(NOTE_EXT) else relpath
    label = Path(target).name
    return f"[[{target}|{label}]]" if "/" in target else f"[[{target}]]"


def load_config(vault: Path, name: str) -> Dict[str, object]:
    """Optional settings from config/<name>.md frontmatter (the owner can edit it in Obsidian)."""
    path = vault / "config" / f"{name}.md"
    if not path.is_file():
        return {}
    return parse_frontmatter(read_text(path)).data
