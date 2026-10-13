---
name: kit-update
description: Bring a new AI Kickstart release into this vault without losing anything the owner wrote — new skills, tips, plan steps and fixes in, their notes, profile, plan progress and edits untouched. Use when the owner says "update my kit", "a new version is out", "update to v1.x", "install the new release", or downloaded a new kit zip.
---

# Kit update

A new release brings new and improved kit files: skills, interview rounds, catalogs, contracts, templates, tools, tips. The owner's own files (profile, plan, notes, answers, indexes) must come through untouched, and so must any kit file they changed. **Target: 20–30 minutes.** Nothing is overwritten that the owner edited, and nothing is deleted.

## Who owns what

- **Kit files** come from the kit and are replaced on update, *but only if the owner never changed them*: skills, interview and round files, catalogs, contracts, templates, dashboards, tools, the reference notes the kit ships, and `_system/kickstart/kit-version.md`.
- **The owner's files** are never replaced. The release may still have something new for them, which you bring in by hand: `AGENTS.md`, `_system/HARNESS-PLAN.md`, `_system/index.md`, the profile files, `_system/kickstart/answers/`, `_system/tools/README.md`, and every `_index.md` hub.
- **Everything else** (their notes) isn't in the kit at all, so an update never touches it.

## 1. Before anything

1. **Backup first. No backup, no update.** Ask the owner to copy the whole vault folder somewhere (or confirm their sync or backup has a version from today). Wait for a yes.
2. **Get the new kit.** The latest zip is on the [Releases page](https://github.com/liqweed/ai-kickstart/releases/latest). Download it and leave it zipped, or unpack it **somewhere else**. Never unzip it on top of the vault.
3. **Get the kit as they first got it.** That's what tells their edits apart from the kit's changes. The version is in `_system/kickstart/kit-version.md`. Vaults from before v1.4 don't have that note: look for the zip they first downloaded (`ai-kickstart-v1.2.zip` in Downloads, say), or ask. Every release is on the same page. If you can't find out, carry on without it: every kit file that differs then counts as a conflict, which is slower but safe.

## 2. Plan the update (nothing is written yet)

**With tools** (you can run commands and Python works; see `_system/tools/README.md`):

```bash
python3 _system/tools/kit_update.py --kit <new zip or folder> --old <old zip or folder>
```

**Without tools**, do the same by hand, folder by folder, and say it's slower: for each file in the new kit's `vault/`, compare it with the vault's copy and the old kit's copy, and sort it into one of the groups below.

Show the owner the plan in one screen, in plain words: *"11 kit files you never changed get the new version. 31 new files arrive: new skills, tools, dashboards and templates. 1 skill you edited also changed in the kit: let's look at it together. Your plan, your index and AGENTS.md need a few new lines, which I'll show you. Your profile, notes and answers aren't touched."*

## 3. Apply the safe part

After a yes: `python3 _system/tools/kit_update.py --kit … --old … --apply`. It adds the new files and replaces untouched kit files. Nothing else. (By hand: copy exactly those files from the new kit, at the same paths.)

## 4. Conflicts: kit files they edited

For each one, show what the release changed (`--diff`) next to what they changed, then offer three choices:

- **Keep mine.** Nothing happens. They keep their version and miss the kit's change.
- **Take the new one.** Replace it, and put their old version in `99-archive/` so nothing is lost.
- **Merge.** You write one version with both changes. Show it, and save it only after a yes.

## 5. Merges: their own files the release changed

Never overwrite these. Run `--diff` to see what's new, and bring in only that:

| File | What to bring in |
|---|---|
| `_system/HARNESS-PLAN.md` | **New steps only** (e.g. `P3.6`), each in its phase, unticked, word for word: after the step that comes before it in the kit's plan, or before the next one if it's the first (`P4.0`). Never renumber, re-tick or reword their steps, and keep their logs. Then tell them which new steps fit them; they can mark the rest `[-]`. |
| `AGENTS.md` | New rows in the *Skills* table. A changed rule only if they agree. Keep anything they added. |
| `_system/index.md` | New folders, notes and skills in the right sections. Keep their own entries. |
| `_system/tools/README.md` | New registry rows. Keep rows for tools they built. |
| `_index.md` hubs | New `auto-index` markers if the kit added them. Then `python3 _system/tools/hub_index.py --apply` refreshes every list. |
| Profile files | Usually nothing. If a template gained a section, offer to add the empty heading. |

## 6. Check and close

1. Run the plan again (no `--apply`): it should show no `update` or `add` left. Conflicts and merges stay on the list even after you've handled them, because the tool can't tell; that's expected.
2. With tools: `python3 _system/tools/selftest.py` (should say OK), then `python3 _system/tools/vault_lint.py` (fix only what the update caused).
3. Tell them what's new in three lines, for example: *"You now have dashboards, a monthly health check and a way to connect apps. New plan steps: P3.6 and P3.7. Want to try one?"*
4. Add an entry to the plan's *Session log*: `Kit update v1.3 → v1.4: 42 files added or updated, 1 merged, plan +7 steps.`

## Chat-only (no file access)

You can't compare files, so keep it simple and safe. Ask the owner to paste the release notes from the website's *What's new* page. Then, together:

1. **New files** (new skills, templates, notes): they copy them from the new kit into the same folders.
2. **Changed kit files**: if they never edited one, they replace it with the new version. If they did, show both versions and merge them as in step 4.
3. **Their plan**: they paste the new `HARNESS-PLAN.md`, and you give them only the new steps to paste into theirs.
