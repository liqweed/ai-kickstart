---
tags: [system, plan]
type: plan
status: active
created: 2026-10-12
updated: 2026-11-04
summary: The step-by-step build plan for my AI setup — one small, verified step per session.
current_phase: P1
next_step: P1.3
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
| **Current phase** | P1 — Get to know you |
| **Next step** | P1.3 |
| **Blocked** | — |
| **Last session** | 2026-11-04 · P1.2 Round 2 |

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

- [x] **P0.1 Install Obsidian and open this folder as a vault.**
  Done when: Obsidian shows `_system/`, `01-life/`, … in the sidebar. Check: open `_system/index.md` in Obsidian.
- [x] **P0.2 Choose your AI tool** (see the guide's *Setup* page). Pick one that can **read and write files in a folder you choose**. If you only have a chat app for now, choose *chat-only mode* (it works, with a bit of copy-paste).
  Done when: the tool is installed and you're signed in. Check: note the choice in the *Decisions log* below.
- [x] **P0.3 Connect the AI to this vault and test it.** Point the tool at this folder, then ask: *"Read `_system/index.md` and `AGENTS.md`, and tell me in three lines what this vault is for."*
  Done when: it answers correctly **and** can create a test note. Check: ask it to create `_inbox/hello.md`, see it appear in Obsidian, then delete it yourself.
- [x] **P0.4 Backup & sync.** Pick one: Obsidian Sync (paid, easiest, includes phone) · iCloud Drive / OneDrive / Google Drive folder · git (for the technical). Optional: install Obsidian on your phone.
  Done when: the vault lives in a backed-up place. Check: edit a note, see the change on a second device or in the cloud folder.
- [x] **P0.5 Privacy baseline.** Read `_system/profile/PREFERENCES.md` → *Ask me first* and *Never*, and adjust them to taste.
  Done when: you're comfortable with both lists. Check: the AI reads them back to you.
- [-] **P0.6 Tools check** — skipped: chat-only for now. *(optional; desktop or terminal agents)*. Say *"Run the tools self-test"*. The AI runs `python3 _system/tools/selftest.py` (Windows: `py`). If Python is missing, it explains the options and asks before installing anything. Chat-only, or not now? Mark `[-]`: every skill also works without the tools.
  Done when: the self-test says **OK**. Check: the AI shows the last line of its output.

## P1 — Get to know you (the interview)

Start each round with: *"Start round N of my kickstart interview."*

- [x] **P1.1 Round 1, Getting to know you** (~15–20 min). Check: `_system/kickstart/answers/round-1-*.md` exists and `LANDSCAPE.md` is filled.
- [x] **P1.2 Round 2, Where could help feel good?** (~20 min). Check: top 3–5 areas ranked; `GOALS.md` drafted.
- [/] **P1.3 Round 3, Deep dives** (~10 min per area). Check: every top area has backlog items in the *Personal backlog* below.
- [ ] **P1.4 Round 4, How you like to work with AI** (~15 min). Check: `PREFERENCES.md` reflects your answers.
- [ ] **P1.5 Synthesis.** The AI drafts MISSION / GOALS / PROJECTS and fills P2.3–P2.5. Check: you've read and approved every profile file.

## P2 — First wins

- [ ] **P2.1 Daily briefing (vault-only version)**, *if you wanted one in Round 4*. Skill: `daily-briefing`.
  Done when: you get a useful briefing from your notes and tasks. Check: two briefings in `07-briefings/daily/` that you actually read.
- [ ] **P2.2 Weekly review.** Skill: `weekly-review`.
  Done when: one complete review exists in `05-planning/weekly/`. Check: you picked next week's priorities with it.
- [ ] **P2.3a First win #1, part 1: a shared shopping list** ★
  Done when: the list note exists and both adults can add to it. Check: two items added from a phone.
- [ ] **P2.3b First win #1, part 2: the weekly meal plan uses it**
  Done when: the weekly review fills the list. Check: one review that did.
- [ ] **P2.4 First win #2:** *(filled in by the synthesis)*
- [ ] **P2.5 First win #3:** *(filled in by the synthesis)*
- [ ] **P2.6 Use-it check.** After a week: which of P2.1–P2.5 did you use twice or more? Tweak or drop the rest.

## P3 — Capture & memory

- [ ] **P3.1 Capture habit.** Decide how quick thoughts get into `_inbox/`: Obsidian mobile, a share-sheet shortcut, dictation, or emailing yourself. Check: 5 captures in a week.
- [ ] **P3.2 Save & ask.** Try `vault-save` on a useful answer, and `vault-query` on a question your notes should know. Check: one saved note and one cited answer.
- [ ] **P3.3 People.** Add the 3–5 most important people with the `people` skill (only what you're comfortable storing). Check: profiles exist and are linked from `01-life/people/`.
- [ ] **P3.4 Lessons.** Add a first entry to `LEARNED.md`. Check: the weekly review now asks about lessons.
- [ ] **P3.5 Tips & habits.** Skim `06-reference/Working with AI - Tips & Insights.md` (the top 10 is enough) and pick **two** habits to try for two weeks. Check: the two habits are written in the *Decisions log* below, and the Round 5 check-in asks how they went.
- [ ] **P3.6 First vault health check.** Say *"Vault health check"* (skill `vault-maintenance`). Skim [[Organizing your vault]] first if you like: ten minutes, and it explains the why.
  Done when: no red findings are left. Check: the before → after counts from `vault_lint.py` (or the by-hand checklist) are in the session log.
- [ ] **P3.7 Dashboards** *(optional)*. Open [[_system/dashboards/Dashboards|Dashboards]] in Obsidian (needs the core *Bases* plugin) and pick the view you'd look at weekly. Pin or bookmark it.
  Done when: one dashboard shows your real notes. Check: you've opened it twice in a week.

## P4 — Connections (read-only first)

Not sure what's possible? Start with P4.0. Then add one step per app you want connected; the Round 3 backlog and P4.0 say which. The rules are in `_system/TOOLS-CONTRACT.md`, Part B.

- [?] **P4.0 Explore what you could connect.** Say *"What could I connect?"* (skill `connect-app`). The AI shows the five or six connections from the [[connections-catalog|Connections catalog]] that fit your life, each with an example of what it would unlock for you, plus one combo.
  Blocked: waiting for a work laptop policy answer.
  Done when: you picked two or three, and they're added below as P4.x steps in your order. Check: the steps exist, with the first one marked ★.

Template:

- [ ] **P4.x Connect <app> (read-only).** Skill `connect-app`. Method: built-in connector / official MCP server / command-line tool / export file. The AI researches the current best option for your tool and OS, prefers official, and vets anything third-party.
  Done when: the AI can *read* from it in a test. Check: it answers "what's on my calendar tomorrow?" (or the equivalent) correctly, **and** `06-reference/connections/<app>.md` documents how it's connected, what it can do, and how to disconnect.
  Only later, and only if you want: allow *drafts* (e.g. email drafts). Sending stays with you.

## P5 — Scripts & tools

Rule of thumb: **if it's a list that must be filtered correctly every time, script it. If it's a question, ask it.**

- [ ] **P5.1 Spot candidates.** Review the session log: what did the AI do by hand more than twice that has one right answer (filtering, renaming, converting, calculating)? Add each to the backlog as effort **L**.
- [ ] **P5.2 First script.** Build the top candidate with the AI: small, one job, readable, in the skill's `scripts/` folder.
  Skill `tool-builder`, following `_system/TOOLS-CONTRACT.md` Part A. The kit's starter tools in `_system/tools/` are working examples.
  Done when: it works on real data. Check: it has a test, `python3 _system/tools/selftest.py` passes, you saw a run on your own notes, it's in the registry (`_system/tools/README.md`), and the skill's `SKILL.md` says when to use it.
- [ ] **P5.3 Put the starter tools to work.** Wire the tools you'll actually use into your routines: e.g. `upcoming.py` in the morning briefing, `recent.py` in the weekly review. (The starter skills already mention them; this step checks they're used.)
  Done when: at least one tool runs as part of a skill you use. Check: a briefing or review that used a tool's output.

## P6 — Automations

- [ ] **P6.1 Choose a runner.** Your AI tool's scheduler, if it has one, or your OS scheduler (macOS/Linux cron or launchd, Windows Task Scheduler).
- [ ] **P6.2 First scheduled job.** Usually *weekly review prep*, a *content digest*, or the monthly `vault_lint.py` report saved as a note. Schedule it.
  Done when: it has run on schedule. Check: **the output file exists and is correct.** "The job ran" isn't proof; the result is.
- [ ] **P6.3 Two-week watch.** Check: every scheduled run in two weeks produced its output. Note misses in the session log.

## P7 — Evolve (recurring)

- [ ] **P7.1 Check-in (Round 5)** two weeks after P1.5. Then monthly.
- [ ] **P7.2 Prune.** Archive skills you haven't used in a month (ask first). Keep `AGENTS.md` short.
- [ ] **P7.3 Quarterly profile review.** Re-read GOALS / PROJECTS / MISSION. Update what's stale.
- [ ] **P7.4 Monthly vault health check.** Skill `vault-maintenance`. Check: a *Maintenance* line in this month's review, with no red findings left.
- [ ] **P7.5 Quarterly tools & connections review.** Skills `tool-builder` (review mode) and `connect-app` (review mode): still used? Still right? Permissions still minimal? Retire what isn't pulling its weight. Check: a dated *Last reviewed* line on each connection note, and the self-test passing.

---

## Personal backlog

*Filled in by interview Round 3 and every check-in. ★ = do first.*

| ID | Area | Idea (outcome-first) | Value 1–3 | Effort S/M/L | Phase | Status |
|---|---|---|---|---|---|---|
| B1 ★ | Home | Never run out of the basics | 3 | S | P2 | planned |
| B2 | Work | Prep notes before every 1:1 | 2 | M | P2 | idea |
| B3 | Health | Remember the yearly check-ups | 2 | S | P4 | idea |

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-10-20 | Chat-only mode for now | No folder access on the work laptop |

## Session log

*Newest first. One entry per session. Older entries move to `05-planning/harness-log-YYYY.md` once this file gets long.*

### 2026-11-04 — P1.2 Round 2, Where could help feel good?
- **Did:** ran round 2; ranked five areas.
  Home logistics came out on top.
- **Checked:** `GOALS.md` drafted and read back.
- **Next:** P1.3 — say "Continue my harness plan"

### 2026-10-20 — P0.5 Privacy baseline
- **Did:** went through *Ask me first* and *Never*.
- **Checked:** the AI read both lists back.
- **Next:** P1.1
- **Notes:** skipped P0.6, chat-only.

<!-- Template:
### YYYY-MM-DD — P?.? <step name>
- **Did:** …
- **Checked:** … (the evidence)
- **Next:** P?.? — say "Continue my harness plan"
- **Notes:** …
-->
