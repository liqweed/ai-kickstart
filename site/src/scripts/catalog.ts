// Ideas menu: tick ideas, filter by effort, and copy the picks as a message for interview Round 2.
import { hasLevel } from "@ai-kickstart/core";
import { $, $$, announce, copyText, flash, load, save } from "./store.ts";

export function initCatalog() {
  const root = $("[data-catalog]");
  if (!root) return;
  const rows = $$<HTMLLabelElement>("[data-row]", root);
  const byId = new Map(rows.map((r) => [r.dataset.id!, r]));
  let picks = load().picks.filter((id) => byId.has(id));
  let level = "all";

  const dialog = $<HTMLDialogElement>("[data-pick-dialog]")!;
  const message = () =>
    `These ideas from the AI Kickstart catalog made me think "oh, yes":\n${picks
      .map((id) => `- ${byId.get(id)!.dataset.name} (${byId.get(id)!.dataset.areaName})`)
      .join("\n")}\n\nPlease use them in Round 2 of my kickstart interview.`;

  const setPicks = (next: string[], msg?: string) => {
    picks = next;
    save({ picks });
    render();
    if (msg) announce(msg);
  };

  const render = () => {
    const set = new Set(picks);
    for (const r of rows) {
      const on = set.has(r.dataset.id!);
      r.dataset.on = String(on);
      $<HTMLInputElement>("input", r)!.checked = on;
      r.hidden = level !== "all" && !hasLevel({ level: r.dataset.rowLevel! }, level);
    }
    for (const area of $$("[data-area]", root)) {
      const mine = $$<HTMLElement>("[data-row]", area);
      const n = mine.filter((r) => set.has(r.dataset.id!)).length;
      area.hidden = mine.every((r) => r.hidden);
      $("[data-area-count]", area)!.textContent = `${mine.length} ideas${n ? ` · ${n} picked` : ""}`;
      const jump = $(`[data-jump="${area.id}"]`, root);
      if (jump) {
        jump.hidden = area.hidden;
        $("[data-jump-picked]", jump)!.textContent = n ? ` · ${n} ✓` : "";
      }
    }
    const areas = new Set(picks.map((id) => byId.get(id)!.dataset.areaName)).size;
    const has = picks.length > 0;
    $("[data-picks-text]", root)!.textContent = has
      ? `${picks.length} picked from ${areas} area${areas > 1 ? "s" : ""}. Saved on this device.`
      : "Nothing picked yet. Tick anything that makes you think “oh, yes”. Most people end up with 5–10.";
    $("[data-tray-text]")!.textContent = has ? `${picks.length} picked · saved on this device` : "Tick ideas you like. They collect here.";
    for (const el of $$("[data-has-picks]")) el.hidden = !has;
    const list = $("[data-picks-list]", root)!;
    list.replaceChildren(
      ...picks.map((id) => {
        const r = byId.get(id)!;
        const li = document.createElement("li");
        const name = document.createElement("span");
        name.className = "picks__name";
        const area = document.createElement("span");
        area.textContent = r.dataset.areaName!;
        name.append(r.dataset.name!, area);
        const x = document.createElement("button");
        x.type = "button";
        x.className = "x";
        x.textContent = "×";
        x.setAttribute("aria-label", `Remove ${r.dataset.name}`);
        x.addEventListener("click", () => setPicks(picks.filter((p) => p !== id), `${r.dataset.name} removed`));
        li.append(name, x);
        return li;
      }),
    );
    $("[data-pick-message]")!.textContent = message();
    for (const pill of $$("[data-level]", root)) pill.setAttribute("aria-pressed", String(pill.dataset.level === level));
  };

  for (const r of rows) {
    $<HTMLInputElement>("input", r)!.addEventListener("change", (e) => {
      const on = (e.target as HTMLInputElement).checked;
      const id = r.dataset.id!;
      setPicks(on ? [...picks.filter((p) => p !== id), id] : picks.filter((p) => p !== id));
    });
  }
  $("[data-filters]", root)!.hidden = false;
  for (const pill of $$("[data-level]", root)) {
    pill.addEventListener("click", () => {
      level = pill.dataset.level!;
      render();
    });
  }
  for (const btn of $$<HTMLButtonElement>("[data-copy-picks]")) {
    btn.addEventListener("click", async () => {
      const ok = await copyText(message());
      flash(btn, ok ? (btn.dataset.short ? "Copied ✓" : "Copied ✓ Paste it in Round 2") : "Copy failed", 3000);
      if (ok) announce("Copied. Paste it when Round 2 starts.");
    });
  }
  for (const btn of $$("[data-open-msg]")) btn.addEventListener("click", () => dialog.showModal());
  for (const btn of $$("[data-close-msg]")) btn.addEventListener("click", () => dialog.close());
  for (const btn of $$("[data-clear-picks]")) {
    btn.addEventListener("click", () => {
      if (dialog.open) dialog.close();
      setPicks([], "Picks cleared");
    });
  }
  $("[data-tray]")!.hidden = false;
  render();
}
