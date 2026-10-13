import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import {
  hasLevel, parseCatalog, parseChangelog, parseConnections, riskOf, parseFrontmatter, parsePhases, parsePrompts, parseRounds, slug, splitPlaceholders,
} from "../src/index.ts";

const repo = (p: string) => readFileSync(new URL(`../../../${p}`, import.meta.url), "utf8");

describe("catalog", () => {
  const areas = parseCatalog(repo("vault/_system/kickstart/function-catalog.md"));
  const items = areas.flatMap((a) => a.items);

  it("reads the real catalog: 16 areas, 104 functions", () => {
    expect(areas).toHaveLength(16);
    expect(items).toHaveLength(104);
  });
  it("splits emoji from the area name", () => {
    expect(areas[0]).toMatchObject({ emoji: "🧭", name: "Daily rhythm & focus", id: "daily-rhythm-focus" });
    expect(areas.find((a) => a.name.startsWith("Kids"))?.emoji).toBe("👨‍👩‍👧");
  });
  it("gives every function a unique id", () => {
    expect(new Set(items.map((i) => i.id)).size).toBe(items.length);
  });
  it("keeps profession rows and skips header rows", () => {
    expect(items.some((i) => i.name === "Teacher")).toBe(true);
    expect(items.some((i) => i.name === "Function" || i.name === "Profession")).toBe(false);
  });
  it("matches levels including moves", () => {
    expect(hasLevel({ level: "S→M" }, "M")).toBe(true);
    expect(hasLevel({ level: "S" }, "M")).toBe(false);
  });
});

describe("connections catalog", () => {
  const { groups, combos } = parseConnections(repo("vault/_system/kickstart/connections-catalog.md"));
  const items = groups.flatMap((g) => g.items);

  it("reads every group and connection, and nothing from the legend", () => {
    expect(groups.length).toBeGreaterThanOrEqual(10);
    expect(items.length).toBeGreaterThanOrEqual(30);
    expect(groups[0]).toMatchObject({ emoji: "📅", name: "Time & plans", id: "time-plans" });
    expect(groups.some((g) => /how to read|combos|free public/i.test(g.name))).toBe(false);
  });
  it("fills every field of every connection", () => {
    for (const c of items) {
      for (const k of ["examples", "unlocks", "try", "via", "start", "riskText", "level"] as const) {
        expect(c[k], `${c.id} ${k}`).toBeTruthy();
      }
      expect(c.level).toMatch(/^[SML](→[SML])?$/);
    }
  });
  it("gives every connection a unique id", () => {
    expect(new Set(items.map((i) => i.id)).size).toBe(items.length);
  });
  it("reads the combos table", () => {
    expect(combos.length).toBeGreaterThanOrEqual(8);
    expect(combos[0]).toEqual({ pair: "Calendar + Maps", what: expect.stringContaining("Leave by") });
  });
  it("ranks risk by the highest level named", () => {
    expect(riskOf("Low to medium")).toBe("medium");
    expect(riskOf("Medium to high, depending on what's stored")).toBe("high");
    expect(riskOf("Low. Feed content is untrusted data.")).toBe("low");
    expect(riskOf("High once it can act: it's your physical home.")).toBe("high");
  });
});

describe("changelog", () => {
  it("reads versions newest first", () => {
    const r = parseChangelog(repo("CHANGELOG.md"));
    expect(r[0].version).toBe(`v${repo("VERSION").trim()}`);
    expect(r[0].date).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(r.at(-1)?.version).toBe("v1.0");
    expect(r[0].items.length).toBeGreaterThan(0);
  });
});

describe("harness phases", () => {
  it("reads P0–P7 from the plan", () => {
    const p = parsePhases(repo("vault/_system/HARNESS-PLAN.md"));
    expect(p.map((x) => x.id)).toEqual(["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]);
    expect(p[0]).toMatchObject({ name: "Foundations" });
  });
});

describe("interview rounds", () => {
  it("reads five rounds with readable names", () => {
    const r = parseRounds(repo("vault/_system/kickstart/interview-protocol.md"));
    expect(r.map((x) => x.n)).toEqual([1, 2, 3, 4, 5]);
    expect(r[0].name).toBe("Getting to know you");
  });
});

describe("prompts", () => {
  const groups = parsePrompts(repo("site/src/content/prompts.md"));
  it("reads 6 groups and 40 prompts", () => {
    expect(groups).toHaveLength(6);
    expect(groups.flatMap((g) => g.prompts)).toHaveLength(40);
  });
  it("keeps multi-line text and notes", () => {
    const first = groups[0].prompts[0];
    expect(first.label).toBe("First contact");
    expect(first.text.split("\n")).toHaveLength(4);
    expect(groups.flatMap((g) => g.prompts).find((p) => p.label.startsWith("Express"))?.note).toBe("Rounds 1 and 2 merged");
  });
  it("splits placeholders", () => {
    expect(splitPlaceholders("Plan <who> for <day>.")).toEqual([
      { kind: "text", value: "Plan " }, { kind: "slot", name: "who" },
      { kind: "text", value: " for " }, { kind: "slot", name: "day" }, { kind: "text", value: "." },
    ]);
  });
});

describe("text helpers", () => {
  it("slugs labels", () => expect(slug('"What should I do now?"')).toBe("what-should-i-do-now"));
  it("reads simple frontmatter", () => {
    expect(parseFrontmatter("---\nname: harness\ndescription: Drive the plan\n---\n# x")).toEqual({ name: "harness", description: "Drive the plan" });
  });
});
