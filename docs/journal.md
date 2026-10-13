---
type: journal
status: active
created: 2026-10-12
updated: 2026-10-13
summary: Maintenance journal for the AI Kickstart repo: decisions and session history. The roadmap lives in master-plan.md.
---

# Maintenance journal

What happened and why, newest first. The open work is in [`master-plan.md`](master-plan.md): when an item there is done, its row is deleted and the session is logged here. (Before 2026-10-13 this file was `HARNESS-PLAN.md` and also held the plan; IDs such as K9 and M0.4 in older entries refer to that plan.)

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-10-12 | Public repo, CC BY 4.0, commit to `main` + `vX.Y` tags | Shareable with credit; low ceremony for a docs repo |
| 2026-10-12 | Private scrub list outside the repo; hook + optional CI secret | The list contains the very names it protects |
| 2026-10-12 | Commits use the GitHub noreply identity | Avoids exposing a personal email in public history |
| 2026-10-12 | Website = Astro static site on Cloudflare (ai-kickstart.me), not GitHub Pages | Pages too limited; Astro reads the kit's Markdown directly. See ARCHITECTURE D14 |
| 2026-10-12 | App stack: tinyjs + Vite+ + TS + React + TanStack Query/Router + Base UI (unstyled) + plain-CSS tokens + Fallow; `site/` + `app/` + `packages/core/` | See ARCHITECTURE D15. Astryx rejected; React Aria runner-up |
| 2026-10-12 | The app is designed in the **same** Claude Design project as the website (round 2), not a new one | The approved tokens and primitives stay in context; one shared stylesheet for site and app |
| 2026-10-12 | Companion app on tinyjs, targeting macOS **and** Windows in v1; progress stays in the vault's Markdown, `~/.ai-kickstart/` holds only app config + install baseline | Modest requirements; one source of truth the AI can also read. Spike first (K11) |
| 2026-10-13 | Roadmap moves to `docs/master-plan.md` (open work only, rows deleted when done); this file becomes the journal | One place to see everything still to do, without wading through history |
| 2026-10-13 | HSTS on for ai-kickstart.me: 1 year, includeSubDomains, `preload` in the header (not yet submitted to the preload list, K18) | There is no reason to serve anything over HTTP |
| 2026-10-13 | Kit vs. person-owned vault files: the person owns the plan, profile (not its README), every `_index.md`, `_system/index.md`, `AGENTS.md`, the tools registry and interview answers; everything else is the kit's | The person's AI is told to edit exactly those files (skill-builder, tool-builder, harness). Person-owned files are never overwritten; an update hands their AI a merge prompt. `kindOf()` in `packages/core` is the one definition |

## Session log

### 2026-10-13 — K19 update model
- **Did:** `packages/core/src/update.ts`. `kindOf()` splits vault files into kit and person (decision above). `hashText()` is SHA-256 via WebCrypto (identical in txiki.js and Node, checked), with CRLF normalised so a line-ending-only change still reads as untouched. `buildManifest()` and `baselineOf()` build the manifest and baseline. `planUpdate()` sorts every file into update / add / conflict / merge / removed (the person deleted it: stays gone) / retired (no longer shipped: stays, theirs now) / unchanged. A person's edit to a file the release didn't change is simply unchanged. `addedSteps()` finds the new plan steps for the hand-off prompt. To copy them "exactly as written", K20's `Step` gained `markdown`. After an update the baseline is the new manifest, so a declined change isn't offered again.
- **Checked:** Vitest rebuilds scenario 8 from the real vault files: v1.1 = today's template without P4.0; v1.2 changes 14 kit files, weekly-review and the plan. Sam's vault (weekly-review edited, plan and GOALS filled, one untouched file re-saved with CRLF) plans exactly 14 updates, 1 conflict (`weekly-review`), 1 merge (`HARNESS-PLAN.md`, with P4.0's Markdown), and the rest unchanged. Edge cases: add, removed, retired, a clash at a new path, a file already brought up to date. Two deliberate breaks (conflict rule, CRLF) each failed tests. `pnpm test` 46/46, site build, `check_site.py`, `scripts/check.sh` green.
- **Not done:** publishing the manifest with a release (K10c). Core's test files still lack Node typings under `tsc` (true before this session too).
- **Next:** K10a once K11 has a Windows run.

### 2026-10-13 — K20 harness plan parser
- **Did:** `parsePlan()` in `packages/core/src/harness.ts` reads the whole `HARNESS-PLAN.md`: frontmatter, the *Now* table, phases (merged with the glance table) with their steps (status from the legend's five marks, ★, title, *Done when*, *Check*, the rest as `detail`), the personal backlog (by column name, so a reordered table still reads), and the session log (Did / Checked / Next / Notes, wrapped lines joined). It never throws: it collects plain-language `problems` (missing section, unknown mark, duplicate step, *Now* pointing nowhere) and sets `usable` false only when there's no step at all, which is the prototype's "can't read your plan" state (§3.8). `nextStep()` is the app's "one next thing": *Now* wins while it names an open step, otherwise the harness skill's rule (a step in progress first, then the first to do, from the current phase on). Recognises sub-steps (`P2.3a`) and skips the `P4.x` template and the commented session template. `parsePhases` is unchanged for the site.
- **Checked:** 18 new Vitest tests against the live vault template (36 steps, clean, starts at P0.1) and a filled-in fixture for an invented person (`packages/core/test/fixtures/harness-plan-filled.md`: every mark, ★ sub-steps, backlog, two log entries, CRLF reads the same), plus four "AI got it wrong" cases. Two deliberate breaks in the parser (template-line skip, comment stripping) each failed tests. An in-progress template edit (an intro paragraph above P0's steps) parses clean. `pnpm test` 36/36, site build, `check_site.py`, `scripts/check.sh` green.
- **Next:** K19 (update model); K10b now waits only on K10a.

### 2026-10-13 — K11 companion app spike, Mac half
- **Did:** installed tinyjs 0.51.1 (txiki.js 26.6.0) into `~/.tinyjs` (the install script was read first; it verifies the release checksum). Scaffolded `app/` from `tinyjs new --template react-ts --pm pnpm` and joined it to the pnpm workspace: React 19 + TypeScript + Vite 8, a TypeScript backend bundled by tinyjs's esbuild, and `@ai-kickstart/design/kickstart.css` imported directly. The page is one window with five checks. The backend (`app/backend/main.ts`) is the only code that touches files. It reads and writes `~/.ai-kickstart/config.json` (temp file + rename) and runs one recursive `tjs.watch` on the vault, pushing `vault-file` events with '/' paths and ignoring `.obsidian/`, `.trash/` and `.git/`. Kept the scaffold layout (`src/` = page, `backend/`) rather than D15's `ui/`, to stay close to upstream tinyjs. Not yet in the app: Vite+ (`vp` not installed; it wraps the same Vite 8) and TanStack (K10a).
- **Checked:** a self-driving test page (`TINYJS_HTML`) inside the real WKWebView against the real backend. Config written and read back. Creating `_inbox/hello.md` from the shell (as an AI would) was noticed as a nested path, and `.obsidian/` writes were ignored. `obsidian://open` was accepted and Obsidian came forward. The built CSS gave dark tokens under a dark system. `tinyjs build` produces a 9.4 MB, ad-hoc-signed, arm64-only `AI Kickstart.app` that launches into one 800×560 window. `pnpm build` (page + backend type-check), `oxlint`, `scripts/check.sh`, `pnpm test` and the site build are all green. Found: `tinyjs new` with no terminal attached spins at 100% CPU after scaffolding (worked around; worth an upstream issue). A test page can't link files outside tinyjs's temp folder (WKWebView read access), so the CSS check inlines the built stylesheet.
- **Not done:** the folder picker needs a human click (computer use had no screen-recording permission this session). No Windows run, no signed and notarised build (K21), and the app icon is still tinyjs's default.
- **Next:** pick a folder in the app; run the README's checks on Windows; then K20/K19 in `packages/core`, which don't depend on the spike.

### 2026-10-13 — Tools, connections and vault curation
- **Did:**
  - Added six vault tools with a shared library, a template, 27 tests and a contract-checking self-test. The registry is `vault/_system/tools/README.md`. The tools are `vault_lint`, `secret_scan`, `upcoming`, `recent`, `fix_frontmatter` and `hub_index`.
  - Wrote `TOOLS-CONTRACT.md`: Part A covers tools, Part B covers connections.
  - Wrote the connections catalog: 40 connections in 12 areas, plus combos. It's also published at `/connections/` (parser `parseConnections` in `packages/core`).
  - Added the `Organizing your vault` reference note, four Bases dashboards, six templates and three skills (`vault-maintenance`, `tool-builder`, `connect-app`).
  - Put `auto-index` markers in six hubs.
  - Harness: new steps P0.6, P3.6, P3.7, P4.0, P5.3, P7.4 and P7.5.
  - Prompts: four new ones (40 in total).
  - Repo: ARCHITECTURE D11 revised (a few tested tools now ship), and new D16 (connections catalog) and D17 (the contract lives in the vault). New `tools` check in `check_kit.py` (self-test, `vault_lint --strict` on the template, hubs current, no `__pycache__`). New CI `tools` matrix (Linux, macOS and Windows on 3.x, plus Linux on 3.9). `build.sh` drops `__pycache__`.
  - Bases syntax checked against the official docs: no `sort` key (it isn't documented), and `if()` truthiness for empty summaries.
- **Checked:**
  - The self-test passes on Python 3.15 and on macOS's built-in 3.9.6.
  - The template vault lints with 0 errors and 0 warnings. Its only tips are the two deliberately empty profile templates.
  - A demo person note gives the expected `hub_index` diff and `upcoming` output.
  - `scripts/check.sh` green. `pnpm test` (18), `pnpm check`, `pnpm build` and `check_site.py` all green (8 pages, 40 connections, 104 functions).
  - Found and fixed on the way:
    - Windows line endings were being normalised by the writers (they now use `read_raw`).
    - macOS `/var` → `/private/var` paths broke `secret_scan` paths.
    - A scrub false positive inside a `difflib` function name.
- **Not done:**
  - The `.base` views are not yet opened in the Obsidian app (K22).
  - No real-Windows run of the tools (K23; CI covers the basics).
- **Next:** K22, then M1.1.

### 2026-10-13 — K13 theme toggle, K15 llms.txt
- **Did:** K13: a header button cycles colours between system, light and dark (`site/src/scripts/theme.ts`), remembered in `localStorage` (`aik.site.theme`). A one-line inline script in `<head>` (`site/src/lib/theme-boot.mjs`) sets `data-kk` before first paint. Astro doesn't hash `is:inline` scripts, so `astro.config.mjs` hashes the same string into `scriptDirective.hashes`, and the CSP stays hash-only. `check_site.py` now fails on any inline script the CSP doesn't hash. K15: a build-time integration (`site/src/integrations/llms.ts`, `turndown` as a dev dependency) converts each built page's `<main>` to Markdown at `<page>/index.html.md` (the spec's rule for URLs ending in `/`). It drops interactive and hidden parts, turns prompt cards and `<pre>` into fenced blocks, catalog rows into list items and setup variants into labelled lines. It then writes `/llms.txt` (H1, summary, *Pages* and *Optional* lists) from each page's title and meta description. `check_site.py` checks the format, that every link resolves, and that the prompts Markdown holds all 36 prompts.
- **Checked:** headless Chromium at 1280 and 390 px with a dark system: system → light → dark → system, each surviving a reload, `data-kk` already set when the document becomes interactive, no console errors or CSP violations, no horizontal scroll. Negative tests: an edited inline script and a missing `.md` page both fail `check_site.py`. `wrangler dev` serves `llms.txt` as `text/plain; charset=utf-8` and `.md` as `text/markdown; charset=utf-8`, so `_headers` is unchanged. `pnpm test`, `pnpm check`, `pnpm build`, `check_site.py`, `scripts/check.sh` all green.
- **Deployed:** pushed and deployed. Live, every `.md` page and `/llms.txt` return 200, and the theme test passes against ai-kickstart.me with no CSP errors. Production (unlike `wrangler dev`) served `.txt` and `.md` without a charset, so `_headers` now sets `charset=utf-8` for `/llms.txt` and `/*.md`. Confirmed live: one `Content-Type` each, with the charset.
- **Next:** M1.1 (maintainer), K11 (needs the machines), K16.

### 2026-10-13 — HSTS on; roadmap split out
- **Did:** HSTS on with `cf` (max-age 1 year, includeSubDomains, preload, nosniff). Wrote `docs/master-plan.md` with the complete open roadmap (first users, website, kit content, companion app, recurring), adding new items K13 theme toggle, K14 ⌘K, K15 `llms.txt`, K16 content parity, K17 CI deploy, K18 preload list, K19 update model, K20 plan parser, K10a–d app slices, K21 signing accounts, R1–R3. Renamed this file from `HARNESS-PLAN.md` and removed the plan sections; done items (K6, K7, K9, M0) are only here now. `check_kit.py` now rejects a master-plan row whose status isn't open.
- **Checked:** `strict-transport-security: max-age=31536000; includeSubDomains; preload` on the apex, a deep page and `www`. The only hostnames are the two proxied records, both on the universal certificate. The maintainer confirmed the WhatsApp share preview looks right. `scripts/check.sh` green.
- **Next:** see `master-plan.md` → Now.

### 2026-10-13 — K9 ai-kickstart.me live
- **Did:** a separate `cf` profile (`ai-kickstart`) for account `f6e4…`; the default login belongs to another organisation and is never used here. The maintainer added the zone and switched the Name.com nameservers. I deployed the static-assets Worker with Wrangler 4.149 (`pnpm run deploy`) and attached ai-kickstart.me as its custom domain. With `cf`: Always Use HTTPS on, minimum TLS 1.2, email obfuscation off, Rocket Loader confirmed off; a `www` placeholder record plus a 301 redirect rule; checked there's no Web Analytics site for this zone. `workers_dev` and preview URLs are off. A `cf migrate` attempt was reverted: the beta's project build can't produce a deploy for this static site. Notes are in `docs/MAINTAINING.md`.
- **Checked:** the zone is active and the `.me` registry delegates to Cloudflare. Universal certificate (Let's Encrypt, TLS 1.3); TLS 1.0 and 1.1 are refused. Every page returns 200, the 404 page works, `http://` and `www` redirect with 301, the security headers are present, nothing is injected, and `workers.dev` returns 404. The full headless browser suite passes against the live domain.
- **Next:** M1.1. Optional: HSTS once we're sure HTTPS is permanent; check the share preview in WhatsApp.

### 2026-10-13 — K9 Astro port
- **Did:** pnpm workspace with `packages/core` (pure TS parsers for catalog, prompts, changelog, harness phases, interview rounds, frontmatter; 13 Vitest tests against the real kit files), `packages/design` (the approved `kickstart.css`), and `site/` (Astro 7, static): Start, Your setup, Ideas menu, Prompts, How it works, What's new, 404. Lists come from the kit through content collections with Zod schemas. The prompt library moved to `site/src/content/prompts.md`. Setup follows `guide/setup.html` in 6 steps (P0.1–P0.5), with every round-1 content gap closed. Strict CSP (hashes, no `unsafe-inline`), `_headers`, `wrangler.jsonc`. Icons and share card copied without their C2PA blocks (the favicon went from 9 KB to 1.6 KB, and it now follows dark mode). New checks: `prompts` sync in `check_kit.py`, `scripts/check_site.py`, CI job `site`. `pnpm-lock.yaml` is excluded from the scrub (generated package names).
- **Checked:** headless Chrome over 20 scenarios (fresh, Windows + chat app, mid-setup tick, share link `#linux-c-4`, finished + older kit, 12 picks + dialog + clipboard, the L filter, a placeholder typed and copied, phone 390 px, dark mode, no-script setup). No console errors, CSP violations or external requests. Header is 57 px on a phone with no horizontal scroll. Found and fixed: a selector clash that hid the first catalog row, and link colours on control-styled anchors. A negative test of the prompt-sync check fails as expected.
- **Not done:** deploy (needs the maintainer's Cloudflare account). The "Why Obsidian" and "what this is not" parts of `guide/why.html` aren't on the site yet (needed before K12).
- **Next:** the maintainer connects Cloudflare and the domain, then a live check (headers, CSP, share preview in WhatsApp). Then M1.1.

### 2026-10-12 — K9/K10 Prototype round 2 reviewed
- **Did:** rendered round 2 headlessly: site scenarios 1–6 (light/dark, 1280×800, phone 390×844), the share preview, and app scenarios 1, 3–9 (800×560 frame, macOS and Windows). Imported the export into `design/prototype/` (renamed from `website-prototype/`, since site and app now share `kickstart.css`) with 16 screenshots and the review. Updated the links in `design/`.
- **Checked:** all five Part A fixes landed (picks column, one recommendation, "Welcome back" card, the Quiver mark, a one-row phone header + share card). The app uses no colour outside the shared tokens (only the window buttons). Its write rules match `04 §4`. No third-party requests besides the prototype runtime. The first-contact prompt matches `guide/setup.html`. Round 1's setup content drift is still open, carried into the README "For the port" list. The SVG marks embed a C2PA content-credentials block (no personal data), to keep or strip at port time.
- **Next:** the K9 Astro port. K11 (tinyjs spike) can run in parallel.

### 2026-10-12 — K9 Website prototype, round 1 reviewed
- **Did:** rendered all 6 Tweaks scenarios (light and dark, 1280×800 and 390×844) and the Prompts, How it works and What's new views. Approved the direction and imported the export plus screenshots into `design/website-prototype/`, with review notes. Wrote `design/claude-design-round-2-prompt.md` (5 site fixes + the app as new pages in the same project, sharing one stylesheet) and `design/logo-quiver-prompt.md`. Re-pointed the app brief's identity clause at "the same project".
- **Checked:** the catalog data matches (16 areas / 103 functions, 36 prompts). The design itself makes no third-party requests (only Claude Design's `support.js` runtime loads React from unpkg). Found setup content drift against `guide/setup.html` and logged it for the port.
- **Next:** the maintainer runs Quiver (logo), then round 2 in Claude Design, then imports the result. After that, K9 Astro port.

### 2026-10-12 — Direction: website + companion app
- **Did:** wrote Claude Design briefs (`design/website-…`, `design/app-…`). Decided: website = Astro static on Cloudflare at ai-kickstart.me (D14); GitHub Pages dropped (`pages.yml` removed, M0.3 skipped); companion app on tinyjs for macOS + Windows, with progress kept in the vault's Markdown. Backlog: K9 (website), K10 (app), K11 (tinyjs spike).
- **Checked:** `scripts/check.sh` green; briefs are Markdown + images only; anti-prescription grep clean.
- **Next:** run the website brief in Claude Design (K9); M0.4 scrub secret; M1.1 friend pilot.

### 2026-10-12 — M0.5 Verify v1.1 Release
- **Did:** the first tag push didn't trigger `release.yml` (the tag arrived in the same push that created the workflows). Deleted and re-pushed the unpublished tag, and the workflow ran.
- **Checked:** [Release v1.1](https://github.com/liqweed/ai-kickstart/releases/tag/v1.1) has `ai-kickstart-v1.1.zip` (112 KB). The downloaded zip holds only `LICENSE README.md START-HERE.html guide/ vault/` and scrubs clean. `Checks` workflow green. `Pages` failed as expected (not enabled yet → M0.3).
- **Next:** M0.3, M0.4 (maintainer, web UI).

### 2026-10-12 — M0.1–M0.2 Repository foundation
- **Did:** scaffolded the repo (AGENTS.md, `.agents/skills/` ×4 + `.claude/skills` symlink, docs, `scripts/` checks/build/hook, workflows, issue templates, LICENSE, CHANGELOG, VERSION) and pushed `main` + tag `v1.1`.
- **Checked:** `scripts/check.sh` green (66 files scrubbed; v1.1; 103 catalog functions; 9 pages; 9 skills). Negative tests: an injected employer and place name was blocked; catalog level drift was reported.
- **Next:** M0.3 (enable Pages), M0.4 (scrub secret). Both need the maintainer in the web UI.
