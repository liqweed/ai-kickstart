---
tags: [system, kickstart]
type: reference
status: active
created: 2026-10-12
updated: 2026-10-12
summary: How the AI conducts the kickstart interview — tone, pacing, rounds, and what gets saved.
---

# Interview protocol

The interview is how the AI gets to know its owner. It runs in **rounds**, one per session, roughly 15–25 minutes each. **Each round reads the answers from the rounds before it** and adapts. Nobody gets asked about their kids' school if they told us in Round 1 they don't have kids.

| Round | Name | Goal | Feeds |
|---|---|---|---|
| 1 | [[round-1-landscape\|Getting to know you]] | Their situation: life, work, devices, tools, comfort with tech, privacy lines | `LANDSCAPE.md`, the shortlist of areas for Round 2 |
| 2 | [[round-2-areas\|Where could help feel good?]] | What drains them, what slips, what they'd love more of. Pick the top 3–5 areas | Ranked areas for Round 3 |
| 3 | [[round-3-deep-dives\|Deep dives]] | One short deep dive per top area: how it works today and what "great" looks like | Backlog items in `HARNESS-PLAN.md` |
| 4 | [[round-4-working-style\|How you like to work with AI]] | Tone, autonomy, guardrails, rhythms. Then **synthesis** | All profile files, first three wins |
| 5 | [[round-5-checkin\|Check-in]] | After ~2 weeks, then monthly: what worked, what didn't, what's next | Plan adjustments, `LEARNED.md` |

## Tone: friendly, accessible, unhurried

- **One question at a time.** At most two short related ones together. Never a wall of questions.
- **Show progress:** "Round 1 · question 3 of about 9".
- **Say why you're asking**, in half a sentence: "*so I can suggest things that work on your phone*".
- **Offer examples or choices** for every question (3–6 options), always plus "something else" and "skip". Many people find it easier to react than to invent.
- **Plain words.** No jargon. If a technical word is unavoidable, explain it in brackets the first time: "MCP (a plug that lets the AI read an app, like your calendar)".
- **Rambling is welcome.** Invite voice dictation and long answers. Structuring them is your job.
- **Reflect back** every 3–4 answers: "So far I've got: … Did I get that right?"
- **Follow the energy.** When they light up about something, ask one follow-up. When an area is clearly irrelevant, skip it without comment.
- **Respect privacy.** Never push for detail. "Keep it as vague as you like" is always true. Never ask for passwords, ID numbers, account numbers, or medical details beyond what they volunteer.
- **Pause anytime.** Tell them at the start: "Say 'pause' whenever and we'll pick up here next time." If they pause, save what you have and note where you stopped.
- **Celebrate, lightly.** End each round with something concrete they'll get from it. Skip the gushing.

## Before each round

1. Read this protocol and the round's file.
2. Read **all** earlier answer files in `_system/kickstart/answers/`, especially their **Signals for next round** sections.
3. Read `_system/profile/LANDSCAPE.md` and `PREFERENCES.md` if they're filled in.
4. Plan the round. Drop questions that are already answered or irrelevant, and add follow-ups the signals suggest. Tell the owner roughly how many questions and minutes to expect.

## After each round

1. **Summarise** in 5–8 bullets, in their words, and ask "anything to fix?"
2. **Save** `_system/kickstart/answers/round-N-YYYY-MM-DD.md` using the format below. Clean bullets, not a transcript.
3. **Update** the profile files that round feeds. Show the diff, or a short summary of the changes, before saving.
4. **Tick** the round's step in `_system/HARNESS-PLAN.md` and add a session-log entry.
5. **Hand off**: say what the next round covers and give the exact words to start it, e.g. *"Start round 2 of my kickstart interview."*

## Answer file format

```markdown
---
tags: [system, kickstart]
type: log
status: done
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: Kickstart interview round N — <one line>
---

# Round N — <name>

## What I heard
- <topic>: <their answer, cleaned up, in their words>
- …

## Skipped / parked
- <question> — <why: skipped, not relevant, "later">

## Signals for next round
<!-- For the agent: what to explore, hypotheses to test, things to avoid, tone notes -->
- …
```

## Chat-only mode (the AI can't write files)

If the AI can't save files, as in a plain chat app, everything still works. At the end of each round, output **one** markdown block headed *"Paste this into `_system/kickstart/answers/round-N-YYYY-MM-DD.md`"*, plus separate blocks for each profile file that changed. At the start of the next round, ask the owner to paste or attach the previous answer files.
