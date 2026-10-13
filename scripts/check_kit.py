#!/usr/bin/env python3
"""Consistency checks for the AI Kickstart kit. Exit 1 on any failure.

1. version  - VERSION matches the START-HERE.html footer, the README credit line, CHANGELOG.md and vault/_system/kickstart/kit-version.md
2. links    - every relative href/src in START-HERE.html points to an existing file
3. offline  - START-HERE.html loads no external resources (stylesheets, scripts, images, fonts, iframes)
4. skills   - every skill in vault/_system/skills/ has name+description frontmatter and is listed in vault/AGENTS.md
5. prompts  - every prompt on START-HERE.html is in site/src/content/prompts.md, word for word
6. plan     - docs/master-plan.md holds open work only: every row has an open status and a unique ID
7. ownership - kit_update.py and packages/core/src/update.ts agree on which files are the person's
8. tools    - the vault tools pass their self-test, the template vault lints clean, and its hubs are current
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = ROOT / "START-HERE.html"
errors = []


def fail(check, msg):
    errors.append(f"[{check}] {msg}")


def check_version():
    version = (ROOT / "VERSION").read_text().strip()
    if f"AI Kickstart · v{version} ·" not in START.read_text():
        fail("version", f"START-HERE.html footer is not v{version}")
    if f"v{version}," not in (ROOT / "README.md").read_text():
        fail("version", f"README.md credit line is not v{version}")
    if not re.search(rf"^## v{re.escape(version)}\b", (ROOT / "CHANGELOG.md").read_text(), re.M):
        fail("version", f"CHANGELOG.md has no '## v{version}' section")
    note = (ROOT / "vault/_system/kickstart/kit-version.md").read_text()
    if f'kit_version: "{version}"' not in note or f"AI Kickstart v{version}**" not in note:
        fail("version", f"vault/_system/kickstart/kit-version.md is not v{version} (frontmatter and text)")
    return version


ATTR = re.compile(r'\b(href|src)\s*=\s*"([^"]+)"', re.I)
RESOURCE_TAG = re.compile(r'<(link|script|img|iframe|source|video|audio)\b[^>]*>', re.I)


def check_links_and_offline():
    text = START.read_text()
    for _attr, url in ATTR.findall(text):
        url = html.unescape(url)
        if re.match(r"^(https?:|mailto:|#|javascript:)", url):
            continue
        if not (ROOT / url.split("#")[0]).exists():
            fail("links", f"START-HERE.html -> {url} (missing)")
    for m in RESOURCE_TAG.finditer(text):
        if re.search(r'\b(href|src)\s*=\s*"(https?:)?//', m.group(0), re.I):
            fail("offline", f"START-HERE.html loads an external resource: {m.group(0)[:90]}")
    if re.search(r"(@import|url\()\s*['\"]?(https?:)?//", text):
        fail("offline", "START-HERE.html references external CSS or a font/image URL")
    if (ROOT / "guide").exists():
        fail("offline", "guide/ is back: the zip ships one offline page, START-HERE.html (K12)")


def check_skills():
    agents = (ROOT / "vault/AGENTS.md").read_text()
    skills = sorted((ROOT / "vault/_system/skills").glob("*/SKILL.md"))
    for skill in skills:
        slug = skill.parent.name
        head = skill.read_text().split("---")
        front = head[1] if len(head) > 2 else ""
        if not re.search(rf"^name:\s*{re.escape(slug)}\s*$", front, re.M):
            fail("skills", f"{slug}: frontmatter 'name' missing or != folder name")
        if not re.search(r"^description:\s*\S", front, re.M):
            fail("skills", f"{slug}: frontmatter 'description' missing")
        if f"`{slug}`" not in agents:
            fail("skills", f"{slug}: not listed in vault/AGENTS.md")
    return len(skills)


def prompts_from_md():
    text = (ROOT / "site/src/content/prompts.md").read_text()
    found, label, block = set(), None, None
    for line in text.splitlines():
        if block is not None:
            if line.strip() == "```":
                found.add((label, "\n".join(block)))
                block = None
            else:
                block.append(line)
        elif line.startswith("### "):
            label = line[4:].strip()
        elif line.startswith("```") and label:
            block = []
    return found


def prompts_from_start():
    pairs = re.findall(r'<div class="bar"><span>(.*?)</span></div>\s*<pre>(.*?)</pre>', START.read_text(), re.S)
    return {(html.unescape(label), html.unescape(body)) for label, body in pairs}


def check_prompts():
    md, start = prompts_from_md(), prompts_from_start()
    if not start:
        fail("prompts", "START-HERE.html has no prompt boxes (the check's pattern may be stale)")
    for label, _ in sorted(start - md):
        fail("prompts", f"START-HERE.html prompt differs from site/src/content/prompts.md: {label}")
    return len(md)


def check_ownership():
    """kit_update.py (manual updates) and update.ts (the app) must agree on which files are the person's."""
    ts = (ROOT / "packages/core/src/update.ts").read_text()
    block = re.search(r"const PERSON_OWNED: RegExp\[\] = \[(.*?)\];", ts, re.S)
    js = [s.replace("\\/", "/") for s in re.findall(r"^\s*/(.+)/,\s*$", block.group(1), re.M)] if block else []
    py = re.findall(r're\.compile\(r"(.+?)"\)', (ROOT / "vault/_system/tools/kit_update.py").read_text())
    if not js or js != py:
        fail("ownership", f"PERSON_OWNED differs: update.ts {js} vs kit_update.py {py}")
    return len(py)


OPEN = {"next", "doing", "todo", "blocked", "idea"}


def check_plan():
    ids, rows = set(), 0
    for n, line in enumerate((ROOT / "docs/master-plan.md").read_text().splitlines(), 1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        m = re.match(r"^([A-Z]+\d+[a-z]?(?:\.\d+)?)\b", cells[0]) if line.startswith("|") else None
        if not m or len(cells) < 5:
            continue
        rows += 1
        status = cells[-1].split(":")[0].strip().lower()
        if status not in OPEN:
            fail("plan", f"docs/master-plan.md:{n} {m.group(1)} has status '{cells[-1]}'. Done items are deleted (log them in docs/journal.md)")
        if m.group(1) in ids:
            fail("plan", f"docs/master-plan.md:{n} duplicate ID {m.group(1)}")
        ids.add(m.group(1))
    return rows


def check_tools():
    tools = ROOT / "vault/_system/tools"
    runs = [
        ("self-test", [sys.executable, str(tools / "selftest.py")]),
        ("template vault lint", [sys.executable, str(tools / "vault_lint.py"), "--strict", "--max", "0"]),
        ("hubs current", [sys.executable, str(tools / "hub_index.py")]),
    ]
    for name, cmd in runs:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            fail("tools", f"{name} failed:\n{(r.stdout + r.stderr).strip()[-1500:]}")
    for leftover in (ROOT / "vault").rglob("__pycache__"):
        fail("tools", f"{leftover.relative_to(ROOT)} exists (tools must set sys.dont_write_bytecode)")
    return len([p for p in tools.glob("*.py") if not p.name.startswith("_") and p.name not in ("vaultlib.py", "selftest.py")])


def main():
    version = check_version()
    check_links_and_offline()
    n_skills = check_skills()
    n_prompts = check_prompts()
    n_plan = check_plan()
    check_ownership()
    n_tools = check_tools()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"check_kit: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"check_kit: OK (v{version}, {n_skills} skills, {n_prompts} prompts, {n_plan} open plan items, {n_tools} tools)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
