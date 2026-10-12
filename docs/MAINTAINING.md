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

1. **Website (`site/`):** a Cloudflare **Worker with static assets**, configured by `site/wrangler.jsonc` (no Worker code, just `dist/`). Connect the repo in Cloudflare → Workers & Pages → Create → Import a repository: root directory `site`, build command `pnpm build`, deploy command `npx wrangler deploy`. Add the custom domain ai-kickstart.me under the Worker's Settings → Domains. Branch previews come with it. Don't enable Web Analytics or any beacon: the site promises no tracking. Manual deploy instead: `pnpm build && cd site && npx wrangler@4 deploy` (asks you to log in to Cloudflare once).
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
| Preview the guide | open `guide/index.html` in a browser |
| Install website tools (once) | `pnpm install` (Node 22.12+, pnpm 10) |
| Website dev server | `pnpm dev` → http://localhost:4321 |
| Website checks | `pnpm test && pnpm check && pnpm build && scripts/check_site.py` |

## Working with an AI agent on the repo

Open your agent in the repo root and say one of:

- *"Continue the maintenance plan."* Does the next step in [`docs/HARNESS-PLAN.md`](HARNESS-PLAN.md).
- *"Add a tip: …"* / *"Add a catalog function: …"* / *"Add a skill to the kit: …"* Uses the `evolve-kit` skill.
- *"Refresh the setup facts."* Uses `refresh-facts`. Do it quarterly.
- *"Review the kit with fresh eyes."* Uses `review-kit`. Do it before a major release.
- *"Release v1.2."* Uses `release`.

## Cadence

| When | What |
|---|---|
| Whenever an idea comes up | Add it to the backlog in `docs/HARNESS-PLAN.md` |
| After giving the kit to a friend | Ask how it went after 2 weeks, and file their feedback as an issue |
| Quarterly | `refresh-facts`, then a minor release if anything changed |
| Twice a year | `review-kit` |

## Releases

See [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md). In short: bump `VERSION` + footers + README + CHANGELOG → `scripts/build.sh` → commit → `git tag -a vX.Y` → `git push origin main --follow-tags` → verify the Release has the zip attached (and, once live, that the website shows the new version).
