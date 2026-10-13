import { isSeparatorRow, parseFrontmatter, tableCells } from "./text.ts";

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

// ---------------------------------------------------------------------------
// The whole plan, as the companion app reads it. The person's AI writes this
// file, so the parser is forgiving: it never throws, it collects `problems`,
// and the app decides whether the plan is still `usable`.

export type StepStatus = "todo" | "doing" | "done" | "skipped" | "blocked";

/** The legend's marks: `[ ]` `[/]` `[x]` `[-]` `[?]`. */
export const STEP_MARKS: Record<string, StepStatus> = { " ": "todo", "/": "doing", x: "done", X: "done", "-": "skipped", "?": "blocked" };

export interface Step {
  /** "P0.1", or a sub-step such as "P2.3a". */
  id: string;
  phase: string;
  title: string;
  status: StepStatus;
  /** ★ marks the step to do first. */
  star: boolean;
  /** Everything after the bold title, joined into one line. */
  detail: string;
  doneWhen?: string;
  check?: string;
  /** The step's lines exactly as written, for prompts that copy it ("add it exactly as written"). */
  markdown: string;
}

export interface PlanPhase extends Partial<Omit<Phase, "id" | "name">> {
  id: string;
  name: string;
  steps: Step[];
}

export interface PlanNow {
  /** "P1", from "P1 — Get to know you". */
  phase?: string;
  nextStep?: string;
  /** Why the plan is stuck, or undefined when the cell is empty or "—". */
  blocked?: string;
  lastSession?: string;
}

export interface BacklogItem {
  id: string;
  area: string;
  idea: string;
  value?: number;
  effort: string;
  phase: string;
  status: string;
  star: boolean;
}

export interface SessionEntry {
  date: string;
  /** The heading after the date, e.g. "P0.3 Connect the AI". */
  title: string;
  stepId?: string;
  did?: string;
  checked?: string;
  next?: string;
  notes?: string;
}

export interface HarnessPlan {
  frontmatter: Record<string, string>;
  now: PlanNow;
  phases: PlanPhase[];
  backlog: BacklogItem[];
  /** Newest first, as written. */
  sessions: SessionEntry[];
  /** Plain-language notes on what didn't match the kit's layout. */
  problems: string[];
  /** False when there's no step to show: the app falls back to its "can't read your plan" state. */
  usable: boolean;
}

const empty = (s: string | undefined) => !s || /^[—–-]?$/.test(s.trim());
const dash = (s: string | undefined) => (empty(s) ? undefined : s!.trim());

/** Level-2 sections by heading, with comments removed (the session-log template lives in one). */
function sections(md: string): { heading: string; lines: string[] }[] {
  const out: { heading: string; lines: string[] }[] = [];
  const body = md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "").replace(/<!--[\s\S]*?-->/g, "");
  for (const line of body.split(/\r?\n/)) {
    const h = line.match(/^##\s+(.+?)\s*$/);
    if (h) out.push({ heading: h[1], lines: [] });
    else out.at(-1)?.lines.push(line);
  }
  return out;
}

/** Table rows (cells) in a section, header and separator dropped. */
function rows(lines: string[]): string[][] {
  const table = lines.map(tableCells).filter((c): c is string[] => c !== null && !isSeparatorRow(c));
  return table.slice(1);
}

const STEP_LINE = /^\s*[-*]\s+\[(.)\]\s+(.*)$/;
const STEP_ID = /^(P\d+)\.(\d+[a-z]?)\b/;

function parseSteps(phase: string, lines: string[], problems: string[]): Step[] {
  const steps: Step[] = [];
  let current: { step: Step; parts: string[]; lines: string[] } | null = null;
  const finish = () => {
    if (!current) return;
    const detail = current.parts.join(" ").replace(/\s+/g, " ").trim();
    const done = detail.match(/Done when:\s*(.*?)(?=\s*Check:|$)/);
    const check = detail.match(/Check:\s*(.*)$/);
    Object.assign(current.step, { markdown: current.lines.join("\n"), detail, doneWhen: done?.[1].trim() || undefined, check: check?.[1].trim() || undefined });
    steps.push(current.step);
    current = null;
  };
  for (const line of lines) {
    const m = line.match(STEP_LINE);
    if (m) {
      finish();
      const [, mark, rest] = m;
      // "**P0.1 Title.** detail", or a bold-less "P0.1 Title" an AI may write.
      const bold = rest.match(/^\*\*(.+?)\*\*\s*(.*)$/);
      const head = (bold ? bold[1] : rest).trim();
      const id = head.match(STEP_ID);
      if (!id) {
        if (!/^P\d+\.x\b/.test(head)) problems.push(`A checkbox in ${phase} has no step number: "${head.slice(0, 60)}"`);
        continue;
      }
      const status = STEP_MARKS[mark];
      if (!status) problems.push(`${id[0]} has an unknown mark [${mark}]; read as "to do"`);
      const title = head.slice(id[0].length).replace(/^[\s:.—–-]+/, "").replace(/[.:]$/, "").trim();
      current = {
        step: { id: id[0], phase, title, status: status ?? "todo", star: rest.includes("★"), detail: "", markdown: "" },
        parts: bold ? [bold[2]] : [],
        lines: [line],
      };
    } else if (current && /^\s+\S/.test(line)) {
      current.parts.push(line.trim());
      current.lines.push(line);
    } else if (current && line.trim()) {
      finish();
    }
  }
  finish();
  return steps;
}

function parseNow(lines: string[]): PlanNow {
  const now: PlanNow = {};
  for (const [k = "", v = ""] of lines.map(tableCells).filter((c): c is string[] => c !== null && !isSeparatorRow(c))) {
    const key = k.replace(/\*/g, "").trim().toLowerCase();
    if (key === "current phase") now.phase = v.match(/^P\d+/)?.[0] ?? dash(v);
    else if (key === "next step") now.nextStep = v.match(/^P\d+\.\d+[a-z]?/)?.[0] ?? dash(v);
    else if (key === "blocked") now.blocked = dash(v);
    else if (key === "last session") now.lastSession = dash(v);
  }
  return now;
}

function parseBacklog(lines: string[]): BacklogItem[] {
  const header = lines.map(tableCells).find((c): c is string[] => c !== null)?.map((h) => h.toLowerCase()) ?? [];
  const col = (name: string) => header.findIndex((h) => h.startsWith(name));
  const at = (cells: string[], name: string) => cells[col(name)]?.trim() ?? "";
  return rows(lines)
    .filter((cells) => cells.some((c) => c.trim()))
    .map((cells) => {
      const id = at(cells, "id").replace("★", "").trim();
      const value = Number.parseInt(at(cells, "value"), 10);
      return {
        id,
        area: at(cells, "area"),
        idea: at(cells, "idea").replace("★", "").trim(),
        value: Number.isNaN(value) ? undefined : value,
        effort: at(cells, "effort"),
        phase: at(cells, "phase"),
        status: at(cells, "status"),
        star: cells.some((c) => c.includes("★")),
      };
    });
}

const SESSION_FIELDS: Record<string, keyof SessionEntry> = { did: "did", checked: "checked", next: "next", notes: "notes" };

function parseSessions(lines: string[]): SessionEntry[] {
  const out: SessionEntry[] = [];
  let field: keyof SessionEntry | null = null;
  for (const line of lines) {
    const h = line.match(/^###\s+(\d{4}-\d{2}-\d{2})\s*[—–-]*\s*(.*)$/);
    if (h) {
      out.push({ date: h[1], title: h[2].trim(), stepId: h[2].match(/^P\d+\.\d+[a-z]?/)?.[0] });
      field = null;
      continue;
    }
    const entry = out.at(-1);
    if (!entry) continue;
    const f = line.match(/^[-*]\s+\*\*(\w+):\*\*\s*(.*)$/);
    if (f && SESSION_FIELDS[f[1].toLowerCase()]) {
      field = SESSION_FIELDS[f[1].toLowerCase()];
      (entry as unknown as Record<string, string>)[field] = f[2].trim();
    } else if (field && /^\s+\S/.test(line)) {
      const e = entry as unknown as Record<string, string>;
      e[field] = (e[field] ? e[field] + " " : "") + line.trim().replace(/^[-*]\s+/, "");
    } else if (line.trim()) {
      field = null;
    }
  }
  return out;
}

/** Parse the person's `_system/HARNESS-PLAN.md`. Never throws. */
export function parsePlan(md: string): HarnessPlan {
  const problems: string[] = [];
  const all = sections(md);
  const find = (re: RegExp) => all.find((s) => re.test(s.heading));

  const nowSection = find(/^Now$/i);
  if (!nowSection) problems.push('The "Now" table is missing');
  const now = parseNow(nowSection?.lines ?? []);

  const glance = new Map(parsePhases(md).map((p) => [p.id, p]));
  const phases: PlanPhase[] = [];
  for (const s of all) {
    const m = s.heading.match(/^(P\d+)\s*[—–:-]+\s*(.+)$/);
    if (!m) continue;
    const { goal, exit, time } = glance.get(m[1]) ?? {};
    phases.push({ id: m[1], name: m[2].replace(/\s*\(.*\)$/, ""), goal, exit, time, steps: parseSteps(m[1], s.lines, problems) });
  }

  const steps = phases.flatMap((p) => p.steps);
  const seen = new Set<string>();
  for (const s of steps) {
    if (seen.has(s.id)) problems.push(`Step ${s.id} appears more than once`);
    seen.add(s.id);
  }
  if (now.nextStep && /^P\d/.test(now.nextStep) && !seen.has(now.nextStep)) problems.push(`"Now" points to ${now.nextStep}, which isn't in the plan`);

  const backlog = find(/^Personal backlog/i);
  if (!backlog) problems.push('The "Personal backlog" table is missing');
  const sessions = find(/^Session log/i);
  if (!sessions) problems.push('The "Session log" is missing');
  if (!phases.length) problems.push("No phases found (headings like \"## P0 — Foundations\")");

  return {
    frontmatter: parseFrontmatter(md),
    now,
    phases,
    backlog: parseBacklog(backlog?.lines ?? []),
    sessions: parseSessions(sessions?.lines ?? []),
    problems,
    usable: steps.length > 0,
  };
}

const OPEN: StepStatus[] = ["doing", "todo"];

/**
 * The one next thing. "Now" wins while it names an open step; otherwise the
 * harness skill's rule: the first step in progress or to do, from the current
 * phase onwards. Undefined when every step is done, skipped or blocked.
 */
export function nextStep(plan: HarnessPlan): Step | undefined {
  const steps = plan.phases.flatMap((p) => p.steps);
  const named = steps.find((s) => s.id === plan.now.nextStep);
  if (named && OPEN.includes(named.status)) return named;
  const from = Math.max(0, plan.phases.findIndex((p) => p.id === plan.now.phase));
  const rest = plan.phases.slice(from).flatMap((p) => p.steps);
  return rest.find((s) => s.status === "doing") ?? rest.find((s) => s.status === "todo");
}
