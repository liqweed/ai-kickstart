---
name: daily-briefing
description: Produce a short morning briefing — today's schedule, top three priorities, what's due, and one nudge from the owner's goals. Use when the owner says "morning briefing", "daily briefing", "what's on today", or "plan my day".
---

# Daily briefing

A briefing the owner can read in **under two minutes** that answers: *what matters today, and what's the first thing to do?*

## Inputs (use what exists, skip what doesn't)

| Input | Where |
|---|---|
| Goals & projects | `_system/profile/GOALS.md` → *Now*, `PROJECTS.md` → *Active* |
| Open tasks | `- [ ]` items in the vault, especially in `PROJECTS.md`, project notes and the last weekly review |
| Due & dates | If you can run commands: `python3 _system/tools/upcoming.py --days 3` (overdue tasks, due dates, birthdays, renewals). Otherwise scan for dated tasks by hand |
| Yesterday | the previous file in `07-briefings/daily/` (what carried over?) |
| Calendar | only if connected (see `06-reference/connections/`); otherwise ask "anything fixed today?" |
| This week's priorities | latest `05-planning/weekly/` review |
| Style | `PREFERENCES.md` |

## Output: `07-briefings/daily/YYYY-MM-DD.md`

```markdown
---
tags: [briefing]
type: briefing
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: Daily briefing for <weekday> <date>
---
# <Weekday> <date>

**Today in one line:** …

## Fixed times
- 09:30 …  (or "Nothing fixed. A good day for deep work.")

## Top 3
1. … — *why today*
2. …
3. …

## Due / slipping
- …

## One nudge
<one sentence linking today to a goal in GOALS.md, or a gentle "you said you wanted more X">

## Start with
<the very first 15-minute action>
```

## Rules

- Three priorities, not ten. If everything is urgent, say so and pick anyway.
- Carry over unfinished top-3 items from yesterday only if they still matter; otherwise ask to drop them.
- Don't invent calendar items. If the calendar isn't connected, say "calendar not connected".
- Keep it under ~200 words.
