---
name: harness
description: Drive the owner's step-by-step AI setup plan in _system/HARNESS-PLAN.md — do the next verified step, show status, add ideas, re-plan. Use when the owner says "continue my harness plan", "next step", "what's next", "harness status", "add to harness", or "re-plan".
---

# Harness

`_system/HARNESS-PLAN.md` is the single source of truth for building the owner's AI setup over many sessions. This skill moves it forward **one small, verified step at a time**, and leaves a clean handoff so the next session (maybe days later, maybe in another AI tool) can pick up without asking.

## Commands

| Owner says | Do |
|---|---|
| "Continue my harness plan" / "next step" | **Session loop** (below) |
| "Harness status" | Count `[x]` / total per phase, show *Now*, the next 3 steps, anything `[?]` blocked. Five lines max. No work. |
| "Add to harness: …" | Add a *Personal backlog* row (ask value 1–3; estimate effort S/M/L and phase). Confirm the row. |
| "Skip that" | Mark the step `[-]` with a reason, log it, move on. |
| "Re-plan" | Re-read the profile and backlog; propose a re-ordering. Apply only after the owner agrees. |

## Session loop

1. **Load, lightly.** Read the plan's frontmatter, the *Now* table, the current phase section and the last 2 session-log entries. Read `_system/profile/PREFERENCES.md`. Don't read the rest of the vault unless the step needs it.
2. **Pick the step.** First `[ ]` or `[/]` step in the current phase whose prerequisites are met, or the step the owner names. If the current phase is all `[x]`/`[-]`, move to the next phase and update *Now*. Backlog items join the phase their row says.
3. **Say the plan in three lines:** what we'll do, how long it should take, and what "done" will look like. Ask before anything that installs software, creates accounts, costs money, touches other people, or is hard to undo.
4. **Do it, small.** If it won't fit in ~30 minutes, split it into sub-steps (`P2.3a`, `P2.3b`, …), write them into the plan, and do the first one.
   - Building a skill? Use the `skill-builder` skill.
   - Connecting an app? Use the `connect-app` skill: research the current method for the owner's tool and OS (it changes often), start **read-only**, document it in `06-reference/connections/<App>.md`.
   - Writing a script? Use the `tool-builder` skill and `_system/TOOLS-CONTRACT.md`: small, single-purpose, tested, registered, and run on real data in front of the owner.
5. **Check.** Run the step's **Check** and show the evidence: the file exists, the output is right, the owner tried it. If it fails, leave the step `[/]` and note why.
6. **Update the plan.**
   - Tick `[x]` only after a passing check.
   - Update *Now* and the frontmatter (`current_phase`, `next_step`, `updated`).
   - Add a session-log entry at the top: **Did / Checked / Next / Notes**.
   - Add any decision to the *Decisions log*, with the why.
7. **Hand off.** End with three lines: what changed, what's next, and the exact phrase to continue ("Continue my harness plan").

## Rules

- **Never tick without evidence.** "It should work" is not a check. A job that "ran" but produced no output did not work.
- **One step per session is a success.** Two is fine. Don't sprint through five without the owner seeing each one work.
- **Plain words.** If the owner rated their tech comfort 1–2, you do the technical parts and narrate briefly. Never leave them with a wall of terminal instructions.
- **Respect the profile.** The steps serve the owner's goals. If a generic step doesn't fit them, propose `[-]`.
- **Keep the plan readable.** Once the session log passes ~40 entries, move older entries to `05-planning/harness-log-YYYY.md` and link it.
- **Portable handoffs.** Write the log so a different AI tool could continue from it alone.
