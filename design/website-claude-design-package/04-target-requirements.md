# 04 · Target requirements: ai-kickstart.me

## §1 Persona & job

**Primary: "the friend who got the link".** Mid-30s to 60s, any profession, sent here by someone they trust. Uses AI occasionally or not at all. Tech comfort anywhere from 1 ("I'd rather not touch settings") to 4. Could be on a Mac, a Windows laptop (possibly a locked-down work machine) or a phone. Mildly curious, mildly sceptical, short on time.
*Job:* "Help me understand whether this is for me, and if it is, get me started without feeling stupid."

**Secondary: "the one setting up".** The same person on Day 1 and in Week 1, mid-task: Obsidian open in one window, an AI app in another, this site on a second screen or a phone. *Job:* "Where am I, and what do I paste next?"

**Tertiary: "the sharer".** Someone who already uses the kit and wants to pass it on. *Job:* "Give me something I can send that explains itself."

**Also: "the returner".** Set up weeks ago, coming back. *Job:* "What's new, and how do I get it without breaking my notes?"

## §2 Scope

In scope: the public website at ai-kickstart.me, covering everything in `01`, with the content in `03`.
Out of scope: the downloadable companion app (separate brief), the vault's own notes, any account or backend.

**North star:** *A sceptical non-technical visitor understands what this is within 10 seconds, and one minute later is holding exactly one clear next step that fits their computer and comfort level.*

## §3 Open design decisions: ARGUE YOUR CHOICE

Use the success criteria in `05` to justify each pick.

**§3.1 Information architecture.** The current guide is 8 sibling pages behind a top nav (see `assets/`). Alternatives include a single long narrative, a short landing plus a deep guide, a "choose your path" entry that personalises everything after it, or something else. **Challenge the 8-page split.** Pick a structure and argue it for all four personas in §1, not just the first.

**§3.2 The first ten seconds.** What does the visitor see and understand before scrolling? The kit's idea is abstract (a place for your AI to live). Argue how to make it concrete: show, tell, a before/after, a day-in-the-life, an artefact… and why your choice beats a generic hero.

**§3.3 Choosing the way in.** The visitor must pick among download zip / read online / (later) app, three AI paths, and four OS families. Argue how many of these decisions the site asks, in what order, and what it can infer (OS detection is possible) versus ask. Show the flow for a comfort-2 Windows user and a comfort-4 Mac user, and show how differently the site treats them.

**§3.4 Setup as a companion.** During setup the site is a second screen. Argue how a visitor keeps their place across window switches and devices (phone ↔ laptop) **without accounts or tracking**: local storage only, shareable URLs, or something else. Show the "mid-setup, came back after making tea" moment.

**§3.5 Prompts as first-class objects.** Prompts are the site's real payload. Argue how they look, how placeholders are marked and filled, and how copying works on desktop and phone. Should a prompt ever be personalised from earlier choices (OS, path)? Show two contrasting prompt contexts.

**§3.6 The catalog.** 103 functions, 16 areas, 3 levels, tick-and-copy. Argue the browsing model (grid, list, guided "pick five", filters by life area or by effort, other) so that it feels like a menu rather than a form. Show the empty state, the "12 picked" state and the copy moment.

**§3.7 Visual identity, and evolve vs replace.** Propose the identity: type, colour, mark, illustration or none, motion. Then argue whether it should **evolve** the current guide's look (warm editorial serif, violet accent, cards) or **replace** it, and why. It must hold in light and dark mode, and could later extend to a small desktop app.

**§3.8 Making progress-over-time feel encouraging.** The harness plan spans weeks or months at the visitor's own pace. Argue how the site communicates "small steps, no pressure", and avoids both gamification guilt and the overwhelm of an 8-phase plan.

**§3.9 Trust without legalese.** Free, open source, local-first, no tracking, made by a named person. Argue where trust is earned on the page and in what form. Consider a non-technical reader's mental model of "open source" and "download".

## §4 Hard constraints

- **Static site.** Hosted on GitHub Pages with a custom domain. No backend, no server-side rendering, no accounts.
- **Plain HTML/CSS/vanilla JS, no build step.** Maintainers edit files directly, and the same front-end approach will be reused in a desktop app built on a system webview.
- **No third-party requests at all:** fonts self-hosted or system fonts, no CDNs, analytics, embeds or social widgets.
- **Offline-capable guide.** The guide portion also ships inside the downloadable zip and must work when opened directly from disk (`file://`), so it needs relative links and no server routing. A landing section may be web-only.
- **Responsive** from 360 px phones to wide desktop. Light and dark mode both first-class (follow the OS).
- **Local persistence only** (`localStorage`) for anything remembered: catalog picks, setup progress, chosen OS/path.
- Content per `03`. Placeholders in prompts use `<angle brackets>`.

## §5 Anti-patterns

- Generic AI-startup look: gradient blobs, glowing orbs, robot/brain imagery, sparkle-everything, "AI-powered" badges.
- Hype or fear copy: "10× your life", "don't get left behind".
- Stock photos of smiling people at laptops.
- Leading with jargon (agents, MCP, LLM, vault, harness) before it's explained.
- Sign-up walls, newsletter pop-ups, cookie banners (there are no cookies, so don't simulate one), dark patterns, fake urgency.
- Walls of text with no clear next action. Equally, a slick page that never actually explains the idea.
- Hiding the Windows / non-technical path behind the Mac / technical one.

## §6 Deliverables

1. The full site prototype covering every "must be able to" in `01`, with real content from `03` and `reference-specs/`.
2. Working interactions: OS/path choice, prompt copy (with placeholder treatment), catalog tick/filter/copy-picks, light/dark.
3. A **Tweaks** switcher with the scenarios in `05`.
4. A one-page rationale: your §3.1–§3.9 arguments in short form.
5. A note on what transfers to a companion desktop app (tokens, primitives, voice) and what stays web-only.
