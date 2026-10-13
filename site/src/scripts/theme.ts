// Theme toggle: follow the system → light → dark. The choice lives in this browser only; the inline
// script in Base.astro applies it before the first paint.
import { announce, $ } from "./store.ts";

type Mode = "auto" | "light" | "dark";
const KEY = "aik.site.theme";
const NEXT: Record<Mode, Mode> = { auto: "light", light: "dark", dark: "auto" };
const NAME: Record<Mode, string> = { auto: "same as your system", light: "light", dark: "dark" };

function stored(): Mode {
  try {
    const t = localStorage.getItem(KEY);
    return t === "light" || t === "dark" ? t : "auto";
  } catch {
    return "auto";
  }
}

export function initTheme() {
  const btn = $<HTMLButtonElement>("[data-theme-toggle]");
  if (!btn) return;
  const label = $("[data-theme-label]", btn)!;

  const show = (mode: Mode) => {
    document.documentElement.dataset.kk = mode;
    btn.dataset.mode = mode;
    label.textContent = `Colours: ${NAME[mode]}. Switch to ${NAME[NEXT[mode]]}.`;
    btn.title = `Colours: ${NAME[mode]}`;
  };

  show(stored());
  btn.hidden = false;
  btn.addEventListener("click", () => {
    const mode = NEXT[btn.dataset.mode as Mode] ?? "auto";
    try {
      if (mode === "auto") localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, mode);
    } catch {
      /* storage off: it still switches, just won't be remembered */
    }
    show(mode);
    announce(`Colours: ${NAME[mode]}`);
  });
}
