# Claude Design, round 2: website polish + companion app (same project)

**Where:** the **same** Claude Design project as the website prototype (round 1; the round-2 result is in [`prototype/`](prototype/)). Keeping one project means the app inherits the approved tokens and primitives directly, instead of rebuilding them from screenshots.

**Upload first:**
1. The whole [`app-claude-design-package/`](app-claude-design-package/) folder.
2. The logo, if it's ready: `logo-mark.svg` (see [`logo-quiver-prompt.md`](logo-quiver-prompt.md)). Without it, the prompt below says to keep the current mark.

**Then paste everything below the line.**

---

Round 1 is approved. Thank you, it's very close to what I hoped for. Please **keep everything** that isn't mentioned below: the five-place IA, the "two mornings" band, the setup companion, the prompt card, the menu-style catalog, the tokens, the type and the voice.

This round has two parts. Do Part A first, because Part B builds on it.

## Part A · Website: five small fixes

Each one is a problem to solve. The solution is yours, so argue it in one or two lines in the rationale page.

1. **The catalog tray hides the menu.** In scenario 5, with the message preview open, the sticky tray fills about half of an 800 px-tall window and the ideas scroll underneath it. People need to keep browsing while their picks stay visible, and the full message should still be previewable before copying.
2. **The chooser gives two answers.** "With a desktop AI app" is marked *Recommended*, and the hint below says "Not sure? Pick the chat app." A nervous beginner needs one consistent recommendation, plus an honest note on when the other paths fit.
3. **A finished setup still gets the pitch.** In scenario 6 (setup done, v1.2 out) the Start page leads with "Find your first step". Someone who finished setup now needs the everyday sentence ("Continue my harness plan."), what's new, and the way into the ideas menu and prompts. Show how Start adapts to *setup finished* without hiding the page's explanation from a first-time visitor.
4. **The brand mark.** If `logo-mark.svg` is uploaded, adopt it as the mark in the header, a favicon (16/32 px) and the app icon in Part B, in light and dark. Check that it reads at 16 px. If it isn't uploaded, keep the current mark.
5. **Sharing preview and phone header.** (a) Design the link preview people see when the site is pasted into WhatsApp or iMessage: the image (1200×630) and the title and description text. It must explain itself to a parent. (b) On a 390 px phone the nav wraps onto two rows, which costs about 160 px before any content. Solve it without hiding any of the five places from keyboard or screen-reader users.

Then **extract the tokens and shared primitives into one stylesheet** (for example `kickstart.css`) that both the site and the app load. The app must not re-declare colours, type or the primitives.

## Part B · The companion app

Build the app as **new pages in this project** (for example `AI Kickstart App.dc.html` and `App Rationale.dc.html`), following the uploaded `app-claude-design-package/` (`00`–`05`, `reference-specs/`).

**Binding clarification:** where the app brief says *"if `assets/website/` exists"*, read it as **"the approved website in this project"**. So the identity (type, colour, mark, tokens) and the website's primitives (prompt card with fillable placeholders, step card with status marks and Done when / Check, choice pills, the menu row) are **binding**. Reuse them through the shared stylesheet, and extend them only where the app has a job the site doesn't have. List each extension in the app rationale.

Everything else in the app brief stays open and must be argued, especially:
- **§3.1, the shape of the app.** Challenge the dashboard default.
- **§3.3, at least three home states** that reshape the screen, not just swap the text.
- **§3.6, the update flow**, including the `weekly-review/SKILL.md` conflict and the `HARNESS-PLAN.md` hand-off prompt.

Differences from the site that you must respect (from the app's `00` and `04`):
- The app is the **functional** side. Explanations live on the website, so link to the right page there instead of repeating them. The site's persuasion pieces (the before/after band, the trust questions, the OS/path chooser) don't belong in the app.
- Window: fully usable at **800×560**, and doesn't need more than 1280×800. Render the prototype inside a window frame, with the macOS/Windows appearance as a Tweak.
- The write rules and local-only rules in `04 §4` are a gate.

Deliverables for Part B: the app's `04 §6` list, including its own **Tweaks** switcher with all the scenarios in its `05`, and an **App Rationale** page.

## Finally

Update the website's Rationale page with the Part A decisions, and add a short **"Shared system"** section that lists the tokens and primitives the site and app now share, and the few that each keeps to itself.
