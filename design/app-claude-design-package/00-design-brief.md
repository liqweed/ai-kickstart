# 00 · Design brief: AI Kickstart companion app

A small, downloadable **desktop companion** for the AI Kickstart kit (see the website brief for what the kit is). It helps a person **start** (create their vault, check prerequisites, connect their AI), **keep their place** between sessions over weeks and months, and **update** the kit safely. All of it happens locally on their own computer.

It is **not** an AI client, a chat app or a note editor. The AI tool and Obsidian do the real work; the app is the friendly guide that sits beside them.

It is the **functional** side of AI Kickstart. All explanations, guides and reference material live on the website (**ai-kickstart.me**), and the app links there instead of repeating them.

## Binding (do not deviate)

- **Voice:** warm, plain, second person, short sentences. Technical terms explained the first time. The same voice as the website.
- **Credit line:** "Designed and shared by Ophir Radnitz" appears in the app (an About surface is fine). It's the only personal detail.
- **Accessibility:** WCAG 2.2 AA contrast in light and dark (follow the OS). Not colour-alone. Fully keyboard-operable with visible focus. Respects reduced motion.
- **Visual identity:** **if the website prototype has been approved**, its identity (type, colour, mark, core primitives) is binding. It is either already in the same Claude Design project (preferred) or exported to `assets/website/`. **If neither exists, identity is open**, but it must be able to share one identity with the website later.
- **Honesty about locality:** every place the app touches the network (only the optional update check) is visible and switchable.

## Aesthetic direction (spirit, not spec)

- A calm, trustworthy desk companion. It should feel like a well-made small utility, not a dashboard full of metrics.
- It must make a non-technical person feel **capable**, and it must never make them feel behind.

## Open: yours to propose

Everything not pinned above: window shape and layout, navigation, how progress is visualised, iconography, motion, density, onboarding pacing.
