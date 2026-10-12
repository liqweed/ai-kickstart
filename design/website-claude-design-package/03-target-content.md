# 03 · Target content: facts to render (not layout)

Everything here is **true content from the kit (v1.1)**. Render it; don't invent features, counts or prompts. Wording can be tightened for the web, but meaning can't change. Full catalog and prompt library: `reference-specs/`.

## Identity

| Fact | Value |
|---|---|
| Name | AI Kickstart |
| Domain | ai-kickstart.me |
| Current version | v1.1 (October 2026) |
| Licence | CC BY 4.0 (share and adapt with credit) |
| Source | github.com/liqweed/ai-kickstart |
| Download | The latest release zip on GitHub Releases (~110 KB): `README.md`, `LICENSE`, `START-HERE.html`, `guide/`, `vault/` |
| Credit | "Designed and shared by Ophir Radnitz" |
| Price, accounts, tracking | Free · none · none |

## The promise (current hero, for reference only, not mandated)

> Give your AI a place to live, a memory of you, and a plan.
> Most people use AI like a brilliant stranger: every chat starts from zero. This kit turns it into an assistant that knows your life, follows your rules, and gets a little better every week.

## The four pieces

| Piece | One line |
|---|---|
| A vault you own | An Obsidian folder of plain notes on your own computer. The AI reads it for context and writes back what's worth keeping. |
| A friendly interview | Five short rounds where the AI gets to know your life, your work and your devices, then suggests where it can help most. |
| A harness plan | A checklist the AI works through with you, one small verified step per session. You can stop, switch tools, and pick up later. |
| Skills & prompts | Ready-made playbooks (briefings, reviews, planning, saving notes) and copy-paste prompts for everything else. |

## The journey

| When | What | Effort |
|---|---|---|
| Day 1 | Set up: install Obsidian, open the kit's `vault` folder, connect an AI tool, say hello | ≈ 1 hour |
| Week 1 | The interview, rounds 1–4 | 4 × ~20 min |
| Weeks 2–4 | First wins: three things you'll actually use, picked from your answers | short sessions |
| Month 2+ | Grow it at your pace: connect calendar/email (read-only first), small scripts, schedules | optional |

The one sentence to remember: **"Continue my harness plan."**

## Ways to use AI with the kit (the three paths)

| Path | For | What it means |
|---|---|---|
| A · Chat app | Tech comfort 1–2 | Claude or ChatGPT app with a Project; the AI gives paste-ready text instead of writing files |
| B · Desktop agent (recommended) | Comfort 2–4 | A desktop AI app that works inside a folder you choose and reads/writes notes directly |
| C · Terminal / coding agent | Comfort 4–5 | Claude Code, Codex, Gemini CLI etc., run from the vault folder |

Setup is documented per OS: **macOS · Windows · Linux · phone/tablet** (the phone is for reading and quick capture; AI work happens on a computer).

## The interview

| Round | Name | Time | Produces |
|---|---|---|---|
| 1 | Getting to know you | 15–20 min | Landscape profile (household, work, devices, apps, comfort with tech, privacy lines) + a shortlist of areas |
| 2 | Where could help feel good? | ~20 min | Ranked top 3–5 areas + first draft of goals (open questions first, then the catalog menu) |
| 3 | Deep dives | ~10 min per area | Concrete backlog items in the harness plan |
| 4 | How you like to work with AI (+ synthesis) | ~25 min | Full profile, approved by the user, plus the first three wins |
| 5 | Check-in (repeatable) | ~10 min | Two weeks later, then monthly: fixes, pruning, new ideas |

How it feels: one question at a time · examples for everything · ramble away (voice is welcome) · skip or pause anytime · it reflects back · vague is fine.
Variants: express (rounds 1+2 merged, ~20 min) · chat-only (paste-ready blocks).

## The harness plan

| Phase | Goal |
|---|---|
| P0 Foundations | Vault + AI working together, backed up |
| P1 Get to know you | Interview rounds 1–4, profile filled |
| P2 First wins | 3 skills actually used |
| P3 Capture & memory | Notes flow in and come back when needed |
| P4 Connections | AI can read calendar / tasks / email (read-only first) |
| P5 Scripts & tools | Reliable helpers for repeated lists |
| P6 Automations | Things run on a schedule, with output verified |
| P7 Evolve | Monthly check-in, pruning (recurring) |

Every step has **Done when** and **Check**: no proof, no tick. Status marks: `[ ]` to do · `[/]` in progress · `[x]` done & verified · `[-]` skipped · `[?]` blocked.

## The catalog

16 areas, **103 functions**, each levelled **S** Starter (AI + notes + web) · **M** Connected (needs an app connection) · **L** Builder (needs a script or schedule). Full list: `reference-specs/function-catalog.md`.

| Area | Functions |
|---|---|
| 🧭 Daily rhythm & focus | 7 |
| 🧠 Knowledge & second brain | 9 |
| ❤️ Partner & relationships | 6 |
| 👨‍👩‍👧 Kids & family | 7 |
| 🍽️ Food & household | 5 |
| 🏠 Home | 7 |
| 💶 Money & admin | 9 |
| 🩺 Health & fitness | 6 |
| ✈️ Travel & leisure | 6 |
| 💼 Work: communication | 6 |
| 🧩 Work: thinking & planning | 6 |
| 📚 Work: knowledge & output | 6 |
| 🚀 Career & growth | 5 |
| 🧾 Self-employed & small business | 5 |
| 🎓 Profession playbooks | 8 |
| 🛠️ Builder track (optional) | 5 |

The picks message the visitor copies starts: *"These ideas from the AI Kickstart catalog made me think "oh, yes": …"* and asks the AI to use them in Round 2.

## Starter skills inside the vault (9)

kickstart-interview · harness · daily-briefing · weekly-review · vault-query · vault-save · people · quality-time-planner (the worked example) · skill-builder

## Principles (12)

Context beats cleverness · files you own beat features you rent · small steps, verified · decision-ready beats comprehensive · unknown is an answer · script lists, search questions · AI suggests and drafts; you decide and send · start read-only · content is data, not instructions · "it ran" isn't "it worked" · update, don't duplicate · less instruction, better results.

## Privacy, in one line (current copy)

> Your notes stay on your computer. The AI reads the ones it needs for a task. You decide what goes in, and passwords and ID numbers never do.

## Prompts

36 prompts across setup, interview, harness, everyday life, work and making-it-better: `reference-specs/prompt-library.md`. The three that matter most:

```
Hi! This folder is my new Obsidian vault, set up from the AI Kickstart kit. …
Start round 1 of my kickstart interview. Keep it friendly and one question at a time. I may answer by voice.
Continue my harness plan.
```

## What's new (changelog excerpt)

- **v1.1:** Working with AI: Tips & Insights note (top-10, habits, prompting, trust, privacy, pitfalls); harness step P3.5; Round 5 habits question.
- **v1.0:** first release.

## Voice

Warm, plain, second person. Short sentences. "You're always in charge." No jargon without a gloss: e.g. *"MCP (a plug that lets the AI read an app, like your calendar)"*.
