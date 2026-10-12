// Header strips: "Setup paused at step 3" and "A new version is out". Shown only when they help.
import { STEPS } from "../lib/choices.ts";
import { $, currentStep, detectOs, load, olderThan, setupFinished, setupLabel, siteVersion } from "./store.ts";

export function initBanners() {
  const s = load();
  const place = document.documentElement.dataset.place;
  const os = s.os ?? detectOs();

  const resume = $("[data-banner=resume]");
  const cur = currentStep(s);
  if (resume && s.path && s.done.length > 0 && cur >= 0 && place !== "setup") {
    $("[data-resume-step]", resume)!.textContent = `step ${cur + 1} of ${STEPS.length}: ${STEPS[cur].title}`;
    $("[data-setup-label]", resume)!.textContent = setupLabel(s, os);
    $<HTMLAnchorElement>("[data-resume-link]", resume)!.href = `/setup/#${os}-${s.path}`;
    resume.hidden = false;
  }

  const update = $("[data-banner=update]");
  const behind = !!s.kitVersion && olderThan(s.kitVersion, siteVersion());
  // On Start, the "Welcome back" card says the same thing, so the strip stays away.
  if (update && behind && place !== "new" && !(place === "start" && setupFinished(s))) {
    $("[data-installed]", update)!.textContent = s.kitVersion!;
    update.hidden = false;
  }
}
