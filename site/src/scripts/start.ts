// Start page: the two choices (computer, way of using AI), or "Welcome back" once setup is done.
import type { Os, Path } from "../lib/choices.ts";
import { $, $$, copyText, detectOs, flash, load, olderThan, save, setupFinished, setupLabel, siteVersion } from "./store.ts";

export function initStart() {
  const root = $("[data-start]");
  if (!root) return;
  let s = load();
  let os: Os = s.os ?? detectOs();
  const chooser = $("[data-start-chooser]", root)!;
  const welcome = $("[data-start-welcome]", root)!;

  const render = () => {
    for (const pill of $$("[data-os-pick]", root)) pill.setAttribute("aria-pressed", String(pill.dataset.osPick === os));
    for (const a of $$<HTMLAnchorElement>("[data-path-pick]", root)) a.href = `/setup/#${os}-${a.dataset.pathPick}`;
    $("[data-os-hint]", root)!.textContent = os === "phone" ? "(setup needs a computer)" : s.os ? "(remembered on this device)" : "(guessed from your browser)";
    $("[data-phone-note]", root)!.hidden = os !== "phone";
  };

  $("[data-os-group]", root)!.hidden = false;
  for (const pill of $$("[data-os-pick]", root)) {
    pill.addEventListener("click", () => {
      os = pill.dataset.osPick as Os;
      s = save({ os });
      render();
    });
  }
  for (const a of $$<HTMLAnchorElement>("[data-path-pick]", root)) {
    a.addEventListener("click", () => save({ os, path: a.dataset.pathPick as Path }));
  }
  const share = $<HTMLButtonElement>("[data-share]", root);
  share?.addEventListener("click", async () => {
    const url = `${location.origin}/setup/${s.path ? "#" + s.path : ""}`;
    if (navigator.share) {
      try {
        await navigator.share({ title: "AI Kickstart setup", url });
        return;
      } catch {
        /* cancelled: fall back to copying */
      }
    }
    flash(share, (await copyText(url)) ? "Link copied ✓" : "Copy failed");
  });

  if (setupFinished(s)) {
    chooser.hidden = true;
    welcome.hidden = false;
    $("[data-setup-label]", welcome)!.textContent = setupLabel(s, os);
    const note = $("[data-welcome-update]", welcome)!;
    if (s.kitVersion && olderThan(s.kitVersion, siteVersion())) {
      $("[data-installed]", note)!.textContent = s.kitVersion;
      note.hidden = false;
    }
    $("[data-show-chooser]", welcome)!.addEventListener("click", () => {
      welcome.hidden = true;
      chooser.hidden = false;
      $("h2", chooser)?.focus();
    });
  }
  render();
}
