---
name: skill-builder
description: Turn something the owner does repeatedly into a reusable skill (a playbook the AI follows) — interview, draft SKILL.md, test on real requests, register it. Use when the owner says "make this a skill", "I keep asking for this", "build a skill for…", or when a harness step says to build a skill.
---

# Skill builder

A **skill** is a markdown playbook in `_system/skills/<name>/SKILL.md`: when a request matches its description, the AI reads it and follows it. Skills are how the system remembers *how* to do things, not just *what* the owner knows.

**Build one when** the owner has asked for roughly the same thing twice, or a harness backlog item says so.

## Steps

1. **Gather the spec.** If interview Round 3 produced a spec for this item (in `_system/kickstart/answers/round-3-*.md` → *Specs*), start there. Otherwise ask, briefly:
   - What triggers it? *(the phrases the owner would actually say)*
   - What does great output look like? *(get or sketch an example)*
   - Inputs: which notes, apps or websites?
   - Hard rules: musts and nevers?
   - Autonomy: suggest / draft / do-then-tell?
   - Does it need settings that rarely change? → plan a **first-run interview** writing `config/<name>.md`.
2. **Draft `SKILL.md`** with the template below. Keep it under ~150 lines. Move long reference material (venue lists, checklists, examples) to `references/*.md` and load it only when needed.
3. **Test with two real requests** from the owner, not invented ones. Fix what was clumsy. Most fixes are about the output shape and the hard rules.
4. **Register it:** add a row to the skills table in `AGENTS.md` and to `_system/index.md`.
5. **Log it** in the harness plan (tick the step, add a session-log entry).

## Template

```markdown
---
name: <kebab-case-name>
description: <What it does, in one sentence>. Use when the owner says "<phrase>", "<phrase>", or <situation>.
---

# <Title>

<One paragraph: purpose and what good looks like.>

## Setup (first run only)
Check for `config/<name>.md`. If missing, ask: <3–6 questions, one at a time>. Save the answers there.

## Inputs
| Need | Where |
|---|---|

## Steps
1. …

## Hard rules
- <non-negotiables, checked from data, never assumed>

## Output
<exact shape: a template or example>

## Follow-through (offer, don't auto-run)
- …
```

## Design patterns worth copying

(All demonstrated in `quality-time-planner`.)

- **The description is the trigger.** Put the owner's real phrases in it.
- **First-run interview → config file.** Ask once, remember forever, let the owner edit the file.
- **Gates before ranking.** Hard constraints filter first. Unknown goes in its own list.
- **Three options, one recommendation.** Decision-ready beats a catalogue.
- **Script lists, search questions.** If a list must be filtered correctly every time, build a small tool (skill `tool-builder`, rules in `_system/TOOLS-CONTRACT.md`). If it's an open question, search. Check the registry (`_system/tools/README.md`) first: a starter tool may already do it.
- **Name the connection, and the fallback.** If a skill reads an app (calendar, email), say which connection note it relies on and what to do when it isn't connected.
- **Offer follow-through; don't auto-run it.** Saving, reminders and messages are offers.
- **Say what you don't know.**
