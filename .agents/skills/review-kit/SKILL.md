---
name: review-kit
description: Audit the AI Kickstart kit with fresh eyes — simulate a first-time, non-technical friend walking through setup and the interview, check consistency between guide and vault, tone, accessibility, privacy fingerprints and dead weight — and turn findings into maintenance-plan items. Use for "review the kit", "audit", "fresh-eyes pass", "is the kit still good?", or before a major release.
---

# Review the kit

The checks catch mechanical drift. This review catches what scripts can't: confusing flows, tone, contradictions, stale advice and bloat.

## Passes

Work through them in order. Record findings as you go. **Don't fix during the review.**

1. **First-time friend walkthrough.** Pretend to be someone with tech comfort 2/5 on Windows who uses a plain chat app. Read `README.md` → `START-HERE.html` → `setup.html` → first-contact prompt → `interview.html`. Wherever they would get stuck, need a term explained, or face a choice without a recommendation, write it down.
2. **Agent walkthrough.** Read `vault/AGENTS.md` → `_system/index.md` → `HARNESS-PLAN.md` → `skills/kickstart-interview` → `interview-protocol.md` → `round-1`. Could a capable agent run Round 1 and tick P1.1 with **no** other context? Note ambiguities, missing file paths and contradictions.
3. **Consistency.** Do the guide and the vault say the same things about the rounds (count, timing, outputs), phases, skill names, file paths and prompts? (`check_kit.py` only covers the catalog, version, links and skills list.)
4. **Generic & private.** Read examples for fingerprints: clusters of specifics (diet + language + city + kids' ages…) that could describe one real household. Run `scripts/scrub.sh`.
5. **Tone & accessibility.** Plain language, no jargon without a gloss, link text that says where it goes, readable contrast in both colour schemes, and the page still makes sense when printed.
6. **Dead weight.** Anything duplicated, over-long, or that no flow leads to? `vault/AGENTS.md` should stay short.

## Output

A short report in the conversation, grouped by severity: **Blocking** (wrong or broken) · **Should fix** (confusing) · **Nice to have**. Then, with the maintainer's OK, add each item to the backlog in `docs/HARNESS-PLAN.md` (one line each, effort S/M/L), and log the review in the session log.
