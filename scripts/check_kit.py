#!/usr/bin/env python3
"""Consistency checks for the AI Kickstart kit. Exit 1 on any failure.

1. version  - VERSION matches every guide footer, the README credit line and CHANGELOG.md
2. catalog  - vault/_system/kickstart/function-catalog.md and guide/catalog.html list the same functions
3. links    - every relative href/src in guide/*.html and START-HERE.html points to an existing file
4. offline  - the guide loads no external resources (stylesheets, scripts, images, fonts, iframes)
5. skills   - every skill in vault/_system/skills/ has name+description frontmatter and is listed in vault/AGENTS.md
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "guide"
errors = []


def fail(check, msg):
    errors.append(f"[{check}] {msg}")


def check_version():
    version = (ROOT / "VERSION").read_text().strip()
    for page in sorted(GUIDE.glob("*.html")):
        if f"AI Kickstart · v{version} ·" not in page.read_text():
            fail("version", f"{page.relative_to(ROOT)} footer is not v{version}")
    if f"v{version}," not in (ROOT / "README.md").read_text():
        fail("version", f"README.md credit line is not v{version}")
    if not re.search(rf"^## v{re.escape(version)}\b", (ROOT / "CHANGELOG.md").read_text(), re.M):
        fail("version", f"CHANGELOG.md has no '## v{version}' section")
    return version


def catalog_from_md():
    text = (ROOT / "vault/_system/kickstart/function-catalog.md").read_text()
    items, area = set(), None
    for line in text.splitlines():
        if line.startswith("## "):
            area = line[3:].strip()
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if area and line.startswith("|") and len(cells) == 3 and not set(cells[0]) <= set("-") \
                and cells[0] not in ("Function", "Profession"):
            items.add((cells[0], cells[2]))
    return items


def catalog_from_html():
    text = (GUIDE / "catalog.html").read_text()
    rows = re.findall(r'\[\s*"((?:[^"\\]|\\.)*)",\s*"((?:[^"\\]|\\.)*)",\s*"((?:[^"\\]|\\.)*)"\s*\]', text)
    return {(name.replace('\\"', '"'), level) for name, _desc, level in rows}


def check_catalog():
    md, js = catalog_from_md(), catalog_from_html()
    for name, level in sorted(md - js):
        fail("catalog", f"in function-catalog.md but not catalog.html (or level differs): {name} [{level}]")
    for name, level in sorted(js - md):
        fail("catalog", f"in catalog.html but not function-catalog.md (or level differs): {name} [{level}]")
    return len(md)


ATTR = re.compile(r'\b(href|src)\s*=\s*"([^"]+)"', re.I)
RESOURCE_TAG = re.compile(r'<(link|script|img|iframe|source|video|audio)\b[^>]*>', re.I)


def check_links_and_offline():
    pages = sorted(GUIDE.glob("*.html")) + [ROOT / "START-HERE.html"]
    for page in pages:
        text = page.read_text()
        for _attr, url in ATTR.findall(text):
            url = html.unescape(url)
            if re.match(r"^(https?:|mailto:|#|javascript:)", url):
                continue
            target = (page.parent / url.split("#")[0]).resolve()
            if not target.exists():
                fail("links", f"{page.relative_to(ROOT)} -> {url} (missing)")
        for m in RESOURCE_TAG.finditer(text):
            if re.search(r'\b(href|src)\s*=\s*"(https?:)?//', m.group(0), re.I):
                fail("offline", f"{page.relative_to(ROOT)} loads an external resource: {m.group(0)[:90]}")
        if re.search(r"@import\s+url\(\s*['\"]?https?:", text):
            fail("offline", f"{page.relative_to(ROOT)} imports external CSS")
    css = (GUIDE / "assets/kit.css").read_text()
    if re.search(r"url\(\s*['\"]?https?:", css):
        fail("offline", "assets/kit.css references an external URL")
    return len(pages)


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


def main():
    version = check_version()
    n_catalog = check_catalog()
    n_pages = check_links_and_offline()
    n_skills = check_skills()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"check_kit: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"check_kit: OK (v{version}, {n_catalog} catalog functions, {n_pages} pages, {n_skills} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
