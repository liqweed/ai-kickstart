# 05 · Success criteria: ai-kickstart.me

## Quantitative bars

- **10-second test:** at a 1280×800 and a 390×844 viewport, the first screen alone answers *what is this, who is it for, what do I do next*.
- **One next action:** from first arrival, a comfort-2 visitor reaches their personal first step (the right OS + path setup instructions) in **≤ 3 interactions**.
- **Prompt copy:** any prompt is copyable with **one** click/tap from wherever it's mentioned. Placeholders are distinguishable without colour.
- **Resume:** a visitor returning mid-setup lands back at their step in **≤ 1** interaction (local storage only).
- **Weight:** each page **≤ 200 KB** transferred excluding optional images, with **zero** third-party requests.
- **Accessibility:** AA contrast in light *and* dark mode. Every interaction keyboard-operable with visible focus. No information conveyed by colour alone. Usable at 200% zoom.

## Qualitative bars

- Reads as **a gift from a thoughtful friend**, not a SaaS product or a developer tool.
- A sceptical, non-technical reader comes away thinking *"I could actually do this"*, not *"this is for techies"*.
- The idea of **files you own + small steps over time + you stay in charge** is something you can *feel* in the experience, not just read in a sentence.
- The catalog feels like browsing a menu, and the harness feels encouraging, not like homework.
- Would survive being sent in a WhatsApp message to a parent.

## Tweaks scenarios (the prototype must ship a switcher for these)

1. **First visit, Mac, unknown comfort**: the default arrival.
2. **First visit, Windows work laptop, comfort 2, chat app only**: the hardest path must still feel first-class.
3. **First visit on a phone**: the reader-only, "send it to my laptop" case.
4. **Mid-setup return**: chose macOS + Path B and finished steps 1–2 of setup. Returns after a break.
5. **Catalog with 12 picks** across 5 areas, ready to copy.
6. **Returning user, new version available** (v1.2 is out; they installed v1.1). Show what's new and the "update without losing notes" entry point.
7. **Light vs dark** for every scenario above.

## Evaluation (how the output will be judged)

| Criterion | Weight |
|---|---|
| North star (§2 of `04`) met for the primary persona | High |
| Strength of the §3 arguments: does each choice cite these criteria, and did it challenge the obvious? | High |
| Setup-as-companion experience (§3.4) and prompt treatment (§3.5) | High |
| Fidelity to `03` facts: nothing invented, nothing missing from `01` | Medium |
| Identity coherence across light/dark and readiness to extend to a desktop app | Medium |
| Hard constraints honoured (`04 §4`), especially zero third-party requests and portable plain-CSS styling | Gate (fail = redo) |
