---
type: plan
status: active
created: 2026-10-12
updated: 2026-10-12
summary: Maintenance plan for the AI Kickstart repo — same harness format the kit teaches.
current_phase: M0
next_step: M0.3
---

# Maintenance plan

> Dogfooding: this repo is maintained with the same harness the kit teaches. Say **"Continue the maintenance plan."** The agent does the next step, proves it, ticks it and logs it. Legend: `[ ]` to do · `[/]` in progress · `[x]` done (verified) · `[-]` skipped · `[?]` blocked.

## Now

| | |
|---|---|
| **Current phase** | M0 — Repository foundation |
| **Next step** | M0.3 |
| **Blocked** | M0.3 and M0.4 need the maintainer in the GitHub web UI |
| **Last session** | 2026-10-12 — repo scaffolded, v1.1 pushed |

## M0 — Repository foundation

- [x] **M0.1 Scaffold the repo.** AGENTS.md, maintainer skills, docs, checks, build, CI/Pages/Release workflows, issue templates, CC BY 4.0. Check: `scripts/check.sh` green; negative tests (an injected term, catalog drift) fail as expected.
- [x] **M0.2 First push + v1.1 tag.** Check: `main` and `v1.1` visible on GitHub.
- [?] **M0.3 Enable Pages** (maintainer: Settings → Pages → Source: GitHub Actions), then re-run the *Pages* workflow. Done when: [liqweed.github.io/ai-kickstart](https://liqweed.github.io/ai-kickstart/) shows the v1.1 footer.
- [?] **M0.4 Add the `SCRUB_PATTERN` secret** (see `docs/MAINTAINING.md`). Done when: the CI log shows `scrub: OK` instead of the skip warning.
- [x] **M0.5 Verify the v1.1 Release.** Done when: the Release page has `ai-kickstart-v1.1.zip` attached and the zip unpacks to `README.md LICENSE START-HERE.html guide/ vault/`.

## M1 — First real users

- [ ] **M1.1 Pilot with one friend.** Hand over the Pages link + the Release zip. Sit in on setup and Round 1 if possible.
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
| K5 | Mobile layout and print check of all guide pages | Many will open the Pages link on a phone | S | todo |
| K6 | Generate the catalog JS from the markdown (build step) | Removes the D7 duplication. The check already guards it, so this is low priority | L | todo |
| K7 | Favicon + social preview image (inline/SVG, offline-safe) | Nicer when the link is shared in chats | S | todo |
| K8 | Translations (guide + vault) | Reach. Needs a structure decision first (D-level change) | L | idea |

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-10-12 | Public repo, CC BY 4.0, commit to `main` + `vX.Y` tags | Shareable with credit; low ceremony for a docs repo |
| 2026-10-12 | Private scrub list outside the repo; hook + optional CI secret | The list contains the very names it protects |
| 2026-10-12 | Commits use the GitHub noreply identity | Avoids exposing a personal email in public history |

## Session log

### 2026-10-12 — M0.5 Verify v1.1 Release
- **Did:** the first tag push didn't trigger `release.yml` (the tag arrived in the same push that created the workflows). Deleted and re-pushed the unpublished tag, and the workflow ran.
- **Checked:** [Release v1.1](https://github.com/liqweed/ai-kickstart/releases/tag/v1.1) has `ai-kickstart-v1.1.zip` (112 KB). The downloaded zip holds only `LICENSE README.md START-HERE.html guide/ vault/` and scrubs clean. `Checks` workflow green. `Pages` failed as expected (not enabled yet → M0.3).
- **Next:** M0.3, M0.4 (maintainer, web UI).

### 2026-10-12 — M0.1–M0.2 Repository foundation
- **Did:** scaffolded the repo (AGENTS.md, `.agents/skills/` ×4 + `.claude/skills` symlink, docs, `scripts/` checks/build/hook, workflows, issue templates, LICENSE, CHANGELOG, VERSION) and pushed `main` + tag `v1.1`.
- **Checked:** `scripts/check.sh` green (66 files scrubbed; v1.1; 103 catalog functions; 9 pages; 9 skills). Negative tests: an injected employer and place name was blocked; catalog level drift was reported.
- **Next:** M0.3 (enable Pages), M0.4 (scrub secret). Both need the maintainer in the web UI.
