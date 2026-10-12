# Design: Claude Design upload packages

Two briefs, built with the "frame the problem, don't pre-bake the answer" method: numbered `00`–`05` Markdown files, images only in `assets/`, and an "argue your choice" section (`04 §3`) for every open decision.

| Package | For | Run |
|---|---|---|
| [`website-claude-design-package/`](website-claude-design-package/) | ai-kickstart.me | **First** |
| [`app-claude-design-package/`](app-claude-design-package/) | Desktop companion app (tinyjs) | **Second**, after the website identity is approved |

## How to run

1. **Website.** Upload the whole `website-claude-design-package/` folder to a new Claude Design project and ask it to build the prototype per `04 §6` and `05`.
2. **Review against reality** (Phase 2). Check the prototype against `03` and the live kit, and note gaps.
3. **Correct additively** (Phase 3). Send *"keep A, B, C; add D, E"*. **Never re-run the same brief.**
4. **Hand the identity to the app brief.** Export screenshots and any tokens of the approved website into `app-claude-design-package/assets/website/`. The app's `00` and `01` then treat that identity as binding. Without that folder, the app brief leaves identity open.
5. **App.** Upload `app-claude-design-package/` to a new project, then repeat steps 2–3.

## Anti-prescription audit (done before handing over)

| Where | Before | After |
|---|---|---|
| Website `00` | Was going to bind the current guide's look (serif, violet, cards) | The current look is a **reference only** (`assets/current-guide-*.jpg`); "evolve vs replace" is an argued decision (`04 §3.7`) |
| Website `01` | Draft listed the 8 current pages as the screens | Replaced with jobs to be done; the page structure is open (`04 §3.1`) |
| App `01` | Draft named a "dashboard home" | Described the job ("one next thing"); the app's shape is open and the dashboard default is explicitly challenged (`04 §3.1`) |
| App `04 §4` | "Native window chrome" | Removed. A visual choice, not a runtime constraint |
| Both `04 §3` | — | Zero "strong default / best for / I propose" hedges (grep-checked) |

**Binding on purpose** (product facts, not design): voice, credit line, accessibility, no third-party requests, static/no-build front end, `file://`-safe guide, local-only app with the vault's Markdown as the source of truth, and the app's limited file-write rules.
