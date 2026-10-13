// Shared by pages (build time) and client scripts (browser). Keep it free of Node APIs.

export const OS = { mac: "Mac", windows: "Windows", linux: "Linux", phone: "Phone or tablet" } as const;
export type Os = keyof typeof OS;

export const PATHS = {
  a: {
    title: "In a chat app",
    short: "Chat app",
    sub: "Claude or ChatGPT, with nothing extra to install. The AI gives you text, and you paste it into your notes. Good on a work laptop.",
    tool: "a chat app (Claude or ChatGPT)",
  },
  b: {
    title: "With a desktop AI app",
    short: "Desktop AI app",
    sub: "It works inside one folder you choose, and reads and writes your notes there directly. The smoothest way to use the kit.",
    tool: "a desktop AI app",
    recommended: true,
  },
  c: {
    title: "From the terminal",
    short: "Terminal agent",
    sub: "If you already use Claude Code, Codex, Gemini CLI or similar.",
    tool: "a terminal agent",
  },
} as const;
export type Path = keyof typeof PATHS;

/** Day 1, in the order of the kit's harness steps P0.1–P0.5 (see vault/_system/HARNESS-PLAN.md). */
export const STEPS = [
  { id: "kit", title: "Get the kit", harness: "Before P0.1" },
  { id: "obsidian", title: "Install Obsidian", harness: "P0.1" },
  { id: "vault", title: "Give your vault a home", harness: "P0.1" },
  { id: "connect", title: "Connect your AI", harness: "P0.2–P0.3" },
  { id: "hello", title: "Say hello", harness: "P0.3" },
  { id: "plan", title: "Hand over to the plan", harness: "P0.4–P0.5" },
] as const;
export type StepId = (typeof STEPS)[number]["id"];

export const RELEASES_URL = "https://github.com/liqweed/ai-kickstart/releases/latest";
export const REPO_URL = "https://github.com/liqweed/ai-kickstart";
/** The release zip, rounded. Update when the kit grows noticeably (dist/ after scripts/build.sh). */
export const ZIP_SIZE = "about 160 KB";
