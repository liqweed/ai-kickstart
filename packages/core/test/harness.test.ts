import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { nextStep, parsePlan, type HarnessPlan } from "../src/index.ts";

const read = (p: string) => readFileSync(new URL(p, import.meta.url), "utf8");
const template = read("../../../vault/_system/HARNESS-PLAN.md");
const filled = read("./fixtures/harness-plan-filled.md");
const step = (plan: HarnessPlan, id: string) => plan.phases.flatMap((p) => p.steps).find((s) => s.id === id);

describe("harness plan: the vault template", () => {
  const plan = parsePlan(template);
  const steps = plan.phases.flatMap((p) => p.steps);

  it("parses cleanly", () => {
    expect(plan.problems).toEqual([]);
    expect(plan.usable).toBe(true);
  });
  it("reads P0–P7 with their glance-table goals", () => {
    expect(plan.phases.map((p) => p.id)).toEqual(["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]);
    expect(plan.phases[1]).toMatchObject({ name: "Get to know you", time: "4 sessions" });
    expect(plan.phases[7].name).toBe("Evolve");
  });
  it("reads all 36 steps, all to do, skipping the P4.x template", () => {
    expect(steps).toHaveLength(36);
    expect(steps.every((s) => s.status === "todo")).toBe(true);
    expect(steps.some((s) => s.id.endsWith(".x"))).toBe(false);
    expect(new Set(steps.map((s) => s.id)).size).toBe(36);
  });
  it("splits title, Done when and Check", () => {
    expect(step(plan, "P0.1")).toMatchObject({
      phase: "P0",
      title: "Install Obsidian and open this folder as a vault",
      doneWhen: "Obsidian shows `_system/`, `01-life/`, … in the sidebar.",
      check: "open `_system/index.md` in Obsidian.",
    });
    expect(step(plan, "P1.1")).toMatchObject({ title: "Round 1, Getting to know you", doneWhen: undefined });
    expect(step(plan, "P1.1")?.check).toMatch(/^`_system\/kickstart\/answers/);
  });
  it("reads an empty Now, backlog and session log (the commented template is not an entry)", () => {
    expect(plan.now).toEqual({ phase: "P0", nextStep: "P0.1" });
    expect(plan.frontmatter).toMatchObject({ current_phase: "P0", next_step: "P0.1" });
    expect(plan.backlog).toEqual([]);
    expect(plan.sessions).toEqual([]);
  });
  it("starts at P0.1", () => {
    expect(nextStep(plan)?.id).toBe("P0.1");
  });
});

describe("harness plan: filled in, a month later", () => {
  const plan = parsePlan(filled);

  it("parses cleanly", () => {
    expect(plan.problems).toEqual([]);
  });
  it("reads every status mark", () => {
    expect(step(plan, "P0.1")?.status).toBe("done");
    expect(step(plan, "P0.6")).toMatchObject({ status: "skipped", title: "Tools check" });
    expect(step(plan, "P0.6")?.detail).toMatch(/^— skipped: chat-only for now\./);
    expect(step(plan, "P1.3")?.status).toBe("doing");
    expect(step(plan, "P4.0")?.status).toBe("blocked");
    expect(step(plan, "P4.0")?.detail).toContain("Blocked: waiting for a work laptop policy answer.");
  });
  it("reads sub-steps written by the synthesis, with the ★", () => {
    expect(step(plan, "P2.3")).toBeUndefined();
    expect(step(plan, "P2.3a")).toMatchObject({ star: true, title: "First win #1, part 1: a shared shopping list", check: "two items added from a phone." });
    expect(step(plan, "P2.3b")?.star).toBe(false);
  });
  it("reads the Now table", () => {
    expect(plan.now).toEqual({ phase: "P1", nextStep: "P1.3", lastSession: "2026-11-04 · P1.2 Round 2" });
  });
  it("reads the backlog by column name, with ★ as a flag", () => {
    expect(plan.backlog).toHaveLength(3);
    expect(plan.backlog[0]).toEqual({ id: "B1", area: "Home", idea: "Never run out of the basics", value: 3, effort: "S", phase: "P2", status: "planned", star: true });
    expect(plan.backlog.filter((b) => b.star).map((b) => b.id)).toEqual(["B1"]);
  });
  it("reads the session log newest first, joining wrapped lines", () => {
    expect(plan.sessions.map((s) => s.date)).toEqual(["2026-11-04", "2026-10-20"]);
    expect(plan.sessions[0]).toMatchObject({
      stepId: "P1.2",
      title: "P1.2 Round 2, Where could help feel good?",
      did: "ran round 2; ranked five areas. Home logistics came out on top.",
      checked: "`GOALS.md` drafted and read back.",
      next: 'P1.3 — say "Continue my harness plan"',
    });
    expect(plan.sessions[1].notes).toBe("skipped P0.6, chat-only.");
  });
  it("picks the step in progress", () => {
    expect(nextStep(plan)?.id).toBe("P1.3");
  });
  it("reads Windows line endings the same", () => {
    expect(parsePlan(filled.replace(/\n/g, "\r\n"))).toEqual(plan);
  });
});

describe("harness plan: what the AI might get wrong", () => {
  const edit = (from: string, to: string) => {
    if (!filled.includes(from)) throw new Error(`fixture lacks: ${from}`);
    return parsePlan(filled.replace(from, to));
  };

  it("falls back to the skill's rule when Now points at a finished step", () => {
    expect(nextStep(edit("| **Next step** | P1.3 |", "| **Next step** | P1.1 |"))?.id).toBe("P1.3");
  });
  it("moves on past a finished phase", () => {
    const plan = edit("- [/] **P1.3 ", "- [x] **P1.3 ");
    expect(nextStep(plan)?.id).toBe("P1.4");
  });
  it("reports an unknown mark, a duplicate step and a dangling Now, but stays usable", () => {
    const plan = parsePlan(
      filled
        .replace("- [ ] **P1.4 ", "- [~] **P1.4 ")
        .replace("- [ ] **P1.5 ", "- [ ] **P1.4 ")
        .replace("| **Next step** | P1.3 |", "| **Next step** | P9.9 |"),
    );
    expect(plan.problems).toEqual([
      "P1.4 has an unknown mark [~]; read as \"to do\"",
      "Step P1.4 appears more than once",
      "\"Now\" points to P9.9, which isn't in the plan",
    ]);
    expect(plan.usable).toBe(true);
  });
  it("is unusable, without throwing, when the phases are gone", () => {
    const plan = parsePlan("# Harness Plan\n\nI rewrote this as prose.\n");
    expect(plan.usable).toBe(false);
    expect(plan.problems).toHaveLength(4);
    expect(nextStep(plan)).toBeUndefined();
  });
});
