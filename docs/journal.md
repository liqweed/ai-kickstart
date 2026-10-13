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

## Session log

### 2026-10-13 — K13 theme toggle, K15 llms.txt
- **Did:** K13: a header button cycles colours between system, light and dark (`site/src/scripts/theme.ts`), remembered in `localStorage` (`aik.site.theme`). A one-line inline script in `<head>` (`site/src/lib/theme-boot.mjs`) sets `data-kk` before first paint. Astro doesn't hash `is:inline` scripts, so `astro.config.mjs` hashes the same string into `scriptDirective.hashes`, and the CSP stays hash-only. `check_site.py` now fails on any inline script the CSP doesn't hash. K15: a build-time integration (`site/src/integrations/llms.ts`, `turndown` as a dev dependency) converts each built page's `<main>` to Markdown at `<page>/index.html.md` (the spec's rule for URLs ending in `/`). It drops interactive and hidden parts, turns prompt cards and `<pre>` into fenced blocks, catalog rows into list items and setup variants into labelled lines. It then writes `/llms.txt` (H1, summary, *Pages* and *Optional* lists) from each page's title and meta description. `check_site.py` checks the format, that every link resolves, and that the prompts Markdown holds all 36 prompts.
- **Checked:** headless Chromium at 1280 and 390 px with a dark system: system → light → dark → system, each surviving a reload, `data-kk` already set when the document becomes interactive, no console errors or CSP violations, no horizontal scroll. Negative tests: an edited inline script and a missing `.md` page both fail `check_site.py`. `wrangler dev` serves `llms.txt` as `text/plain; charset=utf-8` and `.md` as `text/markdown; charset=utf-8`, so `_headers` is unchanged. `pnpm test`, `pnpm check`, `pnpm build`, `check_site.py`, `scripts/check.sh` all green.
- **Not done:** deploy. Both changes go live with the next `pnpm run deploy` (or K17).
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
