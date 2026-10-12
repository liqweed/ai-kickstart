import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import {
  hasLevel, parseCatalog, parseChangelog, parseFrontmatter, parsePhases, parsePrompts, parseRounds, slug, splitPlaceholders,
} from "../src/index.ts";

const repo = (p: string) => readFileSync(new URL(`../../../${p}`, import.meta.url), "utf8");

describe("catalog", () => {
  const areas = parseCatalog(repo("vault/_system/kickstart/function-catalog.md"));
  const items = areas.flatMap((a) => a.items);

  it("reads the real catalog: 16 areas, 103 functions", () => {
    expect(areas).toHaveLength(16);
    expect(items).toHaveLength(103);
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
  it("reads 6 groups and 36 prompts", () => {
    expect(groups).toHaveLength(6);
    expect(groups.flatMap((g) => g.prompts)).toHaveLength(36);
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
