# Companion app (maintainers)

The desktop companion, built on [tinyjs](https://tinyjs.app) (ARCHITECTURE D15). Right now it is the **K11 spike**: one window with five checks that prove the stack on a machine. The design to build toward is in [`design/prototype/`](../design/prototype/).

| Path | What |
|---|---|
| `backend/main.ts` | The only code with file-system access. Runs on txiki.js (QuickJS), **not Node** |
| `src/` | The page: React + TypeScript, styled by `@ai-kickstart/design/kickstart.css` plus layout-only `app.css` |
| `tinyjs.json` | App identity, window size, backend entry, Vite hooks |
| `.agents/skills/tinyjs/` | tinyjs's own agent skill (API reference), from the scaffold |

## Run it

Install tinyjs once (macOS: `curl -fsSL https://tinyjs.app/install | sh`, Windows: `irm https://tinyjs.app/install.ps1 | iex`), then `pnpm install` at the repo root and:

```bash
cd app
tinyjs dev       # the window, with hot reload
tinyjs build     # dist/AI Kickstart.app (macOS) or dist/ai-kickstart.exe (Windows)
pnpm build       # type-check page + backend, bundle the page
pnpm lint
```

Run tinyjs commands from a terminal: with no terminal attached (stdin closed), `tinyjs new` hung in tinyjs 0.51.1.

## Test builds

Push a tag `app-vX.Y.Z` matching `tinyjs.json`'s version: `.github/workflows/app.yml` builds macOS (arm64) and Windows (x64) on GitHub's runners and publishes a GitHub **pre-release** with [`TEST-BUILD.md`](TEST-BUILD.md) as its notes. Pre-releases never become "Latest", so the kit's download links don't move. Unsigned until K21.

## The K11 checks

In the window: **Choose folder…** (any empty folder), then create `_inbox/hello.md` inside it (by hand or with an AI), then **Open in Obsidian**. All five rows should show ✓, and Obsidian should come forward with the folder open as a vault. The app remembers the folder in `~/.ai-kickstart/config.json`.

| Check | macOS 27, Apple silicon (2026-10-13) | Windows 10/11 |
|---|---|---|
| Pick a folder | needs a human click (native dialog) | — |
| Write `~/.ai-kickstart/` | ✓ | — |
| Notice `_inbox/hello.md` (recursive watch, `.obsidian/` ignored) | ✓ | — (libuv's recursive watch differs per OS: check it) |
| Open `obsidian://` | ✓ (system accepted it, Obsidian came forward) | — |
| `kickstart.css` tokens, light + dark | ✓ (dark) | — |
| Packaged build | ✓ 9.4 MB, ad-hoc signed; signed + notarised needs K21 | ✓ builds in CI (6.9 MB zip); not yet run on a real machine |
