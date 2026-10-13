---
name: evolve-kit
description: Make a content change to the AI Kickstart kit — add or edit a tip, a vault skill, a catalog function, an interview question, a harness step, a template, or a guide page — while keeping every copy and cross-reference consistent. Use for "add a tip", "add a skill to the kit", "new catalog item", "change the interview", "new guide page", "improve the wording of…".
---

# Evolve the kit

Most kit content is referenced from several places. A change is done only when **every** place agrees and `scripts/check.sh` passes.

## 1. Frame it (before editing)

- **Who is it for?** The end user (guide, vault notes), their AI (vault skills, `vault/AGENTS.md`), or maintainers (docs, scripts)?
- **Does it earn its place?** Prefer improving an existing piece over adding a new one. The kit's own principle applies: small and finished beats big.
- **Is it generic?** No personal or employer specifics. Examples should fit many lives, and no cluster of examples should mirror one real family.
- **Minor or major?** A change that forces existing users to restructure their vault is **major** (see `CHANGELOG.md` header). Avoid it, or include migration notes.

## 2. Ripple map: what else must change

| You change… | Also update |
|---|---|
| A catalog function | **Both** `vault/_system/kickstart/function-catalog.md` and the `CATALOG` array in `guide/catalog.html` (same name and level). Check the count claims ("103", "around a hundred") on `guide/catalog.html`, `guide/index.html`, `CHANGELOG.md` |
| A vault skill (new/renamed) | `vault/AGENTS.md` skills table · `vault/_system/index.md` (if the index mentions it) · `guide/system.html` starter-skills table · README tree · `guide/index.html` "What's in the box" · skill count claims ("9 starter playbooks") |
| A harness step | `vault/_system/HARNESS-PLAN.md` · `guide/harness.html` (phases table, if phase-level) · any skill or round file that ticks that step by ID (`P1.1`…). **Don't renumber existing steps.** Users' plans reference them, so add new ones as `P3.5`, `P3.6` |
| An interview round/question | The round file · `interview-protocol.md` table (if the goal changed) · `guide/interview.html` round card · question counts ("about 9 questions") |
| A profile file | `vault/_system/profile/README.md` · `vault/_system/index.md` · `guide/system.html` · Round 4 synthesis · **major** version |
| A vault folder | `vault/_system/VAULT-CONTRACT.md` placement table · `vault/_system/index.md` · README tree · `guide/system.html` tree · `guide/index.html` tree |
| A tip | `vault/06-reference/Working with AI - Tips & Insights.md`. If it's a principle, consider `guide/why.html` → *Principles* too |
| A prompt | `guide/prompts.html`. If it's also shown on `interview.html`, `harness.html` or `setup.html`, keep the wording identical |
| A guide page (new) | Nav bar in **every** page · pager links of neighbours · `guide/index.html` · README tree |
| Any guide page | Footer version stays as-is (the `release` skill bumps it) |

## 3. Write it

- End-user voice: warm, plain, second person, short sentences. Explain any technical term the first time.
- Vault notes follow `vault/_system/VAULT-CONTRACT.md` (frontmatter, links, placement), because the kit should model its own rules.
- Guide HTML: reuse existing components from `guide/assets/kit.css` (`.card`, `.callout`, `.prompt`, `.steps`, `.tabs`…). No new external resources. Copy the header and footer from an existing page.

## 4. Verify

1. `scripts/check.sh` passes.
2. Grep for stale counts or names you changed: `grep -rn "<old name>" guide vault README.md`.
3. Guide changes: open the pages in a browser (light + dark), click through, and check the console for errors.
4. Read the changed text once as the **first-time friend**: would they understand it without you?

## 5. Record

- Add a line under an **Unreleased** heading at the top of `CHANGELOG.md` (create it if missing). The `release` skill turns it into a version.
- Commit to `main` with an imperative message. If the change came from the maintenance plan, delete its row from `docs/master-plan.md` and log it in `docs/journal.md`.
