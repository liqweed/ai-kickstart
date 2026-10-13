---
name: evolve-kit
description: Make a content change to the AI Kickstart kit — add or edit a tip, a vault skill, a catalog function, an interview question, a harness step, a template, or a website page — while keeping every copy and cross-reference consistent. Use for "add a tip", "add a skill to the kit", "new catalog item", "change the interview", "new website page", "improve the wording of…".
---

# Evolve the kit

Most kit content is referenced from several places. A change is done only when **every** place agrees and `scripts/check.sh` passes.

## 1. Frame it (before editing)

- **Who is it for?** The end user (website, `START-HERE.html`, vault notes), their AI (vault skills, `vault/AGENTS.md`), or maintainers (docs, scripts)?
- **Does it earn its place?** Prefer improving an existing piece over adding a new one. The kit's own principle applies: small and finished beats big.
- **Is it generic?** No personal or employer specifics. Examples should fit many lives, and no cluster of examples should mirror one real family.
- **Minor or major?** A change that forces existing users to restructure their vault is **major** (see `CHANGELOG.md` header). Avoid it, or include migration notes.

## 2. Ripple map: what else must change

| You change… | Also update |
|---|---|
| A catalog function | `vault/_system/kickstart/function-catalog.md` only (the site's ideas menu parses it). Check the count claims ("around a hundred") in `CHANGELOG.md` and on the site |
| A vault skill (new/renamed) | `vault/AGENTS.md` skills table · `vault/_system/index.md` (if the index mentions it) · README tree · skill count claims ("12 starter playbooks"). The site's skill list is parsed from the skill files |
| A harness step | `vault/_system/HARNESS-PLAN.md` · any skill or round file that ticks that step by ID (`P1.1`…). Phase names and goals reach the site through the parser; a new phase may need the *How it works* text. **Don't renumber existing steps.** Users' plans reference them, so add new ones as `P3.5`, `P3.6` |
| An interview round/question | The round file · `interview-protocol.md` table (if the goal changed) · the round topics in `site/src/pages/how-it-works.astro` · question counts ("about 9 questions") |
| A profile file | `vault/_system/profile/README.md` · `vault/_system/index.md` · `site/src/pages/how-it-works.astro` (system section) · Round 4 synthesis · **major** version |
| A vault folder | `vault/_system/VAULT-CONTRACT.md` placement table · `vault/_system/index.md` · README tree · the tree in `site/src/pages/how-it-works.astro` |
| A tip | `vault/06-reference/Working with AI - Tips & Insights.md`. If it's a principle, consider *Principles* in `site/src/pages/how-it-works.astro` too |
| A vault tool (new/changed) | The tool + a test in `vault/_system/tools/tests/` · registry row in `vault/_system/tools/README.md` · the skill(s) that use it (command + fallback) · counts ("seven come with the kit") in `site/src/pages/how-it-works.astro`, README tree · run `python3 vault/_system/tools/selftest.py`. Follow `vault/_system/TOOLS-CONTRACT.md` Part A |
| A connection (catalog entry) | `vault/_system/kickstart/connections-catalog.md` only (the site parses it; keep the field shape). Counts in CHANGELOG if stated. Methods stay generic; services are examples |
| Who owns a vault file (kit vs the person's) | ARCHITECTURE D18 first · `PERSON_OWNED` in **both** `packages/core/src/update.ts` and `vault/_system/tools/kit_update.py` (checked) · the *Who owns what* list in `vault/_system/skills/kit-update/SKILL.md`. Renaming or moving a person-owned file needs migration notes |
| A contract rule (VAULT- or TOOLS-CONTRACT) | The contract · skills that cite its § numbers (`grep -rn "§" vault/_system/skills`) · `test_contract.py` if a tools rule is machine-checked |
| A template or dashboard | `vault/_system/templates/` or `vault/_system/dashboards/` · `vault/_system/index.md` · the tree in `site/src/pages/how-it-works.astro` |
| A prompt | `site/src/content/prompts.md`. If it's also on `START-HERE.html`, keep the wording identical (checked) |
| A website page (new) | The nav in `site/src/layouts/Base.astro` (keep the phone header one row) · links from neighbouring pages · `scripts/check_site.py` page count |
| `START-HERE.html` | Keep it one self-contained page: inline CSS and JS, no external resources. The footer version stays as-is (the `release` skill bumps it) |

## 3. Write it

- End-user voice: warm, plain, second person, short sentences. Explain any technical term the first time.
- Vault notes follow `vault/_system/VAULT-CONTRACT.md` (frontmatter, links, placement), because the kit should model its own rules.
- Website: reuse the tokens and primitives in `packages/design/kickstart.css` and the page styles in `site/src/styles/site.css`. No new external resources, and no client JS unless a page needs it.

## 4. Verify

1. `scripts/check.sh` passes.
2. Grep for stale counts or names you changed: `grep -rn "<old name>" site/src vault README.md START-HERE.html`.
3. Website changes: `pnpm test && pnpm check && pnpm build && scripts/check_site.py`, then open the changed pages (light + dark, desktop + phone width), click through, and check the console for errors. Same for `START-HERE.html`, opened from the file. Deploy with `pnpm run deploy` once it's committed.
4. Read the changed text once as the **first-time friend**: would they understand it without you?

## 5. Record

- Add a line under an **Unreleased** heading at the top of `CHANGELOG.md` (create it if missing). The `release` skill turns it into a version.
- Commit to `main` with an imperative message. If the change came from the maintenance plan, delete its row from `docs/master-plan.md` and log it in `docs/journal.md`.
