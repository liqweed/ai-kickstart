---
name: refresh-facts
description: Re-verify the time-sensitive facts in the AI Kickstart kit (AI tool names and modes, how agents attach to folders, AGENTS.md/CLAUDE.md/skills conventions, Obsidian settings and CLI, sync options, plan/pricing wording) against current sources and update them. Use quarterly, before a release that's been a while coming, or when someone reports "that setting doesn't exist anymore".
---

# Refresh facts

AI tools change monthly. The kit stays trustworthy only if its few concrete product claims are re-checked from **current sources**. Never from model memory.

## Where the facts live

| Fact | Location |
|---|---|
| The three AI paths and example products (chat app with Projects · desktop agent working in a folder · terminal/coding agents) | `site/src/pages/setup.astro` (connect step), `site/src/lib/choices.ts` (path chooser) |
| How each agent reads instructions (`AGENTS.md`, `CLAUDE.md` + `@` import, native skills folders, the `.claude/skills` symlink) | `site/src/pages/setup.astro` (connect step), `vault/CLAUDE.md`, `site/src/pages/how-it-works.astro` |
| Obsidian: download, "Open folder as vault", *Files and links* settings, Templates plugin, CLI (version + where the toggle is) | `site/src/pages/setup.astro` (Obsidian and vault steps) |
| Sync options (Obsidian Sync, iCloud, OneDrive "Always keep on this device", Syncthing, git) | `site/src/pages/setup.astro` (vault and plan steps) · harness P0.4 |
| Provider data/training settings, "paid plan recommended" | `site/src/pages/setup.astro` (privacy), `site/src/pages/index.astro` |
| Scheduler options (tool schedulers, cron/launchd, Task Scheduler) | `vault/_system/HARNESS-PLAN.md` P6.1 |
| Obsidian Bases (minimum version, where the toggle is, `.base` syntax used by the dashboards) and the CLI commands named in the organizing note | `vault/_system/dashboards/*.base`, `vault/06-reference/Organizing your vault.md` §8–9, `site/src/pages/setup.astro` (Obsidian and vault steps), `site/src/pages/setup.astro` |
| Connections: how people connect each service, which apps offer built-in connectors, MCP status, free public data terms (weather, holidays, OpenStreetMap usage policy) | `vault/_system/kickstart/connections-catalog.md`, `vault/_system/TOOLS-CONTRACT.md` §9–12 |
| Python availability (macOS built-in version, Windows `py` launcher) | `vault/_system/tools/README.md`, harness P0.6 |

## Steps

1. For each row, search the web for the **current** official docs. Prefer vendor documentation over blogs. Record the source URL and its date.
2. Classify each claim: **still true** · **changed** (what's new) · **unverifiable**. Unverifiable claims get softened ("may", "look for…") or removed. Never invent a setting path.
3. Edit with the `evolve-kit` ripple map in mind. The same fact may appear on several pages and in the harness plan.
4. `scripts/check.sh` and `pnpm build && scripts/check_site.py`, then a browser check of `/setup/` with every operating system and AI path chosen, then deploy (`pnpm run deploy`).
5. Add a CHANGELOG **Unreleased** entry ("Refreshed setup facts: …") and log the sources checked in `docs/journal.md`, so the next refresh knows what was verified when.

## Rules

- Keep the kit **tool-agnostic**. Name products only as examples. If a new tool category appears (e.g. phone-native agents with vault access), add it as an option rather than replacing what works.
- Don't chase every release note. Only update what a first-time user would trip over.
