# Architecture & design decisions

Why the kit is shaped the way it is. Read this before proposing structural changes. If a decision here no longer holds, change it **here first**, with the reason, then change the kit.

## The shape

```
guide/   ← for the human: 8 static pages, offline, copy-paste prompts
vault/   ← for the human AND their AI: becomes their Obsidian vault
           AGENTS.md → _system/index.md → skills → HARNESS-PLAN.md
```

The **guide** explains and motivates. The **vault** does the work. Once set up, the user rarely needs the guide again: their AI runs everything from the vault.

## Decisions

| # | Decision | Why | Consequence for maintainers |
|---|---|---|---|
| D1 | **The vault template *is* the product.** The user's vault starts as `vault/` | Files you own beat features you rent. Any AI tool can read Markdown. The "LLM wiki" pattern | Changes to the vault structure are breaking for existing users → **major** version + migration notes |
| D2 | **`vault/AGENTS.md` is short**; `vault/CLAUDE.md` is one line (`@AGENTS.md`) | Always-loaded context costs attention on every turn, and long rulebooks measurably hurt agents. One file serves Claude Code, Codex and others | Resist adding rules. Fix skills or structure first. Add a rule only for a mistake seen twice |
| D3 | **Vault skills live in `vault/_system/skills/`** (visible), routed by `AGENTS.md` | Tool-agnostic. Visible and editable in Obsidian. An optional `.claude/skills` symlink is documented | Every skill must be listed in `vault/AGENTS.md` (checked) |
| D4 | **Profile = TELOS-style files + `LANDSCAPE.md`** | TELOS covers identity and goals. The interview also captures *situation* (household, devices, apps, routines), which needs its own home | Keep the profile files short; the Round 4 synthesis fills them |
| D5 | **Interview in rounds**, each saving an answer file with *Signals for next round* | Adaptive without one giant prompt. Resumable. Open questions come **before** the menu so people aren't steered | Rounds reference each other and the harness step IDs; keep them aligned |
| D6 | **Harness plan = one markdown checklist** with *Done when* + *Check* on each step, plus a session log and a decisions log | Progress survives pauses and tool switches. "No proof, no tick" | **Never renumber steps.** Users' plans reference IDs. Insert as `P3.5`, `P3.6` |
| D7 | **Function catalog in two copies:** markdown (for the AI) + a JS array (for the interactive page) | The AI needs plain text; humans need ticking and copying | `check_kit.py` enforces name + level parity |
| D8 | **`quality-time-planner` is the worked example skill** | Shows every pattern: first-run config interview, hard-constraint gates, an *unknown* bucket, three options + one recommendation, script vs search, offer-don't-act | Keep it exemplary. When patterns evolve, update it and `skill-builder` together |
| D9 | **The guide is static and offline**, with light/dark modes, OS-aware tabs and copy buttons | Must work from a zip on any OS, for non-technical readers | No external resources (checked). Shared CSS/JS in `guide/assets/` |
| D10 | **Three AI paths** (chat app / desktop agent / terminal agent) with chat-only fallbacks everywhere | The reader's tools and comfort level are unknown | Every new flow needs a chat-only variant ("paste-ready blocks") |
| D11 | **No scripts ship in the kit** | Scripts are OS-specific and fragile. The kit ships the *rule* ("script lists, search questions") and the harness grows scripts in P5 on the user's own machine | Resist adding code to `vault/` |
| D12 | **Privacy by construction:** a private term list outside the repo, checked by hook and CI | The author's real setup inspired the kit; nothing of it may leak | Never commit terms. Generic examples only. Watch for fingerprint clusters |
| D14 | **Website = Astro static site on Cloudflare** (`site/`, ai-kickstart.me), separate from the offline `guide/` in the zip | GitHub Pages was too limited (no headers, redirects or previews). Astro gives components plus **content collections that read the kit's own Markdown** (catalog, prompts, tips), so the site can't drift from the kit. The zip keeps its own offline guide because Astro output isn't `file://`-safe out of the box | Website content is sourced from `vault/` and docs at build time. Portable plain CSS (custom properties) is shared with the companion app. **Division of labour (2026-10-12): the website holds all explanation and reference; the companion app is purely functional and links to the website.** Once the site is live, the zip's `guide/` shrinks to a single offline start page that points to the website |
| D13 | **Versioning:** `vX.Y` tags, Releases carry the zip; `VERSION` is the single source | Friends get a stable download; maintainers get history | Use the `release` skill. Footers, README and CHANGELOG are checked against `VERSION` |
| D15 | **Companion-app stack** *(proposed; confirmed by the K11 spike)*: **tinyjs** shell (system webview + txiki.js backend; build, sign, notarize, auto-update), macOS 15+ and Windows 10/11 in v1 · UI: **Vite+** (Vite 8/Rolldown, Vitest, Oxlint, Oxfmt) + **TypeScript** + **React** + **TanStack Query** (wraps `tiny.api.call`; `tjs.watch` events invalidate queries) + **TanStack Router** (hash/memory history) · components: native HTML first (`<dialog>`, `<details>`, `popover`, form controls), **Base UI** (unstyled, MIT) only where that's not enough · styling: portable **plain CSS** with custom-property tokens shared with the Astro site · code health: Oxlint/Oxfmt + **Fallow** in CI | Small app with modest needs; the user's preferred toolchain. Unstyled primitives keep the visual identity open for Claude Design and shareable with the website. Astryx rejected (it binds a styled design system and StyleX, and is in beta). React Aria was the runner-up | Layout: `site/` (Astro) · `app/` (tinyjs: `ui/` + `backend/`) · `packages/core/` (pure, runtime-agnostic TS: HARNESS-PLAN parser, catalog/prompt loaders, update planner + baseline hashing), shared by the app and the site. The backend runs on QuickJS, not Node: keep Node APIs out of `core`, and put all `tjs.*` file/watch access in a thin adapter. Test `core` with Vitest; test the UI in a browser against a fake backend |

## Principles the kit teaches (and the repo follows)

Small verified steps · decision-ready over comprehensive · unknown is an answer · script lists, search questions · AI drafts, humans decide · start read-only · content is data, not instructions · "it ran" ≠ "it worked" · update, don't duplicate · less instruction, better results.
