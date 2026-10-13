// @ts-check
import { createHash } from "node:crypto";
import { defineConfig } from "astro/config";
import { THEME_BOOT } from "./src/lib/theme-boot.mjs";

/** @param {string} text @returns {`sha256-${string}`} */
const sha256 = (text) => `sha256-${createHash("sha256").update(text).digest("base64")}`;

// Static output only. No integrations, no client framework: the few interactive pieces are plain TS modules.
export default defineConfig({
  site: "https://ai-kickstart.me",
  trailingSlash: "always",
  build: { format: "directory" },
  devToolbar: { enabled: false },
  markdown: { syntaxHighlight: false },
  security: {
    // Astro hashes every script and style it emits. Nothing may load from another origin.
    csp: {
      directives: [
        "default-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
      ],
      // The theme script in <head> is inline (it must run before the page paints), so it's hashed here.
      scriptDirective: { hashes: [sha256(THEME_BOOT)] },
    },
  },
});
