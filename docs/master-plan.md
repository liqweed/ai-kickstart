---
type: plan
status: active
updated: 2026-10-13
summary: The roadmap for AI Kickstart (kit, website, companion app). Open work only.
---

# Master plan

The complete roadmap, open work only. **When an item is done, delete its row** and record it in [`journal.md`](journal.md) (what was done, how it was checked). Decisions and history live there too, not here. `scripts/check_kit.py` rejects a row whose status isn't one of the open values below.

**Status:** `next` (do soon) · `doing` · `todo` · `blocked` (say on what) · `idea` (not committed). **★** = priority. **Effort:** S (one session) · M (a few) · L (a project). IDs are stable: never renumber, and don't reuse a deleted ID.

## Now

1. **M1.1** Pilot with one friend, using https://ai-kickstart.me.
2. **K11** tinyjs spike, to find out early whether the app's stack works on Mac and Windows.
3. **K16** Content parity with the offline guide (small; unblocks K12).

## 1 · First users

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| M1.1 ★ | **Pilot with one friend.** Send https://ai-kickstart.me; sit in on setup and Round 1 if possible | They finished Day 1, and their stumbles are written down | S | next |
| M1.2 | **Two-week follow-up** (issue template *Feedback after using the kit*) | Feedback is filed as issues and turned into rows here | S | todo |
| M1.3 | **Fix the top 3 friction points** from M1.2 (`evolve-kit`), then release | The three fixes are released | M | todo |

## 2 · Website (ai-kickstart.me)

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| K14 | **⌘K / Ctrl+K quick find**: one dialog that searches pages, prompts and ideas, with a build-time index and no third-party code | Typing a word finds and copies a prompt, Enter navigates, Esc closes; keyboard-only and screen-reader friendly; works on a phone via a visible button | M | todo |
| K16 ★ | **Content parity with the offline guide** before it shrinks: "Why Obsidian", "What this is not", and the compounding loop from `guide/why.html` | Every explanation in `guide/` has a home on the site | S | todo |
| K12 | **Shrink the zip's `guide/`** to one offline `START-HERE` page pointing to the site. Drop the catalog JS copy (D7) and the prompt sync check | The zip has one guide page; `check_kit.py` no longer needs the catalog and prompt sync. Needs K16 | S | blocked: K16 |
| K17 | **Deploy from CI**: on push to `main`, build + `check_site.py` + `wrangler deploy` with an API token scoped to this account's Workers only, then a live smoke check | A push reaches the live site within minutes, and the smoke check (status codes, headers, no injected scripts) is green | S | todo |
| K5 | **Real-device check** of the site: iPhone Safari, Android Chrome, Windows Edge, print | Notes or fixes for each device | S | todo |
| K18 | **HSTS preload list** submission (hstspreload.org). The header already carries `preload`; joining the list is close to permanent | Decided, and submitted or explicitly declined | S | idea |

## 3 · Kit content

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| K1 ★ | **"Updating your kit" guide**: how an existing user pulls new skills, tips and steps into their vault without losing their notes (per-file guidance + an agent prompt). Shares its model of "kit-owned vs. person-owned files" with K19 | A v1.1 vault updates to the next release by following the guide, with no edited note lost | M | todo |
| K4 | **Windows + chat-app walkthrough** on a real machine | Setup completed end to end on Windows with a chat app; fixes filed | S | todo |
| K2 | **Fictional example vault** ("after 2 months"): filled profile, briefings, a weekly review and a harness log for an invented persona | Linked from the site; scrub-clean; no real family's specifics | M | todo |
| K3 | **Profession packs**: optional skills (teacher, manager, freelancer, healthcare admin…) with an install prompt | At least two packs, each listed in the catalog | M | todo |

## 4 · Companion app

The app is designed (approved prototype in [`design/prototype/`](../design/prototype/)); the stack is proposed in ARCHITECTURE D15. Build order: prove the stack, put the logic in `packages/core` (tested, shared with the site), then the app, then distribution.

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| K11 ★ | **tinyjs spike, Mac + Windows**: a window that picks a folder, watches it for a new file, writes `~/.ai-kickstart/`, opens an `obsidian://` link, and loads `kickstart.css` | It works on a real Mac (signed + notarised) and a real Windows machine; D15 confirmed, or a fallback chosen | S | next |
| K20 | **Harness plan parser** in `packages/core`: phases, steps with status marks, Now table, personal backlog, session log | Vitest covers the vault template plus a filled-in fixture plan | S | todo |
| K19 | **Update model** in `packages/core`: a per-release kit manifest (files, hashes, kind), the install baseline, and a planner that sorts files into untouched / changed by the person / person-owned | Vitest reproduces the prototype's update scenario (14 untouched, 1 conflict on `weekly-review`, 1 addition to `HARNESS-PLAN.md`) | M | todo |
| K10a | **App shell + first run**: vault (create or find), Obsidian check, AI path, first contact detected by `_inbox/hello.md` | The prototype's first-run scenarios 1–3 work on Mac and Windows | M | blocked: K11 |
| K10b | **Next + Plan views** with file watching and the "noticed" line | Scenarios 4–7 work against a real vault edited by an AI | M | blocked: K10a, K20 |
| K10c | **Updates**: download, review, apply only untouched files, hand-off prompts | Scenario 8 works end to end; the write-rules audit (`04 §4`) passes | M | blocked: K19, K10b |
| K10d | **Distribution**: signed + notarised Mac build, signed Windows build, auto-update, download on the site | A friend installs it from the site without security warnings | M | blocked: K21 |
| K21 | **Signing accounts** (maintainer decision): Apple Developer Program for notarisation; a Windows code-signing option (e.g. Azure Trusted Signing) | Both accounts exist, or Windows ships unsigned for the pilot with a written reason | S | todo |

## 5 · Recurring

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| R1 | **`refresh-facts`**, quarterly (next 2027-01) | Sources logged in the journal; changes released | S | todo |
| R2 | **`review-kit`**, twice a year (next 2027-04) | Findings turned into rows here | S | todo |
| R3 | **Dependency bumps**, monthly: pnpm packages (Astro, Wrangler, Vitest), GitHub Actions | CI green on the bump commit, site redeployed | S | todo |

## Ideas (not scheduled)

| ID | Item | Done when | Effort | Status |
|---|---|---|---|---|
| K8 | **Translations** (site + vault). Needs a structure decision first | A decision recorded in ARCHITECTURE | L | idea |
