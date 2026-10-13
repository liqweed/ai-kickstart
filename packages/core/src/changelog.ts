export interface ReleaseItem {
  /** Inline Markdown. */
  text: string;
  /** Nested bullets, inline Markdown each. */
  sub: string[];
}

export interface Release {
  version: string;
  date: string;
  items: ReleaseItem[];
}

/** Parse `CHANGELOG.md`: `## vX.Y — YYYY-MM-DD` followed by `- ` bullets, with indented `- ` sub-bullets one level deep. Newest first, as written. */
export function parseChangelog(md: string): Release[] {
  const releases: Release[] = [];
  let cur: Release | null = null;
  for (const line of md.split(/\r?\n/)) {
    const h = line.match(/^##\s+(v\d+(?:\.\d+)*)\s*(?:[—–-]\s*(\S+))?/);
    if (h) {
      cur = { version: h[1], date: h[2] ?? "", items: [] };
      releases.push(cur);
      continue;
    }
    if (line.startsWith("## ")) cur = null;
    if (!cur) continue;
    const last = cur.items.at(-1);
    const b = line.match(/^- (.+)$/);
    const s = line.match(/^\s{2,}- (.+)$/);
    if (b) cur.items.push({ text: b[1].trim(), sub: [] });
    else if (s && last) last.sub.push(s[1].trim());
    else if (/^\s{2,}\S/.test(line) && last) {
      if (last.sub.length) last.sub[last.sub.length - 1] += " " + line.trim();
      else last.text += " " + line.trim();
    }
  }
  return releases;
}
