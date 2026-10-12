# 03 · Target data: shapes and seed data (facts, not layout)

## Where truth lives

| Data | Lives in | App may… |
|---|---|---|
| Progress (phases, steps, backlog, session log, decisions) | `<vault>/_system/HARNESS-PLAN.md` (Markdown) | **Read only** |
| Interview progress | `<vault>/_system/kickstart/answers/round-N-YYYY-MM-DD.md` (one file per round done) | Read only |
| Profile | `<vault>/_system/profile/*.md` (7 files; empty templates contain `<!-- … -->` guidance comments) | Read only (filled vs still-template) |
| Kit-owned files (skills, interview rounds, catalog, contract, templates) | inside the vault | Replace **only** during a confirmed update |
| App state | `~/.ai-kickstart/` | Read/write |

The vault's Markdown is the single source of truth, because the person's AI reads and edits those same files. The app mirrors them; it never keeps a competing copy of progress.

## App state (`~/.ai-kickstart/`)

| Field | Example | Notes |
|---|---|---|
| vaults[] | `{ name: "Sam's Vault", path: "~/Documents/Sam's Vault", added: 2026-10-14 }` | Usually one |
| kitVersionInstalled | `1.1` | Per vault |
| baseline | `{ "_system/skills/weekly-review/SKILL.md": "sha256:…", … }` | Hashes of kit files *as installed*, so the app can tell "untouched" from "edited by you" |
| updateCheck | `on` | The only network use: reads the public releases list |
| lastSeenVersion | `1.1` | Drives "what's new" |
| aiPath | `B` (desktop agent) | Chosen at first run; tunes the prompts and help |

## Parsed from HARNESS-PLAN.md

- Frontmatter: `current_phase`, `next_step`, `updated`
- *Now* table: current phase · next step · blocked · last session
- Phases P0–P7: step id, title, status mark, "Done when", "Check"
- Personal backlog rows: ID · area · idea · value 1–3 · effort S/M/L · phase · status · ★
- Session log entries (newest first): date · step · Did · Checked · Next · Notes

## Update: the three file kinds

| Kind | Rule | Example (v1.1 → v1.2) |
|---|---|---|
| Kit file, untouched (hash = baseline) | Safe to replace after preview | `_system/kickstart/round-5-checkin.md` |
| Kit file, edited by the person (hash ≠ baseline) | Conflict: keep mine · take new · ask my AI to merge | `_system/skills/weekly-review/SKILL.md` (Sam added a "plan family dinners" step) |
| Person-owned file the new version adds to | Never overwritten; the app produces a merge prompt for their AI | `_system/HARNESS-PLAN.md` gains step P4.0 |

## Seed data: render this, don't invent

**Persona:** Sam (fictional), macOS 15, Path B (desktop agent), comfort 2. Installed 2026-10-14. Today is 2026-11-03.

**Interview:** Round 1 ✓ (10-14) · Round 2 ✓ (10-16) · Round 3 ✓ (10-19) · Round 4 ✓ (10-21) · Round 5 check-in: due ~11-04.

**Plan status**

| Phase | Done / total | Notes |
|---|---|---|
| P0 Foundations | 5 / 5 | |
| P1 Get to know you | 5 / 5 | |
| P2 First wins | 3 / 6 | P2.1 daily briefing `[-]` (Sam didn't want one) · P2.2 weekly review `[x]` · P2.3 Sunday meal plan + shopping list ★ `[x]` · P2.4 meeting notes → actions `[/]` · P2.5 subscriptions audit `[ ]` · P2.6 use-it check `[ ]` |
| P3 Capture & memory | 0 / 5 | |
| P4–P7 | 0 | not started |

*Now:* phase P2 · next step P2.4 · blocked — · last session 2026-10-30.

**Last session log entry**
> **2026-10-30 — P2.4 Meeting notes → actions (started)**
> Did: drafted the skill from Round 3's spec; tested on one real meeting. · Checked: output had owners and dates; the follow-up email was too formal. · Next: P2.4, soften the email tone, test again. · Notes: Sam prefers bullet summaries.

**Personal backlog**

| ID | Area | Idea | Value | Effort | Phase | Status |
|---|---|---|---|---|---|---|
| B1 ★ | Food & household | Sunday meal plan + shopping list | 3 | S | P2 | done |
| B2 | Work: communication | Meeting notes → actions + follow-up | 3 | S | P2 | in progress |
| B3 | Money & admin | Subscriptions audit | 2 | S | P2 | todo |
| B4 | Kids & family | School portal weekly digest | 3 | M | P4 | todo |
| B5 | Home | Home manual (appliances, warranties) | 2 | S | P3 | todo |

**Update available: v1.2 (fictional, for the prototype)**
- New: "Updating your kit" guide · improved weekly-review skill · 6 new tips · new harness step P4.0 "Choose what to connect first"
- Files: 14 untouched kit files to update · 1 conflict (`weekly-review/SKILL.md`) · 1 person-owned addition (`HARNESS-PLAN.md` + P4.0)

## Key prompts (verbatim)

```
Continue my harness plan.
Start round 5 of my kickstart interview.
Hi! This folder is my new Obsidian vault, set up from the AI Kickstart kit. Please read AGENTS.md and _system/index.md (nothing else yet), then tell me in three short lines: 1) what this vault is for, 2) how you'll help me, 3) what we should do first. Then create a test note at _inbox/hello.md that says "It works!" so I can check that you can write here.
```
