// What's new: say which version this browser downloaded, if we know.
import { $, load } from "./store.ts";

export function initNews() {
  const el = $("[data-installed-line]");
  const v = load().kitVersion;
  if (el && v) {
    el.textContent = ` Your vault was set up with ${v}.`;
  }
}
