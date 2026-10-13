import { readdirSync, readFileSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { addedSteps, baselineOf, buildManifest, hashText, kindOf, planUpdate, type KitManifest } from "../src/index.ts";

const vaultDir = fileURLToPath(new URL("../../../vault/", import.meta.url));
const template = readdirSync(vaultDir, { recursive: true, withFileTypes: true })
  .filter((e) => e.isFile() && e.name !== ".DS_Store" && !e.parentPath.includes("__pycache__"))
  .map((e) => {
    const abs = join(e.parentPath, e.name);
    return { path: relative(vaultDir, abs).split(sep).join("/"), text: readFileSync(abs, "utf8") };
  });
const files = (edits: Record<string, (text: string) => string>) =>
  template.map((f) => ({ path: f.path, text: edits[f.path]?.(f.text) ?? f.text }));
const hashes = async (fs: { path: string; text: string }[]) =>
  Object.fromEntries(await Promise.all(fs.map(async (f) => [f.path, await hashText(f.text)] as const)));

const PLAN = "_system/HARNESS-PLAN.md";
const WEEKLY = "_system/skills/weekly-review/SKILL.md";
const withoutP40 = (md: string) => md.replace(/^- \[ \] \*\*P4\.0 [^\n]*\n(?: {2}[^\n]*\n)*/m, "");

describe("which files are the person's", () => {
  it("keeps the plan, profile, indexes, AGENTS.md and answers with the person", () => {
    for (const p of [PLAN, "AGENTS.md", "_system/index.md", "_system/profile/GOALS.md", "01-life/people/_index.md", "_system/tools/README.md", "_system/kickstart/answers/round-1-2026-10-14.md"]) {
      expect(kindOf(p), p).toBe("person");
    }
  });
  it("treats skills, rounds, catalogs, templates, tools and explainers as the kit's", () => {
    for (const p of [WEEKLY, "_system/profile/README.md", "_system/kickstart/round-5-checkin.md", "_system/templates/Person.md", "_system/tools/recent.py", "CLAUDE.md", "06-reference/Working with AI - Tips & Insights.md"]) {
      expect(kindOf(p), p).toBe("kit");
    }
  });
});

describe("hashing", () => {
  it("is sha256 over the text, ignoring line-ending style", async () => {
    expect(await hashText("abc")).toBe("sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    expect(await hashText("a\r\nb\rc\n")).toBe(await hashText("a\nb\nc\n"));
  });
});

describe("the prototype's v1.1 → v1.2 update (scenario 8)", async () => {
  // v1.1: today's template without P4.0. v1.2: P4.0 back, a better weekly-review skill, 14 more kit files changed.
  const changed = [
    // kit-version.md is left out to keep the prototype's numbers; in a real release it changes too.
    ...template.map((f) => f.path).filter((p) => p.startsWith("_system/kickstart/") && kindOf(p) === "kit" && !p.endsWith("kit-version.md")),
    "06-reference/Working with AI - Tips & Insights.md",
    ...["harness", "vault-save", "vault-query", "people", "skill-builder"].map((s) => `_system/skills/${s}/SKILL.md`),
  ];
  const v11 = files({ [PLAN]: withoutP40 });
  const v12 = files({
    ...Object.fromEntries(changed.map((p) => [p, (t: string) => t + "\nImproved in v1.2.\n"])),
    [WEEKLY]: (t) => t + "\n- Look back at the week's lessons.\n",
  });
  const old = await buildManifest("1.1", v11);
  const next = await buildManifest("1.2", v12);

  // Sam's vault a few weeks in: an edited skill, a filled-in plan and profile, CRLF on one untouched file.
  const vault = await hashes(
    v11.map((f) => {
      if (f.path === WEEKLY) return { ...f, text: f.text + "\n- Plan family dinners for the week.\n" };
      if (f.path === PLAN) return { ...f, text: f.text.replace("- [ ] **P0.1 ", "- [x] **P0.1 ") };
      if (f.path === "_system/profile/GOALS.md") return { ...f, text: f.text + "\n- Calmer weekday evenings.\n" };
      if (f.path === "_system/kickstart/round-5-checkin.md") return { ...f, text: f.text.replace(/\n/g, "\r\n") };
      return f;
    }),
  );
  const plan = planUpdate({ baseline: baselineOf(old), vault, next });
  const by = (action: string) => plan.files.filter((f) => f.action === action).map((f) => f.path);

  it("has 14 untouched kit files to update, 1 conflict, 1 hand-off", () => {
    expect(changed).toHaveLength(14);
    expect(plan.to).toBe("1.2");
    expect(by("update").sort()).toEqual([...changed].sort());
    expect(by("conflict")).toEqual([WEEKLY]);
    expect(by("merge")).toEqual([PLAN]);
    expect(plan.count).toMatchObject({ update: 14, conflict: 1, merge: 1, add: 0, removed: 0, retired: 0 });
    expect(plan.count.unchanged).toBe(template.length - 16);
  });
  it("leaves the person's own edits alone when the kit didn't change that file", () => {
    expect(plan.files.find((f) => f.path === "_system/profile/GOALS.md")?.action).toBe("unchanged");
  });
  it("still sees a CRLF copy of an untouched file as untouched", () => {
    expect(plan.files.find((f) => f.path === "_system/kickstart/round-5-checkin.md")?.action).toBe("update");
  });
  it("finds P4.0 as the step to hand to the AI, exactly as written", () => {
    const added = addedSteps(v11.find((f) => f.path === PLAN)!.text, v12.find((f) => f.path === PLAN)!.text);
    expect(added.map((s) => s.id)).toEqual(["P4.0"]);
    expect(added[0].markdown).toMatch(/^- \[ \] \*\*P4\.0 Explore what you could connect\.\*\*.*\n {2}Done when: /);
  });
  it("is clean afterwards: the new baseline plans nothing", () => {
    const after = planUpdate({ baseline: baselineOf(next), vault: baselineOf(next), next });
    expect(after.count.unchanged).toBe(template.length);
  });
});

describe("planner edge cases", () => {
  const m = (version: string, files: [string, string][]): KitManifest => ({
    version,
    files: files.map(([path, hash]) => ({ path, hash, kind: kindOf(path) })),
  });
  const old = m("1", [["a.md", "h1"], ["gone.md", "g1"], ["deleted.md", "d1"], [PLAN, "p1"]]);

  it("adds new files, respects deletions, retires dropped files, and spots a clash", () => {
    const next = m("2", [["a.md", "h2"], ["deleted.md", "d2"], [PLAN, "p1"], ["new.md", "n2"], ["clash.md", "c2"]]);
    const plan = planUpdate({
      baseline: baselineOf(old),
      vault: { "a.md": "h1", "gone.md": "g1", [PLAN]: "mine", "clash.md": "theirs" },
      next,
    });
    expect(Object.fromEntries(plan.files.map((f) => [f.path, f.action]))).toEqual({
      "a.md": "update",
      "clash.md": "conflict",
      "deleted.md": "removed",
      "gone.md": "retired",
      "new.md": "add",
      [PLAN]: "unchanged",
    });
  });
  it("calls a file the person already brought up to date unchanged", () => {
    const plan = planUpdate({ baseline: baselineOf(old), vault: { "a.md": "h2" }, next: m("2", [["a.md", "h2"]]) });
    expect(plan.files[0].action).toBe("unchanged");
  });
});
