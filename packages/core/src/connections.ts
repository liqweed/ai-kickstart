import { isSeparatorRow, slug, tableCells } from "./text.ts";

export type Risk = "low" | "medium" | "high";

export interface Connection {
  /** Stable id, `group/connection`. */
  id: string;
  name: string;
  /** Inline Markdown, as written in the catalog. */
  examples: string;
  unlocks: string;
  try: string;
  via: string;
  start: string;
  /** The highest risk named ("Low to medium" → "medium"). */
  risk: Risk;
  /** The full risk line, e.g. "Medium. Shared calendars contain other people's details." */
  riskText: string;
  /** "S", "M", "L" or a move like "S→M". */
  level: string;
}

export interface ConnectionGroup {
  id: string;
  emoji: string;
  name: string;
  items: Connection[];
}

export interface Combo {
  pair: string;
  what: string;
}

const FIELDS: Record<string, keyof Connection> = {
  examples: "examples",
  unlocks: "unlocks",
  try: "try",
  "connect via": "via",
  start: "start",
  risk: "riskText",
  level: "level",
};

/** The highest of Low / Medium / High mentioned at the start of a risk line. */
export function riskOf(text: string): Risk {
  const head = text.split(/[.:]/)[0].toLowerCase();
  if (head.includes("high")) return "high";
  if (head.includes("medium")) return "medium";
  return "low";
}

/**
 * Parse `vault/_system/kickstart/connections-catalog.md`:
 * `## <emoji> <group>` → `### <connection>` → `- **Field:** value` bullets, and a `## Combos` table.
 * Headings without a leading emoji ("How to read an entry", "Combos") end the current group.
 */
export function parseConnections(md: string): { groups: ConnectionGroup[]; combos: Combo[] } {
  const groups: ConnectionGroup[] = [];
  const combos: Combo[] = [];
  let group: ConnectionGroup | null = null;
  let item: Partial<Connection> | null = null;
  let inCombos = false;

  const flush = () => {
    if (group && item?.name) {
      const c = item as Connection;
      c.risk = riskOf(c.riskText ?? "");
      group.items.push(c);
    }
    item = null;
  };

  for (const line of md.split(/\r?\n/)) {
    const h2 = line.match(/^##\s+(.+?)\s*$/);
    if (h2) {
      flush();
      const g = h2[1].match(/^([^\sA-Za-z0-9*_`[]+)\s+(.+)$/);
      group = g ? { id: slug(g[2]), emoji: g[1], name: g[2], items: [] } : null;
      if (group) groups.push(group);
      inCombos = !g && /^combos\b/i.test(h2[1]);
      continue;
    }
    const h3 = line.match(/^###\s+(.+?)\s*$/);
    if (h3 && group) {
      flush();
      item = { id: `${group.id}/${slug(h3[1])}`, name: h3[1] };
      continue;
    }
    const f = line.match(/^-\s+\*\*([^*:]+):\*\*\s*(.*)$/);
    if (f && item) {
      const key = FIELDS[f[1].trim().toLowerCase()];
      if (key) (item as Record<string, string>)[key] = f[2].trim();
      continue;
    }
    if (inCombos) {
      const cells = tableCells(line);
      if (cells && cells.length === 2 && !isSeparatorRow(cells) && cells[0] !== "Combo") combos.push({ pair: cells[0], what: cells[1] });
    }
  }
  flush();
  return { groups: groups.filter((g) => g.items.length > 0), combos };
}
