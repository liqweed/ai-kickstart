---
name: people
description: Keep short, kind, useful profiles of the people in the owner's life — preferences, important dates, dietary needs, gift ideas, shared history — and answer questions about them. Use when the owner says "add a person", "update X's profile", "what does X like", "gift ideas for X", "whose birthday is coming up".
---

# People

Profiles live in `01-life/people/<First name>.md`. They power gifts, trips, dinners, quality time and keep-in-touch nudges.

## Profile template

```markdown
---
tags: [people]
type: person
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: <relationship> — <one line>
relationship: <partner|child|parent|friend|colleague|…>
birthday: <MM-DD or YYYY-MM-DD, if known>
---
# <Name>

## Basics
- Relationship: …
- Important dates: …

## Likes / dislikes
- …

## Food
- Dietary needs: … (hard constraints first)
- Favourites: …

## Gift ideas
- [ ] …  *(tick when given; note the date)*

## Sizes & practical
- …

## Shared history
- YYYY-MM-DD — …
```

## Rules

- **Only store what the owner tells you**, and what they'd be comfortable with that person reading. Factual and kind.
- No health details beyond what's practically needed (e.g. allergies), and no ID numbers.
- Hard constraints (allergies, dietary needs, accessibility) go at the top of their section. Other skills treat them as **rules, not preferences**.
- Keep `01-life/people/_index.md` as a simple list of profiles grouped by relationship. Optionally add groups like "Household" or "Close friends" for trip and event planning.
- Query mode ("what does X like?"): answer from the profile and cite it. Say when the profile is thin.
