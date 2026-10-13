---
tags: [system, tools]
type: reference
status: active
created: 2026-10-13
updated: 2026-10-13
summary: The registry of vault tools — small, tested scripts for jobs with one right answer — and how to run them.
---

# Vault tools

Small programs for jobs that must be right every time: finding broken links, listing what's due, checking for passwords. The AI runs them for you; you never have to. They follow [[TOOLS-CONTRACT|the Tools & Connections Contract]].

> **Script lists, search questions.** If a list must be filtered correctly every time, a tool does it. If it's an open question, the AI thinks and searches.

## Do I need these?

No. Every skill works without them, more slowly and less exactly, by having the AI read the notes itself. They need:

- an AI that can **run commands** in this folder (a desktop or terminal agent, not a chat app), and
- **Python 3.9 or newer.** Check with `python3 --version` (Windows: `py --version`). Macs usually offer to install it the first time you type `python3`. Otherwise get it from python.org. Ask your AI to help; it should ask before installing anything.

First time: say *"Run the tools self-test"*. The AI runs `python3 _system/tools/selftest.py` and should report **OK** (harness step P0.6).

## Registry

Every tool in the vault is listed here, including scripts that live in a skill's own `scripts/` folder. **Read-only** tools never change a note. **Writers** show what they would change and touch nothing unless you add `--apply`.

| Tool | What it does | Kind | Used by |
|---|---|---|---|
| `vault_lint.py` | Health check: broken links, missing frontmatter, orphans, duplicate names, a stale index, an old inbox, secrets | Read-only | `vault-maintenance` |
| `secret_scan.py` | Finds passwords, API keys, card and bank account numbers (masked in the output) | Read-only | `vault-maintenance`, `tool-builder`, git hook |
| `upcoming.py` | Due tasks, birthdays, anniversaries, renewals and deadlines in the next N days | Read-only | `daily-briefing`, `weekly-review`, `people` |
| `recent.py` | Notes created or updated, and tasks completed, in the last N days | Read-only | `weekly-review`, `vault-maintenance` |
| `fix_frontmatter.py` | Adds missing frontmatter fields, guessed from the folder; never changes existing values | Writer | `vault-maintenance` |
| `hub_index.py` | Rewrites the automatic note list between the markers in `_index.md` hubs | Writer | `vault-maintenance` |
| `kit_update.py` | Brings in a new kit release: adds new files and replaces kit files you never changed; lists the rest for your AI | Writer | `kit-update` |
| `selftest.py` | Runs every tool test and the contract checks | Read-only | harness P0.6, `tool-builder` |

Shared code lives in `vaultlib.py` (not a tool). New tools start from `_template.py`. Tests live in `tests/`.

## How to run them

From the vault folder (Windows: use `py` instead of `python3`):

```bash
python3 _system/tools/vault_lint.py                 # health report
python3 _system/tools/vault_lint.py --only broken-link,orphan
python3 _system/tools/upcoming.py --days 7          # the week ahead
python3 _system/tools/recent.py --days 7            # the week behind
python3 _system/tools/secret_scan.py                # whole vault
python3 _system/tools/fix_frontmatter.py --path 04-learning        # dry run
python3 _system/tools/fix_frontmatter.py --path 04-learning --apply
python3 _system/tools/hub_index.py                  # dry run: shows the diff
python3 _system/tools/selftest.py                   # do the tools work here?
```

Every tool has `--help`, prints Markdown by default, and prints JSON with `--json` (for skills and scripts). `--today YYYY-MM-DD` replays a past date. Exit codes: `0` fine, `1` something to report, `2` a usage mistake.

## Settings

Optional. Each lives in a normal note in `config/`, written by the AI when you ask for a change:

| Note | Keys |
|---|---|
| `config/vault-lint.md` | `inbox_days`, `stale_days`, `ignore` (path prefixes), `types`, `statuses` (extra allowed values) |
| `config/secret-scan.md` | `extra_patterns` (e.g. your country's ID-number format), `allow` (known false alarms) |
| `config/upcoming.md` | `yearly_fields`, `date_fields` (your own frontmatter date fields) |

## Optional: a privacy guard for git users

If your vault is a git repository, this stops a commit that contains a secret. Ask your AI to set it up, or save as `.git/hooks/pre-commit` and make it executable:

```bash
#!/bin/sh
git diff --cached --name-only --diff-filter=ACM -z | xargs -0 python3 _system/tools/secret_scan.py
```

## Adding a tool

Say *"Make this a tool"* (skill: `tool-builder`). It follows [[TOOLS-CONTRACT]] and finishes only when `selftest.py` passes and the tool is in the registry above.
