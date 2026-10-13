---
name: release
description: Cut a new version of the AI Kickstart kit — choose the version number, bump it everywhere, finalise the changelog, run all checks, build the zip, commit, tag and push (CI then publishes the GitHub Release). Use for "release", "cut a version", "ship v1.2", "publish the kit".
---

# Release

A release = a `vX.Y` tag on `main`. Pushing the tag triggers `.github/workflows/release.yml`, which builds the zip and creates the GitHub Release with the changelog section as notes. The website (`site/`) reads `CHANGELOG.md` and `VERSION`, and is deployed by hand with `pnpm run deploy` until CI does it (K17).

## Steps

1. **Preconditions.** Working tree clean (`git status`), on `main`, up to date (`git pull --ff-only`). `CHANGELOG.md` has an **Unreleased** section with at least one entry. If it doesn't, stop: there's nothing to release.
2. **Pick the number.** Major if users must restructure their vault (see the `CHANGELOG.md` header), otherwise minor. Confirm with the maintainer: *"Releasing v1.2 with: … OK?"*
3. **Bump everywhere** (`check_kit.py` verifies all of these):
   - `VERSION` → `1.2`
   - `START-HERE.html` footer: `sed -i '' 's/AI Kickstart · v[0-9.]* · [A-Za-z]* [0-9]*/AI Kickstart · v1.2 · <Month YYYY>/' START-HERE.html` (on Linux, drop the `''`)
   - README credit line: `v1.2, <Month YYYY>.`
   - `CHANGELOG.md`: rename **Unreleased** → `## v1.2 — YYYY-MM-DD`
4. **Check and build:** `scripts/build.sh`. It must end with `build: dist/ai-kickstart-v1.2.zip …`. Open the zip listing and confirm it holds only `README.md LICENSE START-HERE.html vault/`.
5. **Browser smoke test** of `START-HERE.html`, opened from the file: it renders in light and dark, the copy buttons work, and the console shows no errors. The site needs `pnpm test && pnpm check && pnpm build && scripts/check_site.py` green.
6. **Commit, tag, push:**
   ```bash
   git commit -am "Release v1.2"
   git tag -a v1.2 -m "v1.2"
   git push origin main --follow-tags
   ```
7. **Verify the outcome, not the trigger:** wait for the workflows, then confirm the release exists and has the zip attached (`https://github.com/liqweed/ai-kickstart/releases/tag/v1.2`), then run `pnpm run deploy` and confirm ai-kickstart.me/whats-new/ shows v1.2. "The workflow ran" is not proof.
8. **Log it** in `docs/journal.md` (session log) and tell the maintainer the release URL.

## If something fails

- A check fails → fix it in a normal commit, then restart from step 4. Never tag a red build.
- The release workflow **didn't start** (no run listed for the tag; seen when a tag arrives in the same push that creates or changes workflows) → re-push the unpublished tag: `git push origin :refs/tags/v1.2 && git push origin v1.2`.
- A job failed for a passing reason (a network timeout while downloading a tool) and `gh run rerun` is refused (the token here has no admin rights) → check nothing was published (`gh release view <tag>` fails), then re-push the tag as above. Same for app tags (`app-vX.Y.Z`).
- The release workflow failed after the tag was pushed → fix on `main`, then move the tag: `git tag -fa v1.2 -m v1.2 && git push -f origin v1.2`. Only do this if the release isn't published yet, and ask the maintainer first.
