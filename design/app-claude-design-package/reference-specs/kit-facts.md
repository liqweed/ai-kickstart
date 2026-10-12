# Kit facts (trimmed excerpts from the repo)

Source: github.com/liqweed/ai-kickstart, v1.1. Excerpts only. `03-target-content.md` is the authoritative content list.

## Design decisions behind the kit (from docs/ARCHITECTURE.md, abridged)

| # | Decision | Why |
|---|---|---|
| D1 | The vault template *is* the product; the user's vault starts as `vault/` | Files you own beat features you rent; any AI tool can read Markdown |
| D5 | Interview in rounds; each saves an answer file with "Signals for next round" | Adaptive, resumable; open questions come before the menu so people aren't steered |
| D6 | Harness plan = one Markdown checklist with Done when + Check per step, plus session and decisions logs | Progress survives pauses and tool switches. "No proof, no tick" |
| D7 | Function catalog exists twice: Markdown (for the AI) and an interactive page (for people) | The AI needs plain text; people need ticking and copying |
| D9 | The guide is static and offline, light/dark, OS-aware, with copy buttons | Must work from a zip on any OS and on the web, for non-technical readers |
| D10 | Three AI paths with chat-only fallbacks everywhere | The reader's tools and comfort level are unknown |
| D12 | Privacy by construction | Nothing personal may leak; no tracking |

## Voice (from the kit's maintainer rules)

> End-user voice: warm, plain, second person, short sentences. Explain any technical term the first time.

## What a vault looks like (folder map)

```
vault/
├── AGENTS.md            how the AI behaves here
├── _inbox/              quick capture → sorted in the weekly review
├── _system/
│   ├── index.md         the map, read first
│   ├── VAULT-CONTRACT.md
│   ├── HARNESS-PLAN.md
│   ├── profile/         MISSION · GOALS · PROJECTS · LANDSCAPE · PREFERENCES · BELIEFS · LEARNED
│   ├── kickstart/       interview protocol, rounds 1–5, function catalog, answers/
│   ├── skills/          one folder per playbook
│   └── templates/
├── 01-life/ 02-work/ 03-projects/ 04-learning/ 05-planning/
├── 06-reference/        incl. "Working with AI - Tips & Insights"
├── 07-briefings/ 99-archive/ config/
```

## A harness-plan step (verbatim format)

```
- [ ] P0.3 Connect the AI to this vault and test it. Point the tool at this folder, then ask…
  Done when: it answers correctly and can create a test note.
  Check: ask it to create _inbox/hello.md, see it appear in Obsidian, then delete it yourself.
```
