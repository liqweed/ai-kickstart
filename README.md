# AI Kickstart

A head start for working with AI across your personal life, family, home and work. It gives your AI a place to live (an Obsidian vault), a memory of you (a profile built through a friendly interview), playbooks (skills), and a step-by-step plan that grows the setup over many short sessions.

Designed and shared by **Ophir Radnitz**. v1.1, October 2026.

- 🌐 **Website:** [ai-kickstart.me](https://ai-kickstart.me) *(coming soon)*. The full guide is also inside the download.
- ⬇️ **Download the kit:** latest zip on the [Releases page](https://github.com/liqweed/ai-kickstart/releases/latest)

## Start here

1. **Open `START-HERE.html`** (or `guide/index.html`) in your browser. The guide explains everything, with copy-paste prompts.
2. **Move the `vault/` folder** somewhere permanent, rename it (e.g. "My Vault"), and open it in [Obsidian](https://obsidian.md) with *Open folder as vault*.
3. **Point your AI tool at that folder** and say: *"Read AGENTS.md and _system/index.md, then tell me what this vault is for."* After that: **"Continue my harness plan."**

## What's inside

```
ai-kickstart/
├── START-HERE.html         → opens the guide
├── guide/                  → 8 pages: start, why, setup, system, interview, catalog, harness, prompts
└── vault/                  → your future Obsidian vault
    ├── AGENTS.md           → how the AI behaves here (CLAUDE.md imports it)
    ├── _system/
    │   ├── index.md        → map of the vault
    │   ├── VAULT-CONTRACT.md
    │   ├── HARNESS-PLAN.md → the trackable build plan
    │   ├── profile/        → MISSION, GOALS, PROJECTS, LANDSCAPE, PREFERENCES, BELIEFS, LEARNED
    │   ├── kickstart/      → interview protocol, rounds 1–5, function catalog
    │   ├── skills/         → kickstart-interview, harness, daily-briefing, weekly-review,
    │   │                     vault-query, vault-save, people, quality-time-planner, skill-builder
    │   └── templates/
    ├── 06-reference/Working with AI - Tips & Insights.md → habits, prompting, trust, pitfalls
    └── _inbox/ 01-life/ 02-work/ 03-projects/ 04-learning/ 05-planning/
        07-briefings/ 99-archive/ config/
```

What changed between versions: [CHANGELOG.md](CHANGELOG.md).

## Maintaining this repo

The repository also holds maintainer scaffolding that isn't part of the downloadable kit: `AGENTS.md` (for AI agents working on the repo), `.agents/skills/`, `docs/`, `scripts/` and `.github/`. Start with [docs/MAINTAINING.md](docs/MAINTAINING.md). Suggestions are welcome as [issues](https://github.com/liqweed/ai-kickstart/issues). See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits & license

- Profile structure adapted from Daniel Miessler's public **TELOS** framework.
- Vault-as-knowledge-base approach inspired by Andrej Karpathy's **LLM Wiki** pattern.
- Everything else comes from a lot of real, day-to-day use.

Licensed under [CC BY 4.0](LICENSE). Share and adapt freely, with credit. If you improve it, pass the improvements on.
