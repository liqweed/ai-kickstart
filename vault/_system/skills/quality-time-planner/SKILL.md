---
name: quality-time-planner
description: Plan quality time with someone — a partner, a friend, the kids — as a decision-ready plan. Covers nights in, cinema, live shows, dinners out and full evenings, and respects everyone's hard constraints (diet, language, budget, time window, accessibility). Use when the owner says "date night", "plan an evening with…", "what should we watch", "weekend idea with the kids", "somewhere to eat", or "what's on this weekend".
---

# Quality-time planner

> **Also a worked example.** This skill shows the patterns every good personal skill uses: a **first-run interview** that writes a config, **hard-constraint gates**, **ranking signals**, **three options and one recommendation**, and **follow-through the owner controls**. Copy these patterns when building your own skills.

## Who it's for

Read the profiles of everyone involved in `01-life/people/` at the start of every run. Their hard constraints (diet, allergies, accessibility, language) override anything cached.

## Modes

Infer the mode from the request. If it's ambiguous, ask once.

| Mode | Triggers | Deliverable |
|---|---|---|
| **Night in** | "what should we watch", "movie night" | 3 ranked picks: where to stream, runtime, one-line reason each |
| **Out: film / show** | "cinema", "what's on", "concert", "comedy" | Screenings/shows that pass every gate, with times, travel and booking links |
| **Dinner** | "somewhere to eat", "restaurant" | Picks that pass the food gate, near home or near the venue |
| **Full evening** | "plan a date night", "plan an evening" | Dinner + activity as one timed itinerary |
| **Family outing** | "something with the kids this weekend" | Age-appropriate options, weather plan B |

## Phase 0: first-run setup (once)

Check for `config/quality-time.md`. If it exists, read it and skip this phase. If not, run a **short** interview, one topic at a time:

1. **Who** is this usually for? (link their people profiles)
2. **What appeals?** Films, live music, comedy, theatre, museums, walks, food-first evenings…
3. **Taste data?** Any watchlists or ratings services (e.g. Letterboxd, IMDb lists, Goodreads), or a list in the vault?
4. **Budget:** typical spend, and is there a "special occasion" tier?
5. **Logistics:** earliest leave time, latest home time on weeknights vs weekends, transport (car, public transport, bike), babysitter needed?
6. **Hard constraints:** dietary needs, language or subtitle needs, accessibility, "no horror", "nothing over 2.5 hours on a weeknight".

Save the answers to `config/quality-time.md` and confirm them back.

## Gates: hard constraints, checked from data and never assumed

Every candidate passes **every** gate, or it's out. Apply them in this order:

1. **People constraints**: diet, allergies, accessibility. *"Has a gluten-free option" is not the same as "a place a coeliac will enjoy". Prefer places built around the constraint, and flag it when it's only a menu option.*
2. **Language**: e.g. a film must be in a language both understand, or have subtitles they can read.
3. **Time window**: the end time **plus travel home** must fit the latest-home time.
4. **Vetoes** from the config.
5. **Already done**: check past outings in `01-life/social/` so nothing repeats too soon.
6. **Budget.**

When a gate **can't be confirmed** (the venue doesn't publish subtitle info, the menu isn't online), the candidate goes in a separate **"verify before booking"** list with the link. It never sits silently among the confirmed picks. **Unknown is its own answer.**

## Ranking signals

1. **Already wanted**: on someone's watchlist, wishlist or "we should go there" note (the strongest signal)
2. **Affinity**: similar to things they loved before
3. **Fit for the person**: lean toward the interests in their profile
4. **Quality signal**: reviews, ratings, festival selection
5. **Novelty**: not the same kind of thing as the last two outings

## Present

**Three options at most, ordered, with a clear recommendation.** For each: title · when · where · ends at · **one line on why this one**. Then the practical block: leave-home time, transport, dinner slot, booking link. Then, if any, the short "verify before booking" list.

## Data: script it or search it?

- **Search** for questions: what's on, reviews, streaming availability, restaurant options, opening hours.
- **Script** for lists that must be filtered correctly every time, e.g. a cinema chain with a public schedule API, filtered by time window and language. Once the same filtering has been done by hand twice, propose a small script (harness phase P5) in this skill's `scripts/` folder.

## Follow-through (offer, don't auto-run)

- Save the plan to `01-life/social/quality-time/YYYY-MM-DD-<slug>.md`
- Add a booking reminder to the owner's task app or calendar, if connected
- Afterwards: log how it went, and add a line to the people profiles' *Shared history*

**Booking stays manual.** Hand over the links. Never purchase anything.

## Principles

- Decision-ready beats comprehensive.
- Never guess a hard constraint. Confirm it from data, or label it unknown.
- Respect the evening. A great film that ends too late on a school night is a bad recommendation.
- Say what you couldn't load or check.
