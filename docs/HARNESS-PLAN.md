---
type: plan
status: active
created: 2026-10-12
updated: 2026-10-12
summary: Maintenance plan for the AI Kickstart repo — same harness format the kit teaches.
current_phase: M1
next_step: M1.1
---

# Maintenance plan

> Dogfooding: this repo is maintained with the same harness the kit teaches. Say **"Continue the maintenance plan."** The agent does the next step, proves it, ticks it and logs it. Legend: `[ ]` to do · `[/]` in progress · `[x]` done (verified) · `[-]` skipped · `[?]` blocked.

## Now

| | |
|---|---|
| **Current phase** | M1 — First real users |
| **Next step** | K9: connect Cloudflare + domain (maintainer, `docs/MAINTAINING.md`), then a live check · M1.1 (pilot) |
| **Blocked** | — |
| **Last session** | 2026-10-13 — K9 Astro port of the approved prototype built and verified locally |

## M0 — Repository foundation

- [x] **M0.1 Scaffold the repo.** AGENTS.md, maintainer skills, docs, checks, build, CI/Pages/Release workflows, issue templates, CC BY 4.0. Check: `scripts/check.sh` green; negative tests (an injected term, catalog drift) fail as expected.
- [x] **M0.2 First push + v1.1 tag.** Check: `main` and `v1.1` visible on GitHub.
- [-] **M0.3 Enable GitHub Pages.** Skipped: the website moves to Astro on Cloudflare at ai-kickstart.me (K9, decision 2026-10-12). `pages.yml` removed.
- [x] **M0.4 Add the `SCRUB_PATTERN` secret** (see `docs/MAINTAINING.md`). Done when: the CI log shows `scrub: OK` instead of the skip warning. *(Added 2026-10-12; verified on the push that ticked this.)*
- [x] **M0.5 Verify the v1.1 Release.** Done when: the Release page has `ai-kickstart-v1.1.zip` attached and the zip unpacks to `README.md LICENSE START-HERE.html guide/ vault/`.

## M1 — First real users

- [ ] **M1.1 Pilot with one friend.** Hand over the Release zip (and the website link once K9 is live). Sit in on setup and Round 1 if possible.
- [ ] **M1.2 Two-week follow-up.** Collect feedback (issue template *Feedback after using the kit*). Turn findings into backlog items.
- [ ] **M1.3 Fix the top 3 friction points** (`evolve-kit`), then release.

## M2 — Recurring

- [ ] **M2.1 Quarterly `refresh-facts`** (next: 2027-01). Log the sources checked.
- [ ] **M2.2 Half-yearly `review-kit`** (next: 2027-04).

## Backlog

*★ = do first. Effort: S (one session) · M (a few) · L (a project).*

| ID | Idea | Why | Effort | Status |
|---|---|---|---|---|
| K1 ★ | **"Updating your kit" guide**: how an existing user pulls new skills, tips and steps into their vault without overwriting their notes (per-file guidance + an agent prompt that diffs `vault/` against their vault) | Every release after v1.0 raises this question | M | todo |
| K2 | **Fictional example vault** ("after 2 months"): a filled-in profile, briefings, a weekly review and a harness log for an invented persona | People understand the end state faster from an example | M | todo |
| K3 | **Profession packs**: optional add-on skills (teacher, manager, freelancer, healthcare admin…) as a separate folder with an install prompt | The catalog promises profession playbooks; the kit ships none | M | todo |
| K4 | Windows + plain-chat-app walkthrough test on a real machine | Most likely friend profile; the author's own setup is different | S | todo |
| K5 | Mobile layout and print check of all guide pages | Many will open the link on a phone | S | todo |
| K6 | Generate the catalog JS from the markdown (build step) | Removes the D7 duplication. Comes almost free with K9 (Astro content collections). The check guards it until then | M | done for the site (it reads the Markdown); the guide's JS copy goes with K12 |
| K7 | Favicon + social preview image (inline/SVG, offline-safe) | Nicer when the link is shared in chats | S | done in `site/` (mark, favicons, apple-touch icon, `share-card.png`, Open Graph tags); live with K9 |
| K8 | Translations (guide + vault) | Reach. Needs a structure decision first (D-level change) | L | idea |
| K9 ★ | **Website at ai-kickstart.me**: run `design/website-claude-design-package` in Claude Design, then implement the approved prototype as an Astro static site in `site/` (content collections over `vault/` Markdown) on Cloudflare with the custom domain | The domain is bought; the site is the front door for friends | M | doing: built in `site/` + `packages/` (2026-10-13), CI job added; next: Cloudflare project + domain, live check |
| K12 | When the website is live: shrink the zip's `guide/` to one offline `START-HERE` page pointing to ai-kickstart.me (the website owns all explanations) | One source of explanation; less to maintain | S | todo |
| K11 | **tinyjs spike (Mac + Windows)**: a hello-world window that picks a folder, watches it for a new file, writes `~/.ai-kickstart/`, and opens an `obsidian://` link; signed/notarized Mac build plus a Windows build on a real machine | De-risks K10 early. Windows is beta in tinyjs, and file watching is the critical capability | S | todo |
| K10 | **Companion app (tinyjs)**: first run, "one next thing", safe kit updates, local-only (`~/.ai-kickstart/`). Design brief: `design/app-claude-design-package`; approved prototype in `design/prototype/` (round 2). Build after the M1 pilot shows where people actually stall | It solves first-contact verification and K1 (updates) better than docs can | L | idea |

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

## Session log

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
