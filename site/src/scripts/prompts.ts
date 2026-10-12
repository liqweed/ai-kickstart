// Prompt cards: placeholders become small text fields; Copy puts the filled-in prompt on the clipboard.
import { OS, PATHS } from "../lib/choices.ts";
import { $, $$, copyText, flash, load } from "./store.ts";

function fillValue(kind: string | undefined): string {
  const s = load();
  if (kind === "os") return s.os && s.os !== "phone" ? OS[s.os] : "";
  if (kind === "tool") return s.path ? PATHS[s.path].tool : "";
  return "";
}

const fit = (input: HTMLInputElement, name: string) => (input.size = Math.max(input.value.length, name.length) + 1);

/** Re-apply pre-fills (after the visitor changes their computer or AI path), unless they typed something. */
export function refillPrompts() {
  for (const input of $$<HTMLInputElement>("input[data-fill]")) {
    if (input.dataset.touched) continue;
    input.value = fillValue(input.dataset.fill);
    fit(input, input.placeholder);
  }
}

function promptText(card: HTMLElement): string {
  const box = $("[data-text]", card);
  if (!box) return "";
  let out = "";
  for (const node of box.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) out += node.textContent;
    else if (node instanceof HTMLElement && node.dataset.slot !== undefined) {
      const v = $<HTMLInputElement>("input", node)?.value.trim();
      out += v || `<${node.dataset.slot}>`;
    } else out += node.textContent;
  }
  return out;
}

export function initPrompts() {
  for (const card of $$("[data-prompt]")) {
    for (const ph of $$("[data-slot]", card)) {
      const name = ph.dataset.slot!;
      const input = document.createElement("input");
      input.type = "text";
      input.placeholder = name;
      input.setAttribute("aria-label", `Fill in: ${name}`);
      if (ph.dataset.fill) {
        input.dataset.fill = ph.dataset.fill;
        input.value = fillValue(ph.dataset.fill);
      }
      fit(input, name);
      input.addEventListener("input", () => {
        input.dataset.touched = "1";
        fit(input, name);
      });
      ph.replaceChildren("<", input, ">");
    }
    const btn = $<HTMLButtonElement>("[data-copy]", card);
    const live = $("[data-live]", card);
    if (!btn) continue;
    btn.hidden = false;
    btn.addEventListener("click", async () => {
      const ok = await copyText(promptText(card));
      flash(btn, ok ? "Copied ✓" : "Select and copy");
      if (live) live.textContent = ok ? "Copied. Paste it into your AI." : "Copying didn't work. Select the text and copy it.";
    });
  }
}
