# Runtime facts: tinyjs (trimmed)

Source: [tinyjs.app](https://tinyjs.app/), read 2026-10-12. Excerpted facts only; check the site for current details.

- A desktop runtime for macOS, Windows and Linux (no mobile). Backend JavaScript runs on txiki.js (QuickJS + libuv) with full system access (files, processes, sqlite, fetch). The UI is the OS's native webview: WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux. No bundled Chromium, no local HTTP server or open port. Page↔backend calls go over a Unix socket or named pipe.
- Front end: plain HTML/CSS/JS with no build step by default; optional Vite templates.
- Size: about 6 MB total.
- Platform status: macOS is primary and stable (macOS 15+, Apple silicon and Intel). Windows 10/11 (needs WebView2) and Linux (glibc 2.35+, WebKitGTK 4.1) are **beta**; some native calls are not yet ported.
- Distribution: `tinyjs build` makes a codesigned macOS `.app` (optional `.dmg`), and `tinyjs notarize` notarizes it. Windows gets a portable folder, Linux a tarball. Each platform must be built on its own OS.
- A built-in updater checks a sha256 and the code signature, and rolls back on failure.
- Licence: MIT.

**Implication for design:** the prototype's HTML/CSS can transfer almost directly into the app's front end. Rendering differs slightly between the three webview engines.
