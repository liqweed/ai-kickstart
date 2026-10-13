#!/usr/bin/env python3
"""Checks for the built website (site/dist), run after `pnpm build`. Exit 1 on any failure.

1. offline  - no page or stylesheet loads anything from another origin (links to other sites are fine)
2. csp      - every page carries the Content-Security-Policy <meta> Astro generates, and it hashes every inline script
3. links    - every internal href/src points to a file in dist/
4. counts   - the catalog and prompt counts on the pages match the kit
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site/dist"
errors = []
RESOURCE_TAG = re.compile(r"<(link|script|img|iframe|source|video|audio)\b[^>]*>", re.I)
INLINE_SCRIPT = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.S | re.I)
ATTR = re.compile(r'\b(href|src)\s*=\s*"([^"]+)"', re.I)


def target(url):
    path = url.split("#")[0].split("?")[0]
    if not path:
        return None
    p = DIST / path.lstrip("/")
    return p / "index.html" if path.endswith("/") else p


def main():
    if not (DIST / "index.html").exists():
        print("check_site: site/dist not built (run `pnpm build`)", file=sys.stderr)
        return 1
    pages = sorted(DIST.rglob("*.html"))
    for page in pages:
        rel = page.relative_to(DIST)
        text = page.read_text()
        for m in RESOURCE_TAG.finditer(text):
            tag = m.group(0)
            if re.search(r'\b(href|src)\s*=\s*"(https?:)?//', tag, re.I) and not re.search(r'rel="(canonical|alternate)"', tag):
                errors.append(f"[offline] {rel} loads an external resource: {tag[:100]}")
        if 'http-equiv="content-security-policy"' not in text:
            errors.append(f"[csp] {rel} has no CSP meta tag")
        for body in INLINE_SCRIPT.findall(text):
            digest = base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()
            if body.strip() and f"'sha256-{digest}'" not in text:
                errors.append(f"[csp] {rel} has an inline script the CSP doesn't hash: {body[:60]}")
        for _attr, url in ATTR.findall(text):
            if re.match(r"^(https?:|mailto:|#|data:)", url):
                continue
            t = target(url)
            if t and not t.exists():
                errors.append(f"[links] {rel} -> {url} (missing)")
    for css in DIST.rglob("*.css"):
        if re.search(r"(@import|url\()\s*['\"]?(https?:)?//", css.read_text()):
            errors.append(f"[offline] {css.relative_to(DIST)} references an external URL")

    ideas = (DIST / "ideas/index.html").read_text()
    md_items = sum(1 for line in (ROOT / "vault/_system/kickstart/function-catalog.md").read_text().splitlines()
                   if line.startswith("| ") and not line.startswith(("| Function", "| Profession", "|---")))
    if ideas.count("data-row ") != md_items and ideas.count('data-row=""') != md_items:
        n = len(re.findall(r"\bdata-row\b", ideas))
        if n != md_items:
            errors.append(f"[counts] ideas page shows {n} functions, the catalog has {md_items}")
    prompts_md = (ROOT / "site/src/content/prompts.md").read_text().count("\n### ")
    n_cards = (DIST / "prompts/index.html").read_text().count("data-prompt")
    if n_cards != prompts_md:
        errors.append(f"[counts] prompts page shows {n_cards} prompts, prompts.md has {prompts_md}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"check_site: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"check_site: OK ({len(pages)} pages, {md_items} catalog functions, {prompts_md} prompts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
