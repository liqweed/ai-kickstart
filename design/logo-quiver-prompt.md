# Logo mark: prompt for QuiverAI (quiver.ai)

**Goal:** one square **mark** (no text) for AI Kickstart. It's used as the favicon (16/32 px), the companion app icon (up to 1024 px), the website header (about 22 px next to the "AI Kickstart" wordmark, which stays in system serif type) and the social preview.

**Where it comes from:** the round-1 website prototype (git history; round 2 in [`prototype/`](prototype/) adopted the logo) uses "a note with a seed in it" as a placeholder: a rounded square outline with a green dot. Its identity is warm paper and ink, one moss green for actions, highlighter yellow for things you fill in, and no AI clichés. The mark should carry the kit's three ideas: **plain notes you own · small steps that grow over time · you stay in charge**.

## How to run it

- **Model:** Arrow 2 **Telos**. QuiverAI recommends it for "logos with tight geometry". Generate 4 or more per prompt.
- **Reference image (optional, palette and mood only):** `prototype/screenshots/site-s1-light.jpg`. Give it one role: "palette and mood reference only; do not copy layout or text".
- Run the three concept prompts below, pick a winner, then run the **refinement** prompt on it.
- Save the winner as `design/logo/logo-mark.svg`, plus a one-colour version `logo-mark-mono.svg`. Then upload it to Claude Design round 2.

## Prompt (paste into *Prompt*)

Concept A: the note and the sprout (closest to the prototype)

```
Create a square app-icon logo mark for "AI Kickstart", a free kit that helps ordinary people start using AI with plain notes they own. Final uses: 16px favicon, 22px website header mark, 1024px desktop app icon.
Subject: a single sheet of paper / note with one folded corner, and a small two-leaf seedling sprouting from inside the note, as if growing out of the page.
Style: flat geometric vector mark, calm and crafted, like a well-made stationery brand or a small independent publisher. Not a tech startup.
Colors: ink #251E18 for the note outline, moss green #1A6444 for the sprout, warm paper #F9F6F1 as the note fill. At most 3 colors.
Composition: centered, generous padding, strong simple silhouette, optically balanced in a square.
Avoid: robots, brains, sparkles, stars, glowing orbs, gradients, circuit lines, chat bubbles, lightning bolts, rockets, letters or text, 3D, drop shadows.
```

Concept B: the checkbox that grows

```
Create a square logo mark for "AI Kickstart", a kit for taking small, verified steps with AI over weeks and months. Final uses: 16px favicon up to 1024px app icon.
Subject: a rounded square checkbox drawn in ink, with a moss-green seedling sprouting from its bottom-left corner. The two leaves read as a gentle tick mark, so "done" and "growing" are the same gesture.
Style: flat geometric vector mark, quiet and friendly, editorial rather than techy. Consistent stroke weight, rounded joins.
Colors: ink #251E18, moss green #1A6444, optional warm paper #F9F6F1 fill. No other colors.
Composition: centered, square view box, generous padding, readable as a silhouette at 16px.
Avoid: sparkles, stars, robots, brains, gradients, glow, circuit patterns, text or letters, 3D, shadows, rocket imagery.
```

Concept C: the folder as a home (the "place to live")

```
Create a square logo mark for "AI Kickstart", whose promise is "give your AI a place to live, a memory of you, and a plan".
Subject: a simple file folder whose tab is shaped like a small house roof, with a tiny moss-green seed or sprout in front of it. It says "a home made of plain files".
Style: flat geometric vector mark, warm and trustworthy, like a gift from a thoughtful friend. Minimal shapes, consistent line weight.
Colors: ink #251E18, moss green #1A6444, warm paper #F9F6F1. At most 3 colors.
Composition: centered in a square, generous padding, strong silhouette that survives 16px.
Avoid: sparkles, stars, robots, brains, chat bubbles, gradients, glow, circuit lines, rockets, text or letters, 3D, shadows.
```

## Instructions (paste into *Instructions*, same for all three)

```
Production-ready SVG: square viewBox (0 0 64 64), filled shapes or strokes converted to outlines, no embedded raster, no text elements, no filters, no gradients, no masks. Use few paths with clean geometry and whole-number coordinates where possible. Transparent background. The mark must stay recognisable as a solid silhouette at 16x16 px. Keep inner gaps at least 3 units wide.
```

## Refinement (after picking a winner)

```
Keep this mark's concept, proportions and composition. Make three variants on transparent backgrounds:
1) full color: ink #251E18, moss #1A6444, paper #F9F6F1;
2) dark-mode version: ink becomes #EBE7E0, moss becomes #82D2A8, paper fill becomes #1A1713;
3) single-color version in pure #000000 (for masks and monochrome favicons), with the sprout knocked out as negative space if needed.
Simplify any detail that disappears at 16px. Change nothing else.
```

## Check before accepting

- At **16 px** in a browser tab, light and dark, you can still tell what it is.
- Next to the "AI Kickstart" serif wordmark at 22 px, it doesn't look heavier than the text.
- None of the avoid-list imagery crept in. The SVG has no `<image>`, `<text>`, `<filter>` or gradients, and is under about 4 KB.
- It's original. Quiver output is yours to use, but do a quick reverse-image search for near-identical existing marks before shipping it.
