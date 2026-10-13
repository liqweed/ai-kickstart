// Typed, ordered access to the collections, plus small text helpers for pages.
import { getCollection, type CollectionEntry } from "astro:content";

type Name = "catalog" | "connections" | "combos" | "prompts" | "releases" | "phases" | "rounds" | "skills";

export async function ordered<N extends Name>(name: N): Promise<CollectionEntry<N>[]> {
  const list = (await getCollection(name)) as CollectionEntry<N>[];
  return list.sort((a, b) => (a.data as { order: number }).order - (b.data as { order: number }).order);
}

/** A prompt from the library by id, e.g. "harness/the-main-one". Fails the build if it's missing. */
export async function prompt(id: string) {
  for (const g of await ordered("prompts")) {
    const p = g.data.prompts.find((x) => x.id === id);
    if (p) return p;
  }
  throw new Error(`site: prompt "${id}" not found in site/src/content/prompts.md`);
}

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/** Inline Markdown from the kit (**bold**, *em*, `code`, [text](https://…)) to safe HTML. */
export function inline(md: string): string {
  return esc(md)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>")
    .replace(/\[([^\]]+)\]\((https:\/\/[^)\s]+)\)/g, '<a href="$2">$1</a>');
}

/** "2026-10-12" -> "October 2026". */
export const monthYear = (iso: string) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString("en-GB", { month: "long", year: "numeric", timeZone: "UTC" });
