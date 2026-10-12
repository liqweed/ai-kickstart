// "Your setup": the step companion. Progress, computer and AI path live in this browser;
// a link like /setup/#windows-a-3 carries them to another device.
import { OS, PATHS, STEPS, type Os, type Path, type StepId } from "../lib/choices.ts";
import { refillPrompts } from "./prompts.ts";
import { $, $$, announce, copyText, currentStep, detectOs, flash, load, save, siteVersion, type State } from "./store.ts";

const IDS = STEPS.map((x) => x.id) as StepId[];

/** "#mac-b-3" -> os, path, step number (each part optional, any order). */
function readHash(): { os?: Os; path?: Path; step?: number } {
  const out: { os?: Os; path?: Path; step?: number } = {};
  for (const part of location.hash.replace(/^#/, "").split("-")) {
    if (part in OS) out.os = part as Os;
    else if (part in PATHS) out.path = part as Path;
    else if (/^\d+$/.test(part)) out.step = Math.min(Math.max(Number(part), 1), IDS.length);
  }
  return out;
}

export function initSetup() {
  const root = $(".setup[data-os]");
  if (!root) return;

  let s: State = load();
  const h = readHash();
  if (h.os || h.path || h.step) {
    s = save({
      os: h.os ?? s.os,
      path: h.path ?? s.path,
      ...(h.step ? { done: IDS.slice(0, h.step - 1) } : {}),
    });
  }
  let os: Os = s.os ?? detectOs();
  const steps = $$("[data-step]", root);

  const shareUrl = () => {
    const cur = currentStep(s);
    const n = cur === -1 ? IDS.length : cur + 1;
    return `${location.origin}/setup/#${os === "phone" ? "" : os + "-"}${s.path ?? "b"}-${n}`;
  };

  /** openCurrent: expand only the current step (on load and after ticking), never while someone is reading. */
  const render = (openCurrent: boolean) => {
    root.dataset.os = os;
    root.dataset.path = s.path ?? "b";
    for (const pill of $$("[data-set-os]", root)) pill.setAttribute("aria-pressed", String(pill.dataset.setOs === os));
    for (const pill of $$("[data-set-path]", root)) pill.setAttribute("aria-pressed", String(pill.dataset.setPath === s.path));
    $("[data-choose-path]", root)!.hidden = !!s.path;
    $("[data-steps-area]", root)!.hidden = !s.path;
    $("[data-phone-steps]", root)!.hidden = os !== "phone";

    const cur = currentStep(s);
    steps.forEach((li, i) => {
      const id = li.dataset.step as StepId;
      const done = s.done.includes(id);
      const isCur = i === cur;
      $("[data-mark]", li)!.textContent = done ? "[x]" : isCur ? "[/]" : "[ ]";
      $("[data-status]", li)!.textContent = done ? " · done" : isCur ? " · you are here" : "";
      li.dataset.current = String(isCur);
      $("[data-actions]", li)!.hidden = false;
      $("[data-tick]", li)!.hidden = done;
      $("[data-untick]", li)!.hidden = !done;
      if (openCurrent) ($("details", li) as HTMLDetailsElement).open = isCur;
    });
    $("[data-progress]", root)!.textContent =
      cur === -1 ? `[x] ${IDS.length} of ${IDS.length} done` : `[/] ${s.done.length} of ${IDS.length} done · now: step ${cur + 1}, ${STEPS[cur].title}`;
    $("[data-all-done]", root)!.hidden = cur !== -1;
    $("[data-share-url]", root)!.textContent = shareUrl();
    if (s.path) history.replaceState(null, "", `#${os}-${s.path}`);
    refillPrompts();
  };

  const scrollToCurrent = () => {
    const cur = currentStep(s);
    const target = cur === -1 ? $("[data-all-done]", root) : steps[cur];
    target?.scrollIntoView({ block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  };

  for (const g of $$("[data-pills]", root)) g.hidden = false;
  for (const pill of $$("[data-set-os]", root)) {
    pill.addEventListener("click", () => {
      os = pill.dataset.setOs as Os;
      s = save({ os });
      render(false);
    });
  }
  for (const pill of $$("[data-set-path]", root)) {
    pill.addEventListener("click", () => {
      s = save({ os, path: pill.dataset.setPath as Path });
      render(false);
    });
  }
  steps.forEach((li, i) => {
    const id = li.dataset.step as StepId;
    $("[data-tick]", li)!.addEventListener("click", () => {
      s = save({
        done: [...s.done.filter((d) => d !== id), id],
        ...(id === "kit" && !s.kitVersion ? { kitVersion: siteVersion() } : {}),
      });
      announce(`Step ${i + 1} done.`);
      render(true);
      scrollToCurrent();
    });
    $("[data-untick]", li)!.addEventListener("click", () => {
      s = save({ done: s.done.filter((d) => d !== id) });
      render(false);
    });
  });
  for (const btn of $$<HTMLButtonElement>("[data-share-setup]", root)) {
    btn.addEventListener("click", async () => {
      const url = shareUrl();
      if (navigator.share && os === "phone") {
        try {
          await navigator.share({ title: "AI Kickstart setup", url });
          return;
        } catch {
          /* cancelled: copy instead */
        }
      }
      flash(btn, (await copyText(url)) ? "Link copied ✓" : "Copy failed. Select the link above.");
    });
  }

  render(true);
  if (s.done.length) scrollToCurrent();
}
