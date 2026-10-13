---
title: Vault Index
type: navigation
status: active
created: 2026-10-12
updated: 2026-10-13
summary: Map of this vault. Agents read this first, every session.
tags: [system, index]
---

# Vault Index

**Agents: read this first.** It says what exists and where. Before writing, follow [[VAULT-CONTRACT|the Vault Writing Contract]].

> Starter version from the AI Kickstart kit. The agent keeps it current as the vault grows (contract §5).

## System (`_system/`)

| Path | What |
|---|---|
| `_system/VAULT-CONTRACT.md` | Rules for every write |
| `_system/TOOLS-CONTRACT.md` | Rules for tools (scripts) and connections: quality, safety, privacy |
| `_system/HARNESS-PLAN.md` | **The build plan**: what's done, what's next. Say "continue my harness plan" |
| `_system/profile/` | Who the owner is: MISSION, GOALS, PROJECTS, LANDSCAPE, PREFERENCES, BELIEFS, LEARNED |
| `_system/kickstart/` | Interview protocol, rounds, function catalog, **connections catalog**, the kit version (`kit-version.md`). Answers go in `answers/` |
| `_system/skills/` | Playbooks (one folder per skill, each with `SKILL.md`) |
| `_system/tools/` | Tested scripts for exact jobs (health check, what's due, what changed, secret scan, kit update). Registry: `_system/tools/README.md` |
| `_system/dashboards/` | Live Bases views: projects, people, inbox, needs attention |
| `_system/templates/` | Note templates: base, project, meeting, person, decision, reference, idea, source, connection |
| `config/` | Per-skill settings, written by first-run interviews |

## Life (`01-life/`)

| Area | What |
|---|---|
| `people/` | One note per person (skill: `people`) |
| `home/` | Home manual, appliances, maintenance, providers |
| `family/` | Family logistics, kids, pets |
| `health/` | Health records and routines |
| `money/` | Budget, subscriptions, insurance, admin |
| `social/` | Outings, quality time, events |
| `travel/` | Trip plans |
| `hobbies/` | Hobbies, watch/read lists |

## Work (`02-work/`)

One folder per job, client or business. *(Filled in after the interview.)*

## Projects (`03-projects/`)

`active/` · `ideas/` · `archive/`. *(None yet.)*

## Learning (`04-learning/`)

One folder per topic. *(None yet.)*

## Planning (`05-planning/`)

- `weekly/YYYY-WXX.md`: weekly reviews (skill: `weekly-review`)
- `monthly/YYYY-MM.md`: monthly reviews

## Reference (`06-reference/`)

Stable facts and how-tos. `connections/` documents each connected app.

- **`06-reference/Working with AI - Tips & Insights.md`**: habits, prompting, trust, privacy and pitfalls. Good to skim in week 2 and revisit monthly.
- **`06-reference/Organizing your vault.md`**: how to organise and curate the vault: folders, links, properties, tags, hubs, rhythms, plugins.

## Briefings (`07-briefings/`)

- `daily/YYYY-MM-DD.md`: daily briefings (skill: `daily-briefing`)

## Other

- `_inbox/`: quick capture, sorted during the weekly review
- `99-archive/`: retired notes

## Navigation guide

1. Find the section here.
2. Open the hub note (`_index.md`) for that area, if there is one. Lists between `auto-index` markers are generated (`hub_index.py`). Don't edit them by hand.
3. Browse the folder.
4. Check `_system/profile/` when a recommendation should fit the owner's goals and preferences.
