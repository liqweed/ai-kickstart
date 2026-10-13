---
name: review-kit
description: Audit the AI Kickstart kit with fresh eyes — simulate a first-time, non-technical friend walking through setup and the interview, check consistency between the website and the vault, tone, accessibility, privacy fingerprints and dead weight — and turn findings into maintenance-plan items. Use for "review the kit", "audit", "fresh-eyes pass", "is the kit still good?", or before a major release.
---

# Review the kit

The checks catch mechanical drift. This review catches what scripts can't: confusing flows, tone, contradictions, stale advice and bloat.

## Passes

Work through them in order. Record findings as you go. **Don't fix during the review.**

1. **First-time friend walkthrough.** Pretend to be someone with tech comfort 2/5 on Windows who uses a plain chat app. Read `README.md` → `START-HERE.html` → ai-kickstart.me `/setup/` (Windows, chat app) → the first-contact prompt → the interview on `/how-it-works/`. Wherever they would get stuck, need a term explained, or face a choice without a recommendation, write it down.
2. **Agent walkthrough.** Read `vault/AGENTS.md` → `_system/index.md` → `HARNESS-PLAN.md` → `skills/kickstart-interview` → `interview-protocol.md` → `round-1`. Could a capable agent run Round 1 and tick P1.1 with **no** other context? Note ambiguities, missing file paths and contradictions.
3. **Consistency.** Do the website, `START-HERE.html` and the vault say the same things about the rounds (count, timing, outputs), phases, skill names, file paths and prompts? (The site parses lists from the vault, but the explanations around them are hand-written. `check_kit.py` only covers the version, the offline page, its prompts and the skills list.)
4. **Generic & private.** Read examples for fingerprints: clusters of specifics (diet + language + city + kids' ages…) that could describe one real household. Run `scripts/scrub.sh`.
5. **Tone & accessibility.** Plain language, no jargon without a gloss, link text that says where it goes, readable contrast in both colour schemes, and the page still makes sense when printed.
6. **Dead weight.** Anything duplicated, over-long, or that no flow leads to? `vault/AGENTS.md` should stay short.

## Output

A short report in the conversation, grouped by severity: **Blocking** (wrong or broken) · **Should fix** (confusing) · **Nice to have**. Then, with the maintainer's OK, add each item as a row in `docs/master-plan.md` (one row each, effort S/M/L), and log the review in `docs/journal.md`.
