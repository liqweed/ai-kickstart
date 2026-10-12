// What the site remembers, in this browser only (localStorage). No cookies, nothing leaves the device.
import { OS, PATHS, STEPS, type Os, type Path, type StepId } from "../lib/choices.ts";

export interface State {
  os?: Os;
  path?: Path;
  done: StepId[];
  /** Catalog function ids, e.g. "daily-rhythm-focus/morning-briefing". */
  picks: string[];
  /** Site version when the visitor downloaded the kit (ticked step 1): stands in for "your vault's version". */
  kitVersion?: string;
}

const KEY = "aik.site.v1";
const STEP_IDS = STEPS.map((s) => s.id) as StepId[];

export function load(): State {
  let raw: Partial<State> = {};
  try {
    raw = JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    raw = {};
  }
  return {
    os: raw.os && raw.os in OS ? raw.os : undefined,
    path: raw.path && raw.path in PATHS ? raw.path : undefined,
    done: Array.isArray(raw.done) ? raw.done.filter((d): d is StepId => STEP_IDS.includes(d as StepId)) : [],
    picks: Array.isArray(raw.picks) ? raw.picks.filter((p) => typeof p === "string") : [],
    kitVersion: typeof raw.kitVersion === "string" ? raw.kitVersion : undefined,
  };
}

export function save(patch: Partial<State>): State {
  const next = { ...load(), ...patch };
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    /* private mode or storage off: the page still works, it just won't remember */
  }
  return next;
}

/** Index of the first unticked step, or -1 when all are done. */
export const currentStep = (s: State) => STEP_IDS.findIndex((id) => !s.done.includes(id));
export const setupFinished = (s: State) => !!s.path && currentStep(s) === -1;
export const setupLabel = (s: State, os: Os) => `${OS[os]}${s.path ? " · " + PATHS[s.path].short : ""}`;

export function detectOs(): Os {
  const nav = navigator as Navigator & { userAgentData?: { platform?: string; mobile?: boolean } };
  const ua = `${nav.userAgentData?.platform ?? ""} ${navigator.platform} ${navigator.userAgent}`;
  if (nav.userAgentData?.mobile || /iPhone|iPad|iPod|Android/i.test(ua)) return "phone";
  if (/Mac/i.test(ua)) return navigator.maxTouchPoints > 1 ? "phone" : "mac"; // iPadOS reports "Mac"
  if (/Win/i.test(ua)) return "windows";
  if (/Linux|X11|CrOS/i.test(ua)) return "linux";
  return "mac";
}

export const siteVersion = () => document.documentElement.dataset.version ?? "";

/** "v1.1" < "v1.2"? */
export function olderThan(a: string, b: string): boolean {
  const n = (v: string) => v.replace(/^v/, "").split(".").map(Number);
  const [x, y] = [n(a), n(b)];
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    if ((x[i] ?? 0) !== (y[i] ?? 0)) return (x[i] ?? 0) < (y[i] ?? 0);
  }
  return false;
}

export function announce(msg: string) {
  const el = document.querySelector<HTMLElement>("[data-announce]");
  if (!el) return;
  el.textContent = "";
  requestAnimationFrame(() => (el.textContent = msg));
}

export async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.className = "kk-sr";
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try {
      ok = document.execCommand("copy");
    } catch {
      ok = false;
    }
    ta.remove();
    return ok;
  }
}

/** Briefly swap a button's label after copying. */
export function flash(btn: HTMLElement, label: string, ms = 2600) {
  const original = btn.dataset.label ?? btn.textContent ?? "";
  btn.dataset.label = original;
  btn.textContent = label;
  btn.dataset.copied = "true";
  clearTimeout(Number(btn.dataset.timer));
  btn.dataset.timer = String(
    window.setTimeout(() => {
      btn.textContent = original;
      btn.dataset.copied = "false";
    }, ms),
  );
}

export const $ = <T extends Element = HTMLElement>(sel: string, root: ParentNode = document) => root.querySelector<T>(sel);
export const $$ = <T extends Element = HTMLElement>(sel: string, root: ParentNode = document) => [...root.querySelectorAll<T>(sel)];
