# Changelog

All notable changes to the AI Kickstart kit. Versions are git tags (`vX.Y`). Each tag publishes a zip on the [Releases](https://github.com/liqweed/ai-kickstart/releases) page.

- **Minor (x.Y):** new or changed content: tips, skills, catalog items, guide pages, wording.
- **Major (X.0):** structural changes to the vault template that an existing user would have to migrate (folder layout, profile files, harness-plan format).

## v1.2 — 2026-10-13

- **Clearer for people who already use AI:** the README has a short section for an AI reading the kit on someone's behalf, and the setup pages, harness plan (P0) and `harness` skill now say that an existing setup elsewhere (custom instructions, an AI's memory, another notes app) doesn't count as a done step, and that Obsidian comes first.
- **Setup, path B:** a short note for Craft Agents users (a free, open-source desktop agent): one workspace just for the vault, the permission mode to start in, and where its sources and automations fit in the harness plan.
- **Vault tools** (`vault/_system/tools/`): six tested helper scripts. Python 3.9+, standard library only, Mac/Windows/Linux, all optional.
  - `vault_lint.py`: health check for broken links, missing frontmatter, orphans, duplicate names, index drift, an old inbox, stale notes, unused attachments and secrets.
  - `secret_scan.py`: finds passwords, API keys, card and IBAN numbers, with masked output and an optional git commit guard.
  - `upcoming.py`: due tasks, birthdays, anniversaries, renewals.
  - `recent.py`: what changed and what got done.
  - `fix_frontmatter.py`: dry run by default, `--apply` to write.
  - `hub_index.py`: automatic lists in `_index.md` hubs between markers.
  - Plus a shared library, a template, 27 tests and `selftest.py`, which also checks every tool against the contract. A registry lists them all in `tools/README.md`.
- **`_system/TOOLS-CONTRACT.md`**: rules for building and running tools (shape, safety, privacy, definition of done, upkeep) and for connections (the export → read-only → draft → act ladder, choosing a method, vetting third-party connectors, logins and permissions, the dangerous combination, records and reviews).
- **Connections catalog** (`_system/kickstart/connections-catalog.md`): 40 connections in 12 areas. Each has what it unlocks, a first question to try, how people connect it, where to start, risk and effort. Plus combos and free public data sources. Also on the website at `/connections/`.
- **Three new skills:**
  - `vault-maintenance`: monthly health check, fixed in small batches.
  - `tool-builder`: build, fix and review tools.
  - `connect-app`: explore what's possible, connect one app safely, review connections.
- **`06-reference/Organizing your vault.md`**: folders vs links vs properties vs tags vs hubs, note shapes, writing for future you, the note lifecycle, rhythms, imports, Obsidian features and CLI, plugins, and signs of rot.
- **Dashboards** (`_system/dashboards/`): Obsidian Bases views for projects, people, inbox and notes that need attention.
- **Templates:** Person, Decision, Reference, Idea, Source Note, Connection.
- Hub notes for people, projects, learning, work, reference and connections now keep their note lists automatically (`auto-index` markers).
- **Harness plan:** new steps P0.6 (tools check), P3.6 (first health check), P3.7 (dashboards), P4.0 (explore connections), P5.3 (put the tools to work), P7.4 (monthly health check) and P7.5 (quarterly tools and connections review). P4.x and P5.2 now point to the new skills.
- Existing skills use the tools when available, each with a fallback:
  - `daily-briefing` and `weekly-review` use `upcoming` and `recent`;
  - `people` uses birthdays and the auto-index hub;
  - `skill-builder` points to the tool registry.
- **Vault Writing Contract:** new types (`navigation`, `source`, `connection`), placement rows for tools, dashboards and connections, the hub markers, and a *Keep it healthy* section.
- **Function catalog:** new *Vault health check*; *Connect your apps* points to the connections catalog.
- Four new tips (summaries, monthly health check, connections multiply, tools need tests, the dangerous combination). The setup pages mention the Bases setting, the CLI version and optional Python.

## v1.1 — 2026-10-12

- Added `vault/06-reference/Working with AI - Tips & Insights.md`: a top-10, habits, prompting, trust and verification, context, privacy, life admin, family, work, technical tips and a pitfalls table.
- Harness plan: new step **P3.5** (pick two habits from the tips note).
- Interview Round 5: new question about how those habits went.
- Guide landing page and README link to the tips note.
- Repository scaffolding for maintainers: `AGENTS.md`, maintainer skills, docs, checks, build and release automation.

## v1.0 — 2026-10-12

- First release: 8-page offline HTML guide, Obsidian vault template, 5-round interview, function catalog (103 functions), harness plan P0–P7, 9 starter skills.
