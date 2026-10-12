# 05 · Success criteria: companion app

## Quantitative bars

- **5-second next step:** on open, the next action and its prompt are visible without scrolling or clicking, at 800×560.
- **One-click copy** of the next prompt from the home state.
- **First run:** from "app opened" to "It works!" (hello.md detected) in **≤ 6 screens/steps** for Sam, including installing nothing beyond Obsidian.
- **Update clarity:** before applying, the person can see how many files change, which (if any) they edited, and that none of their notes are touched, all in **one** view. Detail is available in one more interaction.
- **Edge states:** every state in the Tweaks list below has a designed screen with exactly one recovery action.
- **Accessibility:** AA contrast in light and dark, keyboard-complete, not colour-alone, usable at 200% text size.

## Qualitative bars

- Feels like a **calm, well-made small utility**, not a productivity dashboard.
- After a three-week gap, Sam feels *welcomed back*, not behind.
- It's always clear that **the AI and Obsidian do the work**; this app keeps your place and keeps you safe.
- A non-technical person would accept an update from it the way they accept a phone update.

## Tweaks scenarios (the prototype must ship a switcher for these)

1. **Fresh install, no vault yet**: first run.
2. **Kit already unzipped**: connect an existing vault (v1.1, nothing done yet).
3. **Waiting for first contact**: the prompt has been copied; the app is watching for `_inbox/hello.md`. Then the success moment.
4. **Mid-interview**: round 2 paused halfway (round 1 file exists, round 2 doesn't).
5. **Sam today** (seed): P2.4 in progress, check-in due tomorrow.
6. **Back after three weeks**: same as 5, but the last session was 2026-10-09.
7. **Phase just completed**: P2 finished, and the app noticed it.
8. **Update available** (v1.2) with 1 conflict and 1 AI-merge hand-off.
9. **Vault missing** (folder moved/renamed).
10. **Obsidian not installed** (during first run).
11. **Light vs dark**, and **macOS vs Windows** webview appearance, for scenarios 1, 5 and 8.

## Evaluation (how the output will be judged)

| Criterion | Weight |
|---|---|
| North star met: the 5-second next step in every home state | High |
| Strength of §3 arguments, especially §3.1 (shape), §3.3 (home states) and §3.6 (updates) | High |
| First-run flow handles the three-app choreography clearly (§3.2) | High |
| Fidelity to `03` (seed data rendered, nothing invented) and to the write rules in `04 §4` | Gate |
| Shares identity and primitives with the website (if the approved website is in the project or in `assets/website/`) | Medium |
