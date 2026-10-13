---
tags: [reference, system]
type: reference
status: active
created: 2026-10-13
updated: 2026-10-13
summary: How to organise and curate this vault so it stays useful for years — folders, links, properties, tags, hubs, the note lifecycle, rhythms, imports, Obsidian features, plugins and anti-patterns.
---

# Organizing your vault

A second brain is only useful if things can be **found again**: by you, and by your AI. The AI never reads the whole vault. It reads the [[_system/index|index]], then hub notes, then the one-line `summary` of each candidate, and opens only the 3–8 notes that matter. Good structure makes it fast and right. Messy structure makes it slow, expensive and confidently wrong.

The rules the AI follows are in [[VAULT-CONTRACT|the Vault Writing Contract]]. This note explains the *why*, for you.

## 1. Five ways to organise, each with one job

| Tool | Answers | Use it for | Don't |
|---|---|---|---|
| **Folder** | *Where does it live?* | One home per note, by area of life (`01-life/home/`, `02-work/…`). Shallow: two or three levels. | Nest deeper than three levels, or make a folder for two notes |
| **Link** `[[…]]` | *What is it related to?* | Connections across areas: a person, a project, a decision, a source. A note can link to many | Link everything to everything. Link when you'd actually follow it |
| **Property** (frontmatter) | *What is it, and what state is it in?* | `type`, `status`, `summary`, dates, `relationship`, `birthday`, `renewal`. Dashboards and tools read these | Invent a new property for every note. Reuse names |
| **Tag** `#…` / `tags:` | *What theme cuts across areas?* | A few cross-cutting themes (`#recipe`, `#tax`, `#gift-idea`) | Repeat the folder as a tag, or grow hundreds of one-off tags |
| **Hub** (`_index.md`) | *What's in here, and where do things go?* | One per area or big folder: a short map plus a list of notes. The AI's signposts | Write essays in hubs. Keep them short and current |

**Rule of thumb:** folders for *where*, links for *related*, properties for *what and when*, tags sparingly for *themes*, hubs for *maps*.

## 2. Note shapes

- **Topic note** (most notes): one subject, a descriptive title you'd search for ("Dishwasher – model, manual, filter"), a one-line `summary`, a link to its hub or project. Update it over the years instead of making a new one.
- **Hub note** (`_index.md`): a map of a folder. The `hub_index.py` tool can keep its note list current automatically (see [[_system/tools/README|Vault tools]]).
- **Project note**: something with an end. Why, done-when, next step, decisions, log. Template: *Project Note*.
- **Series** (briefings, weekly reviews, meeting notes): dated names `YYYY-MM-DD`, `YYYY-WXX`. They don't need links between them.
- **Log** inside a note: dated bullets, newest first ("2026-10-13 — serviced the boiler, next due 2027-10").
- **Person**: one per person, first name as the title (skill `people`). Hard constraints (allergies, accessibility) at the top.

**Titles:** say what it is. "Insurance" is vague; "Home insurance – policy, excess, how to claim" is findable. Avoid "Notes", "Misc", "Untitled", "New".

## 3. Write for future you (and your AI)

- **A `summary` on every note.** One sentence that lets someone decide whether to open it. It's the most valuable line in the note.
- **Decisions with their why.** "Chose the green sofa (fits the stairs; the grey one didn't)". Without the why, the decision gets re-made.
- **Absolute dates.** "Next Tuesday" means nothing in six months. Write `2026-10-20`.
- **Sources next to claims**, for anything about health, money or law. Mark what you couldn't confirm.
- **Short beats complete.** A note you'll actually re-read beats a long note you won't.
- **No secrets, ever.** Passwords, card numbers and ID numbers live in a password manager. `secret_scan.py` checks.

## 4. The lifecycle of a note

```
capture → _inbox/ → (weekly review) → its home folder, status: active
        → done / someday → 99-archive/ when it's no longer useful
```

- **Capture fast, sort later.** Anything goes into `_inbox/`, from your phone, a quick note or the AI. Don't organise while capturing.
- **Process weekly** (skill `weekly-review`): each inbox item is filed, turned into a task, merged into an existing note, or deleted.
- **Status, not deletion:** `active` → `done` / `someday` → `archive`. Archived notes move to `99-archive/` with Obsidian, so links keep working.
- **Delete only junk** (duplicates after merging, empty notes, outdated copies), and ask yourself whether you'd miss it.

## 5. Rhythms

| When | What | How |
|---|---|---|
| Daily | Capture; read the briefing | Phone → `_inbox/` · "Morning briefing" |
| Weekly | Empty the inbox; review projects; pick priorities | "Weekly review" (20–30 min) |
| Monthly | Health check: links, frontmatter, duplicates, index, secrets | "Vault health check" (skill `vault-maintenance`) |
| Quarterly | Profile, tools and connections review; prune what's unused | Harness P7.3, P7.5 |

## 6. Search before you create

Most vault rot is **near-duplicates**: "Kitchen renovation", "kitchen reno ideas" and "Kitchen 2026". Before creating a note, search for it, and you and the AI both **update** the existing one. When you find duplicates, merge them into the better note and archive the other (`vault_lint.py` lists notes with the same name).

## 7. Bringing in notes from elsewhere

1. Export from the old app (most offer Markdown) and import with Obsidian's official **Importer** plugin into a holding folder, e.g. `_inbox/imported/`.
2. Ask the AI: *"Vault health check on `_inbox/imported/`."* Then add frontmatter with `fix_frontmatter.py`, write summaries, find duplicates and broken links.
3. Move notes to their homes in batches (by topic), merging duplicates as you go. Big imports can be parked: add the folder to `ignore` in `config/vault-lint.md` until you get to it.

## 8. Obsidian features worth knowing

- **Quick switcher** (Ctrl/Cmd+O) and **command palette** (Ctrl/Cmd+P): faster than clicking.
- **Search operators:** `path:01-life`, `tag:#recipe`, `[status:active]`, `task-todo:`, `"exact phrase"`.
- **Properties:** edit frontmatter as a form. The *All properties* view shows every property in use: good for spotting typos (`Status` vs `status`).
- **Backlinks and outgoing links** (right sidebar): what points here, and where this points.
- **Bases** (core): live tables and cards from your properties. See [[_system/dashboards/Dashboards|Dashboards]].
- **File recovery** (core): automatic snapshots, so you can undo an AI's edit even without git.
- **Bookmarks:** pin the notes you open daily.
- **Command line** (Obsidian 1.12.7+, Settings → General → *Command line interface*, with the app running): lets the AI move notes **with links updated**, and search, list orphans or query a base. Examples: `obsidian move file=Note to=99-archive/`, `obsidian search query="boiler"`, `obsidian orphans`, `obsidian unresolved`, `obsidian base:query file=Projects format=md`. Optional; the kit works without it.

## 9. Plugins

Start with **core plugins only**. Community plugins can be great, but each one runs code with full access to your vault, so install few, popular and well-maintained ones, and only for a need you actually have. Obsidian's *Restricted mode* keeps them all off until you choose.

Worth knowing about (all optional):

| Plugin | Good for | Note |
|---|---|---|
| **Importer** (official) | Bringing notes in from other apps | Use once, then turn it off |
| **Tasks** | Due dates (`📅 2026-10-20`), recurring tasks, task queries | `upcoming.py` understands its dates |
| **Templater** | Smarter templates (dates, prompts, folders) | The core *Templates* plugin is enough to start |
| **Calendar** / **Periodic Notes** | Daily and weekly notes from a calendar view | Only if you write daily notes |
| **Git** | Automatic version history and backup, for git users | Pairs with the `secret_scan.py` commit guard |
| **Dataview** | Older, powerful query language | **Bases** (core) now covers most needs |
| **Excalidraw** | Sketches and diagrams inside the vault | |

## 10. Signs of rot, and the fix

| You notice | Likely cause | Fix |
|---|---|---|
| The AI "can't find" things you know you wrote | Missing summaries, stale index, vague titles | `vault-maintenance`; better titles and summaries |
| Two answers that disagree | Duplicate notes | Merge, archive the other |
| `_inbox/` keeps growing | The weekly review keeps slipping | A shorter review; capture less |
| Endless folders with one note each | Organising before there's anything to organise | Flatten. Folders appear when the third note arrives |
| Hundreds of tags | Tagging instead of filing or linking | Keep 10–20 tags; the rest become links or properties |
| You never re-read anything | Collecting, not using | Save less; save decisions and answers, not everything |
| Notes full of "next week" | Relative dates | Absolute dates (`YYYY-MM-DD`) |
