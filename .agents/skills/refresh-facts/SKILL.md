---
name: refresh-facts
description: Re-verify the time-sensitive facts in the AI Kickstart kit (AI tool names and modes, how agents attach to folders, AGENTS.md/CLAUDE.md/skills conventions, Obsidian settings and CLI, sync options, plan/pricing wording) against current sources and update them. Use quarterly, before a release that's been a while coming, or when someone reports "that setting doesn't exist anymore".
---

# Refresh facts

AI tools change monthly. The kit stays trustworthy only if its few concrete product claims are re-checked from **current sources**. Never from model memory.

## Where the facts live

| Fact | Location |
|---|---|
| The three AI paths and example products (chat app with Projects · desktop agent working in a folder · terminal/coding agents) | `guide/setup.html` §1, §3 |
| How each agent reads instructions (`AGENTS.md`, `CLAUDE.md` + `@` import, native skills folders, the `.claude/skills` symlink) | `guide/setup.html` §3, `vault/CLAUDE.md`, `guide/system.html` |
| Obsidian: download, "Open folder as vault", *Files and links* settings, Templates plugin, CLI (version + where the toggle is) | `guide/setup.html` §2 |
| Sync options (Obsidian Sync, iCloud, OneDrive "Always keep on this device", Syncthing, git) | `guide/setup.html` §2 phone tab, §4 · harness P0.4 |
| Provider data/training settings, "paid plan recommended" | `guide/setup.html` §5, `guide/index.html` |
| Scheduler options (tool schedulers, cron/launchd, Task Scheduler) | `vault/_system/HARNESS-PLAN.md` P6.1 |
| "As of <season year>" snapshot line | `guide/setup.html` §1 callout |

## Steps

1. For each row, search the web for the **current** official docs. Prefer vendor documentation over blogs. Record the source URL and its date.
2. Classify each claim: **still true** · **changed** (what's new) · **unverifiable**. Unverifiable claims get softened ("may", "look for…") or removed. Never invent a setting path.
3. Edit with the `evolve-kit` ripple map in mind. The same fact may appear on several pages and in the harness plan.
4. Update the "snapshot from <season year>" line on `guide/setup.html`.
5. `scripts/check.sh`, then a browser check of `setup.html` (all tabs).
6. Add a CHANGELOG **Unreleased** entry ("Refreshed setup facts: …") and log the sources checked in `docs/HARNESS-PLAN.md`, so the next refresh knows what was verified when.

## Rules

- Keep the kit **tool-agnostic**. Name products only as examples. If a new tool category appears (e.g. phone-native agents with vault access), add it as an option rather than replacing what works.
- Don't chase every release note. Only update what a first-time user would trip over.
