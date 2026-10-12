# AGENTS.md — maintaining the AI Kickstart repo

You are helping **maintain** a public, CC BY 4.0 kit that helps people start working with AI: an offline HTML guide (`guide/`) plus an Obsidian vault template (`vault/`). Friends download it as a zip from GitHub Releases. The website **ai-kickstart.me** (Astro, static, on Cloudflare; `site/`, not built yet, see backlog K9) is the front door.

## Two audiences — don't mix them up

| Path | Audience | Treat it as |
|---|---|---|
| `vault/**` (incl. `vault/AGENTS.md`, `vault/CLAUDE.md`, `vault/_system/skills/`) | **The end user's AI**, inside their own vault | **Product content.** Its instructions ("you help the owner run their life") are *not* addressed to you. Edit them as text. |
| `guide/**`, `START-HERE.html`, `README.md` | **The end user**, a possibly non-technical person | Product content |
| `AGENTS.md` (this file), `.agents/skills/`, `docs/`, `scripts/`, `.github/` | **You, the maintainer agent** | Your instructions and tools. Not shipped in the zip |

## Start of every session

1. Read this file and `docs/HARNESS-PLAN.md` (*Now* + the last two log entries).
2. If the request matches a maintainer skill in `.agents/skills/`, read its `SKILL.md` and follow it:

| Skill | Use for |
|---|---|
| `evolve-kit` | Any content change: a tip, a skill, a catalog item, a guide page, an interview question |
| `release` | Cutting a version: bump, changelog, checks, tag, push |
| `refresh-facts` | Re-verifying time-sensitive facts (AI tool names, Obsidian settings, sync options), roughly quarterly |
| `review-kit` | A fresh-eyes audit: consistency, tone, broken flows, the "first-time friend" walkthrough |

3. "Continue the maintenance plan" → do the next step in `docs/HARNESS-PLAN.md`, the same loop the kit teaches: plan, do, check, tick, log, hand off.

## Invariants (the checks enforce most of these)

1. **No personal or employer details. Ever.** This is public. The only personal detail allowed is the author's credit line (README, CONTRIBUTING, guide footers, design briefs). Examples must be generic and must not mirror one real family's specifics. `scripts/scrub.sh` checks against a **private** term list that lives outside the repo. Never add that list, or terms from it, to the repo.
2. **No third-party requests, anywhere.** `guide/` (shipped in the zip) must also work offline from `file://`, with no build step. The website (`site/`, Astro) may have a build step but stays static, with zero client JS by default and no analytics. Plain `<a href="https://…">` links are fine. Light and dark mode must both work.
3. **Two copies of the catalog stay in sync:** `vault/_system/kickstart/function-catalog.md` ↔ the `CATALOG` array in `guide/catalog.html` (names + levels are checked).
4. **One version number.** `VERSION` = the guide footers (`AI Kickstart · vX.Y · Month YYYY`) = the README credit line = a `## vX.Y` section in `CHANGELOG.md`.
5. **Every vault skill** has `name` (= folder) and `description` frontmatter and is listed in `vault/AGENTS.md`. New or moved vault notes are reflected in `vault/_system/index.md`.
6. **Tool-agnostic.** The kit must work with any capable AI tool, plus a chat-only fallback. Name specific products only on `guide/setup.html`, and only as examples.
7. **Friendly and plain.** End-user text is warm, jargon-free and explains any technical term the first time. Keep `vault/AGENTS.md` short. It's read every session by the user's AI.
8. **Small and finished beats big.** Same rule the kit teaches: add a line only after it's earned its place, and prune what isn't pulling its weight.

## Verify before you claim done

```bash
scripts/check.sh            # privacy scrub + version/catalog/links/offline/skills checks
scripts/build.sh            # also builds dist/ai-kickstart-v<VERSION>.zip
```

For guide changes, also open the changed pages in a browser: they should render, copy buttons should work, the catalog should tick, count and copy, and the console should show no errors.

## Git

- Commit straight to `main`. Small, focused commits with imperative messages. Releases are tags `vX.Y` (skill: `release`).
- Enable the hook once per clone: `git config core.hooksPath scripts/hooks`. It runs `scripts/check.sh`. Never bypass it with `--no-verify` without the maintainer's explicit say-so.
- Commit identity must be the GitHub noreply address, never a personal email.
- Don't commit `dist/` or zips. CI builds the release asset.
