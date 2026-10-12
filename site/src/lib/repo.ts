// Build-time access to the kit's own files (Node only; never imported by client scripts).
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

/** The repo root: astro commands run inside site/. */
const ROOT = (() => {
  for (const dir of [resolve(process.cwd(), ".."), process.cwd()]) {
    if (existsSync(resolve(dir, "VERSION")) && existsSync(resolve(dir, "vault"))) return dir;
  }
  throw new Error("site: can't find the kit (VERSION + vault/). Run astro from site/.");
})();

export const repoFile = (path: string): string => readFileSync(resolve(ROOT, path), "utf8");
export const repoDirs = (path: string): string[] =>
  readdirSync(resolve(ROOT, path), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort();

/** "1.1" from VERSION. */
export const VERSION = repoFile("VERSION").trim();
