# Maintaining the AI Kickstart

For humans. (AI agents: start with [`AGENTS.md`](../AGENTS.md).)

## One-time setup per clone

```bash
git clone git@github.com:liqweed/ai-kickstart.git && cd ai-kickstart
git config user.email "<your-id>+<your-login>@users.noreply.github.com"   # never a personal email
git config core.hooksPath scripts/hooks                                    # pre-commit runs scripts/check.sh
```

**Private scrub list.** Create `~/.config/ai-kickstart/scrub-terms.txt`: one case-insensitive regex per line (names of people and pets, places, employers, private hosts, personal emails, home paths). It must **never** be committed. Without it, the hook refuses to commit; contributors can run `scripts/check.sh --optional-scrub`.

## Repository settings (one-time, in the GitHub web UI)

1. **Website (`site/`, live since 2026-10-13):** a Cloudflare Worker with static assets (no Worker code), configured by `site/wrangler.jsonc`, which pins the account ID, the custom domain and `workers_dev: false`. Zone ai-kickstart.me is on Cloudflare's Free plan; the domain is registered at Name.com with Cloudflare nameservers.
   - **Deploy:** `pnpm run deploy` at the repo root (builds, runs `scripts/check_site.py`, then `wrangler deploy`). Wrangler needs its own login once: `cd site && npx wrangler login`.
   - **Account tasks** (zone settings, DNS, rules, certificates) use the `cf` CLI with the `ai-kickstart` profile. Always pass `--profile ai-kickstart` and set `CLOUDFLARE_ACCOUNT_ID`: the folder binding alone did not stop an account-level command from going to another account. Zone commands take `-z <zone-id>`.
   - **Don't run `cf build` / `cf deploy` / `cf dev` here.** `cf` 1.0 beta can't build this static site, and without a terminal it rewrites the project (adds Astro's server adapter) without asking. Re-check when `cf` leaves beta.
   - **Zone settings that must stay:** Always Use HTTPS on, HSTS on (1 year, includeSubDomains, preload), minimum TLS 1.2, email obfuscation off, Rocket Loader off, no Web Analytics / RUM site for this zone (each would inject a script and break the no-tracking promise and the CSP). `www` is a proxied `AAAA 100::` placeholder plus one redirect rule (301 to the bare domain, keeping path and query).
2. **CI scrub (optional, recommended):** Settings → Secrets and variables → Actions → New secret `SCRUB_PATTERN`, value = the terms joined with `|`:
   ```bash
   grep -vE '^[[:space:]]*(#|$)' ~/.config/ai-kickstart/scrub-terms.txt | paste -sd'|' - | tr -d '\n' | pbcopy
   ```
   `scrub.sh` also tolerates stray newlines/CRs and refuses a pattern that would match everything. Without the secret, CI skips the scrub with a warning. The local hook remains the main guard.
3. **Issues:** keep them enabled. The templates in `.github/ISSUE_TEMPLATE/` collect friend feedback.

## Everyday commands

| Task | Command |
|---|---|
| All checks | `scripts/check.sh` |
| Build the zip locally | `scripts/build.sh` → `dist/ai-kickstart-v<VERSION>.zip` |
| Vault tools self-test | `python3 vault/_system/tools/selftest.py` (also run by `check.sh`) |
| Lint the template vault | `python3 vault/_system/tools/vault_lint.py --strict` |
| Preview the offline page | open `START-HERE.html` in a browser |
| Install website tools (once) | `pnpm install` (Node 22.12+, pnpm 10) |
| Website dev server | `pnpm dev` → http://localhost:4321 |
| Website checks | `pnpm test && pnpm check && pnpm build && scripts/check_site.py` |

## Working with an AI agent on the repo

Open your agent in the repo root and say one of:

- *"Continue the maintenance plan."* Does the first item under *Now* in [`docs/master-plan.md`](master-plan.md), deletes its row when done, and logs the session in [`docs/journal.md`](journal.md).
- *"Add a tip: …"* / *"Add a catalog function: …"* / *"Add a skill to the kit: …"* Uses the `evolve-kit` skill.
- *"Refresh the setup facts."* Uses `refresh-facts`. Do it quarterly.
- *"Review the kit with fresh eyes."* Uses `review-kit`. Do it before a major release.
- *"Release v1.2."* Uses `release`.

## Cadence

| When | What |
|---|---|
| Whenever an idea comes up | Add a row to `docs/master-plan.md` (status `idea` or `todo`) |
| After giving the kit to a friend | Ask how it went after 2 weeks, and file their feedback as an issue |
| Quarterly | `refresh-facts`, then a minor release if anything changed |
| Twice a year | `review-kit` |

## Releases

See [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md). In short: bump `VERSION` + footers + README + CHANGELOG → `scripts/build.sh` → commit → `git tag -a vX.Y` → `git push origin main --follow-tags` → verify the Release has the zip attached (and, once live, that the website shows the new version).
