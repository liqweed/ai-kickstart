import { isSeparatorRow, tableCells } from "./text.ts";

export interface Phase {
  id: string;
  name: string;
  goal: string;
  exit: string;
  time: string;
}

/** Parse the "Phases at a glance" table of `vault/_system/HARNESS-PLAN.md`. */
export function parsePhases(md: string): Phase[] {
  const start = md.indexOf("## Phases at a glance");
  if (start < 0) return [];
  const phases: Phase[] = [];
  for (const line of md.slice(start).split(/\r?\n/).slice(1)) {
    if (line.startsWith("## ") || line.startsWith("---")) break;
    const cells = tableCells(line);
    if (!cells || cells.length < 4 || isSeparatorRow(cells)) continue;
    const m = cells[0].match(/^\*\*(P\d+)\*\*\s*(.+)$/);
    if (!m) continue;
    phases.push({ id: m[1], name: m[2], goal: cells[1], exit: cells[2], time: cells[3] });
  }
  return phases;
}
