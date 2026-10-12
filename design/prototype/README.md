# Prototype: website + companion app (Claude Design, round 2)

The approved design for **ai-kickstart.me** and the **companion app**, exported from one Claude Design project on 2026-10-12. Round 1 (website only) was built from [`../website-claude-design-package/`](../website-claude-design-package/). Round 2 added the app from [`../app-claude-design-package/`](../app-claude-design-package/) with [`../claude-design-round-2-prompt.md`](../claude-design-round-2-prompt.md). Round 1 lives in git history (commit `6ffdf65`, folder `design/website-prototype/`).

This is the **reference for K9** (the Astro port in `site/`) and **K10** (the app). It is not shipped in the zip and not deployed.

| File | What |
|---|---|
| `AI Kickstart Site.dc.html` | The whole site: Start · Your setup · Ideas menu · Prompts · How it works · What's new, plus the Tweaks scenario switcher (6 scenarios, theme) |
| `AI Kickstart App.dc.html` | The app inside a window frame: first run, Next, Plan, Updates, Settings, recovery cards. Tweaks: 13 scenarios, theme, macOS/Windows, 800×560 / 1280×800 |
| `Rationale.dc.html` | Website §3.1–§3.9, the round 2 Part A decisions, and the **Shared system** list |
| `App Rationale.dc.html` | App §3.1–§3.8, the write-rules audit, and which primitives the app reuses or extends |
| `kickstart.css` | **The one stylesheet**: tokens (light + dark) and shared primitives, loaded by every page |
| `Prompt.dc.html`, `Mark.dc.html` | Shared components: the prompt card, the mark (coloured by tokens) |
| `Share Preview.dc.html`, `share-card.png` | Link preview for WhatsApp/iMessage (1200×630), with title and description |
| `kickstart-mark(-dark).svg`, `favicon.svg`, `favicon-16/32(-dark).png`, `app-icon-mac(-dark).svg`, `app-icon-512.png` | The mark and its icon exports |
| `kit-content.js` | Catalog (16 areas, 103) and prompts (6 groups, 36), standing in for build-time Markdown. Unchanged from round 1 |
| `support.js` | Claude Design's prototype runtime. It loads React and Babel from unpkg, so **viewing needs a network connection**. The real site and app must not use it |
| `screenshots/` | Site scenarios at 1280×800 (phone at 390×844, light and dark), the share preview, and app scenarios 1, 3–9 at 800×560 inside the frame |

**To view:** serve the folder (`python3 -m http.server` inside it) and open a `.dc.html` page. Opening from `file://` may block the module import of `kit-content.js`.

## Review, round 2 (2026-10-12)

Verdict: **approved, ready to port.** All five Part A fixes landed, and the app holds to the shared system.

| Round 2 ask | Result |
|---|---|
| 1 · Tray hides the menu | Wide: a sticky "Your picks" column beside the menu. Narrow: a one-row tray. The full message opens in a dialog |
| 2 · Two answers on the chooser | One recommendation (desktop AI app); the hint agrees and names when the chat app fits |
| 3 · Finished setup gets the pitch | Only the action card changes to "Welcome back": the everyday sentence, what's new, two doors. "Show the first steps" brings the chooser back |
| 4 · Mark | The Quiver logo, adopted as a token-coloured component, flat green. It still reads at 16 px as a framed sprout |
| 5 · Share preview + phone header | A 1200×630 card ("Give your AI a memory of you." + free + local). The phone header is one row (~56 px) with a scrolling nav, and all five places stay in the tab order |
| One stylesheet | `kickstart.css`; the app adds no colours, type or primitives of its own outside its rail/strip/pulse/recovery layouts |
| App | Opens on **Next** (one prompt, one Copy), not a dashboard. Four home shapes, a 5-step detected first run, one recovery pattern, an update view that counts files and settles the `weekly-review` conflict with *Ask my AI to merge them* as default. The write-rules audit matches `04 §4` |

Checked: no third-party requests in the design itself (only `support.js`). The first-contact prompt matches `guide/setup.html` word for word. The SVG mark files carry an embedded C2PA "content credentials" block from Claude (most of each 9 KB file; no personal data). Decide at port time whether to keep it or strip it for the favicon.

### For the port (content, not design)

**Ported 2026-10-13** into `site/`. The setup items below are done there (6 steps tracking P0.1–P0.5, following `guide/setup.html`); prompts render from `site/src/content/prompts.md`; the C2PA blocks are stripped from the shipped icons. Kept for the record:

Still open from round 1. The content comes from the kit's Markdown at build time anyway:

- **Setup steps are thinner than `guide/setup.html`.** Missing: move and rename the vault folder somewhere permanent (and the OneDrive/iCloud notes); the three Obsidian settings; path A uploads more than two files and needs the *chat-only project instructions*; path B's "project instructions" field; path C's optional skills link; backup & sync (P0.4) and privacy (P0.5). Setup should track harness steps P0.1–P0.5. The app's path A "Your AI" step repeats the "two files" shortcut.
- **"Pick the folder called vault inside the kit".** The guide says to move it out and rename it first. Follow the guide.
- **The v1.2 release text** ("Updating your kit" guide, 6 tips, P4.0) is a scenario stand-in taken from the app brief, not a real changelog.
- Check every prompt against `vault/` and `guide/prompts.html` at build time, not against `kit-content.js`.

App-only notes for K10: scenario 6's "last session 9 October" predates the seed install date (the designer kept it as given). "Simulate" buttons stand in for file-system events, which the K11 spike must prove on Windows.
