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
| **Next step** | M1.1 (pilot) · K9 (website brief → Claude Design) |
| **Blocked** | — |
| **Last session** | 2026-10-12 — repo scaffolded, v1.1 pushed |

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
| K6 | Generate the catalog JS from the markdown (build step) | Removes the D7 duplication. Comes almost free with K9 (Astro content collections). The check guards it until then | M | todo |
| K7 | Favicon + social preview image (inline/SVG, offline-safe) | Nicer when the link is shared in chats | S | todo |
| K8 | Translations (guide + vault) | Reach. Needs a structure decision first (D-level change) | L | idea |
| K9 ★ | **Website at ai-kickstart.me**: run `design/website-claude-design-package` in Claude Design, then implement the approved prototype as an Astro static site in `site/` (content collections over `vault/` Markdown) on Cloudflare with the custom domain | The domain is bought; the site is the front door for friends | M | todo |
| K12 | When the website is live: shrink the zip's `guide/` to one offline `START-HERE` page pointing to ai-kickstart.me (the website owns all explanations) | One source of explanation; less to maintain | S | todo |
| K11 | **tinyjs spike (Mac + Windows)**: a hello-world window that picks a folder, watches it for a new file, writes `~/.ai-kickstart/`, and opens an `obsidian://` link; signed/notarized Mac build plus a Windows build on a real machine | De-risks K10 early. Windows is beta in tinyjs, and file watching is the critical capability | S | todo |
| K10 | **Companion app (tinyjs)**: first run, "one next thing", safe kit updates, local-only (`~/.ai-kickstart/`). Design brief: `design/app-claude-design-package`. Build after the M1 pilot shows where people actually stall | It solves first-contact verification and K1 (updates) better than docs can | L | idea |

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-10-12 | Public repo, CC BY 4.0, commit to `main` + `vX.Y` tags | Shareable with credit; low ceremony for a docs repo |
| 2026-10-12 | Private scrub list outside the repo; hook + optional CI secret | The list contains the very names it protects |
| 2026-10-12 | Commits use the GitHub noreply identity | Avoids exposing a personal email in public history |
| 2026-10-12 | Website = Astro static site on Cloudflare (ai-kickstart.me), not GitHub Pages | Pages too limited; Astro reads the kit's Markdown directly. See ARCHITECTURE D14 |
| 2026-10-12 | Companion app on tinyjs, targeting macOS **and** Windows in v1; progress stays in the vault's Markdown, `~/.ai-kickstart/` holds only app config + install baseline | Modest requirements; one source of truth the AI can also read. Spike first (K11) |

## Session log

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
