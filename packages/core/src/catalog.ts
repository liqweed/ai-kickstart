import { isSeparatorRow, slug, tableCells } from "./text.ts";

export interface CatalogItem {
  /** Stable id, `area/function`, used to remember picks. */
  id: string;
  name: string;
  /** Inline Markdown (may contain **bold**, *italics*, `code`). */
  desc: string;
  /** "S", "M", "L" or a move like "S→M". */
  level: string;
}

export interface CatalogArea {
  id: string;
  emoji: string;
  name: string;
  items: CatalogItem[];
}

const HEADER_FIRST_CELLS = new Set(["Function", "Profession"]);

/** Parse `vault/_system/kickstart/function-catalog.md`: one `## <emoji> <area>` per area, then a 3-column table. */
export function parseCatalog(md: string): CatalogArea[] {
  const areas: CatalogArea[] = [];
  let area: CatalogArea | null = null;
  for (const line of md.split(/\r?\n/)) {
    const h = line.match(/^##\s+(\S+)\s+(.+?)\s*$/);
    if (h) {
      area = { id: slug(h[2]), emoji: h[1], name: h[2], items: [] };
      areas.push(area);
      continue;
    }
    const cells = tableCells(line);
    if (!area || !cells || cells.length !== 3 || isSeparatorRow(cells) || HEADER_FIRST_CELLS.has(cells[0])) continue;
    const [name, desc, level] = cells;
    area.items.push({ id: `${area.id}/${slug(name)}`, name, desc, level });
  }
  return areas.filter((a) => a.items.length > 0);
}

/** Does an item's level ("S→M") include the given level letter? */
export function hasLevel(item: Pick<CatalogItem, "level">, level: string): boolean {
  return item.level.split(/→|->/).map((s) => s.trim()).includes(level);
}
