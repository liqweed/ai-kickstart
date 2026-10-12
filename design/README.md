# Design: Claude Design upload packages

Two briefs, built with the "frame the problem, don't pre-bake the answer" method: numbered `00`–`05` Markdown files, images only in `assets/`, and an "argue your choice" section (`04 §3`) for every open decision.

| Package | For | Run |
|---|---|---|
| [`website-claude-design-package/`](website-claude-design-package/) | ai-kickstart.me | **First** |
| [`app-claude-design-package/`](app-claude-design-package/) | Desktop companion app (tinyjs) | **Second**, in the **same** project, after the website identity is approved |
| [`prototype/`](prototype/) | Round-2 export: website + app in one project, one stylesheet, approved 2026-10-12, with review notes | Reference for K9 and K10 |
| [`claude-design-round-2-prompt.md`](claude-design-round-2-prompt.md) | Round 2: website fixes + the app as new pages | Paste into the same project |
| [`logo-quiver-prompt.md`](logo-quiver-prompt.md) | Logo mark (favicon, app icon) via QuiverAI | Before round 2 if possible |

## How to run

1. **Website.** Upload the whole `website-claude-design-package/` folder to a new Claude Design project and ask it to build the prototype per `04 §6` and `05`.
2. **Review against reality** (Phase 2). Check the prototype against `03` and the live kit, and note gaps.
3. **Correct additively** (Phase 3). Send *"keep A, B, C; add D, E"*. **Never re-run the same brief.**
4. **App, in the same project.** Upload `app-claude-design-package/` into the website's Claude Design project and paste [`claude-design-round-2-prompt.md`](claude-design-round-2-prompt.md). The approved site's tokens and primitives are then binding for the app, with no screenshot hand-off. *(Fallback for a separate project: export screenshots and tokens into `app-claude-design-package/assets/website/`.)*
5. **Import.** Export the project into `prototype/` (site and app together, since they share `kickstart.css`), and record the review in its README. Then repeat steps 2–3 as needed.

## Anti-prescription audit (done before handing over)

| Where | Before | After |
|---|---|---|
| Website `00` | Was going to bind the current guide's look (serif, violet, cards) | The current look is a **reference only** (`assets/current-guide-*.jpg`); "evolve vs replace" is an argued decision (`04 §3.7`) |
| Website `01` | Draft listed the 8 current pages as the screens | Replaced with jobs to be done; the page structure is open (`04 §3.1`) |
| App `01` | Draft named a "dashboard home" | Described the job ("one next thing"); the app's shape is open and the dashboard default is explicitly challenged (`04 §3.1`) |
| App `04 §4` | "Native window chrome" | Removed. A visual choice, not a runtime constraint |
| Both `04 §3` | — | Zero "strong default / best for / I propose" hedges (grep-checked) |

**Binding on purpose** (product facts, not design): voice, credit line, accessibility, no third-party requests, static/no-build front end, `file://`-safe guide, local-only app with the vault's Markdown as the source of truth, and the app's limited file-write rules.
