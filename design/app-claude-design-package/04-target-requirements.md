# 04 · Target requirements: companion app

## §1 Persona & job

**Primary: Sam** (seed data in `03`), and people like Sam: non-technical to moderately technical. They downloaded this because a friend recommended the kit, or from ai-kickstart.me.
*Jobs:* "Get me set up without getting lost." Then: "When I have 20 minutes, tell me what to do next." Later: "Keep my kit up to date without breaking my stuff."

**Secondary: the returning-after-a-gap user.** Three weeks without opening anything. *Job:* "Remind me where I was, without making me feel bad."

## §2 Scope

In scope: a desktop app window (plus any secondary surface you can argue for, see §3.1) covering everything in `01`, rendering the seed data in `03`.
Out of scope: chatting with AI, editing notes, the website, accounts, sync, mobile.

**North star:** *On any day, within 5 seconds of opening the app, Sam knows the one thing to do next and has the prompt for it ready to paste.*

## §3 Open design decisions: ARGUE YOUR CHOICE

Justify each pick against `05`.

**§3.1 What shape is this app?** Candidates include a regular window with a home view, a compact companion that docks beside the AI app, a menu-bar/tray presence plus a window, a wizard that later becomes a dashboard, and others. **Challenge the "dashboard" default.** The app is opened briefly and often, mostly to grab one prompt. Pick a shape and argue it.

**§3.2 First run, from download to "It works!".** Design the whole flow for Sam: create vault → Obsidian → choose AI path → paste first-contact prompt → the app detects `hello.md`. Argue the number of steps, what happens if Obsidian isn't installed, and how the app shows it is *waiting* for something happening in another app. Show the success moment.

**§3.3 The "one next thing".** The home state must surface a single next step and its prompt. Argue how it adapts across contexts: mid-interview, mid-step `[/]`, a phase just completed, a check-in due, nothing urgent. Show at least three contrasting home states, and don't just swap the text: reshape the screen if the state warrants it.

**§3.4 Progress over months without guilt.** P0–P7, the backlog and session history. Argue how progress is represented (or deliberately not), how a three-week gap is greeted, and how skipped `[-]` steps read as a valid choice rather than failure. Gamification is not banned outright, but you must argue for any part of it you use.

**§3.5 Noticing change in the vault.** The AI edits Markdown in another app; this app watches the files. Argue how the app acknowledges changes it noticed (a step ticked, a round finished, new backlog items) at the right volume: neither silent nor noisy.

**§3.6 Updates a beginner can trust.** Present what's new, the file preview and the three file kinds from `03` (untouched / edited-by-you conflict / your-file-gets-an-addition → AI merge prompt). Argue the level of detail by default versus on demand. Show the conflict decision for `weekly-review/SKILL.md` and the hand-off prompt for `HARNESS-PLAN.md`.

**§3.7 Honesty surfaces.** "Local only", the optional update check, what's stored in `~/.ai-kickstart/`. Argue where and how often these appear so they build trust without nagging.

**§3.8 Errors and edge states.** Vault moved or missing, unparseable plan, Obsidian missing, no write permission, update failed. Argue a consistent recovery pattern; don't design five unrelated error screens.

## §4 Hard constraints

- **Runtime:** [tinyjs](https://tinyjs.app/). A native system webview (WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux) with a JavaScript backend that has file-system access. The front end is **plain HTML/CSS/vanilla JS** (no framework, no build step), and it shares portable CSS (tokens as custom properties) with the website.
- **Platforms:** **macOS 15+ and Windows 10/11 are both v1 targets.** Linux comes later. Rendering differs slightly between WebKit and WebView2, so avoid effects that depend on one engine.
- **Window:** resizable. It must work fully at **800×560**, and must not need more than 1280×800 to shine.
- **Local-only:** no telemetry, accounts or AI calls. The only network use is the optional update check against the public releases list, and it must be visible and switchable.
- **File writes** are limited to: creating a new vault from the bundled template · replacing kit files during a confirmed update · `~/.ai-kickstart/`. **Everything else in the vault is read-only for the app.** Progress changes happen in the vault, made by the AI or by the person in Obsidian.
- Light/dark follow the OS. AA contrast. Keyboard-complete.
- Data per `03`; don't invent fields.

## §5 Anti-patterns

- A metrics dashboard: streaks, percentages everywhere, charts of "productivity".
- Nagging: badges, red dots and "you haven't opened me in 3 weeks!" guilt.
- Pretending to be the AI: chat bubbles, an assistant persona, an AI avatar.
- Hiding what an update will do to files, or forcing it.
- Developer-tool aesthetics: terminal fonts as decoration, raw paths without plain-language labels, diff views as the *default* update UI.
- Generic AI-startup visuals (glows, gradients, sparkles, robots).

## §6 Deliverables

1. Prototype of every job in `01` with the seed data from `03`, including the first-run flow end to end and at least three home states.
2. The update flow, including the conflict and the AI-merge hand-off.
3. A **Tweaks** switcher with the scenarios in `05`.
4. A one-page rationale for §3.1–§3.8.
5. A short list of the primitives you'd share with the website (and any you'd keep app-only).
