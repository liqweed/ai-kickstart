// Every list on the site comes from the kit itself, parsed by @ai-kickstart/core at build time.
// The schemas make the build fail loudly if the kit's Markdown drifts out of shape.
import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { parseCatalog, parseChangelog, parseConnections, parseFrontmatter, parsePhases, parsePrompts, parseRounds } from "@ai-kickstart/core";
import { repoDirs, repoFile } from "./lib/repo.ts";

const withOrder = <T extends object>(list: T[], id: (t: T) => string) => list.map((t, order) => ({ ...t, id: id(t), order }));

const catalog = defineCollection({
  loader: () => withOrder(parseCatalog(repoFile("vault/_system/kickstart/function-catalog.md")), (a) => a.id),
  schema: z.object({
    order: z.number(),
    emoji: z.string(),
    name: z.string(),
    items: z.array(z.object({ id: z.string(), name: z.string().min(1), desc: z.string().min(1), level: z.string().regex(/^[SML](→[SML])?$/) })).min(1),
  }),
});

const LEVEL = z.string().regex(/^[SML](→[SML])?$/);
const connectionsMd = () => parseConnections(repoFile("vault/_system/kickstart/connections-catalog.md"));

const connections = defineCollection({
  loader: () => withOrder(connectionsMd().groups, (g) => g.id),
  schema: z.object({
    order: z.number(),
    emoji: z.string(),
    name: z.string(),
    items: z.array(z.object({
      id: z.string(),
      name: z.string().min(1),
      examples: z.string().min(1),
      unlocks: z.string().min(1),
      try: z.string().min(1),
      via: z.string().min(1),
      start: z.string().min(1),
      risk: z.enum(["low", "medium", "high"]),
      riskText: z.string().min(1),
      level: LEVEL,
    })).min(1),
  }),
});

const combos = defineCollection({
  loader: () => withOrder(connectionsMd().combos, (c) => c.pair),
  schema: z.object({ order: z.number(), pair: z.string().min(1), what: z.string().min(1) }),
});

const prompts = defineCollection({
  loader: () => withOrder(parsePrompts(repoFile("site/src/content/prompts.md")), (g) => g.id),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    prompts: z.array(z.object({ id: z.string(), label: z.string(), note: z.string().optional(), text: z.string().min(1) })).min(1),
  }),
});

const releases = defineCollection({
  loader: () => withOrder(parseChangelog(repoFile("CHANGELOG.md")), (r) => r.version),
  schema: z.object({ order: z.number(), version: z.string(), date: z.string(), items: z.array(z.string()) }),
});

const phases = defineCollection({
  loader: () => withOrder(parsePhases(repoFile("vault/_system/HARNESS-PLAN.md")), (p) => p.id),
  schema: z.object({ order: z.number(), name: z.string(), goal: z.string(), exit: z.string(), time: z.string() }),
});

const rounds = defineCollection({
  loader: () => withOrder(parseRounds(repoFile("vault/_system/kickstart/interview-protocol.md")), (r) => String(r.n)),
  schema: z.object({ order: z.number(), n: z.number(), name: z.string(), goal: z.string(), feeds: z.string() }),
});

const skills = defineCollection({
  loader: () =>
    repoDirs("vault/_system/skills").map((dir, order) => {
      const fm = parseFrontmatter(repoFile(`vault/_system/skills/${dir}/SKILL.md`));
      return { id: dir, order, name: fm.name ?? "", description: fm.description ?? "" };
    }),
  schema: z.object({ order: z.number(), name: z.string().min(1), description: z.string().min(1) }),
});

export const collections = { catalog, connections, combos, prompts, releases, phases, rounds, skills };
