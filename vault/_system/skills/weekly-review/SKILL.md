---
name: weekly-review
description: Run a guided weekly review — look back, empty the inbox, update projects, pick next week's priorities, capture lessons, and take one harness step. Use when the owner says "weekly review", "plan my week", "review my week", or on the scheduled weekly slot.
---

# Weekly review

The weekly review is the heartbeat of the system: it's when loose ends get tied, the inbox gets emptied and next week gets chosen on purpose. **Target: 20–30 minutes**, interactive.

## Steps

1. **Look back (5 min).** Read the last 7 daily briefings (if any), the previous weekly review, and `PROJECTS.md`. With tools: `python3 _system/tools/recent.py --days 7` lists what changed and what got done. Ask: *"What went well? What didn't? Anything still on your mind?"* Write their answer down, briefly.
2. **Empty the inbox (5 min).** For each note in `_inbox/`, propose where it goes (per `VAULT-CONTRACT.md` §2): file it, turn it into a task, or delete it. **Ask before deleting.** Group similar items to keep it quick.
3. **Projects (5 min).** For each active project in `PROJECTS.md`: one-line status and next step. Is anything stuck? Done? Should something move to *Waiting / someday*?
4. **Look ahead (5 min).** Ask about next week's fixed commitments (or read the calendar if connected). With tools: `python3 _system/tools/upcoming.py --days 10` adds deadlines, birthdays and renewals. Propose **3 priorities** tied to `GOALS.md` → *Now*. The owner picks.
5. **Lessons (1 min).** *"Anything worth adding to LEARNED?"* If yes, propose the line.
6. **Harness (optional, 1 min).** Show the next harness step and ask: *"Want to do it now, or this week?"*
7. **First week of the month?** Offer the monthly health check (skill `vault-maintenance`), now or later this week.

## Output: `05-planning/weekly/YYYY-WXX.md`

```markdown
---
tags: [planning, review]
type: review
status: done
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: Weekly review YYYY-WXX — <one line>
---
# Week XX review

## Looking back
- Went well: …
- Didn't: …

## Inbox
- Filed N, tasks N, deleted N

## Projects
| Project | Status | Next step |

## Next week's 3 priorities
1. …

## Lesson
- …
```

Then update `PROJECTS.md` with the new statuses (show the changes first).
