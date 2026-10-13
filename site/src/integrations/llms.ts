// /llms.txt (https://llmstxt.org/) plus a Markdown copy of each page, written after the build.
// The Markdown is converted from the built pages themselves, so it can't drift from what visitors see.
// Interactive parts (buttons, pills, dialogs, hidden panels) are dropped; prompt cards become code blocks.
import { readFile, writeFile } from "node:fs/promises";
import type { AstroIntegration } from "astro";
import TurndownService from "turndown";
import { PATHS, REPO_URL } from "../lib/choices.ts";

/** In nav order. `optional` pages go under the spec's "Optional" heading. */
const PAGES: { path: string; optional?: boolean }[] = [
  { path: "/" },
  { path: "/setup/" },
  { path: "/ideas/" },
  { path: "/connections/" },
  { path: "/prompts/" },
  { path: "/how-it-works/" },
  { path: "/whats-new/", optional: true },
];

/** The spec's rule for URLs without a file name: append index.html.md. */
export const mdPath = (path: string) => `${path}index.html.md`;

const classes = (n: HTMLElement) => (n.getAttribute?.("class") ?? "").split(/\s+/);
const has = (n: HTMLElement, c: string) => classes(n).includes(c);
/** Child elements (the build-time DOM has no iterable `children`). */
const kids = (n: Node) => Array.from(n.childNodes).filter((c): c is HTMLElement => c.nodeType === 1);
const text = (n: Element | null) => (n?.textContent ?? "").replace(/\s+/g, " ").trim();

function converter(site: URL) {
  const td = new TurndownService({ headingStyle: "atx", codeBlockStyle: "fenced", bulletListMarker: "-", emDelimiter: "*" });

  td.addRule("absolute-links", {
    filter: (n) => n.nodeName === "A" && !!n.getAttribute("href"),
    replacement: (content, n) => {
      const href = (n as HTMLElement).getAttribute("href")!;
      return content.trim() ? `[${content.trim()}](${new URL(href, site).href})` : "";
    },
  });

  td.addRule("prompt", {
    filter: (n) => has(n as HTMLElement, "kk-prompt"),
    replacement: (_c, n) => {
      const el = n as HTMLElement;
      const label = text(el.querySelector(".kk-prompt__label"));
      const note = text(el.querySelector(".kk-prompt__note"));
      const body = (el.querySelector(".kk-prompt__text")?.textContent ?? "").trim();
      return `\n\n**${label}**${note ? ` (${note})` : ""}\n\n\`\`\`text\n${body}\n\`\`\`\n\n`;
    },
  });

  td.addRule("catalog-row", {
    filter: (n) => has(n as HTMLElement, "kk-row"),
    replacement: (_c, n) => {
      const el = n as HTMLElement;
      const desc = td.turndown(el.querySelector(".kk-row__desc")?.innerHTML ?? "");
      return `\n- **${text(el.querySelector(".kk-row__name"))}** (${text(el.querySelector(".kk-tag"))}): ${desc}`;
    },
  });

  td.addRule("summary", {
    filter: "summary",
    replacement: (c, n) => {
      const el = n as HTMLElement;
      if (!has(el, "kk-step__head")) return `\n\n**${c.trim()}**\n\n`;
      return `\n\n### ${text(el.querySelector(".kk-step__title"))} (${text(el.querySelector(".kk-step__kicker"))})\n\n`;
    },
  });
  td.addRule("legend", { filter: (n) => has(n.parentNode as HTMLElement, "legend"), replacement: (c) => `\n- ${c.trim()}` });
  td.addRule("variant-tag", { filter: (n) => has(n as HTMLElement, "variant-tag"), replacement: (c) => `**${c.trim()}:** ` });

  td.addRule("proof", {
    filter: (n) => has(n as HTMLElement, "kk-proof"),
    replacement: (_c, n) => {
      const el = n as HTMLElement;
      const paths = (el.getAttribute("data-path") ?? "").split(/\s+/).filter((p): p is keyof typeof PATHS => p in PATHS);
      const who = paths.map((p) => PATHS[p].short).join(" or ");
      const [doneWhen, , check] = kids(el).slice(1).map((c) => text(c));
      return `\n\n${who ? `*${who}.* ` : ""}**Done when:** ${doneWhen} **Check:** ${check}\n\n`;
    },
  });

  td.addRule("pre", {
    filter: "pre",
    replacement: (_c, n) => `\n\n\`\`\`text\n${(n.textContent ?? "").replace(/\n+$/, "")}\n\`\`\`\n\n`,
  });

  td.addRule("table", {
    filter: "table",
    replacement: (_c, n) => {
      const rows = Array.from((n as HTMLElement).querySelectorAll("tr")).map((tr) => kids(tr).map((c) => td.turndown(c.innerHTML).replace(/\|/g, "\\|")));
      const line = (r: string[]) => `| ${r.join(" | ")} |`;
      return `\n\n${[line(rows[0]), line(rows[0].map(() => "---")), ...rows.slice(1).map(line)].join("\n")}\n\n`;
    },
  });

  // Added last: a later rule wins, and td.remove() would lose to the built-in rules (headings, lists…).
  td.addRule("drop", {
    filter: (n) => {
      const el = n as HTMLElement;
      return (
        ["H1", "BUTTON", "DIALOG", "SCRIPT", "STYLE", "INPUT", "NAV", "svg"].includes(el.nodeName) ||
        el.hasAttribute?.("hidden") ||
        el.getAttribute?.("aria-hidden") === "true" ||
        ["kk-sr", "step-mark", "step-chev", "area__count", "kk-prompt__hint", "tray", "picks", "rounds__n"].some((c) => has(el, c))
      );
    },
    replacement: () => "",
  });

  return td;
}

/**
 * Prompt text becomes <pre>, since the converter collapses whitespace everywhere else. Elsewhere, inline
 * elements styled as separate lines (a title and its subtitle) get a space between them.
 */
const prepare = (main: string) =>
  main
    .replace(/<div class="kk-prompt__text"([^>]*)>([\s\S]*?)<\/div>/g, '<pre class="kk-prompt__text"$1>$2</pre>')
    .split(/(<pre[\s\S]*?<\/pre>)/)
    .map((part, i) => (i % 2 ? part : part.replace(/(<\/(?:span|strong|em|a)>)(?=<(?:span|strong|em|a)\b)/g, "$1 ")))
    .join("");

const pick = (html: string, re: RegExp) => html.match(re)?.[1]?.trim() ?? "";
const unescape = (s: string) => s.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");

export default function llms(): AstroIntegration {
  let site: URL;
  return {
    name: "ai-kickstart:llms",
    hooks: {
      "astro:config:done": ({ config }) => {
        site = new URL(config.site!);
      },
      "astro:build:done": async ({ dir, logger }) => {
        const td = converter(site);
        const entries: { optional?: boolean; line: string }[] = [];
        let summary = "";
        for (const { path, optional } of PAGES) {
          const html = await readFile(new URL(`.${path}index.html`, dir), "utf8");
          const title = unescape(pick(html, /<title>([^<]*)<\/title>/)).replace(/^AI Kickstart · | · AI Kickstart$/g, "");
          const description = unescape(pick(html, /<meta name="description" content="([^"]*)"/));
          const h1 = unescape(pick(html, /<h1[^>]*>([\s\S]*?)<\/h1>/).replace(/<[^>]+>/g, "")).replace(/\s+/g, " ");
          const main = prepare(pick(html, /<main[^>]*>([\s\S]*)<\/main>/));
          if (!main || !description || !h1) throw new Error(`llms: ${path} has no <main>, <h1> or description`);
          // The page's own <h1> leads; the converter drops it from the body.
          const md = td.turndown(main).replace(/\n{3,}/g, "\n\n");
          const pageUrl = new URL(path, site);
          await writeFile(new URL(`.${mdPath(path)}`, dir), `# ${h1}\n\n> ${description}\n\nWeb page: ${pageUrl.href}\n\n${md}\n`);
          if (path === "/") summary = description;
          entries.push({ optional, line: `- [${title}](${new URL(mdPath(path), site).href}): ${description}` });
        }
        const txt = [
          "# AI Kickstart",
          "",
          `> ${summary}`,
          "",
          "AI Kickstart is a free, open kit (CC BY 4.0): an Obsidian vault of plain Markdown notes, a short interview that teaches your AI about you, and a step-by-step plan. It works with any capable AI tool, or with a chat app alone. Each link below is a Markdown version of a page on the site, made from the kit when the site is built.",
          "",
          "## Pages",
          "",
          ...entries.filter((e) => !e.optional).map((e) => e.line),
          "",
          "## Optional",
          "",
          ...entries.filter((e) => e.optional).map((e) => e.line),
          `- [Source on GitHub](${REPO_URL}): the kit itself, the vault template and this site`,
          "",
        ].join("\n");
        await writeFile(new URL("./llms.txt", dir), txt);
        logger.info(`llms.txt + ${PAGES.length} Markdown pages`);
      },
    },
  };
}
