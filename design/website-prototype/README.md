# Website prototype (Claude Design, round 1)

The approved design direction for **ai-kickstart.me**, exported from Claude Design on 2026-10-12. It was built from [`../website-claude-design-package/`](../website-claude-design-package/). This is the **reference for K9** (the Astro port in `site/`). It is not shipped in the zip and not deployed.

| File | What |
|---|---|
| `AI Kickstart Site.dc.html` | The whole site as one prototype: Start · Your setup · Ideas menu · Prompts · How it works · What's new, plus the Tweaks scenario switcher |
| `Prompt.dc.html` | The prompt card component (fillable `<placeholders>`, one-click copy) |
| `Rationale.dc.html` | The designer's §3.1–§3.9 arguments and "what transfers to the app" |
| `kit-content.js` | Catalog (16 areas, 103) and prompts (6 groups, 36), standing in for build-time Markdown |
| `support.js` | Claude Design's prototype runtime. It loads React and Babel from unpkg, so **viewing needs a network connection**. The real site must not use it |
| `screenshots/` | Scenarios 1–6 at 1280×800 (scenario 3 at 390×844), light and dark samples |

**To view:** serve the folder (`python3 -m http.server` inside it) and open `AI Kickstart Site.dc.html`. Opening it from `file://` may block the module import of `kit-content.js`.

## Review (2026-10-12)

Verdict: **approved direction.** It meets the brief's gates: system fonts, zero third-party requests in the design itself, tokens as CSS custom properties with full light and dark sets, 44 px targets, visible focus, reduced motion. The IA (5 places instead of 8 pages), the before/after "Morning briefing" band, the setup companion with `[ ] [/] [x]` marks and Done when/Check, the fillable prompt card and the menu-style catalog all land.

Not perfect yet. These go into round 2 (design) or the port (content):

### Design fixes → round 2 prompt ([`../claude-design-round-2-prompt.md`](../claude-design-round-2-prompt.md))

1. **Catalog tray covers the menu.** With the message preview open, the sticky tray fills about half of an 800 px viewport, and the list scrolls underneath it.
2. **Contradictory advice on the chooser.** "Desktop AI app" is marked *Recommended*, and the hint below says "Not sure? Pick the chat app."
3. **Finished-setup visitors still get the pitch.** In scenario 6 (setup done, v1.2 out) the Start page still leads with "Find your first step". A returning user needs "Continue my harness plan." and what's new.
4. **The mark is a placeholder.** A rounded square with a dot doesn't hold up as a favicon or an app icon. A logo is being made separately (see [`../logo-quiver-prompt.md`](../logo-quiver-prompt.md)), and the prototype should adopt it.
5. **No share preview.** "Survives being sent in WhatsApp" needs a social preview image and description (backlog K7).
6. **Phone header** wraps the nav onto two rows (≈160 px of chrome before the content).

### Content fixes → do in the Astro port (content comes from the kit's Markdown anyway)

- **Setup steps are thinner than `guide/setup.html`.** Missing: move and rename the vault folder somewhere permanent (and the OneDrive/iCloud notes); the three Obsidian settings; path A uploads more than two files and needs the *chat-only project instructions*; path B's "project instructions" field; path C's optional skills link; the hand-over "Continue my harness plan." after hello; backup & sync (P0.4) and privacy (P0.5). Setup should track harness steps P0.1–P0.5.
- **Step 3 says "pick the folder called vault inside the kit".** The guide says to move it out and rename it first. Follow the guide.
- **The v1.2 changelog entry** is a scenario placeholder.
- Check every prompt against `vault/` and `guide/prompts.html` at build time, not against `kit-content.js`.
