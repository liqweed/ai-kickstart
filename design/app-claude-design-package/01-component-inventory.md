# 01 · Component inventory: companion app

Framed as **jobs and problems**. How many screens, how they're grouped and how they're navigated is open (`04 §3.1`).

## Must be able to…

### Start from nothing (first run)
- Explain in a sentence or two what the app does, and promise that it is local-only.
- **Create a new vault** from the bundled kit template in a location the person chooses, **or connect an existing one** (someone who already unzipped the kit, or a returning user on a new install).
- **Check prerequisites:** is Obsidian installed? Which AI path will they use (chat app / desktop agent / terminal agent)? Then open the new vault in Obsidian (Obsidian supports `obsidian://open?path=…` links).
- **First contact:** give them the first-contact prompt to paste into their AI, then **notice when it worked**. The prompt asks the AI to create `_inbox/hello.md`, and the app can watch the folder for that file.
- **Problem:** this is the scariest hour for a beginner. Three apps are involved (this one, Obsidian, an AI app), and each "it worked" moment must be unmistakable.

### Keep their place (the everyday job)
- Show **where they are**: current phase and next step from the harness plan, interview rounds done or pending, the last session's handoff note.
- Give them **the prompt to paste next**, usually "Continue my harness plan", or the right interview round.
- Notice when progress happens. The AI edits the vault's Markdown files, and the app watches those files and reflects changes.
- Let them **jump into Obsidian** at the relevant note.
- **Problem:** progress spans weeks or months, at the person's own pace, with long gaps. It must feel encouraging after a three-week break, never guilt-inducing.

### Show the plan and the backlog
- Phases P0–P7 with step statuses (`[ ]` `[/]` `[x]` `[-]` `[?]`), plus the personal backlog (ideas with value, effort and phase, ★ = first).
- **Problem:** depth on demand. Most days, people need one next step, not eight phases.

### Point to the website for everything explanatory
- Explanations, the full guide, the catalog, the prompt library and tips all live on **ai-kickstart.me**. The app links to the right place in context ("what's a harness plan?" → the website), rather than duplicating it.
- **Exception:** the operational prompts the app hands over (first contact, "Continue my harness plan", interview rounds, update-merge prompts) are built in, so they work offline.
- **Problem:** the app should feel complete for doing things, while never becoming a second documentation site.

### Update the kit safely
- When a new kit version exists (optional check against the public releases), show **what's new in plain words**, preview exactly which files change, and apply the update **without touching the person's own notes**.
- Three kinds of file are involved (facts in `03`): kit files the person never touched (safe to update) · kit files they edited (a conflict, so they choose) · their own files where the new version *adds* something, such as a new plan step (the app can't merge these itself; it can hand the AI a ready-made prompt to merge them).
- **Problem:** a non-technical person must be able to trust an update the way they trust a phone OS update, while still seeing what happens to their files.

### Settings & honesty
- Vault location(s) · update check on/off · theme follows the OS · "what this app stores and where" (`~/.ai-kickstart/`) · remove app data · About (version, credit, licence, source link).

### Recover gracefully
- The vault folder was moved, renamed or deleted · the plan file was edited into an unparseable shape · Obsidian is not installed · no permission to write to the chosen folder · the update download failed.

## Already-canonical primitives (binding: reuse, don't reinvent)

- **If the approved website is in the same project or in `assets/website/`:** the website's approved primitives (prompt block, step/status marks, catalog item) are binding. Reuse them.
- Otherwise: none.
