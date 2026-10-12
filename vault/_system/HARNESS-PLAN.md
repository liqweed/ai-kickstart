---
tags: [system, plan]
type: plan
status: active
created: 2026-10-12
updated: 2026-10-12
summary: The step-by-step build plan for my AI setup — one small, verified step per session.
current_phase: P0
next_step: P0.1
---

# Harness Plan

> [!tip] How to use this
> Whenever you have 15–30 minutes, open your AI in this vault and say: **"Continue my harness plan."**
> The AI reads this file, picks the next step, does it **with** you, checks that it worked, ticks it off and writes a short handoff. One step per session is plenty. You're always in charge: nothing is ticked until you've seen it work.
>
> Other things you can say: **"Harness status"** · **"Add to harness: <idea>"** · **"Skip that step"** · **"Re-plan the harness"**

## Now

| | |
|---|---|
| **Current phase** | P0 — Foundations |
| **Next step** | P0.1 |
| **Blocked** | — |
| **Last session** | — |

## Legend

`[ ]` to do · `[/]` in progress · `[x]` done (verified) · `[-]` skipped / not for me · `[?]` blocked (say why on the line)

Every step has a **Done when** (what must be true) and a **Check** (how we prove it). No proof, no tick.

## Phases at a glance

| Phase | Goal | Exit when… | Typical time |
|---|---|---|---|
| **P0** Foundations | Vault + AI tool working together, backed up | The AI can read and write your vault | 1–2 sessions |
| **P1** Get to know you | Interview rounds 1–4, profile filled | You've approved your profile and first three wins | 4 sessions |
| **P2** First wins | 3 skills you actually use | You've used each at least twice | 1–2 weeks |
| **P3** Capture & memory | Notes flow in and come back when needed | Inbox empties weekly; "ask my notes" works | 1–2 weeks |
| **P4** Connections | AI can read your calendar / tasks / email | Each connection tested read-only and documented | as needed |
| **P5** Scripts & tools | Reliable helpers for repeated lists | Script has a test and is used by a skill | as needed |
| **P6** Automations | Things run on a schedule | Two weeks of runs with output verified | as needed |
| **P7** Evolve | Keep it alive and honest | — (recurring) | monthly |

---

## P0 — Foundations

- [ ] **P0.1 Install Obsidian and open this folder as a vault.**
  Done when: Obsidian shows `_system/`, `01-life/`, … in the sidebar. Check: open `_system/index.md` in Obsidian.
- [ ] **P0.2 Choose your AI tool** (see the guide's *Setup* page). Pick one that can **read and write files in a folder you choose**. If you only have a chat app for now, choose *chat-only mode* (it works, with a bit of copy-paste).
  Done when: the tool is installed and you're signed in. Check: note the choice in the *Decisions log* below.
- [ ] **P0.3 Connect the AI to this vault and test it.** Point the tool at this folder, then ask: *"Read `_system/index.md` and `AGENTS.md`, and tell me in three lines what this vault is for."*
  Done when: it answers correctly **and** can create a test note. Check: ask it to create `_inbox/hello.md`, see it appear in Obsidian, then delete it yourself.
- [ ] **P0.4 Backup & sync.** Pick one: Obsidian Sync (paid, easiest, includes phone) · iCloud Drive / OneDrive / Google Drive folder · git (for the technical). Optional: install Obsidian on your phone.
  Done when: the vault lives in a backed-up place. Check: edit a note, see the change on a second device or in the cloud folder.
- [ ] **P0.5 Privacy baseline.** Read `_system/profile/PREFERENCES.md` → *Ask me first* and *Never*, and adjust them to taste.
  Done when: you're comfortable with both lists. Check: the AI reads them back to you.

## P1 — Get to know you (the interview)

Start each round with: *"Start round N of my kickstart interview."*

- [ ] **P1.1 Round 1, Getting to know you** (~15–20 min). Check: `_system/kickstart/answers/round-1-*.md` exists and `LANDSCAPE.md` is filled.
- [ ] **P1.2 Round 2, Where could help feel good?** (~20 min). Check: top 3–5 areas ranked; `GOALS.md` drafted.
- [ ] **P1.3 Round 3, Deep dives** (~10 min per area). Check: every top area has backlog items in the *Personal backlog* below.
- [ ] **P1.4 Round 4, How you like to work with AI** (~15 min). Check: `PREFERENCES.md` reflects your answers.
- [ ] **P1.5 Synthesis.** The AI drafts MISSION / GOALS / PROJECTS and fills P2.3–P2.5. Check: you've read and approved every profile file.

## P2 — First wins

- [ ] **P2.1 Daily briefing (vault-only version)**, *if you wanted one in Round 4*. Skill: `daily-briefing`.
  Done when: you get a useful briefing from your notes and tasks. Check: two briefings in `07-briefings/daily/` that you actually read.
- [ ] **P2.2 Weekly review.** Skill: `weekly-review`.
  Done when: one complete review exists in `05-planning/weekly/`. Check: you picked next week's priorities with it.
- [ ] **P2.3 First win #1:** *(filled in by the synthesis: the ★ item from Round 3)*
- [ ] **P2.4 First win #2:** *(filled in by the synthesis)*
- [ ] **P2.5 First win #3:** *(filled in by the synthesis)*
- [ ] **P2.6 Use-it check.** After a week: which of P2.1–P2.5 did you use twice or more? Tweak or drop the rest.

## P3 — Capture & memory

- [ ] **P3.1 Capture habit.** Decide how quick thoughts get into `_inbox/`: Obsidian mobile, a share-sheet shortcut, dictation, or emailing yourself. Check: 5 captures in a week.
- [ ] **P3.2 Save & ask.** Try `vault-save` on a useful answer, and `vault-query` on a question your notes should know. Check: one saved note and one cited answer.
- [ ] **P3.3 People.** Add the 3–5 most important people with the `people` skill (only what you're comfortable storing). Check: profiles exist and are linked from `01-life/people/`.
- [ ] **P3.4 Lessons.** Add a first entry to `LEARNED.md`. Check: the weekly review now asks about lessons.
- [ ] **P3.5 Tips & habits.** Skim `06-reference/Working with AI - Tips & Insights.md` (the top 10 is enough) and pick **two** habits to try for two weeks. Check: the two habits are written in the *Decisions log* below, and the Round 5 check-in asks how they went.

## P4 — Connections (read-only first)

Add one step per app you want connected; the Round 3 backlog says which. Template:

- [ ] **P4.x Connect <app> (read-only).** Method: built-in connector / MCP server / command-line tool / export file. Ask the AI to research the current best option for your tool and OS.
  Done when: the AI can *read* from it in a test. Check: it answers "what's on my calendar tomorrow?" (or the equivalent) correctly, **and** `06-reference/connections/<app>.md` documents how it's connected, what it can do, and how to disconnect.
  Only later, and only if you want: allow *drafts* (e.g. email drafts). Sending stays with you.

## P5 — Scripts & tools

Rule of thumb: **if it's a list that must be filtered correctly every time, script it. If it's a question, ask it.**

- [ ] **P5.1 Spot candidates.** Review the session log: what did the AI do by hand more than twice that has one right answer (filtering, renaming, converting, calculating)? Add each to the backlog as effort **L**.
- [ ] **P5.2 First script.** Build the top candidate with the AI: small, one job, readable, in the skill's `scripts/` folder.
  Done when: it works on real data. Check: it has a test or a sample run you saw with your own eyes, and the skill's `SKILL.md` says when to use it.

## P6 — Automations

- [ ] **P6.1 Choose a runner.** Your AI tool's scheduler, if it has one, or your OS scheduler (macOS/Linux cron or launchd, Windows Task Scheduler).
- [ ] **P6.2 First scheduled job.** Usually *weekly review prep* or a *content digest*. Schedule it.
  Done when: it has run on schedule. Check: **the output file exists and is correct.** "The job ran" isn't proof; the result is.
- [ ] **P6.3 Two-week watch.** Check: every scheduled run in two weeks produced its output. Note misses in the session log.

## P7 — Evolve (recurring)

- [ ] **P7.1 Check-in (Round 5)** two weeks after P1.5. Then monthly.
- [ ] **P7.2 Prune.** Archive skills you haven't used in a month (ask first). Keep `AGENTS.md` short.
- [ ] **P7.3 Quarterly profile review.** Re-read GOALS / PROJECTS / MISSION. Update what's stale.

---

## Personal backlog

*Filled in by interview Round 3 and every check-in. ★ = do first.*

| ID | Area | Idea (outcome-first) | Value 1–3 | Effort S/M/L | Phase | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

## Decisions log

| Date | Decision | Why |
|---|---|---|
| | | |

## Session log

*Newest first. One entry per session. Older entries move to `05-planning/harness-log-YYYY.md` once this file gets long.*

<!-- Template:
### YYYY-MM-DD — P?.? <step name>
- **Did:** …
- **Checked:** … (the evidence)
- **Next:** P?.? — say "Continue my harness plan"
- **Notes:** …
-->
