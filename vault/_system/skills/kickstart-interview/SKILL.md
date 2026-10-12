---
name: kickstart-interview
description: Run the friendly, multi-round kickstart interview that gets to know the owner (life, work, devices, wishes, working style) and turns it into their profile and harness plan. Use when the owner says "start the interview", "get to know me", "start round N", "kickstart", "check-in", or when the profile files are still empty.
---

# Kickstart interview

The interview turns a stranger into an assistant that knows its owner. It runs in five rounds, and **every round builds on the answers before it**.

## Steps

1. **Read** `_system/kickstart/interview-protocol.md`. It defines tone, pacing and what gets saved. Follow it closely: friendly, one question at a time, examples for every question, skip always allowed.
2. **Find the round.** List `_system/kickstart/answers/`.
   - Owner named a round → run that one.
   - No answers yet → Round 1.
   - Otherwise → the next round without an answer file. If Round 3 is partly done, continue with the remaining top areas.
   - Round 4 done → offer Round 5 (check-in) if it's been ~2 weeks since the last answer file; otherwise suggest "Continue my harness plan" instead.
3. **Prepare.** Read the round file (`round-N-*.md`), every earlier answer file (especially *Signals for next round*), `LANDSCAPE.md` and `PREFERENCES.md`. Drop questions already answered and add follow-ups the signals suggest.
4. **Run the round** as the protocol describes. Show progress, reflect back every few answers, honour "pause".
5. **Close the round** exactly as the protocol's *After each round* section says: summary → save the answer file → update the profile (show changes first) → tick the harness step → hand off with the exact phrase for the next round.

## If the owner is in a hurry

Offer the **express version**: Rounds 1 and 2 merged, ~10 core questions, 20 minutes. Then go straight to synthesis with sensible defaults, and mark the deep dives as backlog steps in the harness plan to do later.

## If the AI can't write files

Use the protocol's *Chat-only mode*: produce paste-ready markdown blocks at the end of each round.
