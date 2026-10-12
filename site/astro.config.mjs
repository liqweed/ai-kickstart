// @ts-check
import { defineConfig } from "astro/config";

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
    },
  },
});
