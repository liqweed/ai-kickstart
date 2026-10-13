---
name: vault-maintenance
description: Keep the vault healthy and easy for the AI to navigate — find broken links, missing frontmatter, orphans, duplicates, a stale index, an old inbox and anything that looks like a password, then fix them in small batches with the owner's OK. Use when the owner says "vault health check", "tidy my vault", "clean up my notes", "maintenance", on the monthly slot, or after importing notes from another app.
---

# Vault maintenance

A vault rots quietly: duplicate notes, dead links, an index that no longer matches the folders, an inbox nobody empties. Then the AI starts guessing. This skill is the monthly tidy-up. **Target: 15–20 minutes**, interactive. Nothing is deleted or moved without a yes.

## 1. Check (read-only)

**With tools** (the AI can run commands and Python works; see `_system/tools/README.md`):

```bash
python3 _system/tools/selftest.py          # are the tools themselves OK? If not, stop and fix (skill: tool-builder)
python3 _system/tools/vault_lint.py        # the health report
python3 _system/tools/hub_index.py         # hubs whose automatic lists are out of date (dry run)
python3 _system/tools/recent.py --days 31  # what changed this month, for the summary
```

**Without tools** (chat-only, or no Python), do a lighter pass by hand and say it's lighter:
1. List `_inbox/` and note anything older than two weeks.
2. Compare the folders with `_system/index.md`: anything missing or no longer there?
3. Open the 10 most recently changed notes. Check their frontmatter (Vault Writing Contract §3) and that their links point to real notes.
4. Search the vault for `password`, `pin`, `IBAN`, `api key` and look at each hit.

## 2. Report in one screen

```markdown
**Vault health, <Month YYYY>:** <one line: "in good shape" / "a few things to fix">

| Check | Found | Proposal |
|---|---|---|
| 🔴 Secrets | 1 | Move to your password manager, then delete the line |
| 🔴 Broken links | 4 | Fix 3 (typos), create 1 stub note |
| 🟡 Missing frontmatter | 12 | Add with the tool, then I write summaries |
| 🟡 Index drift | 2 folders | Add them to the index |
| 🟡 Inbox older than 14 days | 6 | Sort now, or in Sunday's review? |
| 🟢 Orphans / empty notes / unused attachments | 9 | Link, archive or leave. Your call |
```

Errors first (🔴 secrets, broken links, unreadable frontmatter), then warnings (🟡), then tips (🟢). Skip rows with nothing found.

## 3. Fix in small batches

Ask *"Fix the red ones now?"*, then one batch at a time, showing what changes:

| Finding | Fix |
|---|---|
| **Secret** | Never repeat it in the chat. Tell the owner the file and line. They move it to a password manager; you delete the line after they confirm. If the vault is synced or in git, mention that old versions may still hold it (consider changing that password). |
| **Broken link** | Typo → fix the link. Real but missing note → offer a stub (Vault Writing Contract §4). Obsolete → remove the brackets. |
| **Missing frontmatter** | `fix_frontmatter.py --path <folder>` (dry run), show, then `--apply`. Then write a one-line `summary` for each note: that sentence is what lets future sessions skip opening the note. |
| **Index drift** | Update `_system/index.md` (Vault Writing Contract §5). |
| **Hub lists stale** | `hub_index.py --apply` after showing the diff. To give another hub an automatic list, add the `auto-index` markers (see the tool's `--help`). |
| **Duplicate names** | Open both. Propose a merge into the better one; move the other to `99-archive/` with Obsidian (or `obsidian move`) so links follow. Ask first. |
| **Old inbox** | Sort with the owner (as in `weekly-review` step 2), or park it for Sunday. |
| **Orphans** | Link from the right hub or project, or archive. Many orphans in one folder → that folder needs a hub note. |
| **Stale "active" notes** | Ask: still active? → bump `updated`, or set `status` to `done` / `someday` / `archive`. |
| **Unused attachments** | List them. Delete only with an explicit yes. |

Rules: **never bulk-delete or bulk-move without a yes** (Vault Writing Contract §9). Move notes with Obsidian (or `obsidian move`), never by renaming files on disk, so links survive.

## 4. Close

1. Re-run `vault_lint.py` and show the before → after counts.
2. If something keeps recurring (the same mistake twice), propose **one** structural fix: a hub note, a template, a skill tweak. Prefer that over a new rule in `AGENTS.md`.
3. Add one line to the current month's review (`05-planning/monthly/YYYY-MM.md`, under *Maintenance*), or create it with a summary: `Maintenance: 0 errors, 3 warnings left (orphans in 04-learning/…)`.
4. Tick harness step **P3.6** the first time, and **P7.4** each month.

## Settings

Thresholds and ignore lists live in `config/vault-lint.md` (see `_system/tools/README.md`). For example, a folder of imported notes you'll sort later: `ignore: ["04-learning/imported/"]`.
