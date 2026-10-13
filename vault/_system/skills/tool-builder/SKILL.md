---
name: tool-builder
description: Build, fix or review a small, tested script ("tool") for a job with one right answer — filtering a list, checking notes, calculating dates, converting an export — following the Tools & Connections Contract, with a test, a registry entry and a skill that uses it. Use when the owner says "make this a tool", "write a script for…", "automate this check", "the tool is broken", "review my tools", or when a harness step (P5) says to build one.
---

# Tool builder

A **tool** is a small Python program in the vault that does one exact job the same way every time. Skills decide *when* to use it, and the AI does the judgment around it. The rules are in `_system/TOOLS-CONTRACT.md`. **Read Part A before you start.**

## Modes

| Owner says | Mode |
|---|---|
| "Make this a tool", "write a script for…" | **Build** (below) |
| "The tool is broken", "fix upcoming.py", the self-test failed | **Fix**: reproduce in a test first, then fix, then run the self-test |
| "Review my tools", harness P7.5 | **Review** (end of this file) |

## Build

1. **Is it a tool job?** It needs one right answer, and the AI has done it by hand at least twice. If it's judgment (ranking, writing, "what's good"), say so and offer a skill instead (`skill-builder`). Check the registry (`_system/tools/README.md`): maybe a tool almost does it already, and adding an option beats a new tool.
2. **Spec in five lines**, confirmed by the owner:
   - **Job:** one sentence.
   - **Reads:** which notes, folders or file.
   - **Writes:** nothing, or exactly what (then it's a writer: dry run by default, `--apply` to write).
   - **Output:** show an example of the exact result.
   - **Used by:** which skill, and when.
   Network or secrets needed? Stop and get an explicit OK (TOOLS-CONTRACT §3–4).
3. **Check Python** once: `python3 --version` (Windows: `py --version`) must be 3.9 or newer. Missing? Ask before installing anything (harness P0.6).
4. **Copy the template.** Shared tool: `_system/tools/_template.py` → `_system/tools/<name>.py`. One skill only: → `_system/skills/<skill>/scripts/<name>.py`. Fill in the header block. Use `vaultlib.py` helpers (walking notes, frontmatter, links, tasks, dates) rather than rewriting them.
5. **Write the test first** (TOOLS-CONTRACT §5): in `_system/tools/tests/test_<name>.py`, or `scripts/test_<name>.py` next to a skill script. Build a tiny vault in a temporary folder and cover the normal case, one edge case, and one thing that must not happen. Copy the style of `tests/test_tools.py`.
6. **Write the tool** until the test passes. Keep it small: if it passes ~200 lines, it's probably two tools.
7. **Run `python3 _system/tools/selftest.py`.** Every check must pass, including the contract checks.
8. **Run it on the owner's real notes, in front of them.** Writers: dry run first, then `--apply` only after they say yes. Ask: *"Is this exactly right?"* Fix what isn't.
9. **Register and wire up:**
   - Add a row to the registry in `_system/tools/README.md`.
   - In the skill that uses it, add the command, when to run it, and the **fallback without the tool**.
   - If it has settings: `config/<name>.md`, documented in the registry.
10. **Log it**: harness session log (P5.2 / P5.x), and *Decisions log* if you chose something non-obvious.

## Good habits

- **Plain messages.** "3 notes have no summary. Run with --apply to add the fields." beats a stack trace.
- **Deterministic.** Sort everything. Use `--today` in tests instead of the real date.
- **Fail loudly, early.** Bad input → a clear message and exit code 2. Never guess.
- **Explain the tool to the owner in two lines** after building it: what it does, and the phrase that triggers it.
- **Explain as you go** if the owner's tech comfort is low. They don't need to read the code, but they should know what it touches.

## Review (quarterly, harness P7.5)

1. Run the self-test. Fix or retire any failure.
2. For each registry row: has it run in the last three months? (Ask, or check the skills that use it.) Unused → propose archiving: move it to `99-archive/tools/` and remove its registry row and skill references.
3. Is each one still right? Run it once on real notes and eyeball the output with the owner.
4. Anything new done by hand twice since the last review? Add it to the harness backlog as an **L** item.
5. Log the review in the harness session log.
