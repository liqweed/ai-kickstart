export interface Release {
  version: string;
  date: string;
  /** Inline Markdown, one per bullet. */
  items: string[];
}

/** Parse `CHANGELOG.md`: `## vX.Y — YYYY-MM-DD` followed by `- ` bullets. Newest first, as written. */
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
    const b = line.match(/^- (.+)$/);
    if (cur && b) cur.items.push(b[1].trim());
    else if (cur && /^\s{2,}\S/.test(line) && cur.items.length) cur.items[cur.items.length - 1] += " " + line.trim();
  }
  return releases;
}
