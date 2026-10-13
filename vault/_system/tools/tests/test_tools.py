"""Behaviour tests for the vault tools. Each test builds a small, throwaway vault in a temp folder.

Run all tool tests with: python3 _system/tools/selftest.py
Fake secrets below are assembled from pieces, so this file itself never looks like it holds one.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import datetime as dt
import io
import json
import subprocess
import tempfile
import textwrap
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import fix_frontmatter  # noqa: E402
import hub_index  # noqa: E402
import kit_update  # noqa: E402
import recent  # noqa: E402
import secret_scan  # noqa: E402
import upcoming  # noqa: E402
import vault_lint  # noqa: E402
import vaultlib as vl  # noqa: E402

TODAY = dt.date(2026, 10, 13)
FAKE_KEY = "sk-" + "proj-" + "Ab3" * 10
FAKE_CARD = "4012 " + "8888 8888 1881"
FAKE_IBAN = "GB82 " + "WEST 1234 5698 7654 32"


def fm(**kw: str) -> str:
    base = {"tags": "[test]", "type": "note", "status": "active", "created": "2026-10-01",
            "updated": "2026-10-01", "summary": "A test note."}
    base.update(kw)
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in base.items()) + "---\n"


class VaultCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, relpath: str, text: str) -> Path:
        p = self.vault / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
        return p

    def basic_vault(self) -> None:
        self.write("_system/index.md", fm(type="navigation") + "# Index\n`01-life/` with `people/`. `03-projects/active/` too.\n"
                   "Also `_system/VAULT-CONTRACT.md` and `06-reference/Gone.md`.\n")
        self.write("_system/VAULT-CONTRACT.md", fm(type="reference") + "# Contract\nRules live here, linked from [[index]].\n")
        self.write("_system/skills/demo/SKILL.md", "---\nname: demo\ndescription: x\n---\nSee [[Nowhere]].\n")
        self.write("01-life/people/_index.md", fm(type="navigation") + "# People\n\n<!-- auto-index:start group=relationship -->\n<!-- auto-index:end -->\n\nKept text.\n")
        self.write("01-life/people/Sam.md", fm(type="person", relationship="friend", birthday="10-20") + "# Sam\nLikes [[Tea]] and [[01-life/people/_index\\|people/]].\n")
        self.write("01-life/people/Robin.md", fm(type="person", relationship="family", birthday="1990-10-12") + "# Robin\nSibling. See [[Sam]].\n")
        self.write("01-life/Tea.md", fm() + "# Tea\nGreen tea notes, linked from [[Sam]].\n")
        self.write("03-projects/active/Kitchen.md", fm(type="project", due="2026-10-20") + textwrap.dedent("""\
            # Kitchen
            - [ ] Order tiles 📅 2026-10-15
            - [ ] Call the plumber due: 2026-10-10
            - [ ] Pick paint [due:: 2026-11-30]
            - [x] Measure the room ✅ 2026-10-11
            - [ ] Someday, no date
            ```
            - [ ] In a code block 📅 2026-10-14
            ```
            """))
        self.write("notes/Loose.md", "Just some loose thoughts without any frontmatter at all here.\n")
        self.write("notes/Broken.md", fm(summary="Has a broken link.") + "See [[Does not exist]] and `[[in code]]`.\n")
        self.write("_inbox/old idea.md", fm(created="2026-01-01") + "An old idea from January, still unsorted.\n")
        self.write("04-learning/tea.md", fm() + "# tea (duplicate name)\nAnother tea note, linked to [[Sam]].\n")


class TestVaultlib(VaultCase):
    def test_frontmatter_parsing(self) -> None:
        f = vl.parse_frontmatter("---\ntags: [a, \"b, c\"]\nlist:\n  - x\n  - y\ntitle: 'Quoted'\nempty:\n---\nbody")
        self.assertEqual(f.data["tags"], ["a", "b, c"])
        self.assertEqual(f.data["list"], ["x", "y"])
        self.assertEqual(f.data["title"], "Quoted")
        self.assertEqual(f.data["empty"], "")
        self.assertEqual(f.problems, [])
        self.assertTrue(vl.parse_frontmatter("---\nunclosed: yes\n").problems)
        self.assertFalse(vl.parse_frontmatter("no frontmatter").present)

    def test_wikilinks_ignore_code_and_handle_escaped_pipes(self) -> None:
        text = "[[A]] [[B|alias]] [[C#Head]] ![[d.png]] [[E\\|table alias]] `[[F]]`\n```\n[[G]]\n```\n<!-- [[H]] -->"
        self.assertEqual([l.target for l in vl.wikilinks(text)], ["A", "B", "C", "d.png", "E"])

    def test_next_occurrence_and_leap_day(self) -> None:
        self.assertEqual(vl.next_occurrence(10, 20, TODAY), dt.date(2026, 10, 20))
        self.assertEqual(vl.next_occurrence(1, 5, TODAY), dt.date(2027, 1, 5))
        self.assertEqual(vl.next_occurrence(2, 29, dt.date(2027, 2, 1)), dt.date(2027, 2, 28))

    def test_resolver(self) -> None:
        self.basic_vault()
        r = vl.LinkResolver(self.vault)
        self.assertEqual(r.resolve("Sam"), "01-life/people/Sam.md")
        self.assertEqual(r.resolve("01-life/people/_index"), "01-life/people/_index.md")
        self.assertEqual(r.resolve("people/sam"), "01-life/people/Sam.md")
        self.assertIsNone(r.resolve("Nobody"))


class TestSecretScan(VaultCase):
    def test_finds_and_masks(self) -> None:
        self.write("a.md", f"key: {FAKE_KEY}\ncard {FAKE_CARD}\niban {FAKE_IBAN}\npassword: Tr0ub4dor&3\n")
        found = secret_scan.scan_vault(self.vault, config={})
        self.assertEqual(sorted(f["kind"] for f in found),
                         sorted(["API key (OpenAI-style)", "card number", "bank account (IBAN)", "password or secret"]))
        out = io.StringIO()
        with redirect_stdout(out):
            secret_scan.main(["--vault", str(self.vault)])
        self.assertNotIn(FAKE_KEY, out.getvalue())
        self.assertNotIn("Tr0ub4dor", out.getvalue())

    def test_no_false_alarms(self) -> None:
        self.write("b.md", "password: in the password manager\nOrder 1234 5678 9012 3456 shipped\n"
                           f"card {FAKE_CARD} <!-- secret-scan: ignore -->\nDate 2026-10-13, phone +31 20 123 4567\n")
        self.assertEqual(secret_scan.scan_vault(self.vault, config={}), [])

    def test_extra_patterns_and_allow(self) -> None:
        self.write("c.md", "member no ZX-99881\nallowed ZX-11111\n")
        found = secret_scan.scan_vault(self.vault, config={"extra_patterns": [r"ZX-\d{5}"], "allow": ["ZX-11111"]})
        self.assertEqual([f["line"] for f in found], [1])

    def test_exit_codes(self) -> None:
        self.write("ok.md", "nothing here\n")
        self.assertEqual(secret_scan.main(["--vault", str(self.vault), "--json"]), 0)
        self.write("bad.md", f"{FAKE_KEY}\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(secret_scan.main(["--vault", str(self.vault)]), 1)


class TestVaultLint(VaultCase):
    def test_finds_the_planted_problems(self) -> None:
        self.basic_vault()
        self.write("notes/Leak.md", fm(summary="Oops.") + f"token {FAKE_KEY}, linked from nowhere but [[Tea]].\n")
        found = vault_lint.lint(self.vault, TODAY, config={})
        by = {}
        for f in found:
            by.setdefault(f["check"], []).append(f)
        self.assertEqual([f["detail"] for f in by["broken-link"]], ["[[Does not exist]] has no matching note or file"])
        self.assertEqual([f["file"] for f in by["frontmatter-missing"]], ["notes/Loose.md"])
        self.assertIn("notes/Loose.md", [f["file"] for f in by["orphan"]])
        self.assertEqual([f["file"] for f in by["inbox-age"]], ["_inbox/old idea.md"])
        self.assertEqual(sorted(f["file"] for f in by["duplicate-name"]), ["01-life/Tea.md", "04-learning/tea.md"])
        self.assertTrue(any("notes/" in str(f["detail"]) for f in by["index-drift"]))
        self.assertTrue(any("06-reference/Gone.md" in str(f["detail"]) for f in by["index-drift"]))
        self.assertEqual([f["file"] for f in by["secret"]], ["notes/Leak.md"])
        # Skills are exempt from link checks; links in code are ignored.
        self.assertFalse(any("Nowhere" in str(f["detail"]) or "in code" in str(f["detail"]) for f in found))

    def test_field_checks_and_config(self) -> None:
        self.write("_system/index.md", fm(type="navigation") + "`x/`\n")
        self.write("x/A.md", fm(type="recipe", status="active", updated="2025-01-01", created="2025-02-01") + "Body text long enough to count here.\n[[B]]\n")
        self.write("x/B.md", "---\ntags: [x]\ntype: note\n---\nNo status, no dates, no summary. Linked [[A]].\n")
        found = vault_lint.lint(self.vault, TODAY, config={})
        details = [str(f["detail"]) for f in found]
        self.assertTrue(any("type 'recipe'" in d for d in details))
        self.assertTrue(any("updated is earlier than created" in d for d in details))
        self.assertTrue(any(d.startswith("missing: status, created, updated, summary") for d in details))
        found = vault_lint.lint(self.vault, TODAY, config={"types": ["recipe"], "stale_days": 9999})
        self.assertFalse(any("type 'recipe'" in str(f["detail"]) for f in found))

    def test_exit_code_and_only(self) -> None:
        self.basic_vault()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(vault_lint.main(["--vault", str(self.vault), "--today", "2026-10-13"]), 1)
            self.assertEqual(vault_lint.main(["--vault", str(self.vault), "--today", "2026-10-13", "--only", "orphan"]), 0)
            self.assertEqual(vault_lint.main(["--vault", str(self.vault), "--only", "nonsense"]), 2)


class TestUpcoming(VaultCase):
    def test_dates_and_tasks(self) -> None:
        self.basic_vault()
        items = upcoming.collect(self.vault, TODAY, 14, config={})
        got = [(i["date"], i["kind"], i["text"]) for i in items]
        self.assertIn(("2026-10-10", "due", "Call the plumber"), got)          # overdue
        self.assertIn(("2026-10-15", "due", "Order tiles"), got)
        self.assertIn(("2026-10-20", "birthday", "Sam: birthday"), got)
        self.assertIn(("2026-10-20", "due", "Kitchen: due"), got)
        self.assertIn(("2027-10-12", "birthday", "Robin: birthday (37)"), [(i["date"], i["kind"], i["text"]) for i in upcoming.collect(self.vault, TODAY, 365, config={})])
        texts = [i["text"] for i in items]
        self.assertNotIn("Measure the room", texts)       # done
        self.assertNotIn("Pick paint", texts)             # beyond 14 days
        self.assertFalse(any("code block" in t for t in texts))
        no_overdue = upcoming.collect(self.vault, TODAY, 14, include_overdue=False, config={})
        self.assertNotIn("Call the plumber", [i["text"] for i in no_overdue])

    def test_custom_fields(self) -> None:
        self.write("w.md", fm(warranty_until="2026-10-30") + "Dishwasher.\n")
        items = upcoming.collect(self.vault, TODAY, 30, config={"date_fields": ["warranty_until"]})
        self.assertEqual([i["kind"] for i in items], ["warranty_until"])


class TestRecent(VaultCase):
    def test_window(self) -> None:
        self.basic_vault()
        self.write("01-life/New.md", fm(created="2026-10-12", updated="2026-10-12") + "Brand new.\n")
        res = recent.collect(self.vault, TODAY, 7)
        self.assertIn("01-life/New.md", [e["file"] for e in res["created"]])
        self.assertNotIn("_inbox/old idea.md", [e["file"] for e in res["created"] + res["updated"]])
        self.assertEqual([e["text"] for e in res["completed_tasks"]], ["Measure the room"])


class TestFixFrontmatter(VaultCase):
    def test_dry_run_then_apply(self) -> None:
        loose = self.write("01-life/people/Kim.md", "# Kim\nFriend from the choir.\n")
        partial = self.write("03-projects/ideas/Boat.md", "---\ntags: [projects]\nsummary: Maybe a boat.\n---\n# Boat\n")
        broken = self.write("x/Broken.md", "---\ntags: [x\n")
        before = loose.read_text(encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(fix_frontmatter.main(["--vault", str(self.vault)]), 1)
        self.assertEqual(loose.read_text(encoding="utf-8"), before)  # dry run wrote nothing
        with redirect_stdout(io.StringIO()):
            fix_frontmatter.main(["--vault", str(self.vault), "--apply"])
        k = vl.parse_frontmatter(loose.read_text(encoding="utf-8"))
        self.assertEqual((k.data["type"], k.data["status"], k.data["tags"]), ("person", "active", ["life", "people"]))
        self.assertTrue(loose.read_text(encoding="utf-8").endswith("# Kim\nFriend from the choir.\n"))
        b = vl.parse_frontmatter(partial.read_text(encoding="utf-8"))
        self.assertEqual(b.data["tags"], ["projects"])            # existing value kept
        self.assertEqual(b.data["summary"], "Maybe a boat.")
        self.assertEqual((b.data["type"], b.data["status"]), ("idea", "someday"))
        self.assertEqual(broken.read_text(encoding="utf-8"), "---\ntags: [x\n")  # unreadable: left alone
        with redirect_stdout(io.StringIO()):
            fix_frontmatter.main(["--vault", str(self.vault), "--apply"])  # idempotent
        self.assertEqual(b.data, vl.parse_frontmatter(partial.read_text(encoding="utf-8")).data)

    def test_keeps_windows_line_endings(self) -> None:
        p = self.vault / "n.md"
        p.write_bytes(b"---\r\ntags: [a]\r\n---\r\nBody\r\n")
        with redirect_stdout(io.StringIO()):
            fix_frontmatter.main(["--vault", str(self.vault), "--apply"])
        raw = p.read_bytes()
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        self.assertTrue(raw.endswith(b"---\r\nBody\r\n"))


class TestHubIndex(VaultCase):
    def test_generate_group_and_idempotent(self) -> None:
        self.basic_vault()
        hub = self.vault / "01-life/people/_index.md"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(hub_index.main(["--vault", str(self.vault)]), 1)  # dry run: would change
            self.assertEqual(hub_index.main(["--vault", str(self.vault), "--apply"]), 0)
        text = hub.read_text(encoding="utf-8")
        self.assertIn("### Family\n- [[01-life/people/Robin|Robin]] — A test note.", text)
        self.assertIn("### Friend\n- [[01-life/people/Sam|Sam]]", text)
        self.assertTrue(text.startswith("---\n") and text.rstrip().endswith("Kept text."))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(hub_index.main(["--vault", str(self.vault)]), 0)  # now current

    def test_subfolders_and_broken_markers(self) -> None:
        self.write("03-projects/_index.md", "# Projects\n<!-- auto-index:start depth=2 -->\n<!-- auto-index:end -->\n")
        self.write("03-projects/active/Kitchen.md", fm(summary="New kitchen.") + "x\n")
        self.write("04-learning/_index.md", "# Learning\n<!-- auto-index:start -->\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(hub_index.main(["--vault", str(self.vault), "--apply"]), 1)  # one broken hub
        text = (self.vault / "03-projects/_index.md").read_text(encoding="utf-8")
        self.assertIn("- **active/** — 1 note\n  - [[03-projects/active/Kitchen|Kitchen]] — New kitchen.", text)


class TestKitUpdate(VaultCase):
    OLD = {
        "AGENTS.md": "# Agents v1\n",
        "_system/HARNESS-PLAN.md": "- [ ] P0.1 Install\n",
        "_system/profile/GOALS.md": "# Goals\n",
        "_system/skills/a/SKILL.md": "skill a v1\n",
        "_system/skills/b/SKILL.md": "skill b v1\n",
        "_system/templates/T.md": "template\n",
        "_system/old-only.md": "retired soon\n",
    }
    NEW = {
        "AGENTS.md": "# Agents v2\n",
        "_system/HARNESS-PLAN.md": "- [ ] P0.1 Install\n- [ ] P0.6 Tools\n",
        "_system/profile/GOALS.md": "# Goals\n",
        "_system/skills/a/SKILL.md": "skill a v2\n",
        "_system/skills/b/SKILL.md": "skill b v2\n",
        "_system/skills/c/SKILL.md": "skill c\n",
        "_system/templates/T.md": "template v2\n",
        "_system/kickstart/kit-version.md": "---\nkit_version: \"1.4\"\n---\n",
    }

    def kit(self, name: str, files: dict) -> Path:
        root = self.vault.parent / f"{self.vault.name}-{name}" / "vault"
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(text.encode("utf-8"))  # bytes, so Windows doesn't turn \n into \r\n
        self.addCleanup(lambda: __import__("shutil").rmtree(root.parent, ignore_errors=True))
        return root.parent

    def lived_in_vault(self) -> None:
        for rel, text in self.OLD.items():
            self.write(rel, text)
        self.write("_system/skills/b/SKILL.md", "skill b v1\nmy own tweak\n")             # edited kit file
        self.write("_system/profile/GOALS.md", "# Goals\n- run a 10k\n")                  # their profile
        self.write("_system/HARNESS-PLAN.md", "- [x] P0.1 Install\n")                      # their progress
        (self.vault / "_system/skills/a/SKILL.md").write_bytes(b"skill a v1\r\n")         # only line endings changed
        (self.vault / "_system/templates/T.md").unlink()                                   # they deleted it
        self.write("01-life/Tea.md", "My tea notes.\n")                                   # not in the kit at all

    def snapshot(self) -> dict:
        return {vl.rel(self.vault, p): p.read_bytes() for p in self.vault.rglob("*") if p.is_file()}

    def test_plan_apply_and_idempotent(self) -> None:
        self.lived_in_vault()
        old, new = self.kit("old", self.OLD), self.kit("new", self.NEW)
        actions = {r["path"]: r["action"] for r in kit_update.plan(self.vault, kit_update.load_kit(new), kit_update.load_kit(old))}
        self.assertEqual(actions, {
            "AGENTS.md": "merge", "_system/HARNESS-PLAN.md": "merge", "_system/profile/GOALS.md": "unchanged",
            "_system/skills/a/SKILL.md": "update", "_system/skills/b/SKILL.md": "conflict", "_system/skills/c/SKILL.md": "add",
            "_system/templates/T.md": "removed", "_system/kickstart/kit-version.md": "add", "_system/old-only.md": "retired"})
        before = self.snapshot()
        args = ["--vault", str(self.vault), "--kit", str(new), "--old", str(old)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kit_update.main(args), 1)
        self.assertEqual(self.snapshot(), before, "the dry run wrote something")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(kit_update.main(args + ["--apply"]), 1)  # the conflict and merges still need a person
        after = self.snapshot()
        changed = {p for p in after if before.get(p) != after[p]}
        self.assertEqual(changed, {"_system/skills/a/SKILL.md", "_system/skills/c/SKILL.md", "_system/kickstart/kit-version.md"})
        self.assertFalse((self.vault / "_system/templates/T.md").exists(), "a deleted file came back")
        with redirect_stdout(io.StringIO()) as out:
            kit_update.main(args + ["--json"])
        report = json.loads(out.getvalue())
        self.assertEqual((report["count"]["update"], report["count"]["add"]), (0, 0))
        self.assertEqual(report["versions"]["new"], "1.4")

    def test_zip_input_without_old(self) -> None:
        self.lived_in_vault()
        new = self.kit("new", self.NEW)
        zpath = self.vault.parent / f"{self.vault.name}-kit.zip"
        self.addCleanup(lambda: zpath.unlink() if zpath.exists() else None)
        with zipfile.ZipFile(zpath, "w") as z:
            z.writestr("ai-kickstart/START-HERE.html", "<p>not part of the vault</p>")
            for rel, text in self.NEW.items():
                z.writestr(f"ai-kickstart/vault/{rel}", text)
        from_zip = kit_update.load_kit(zpath)
        self.assertEqual(from_zip, kit_update.load_kit(new))
        actions = {r["path"]: r["action"] for r in kit_update.plan(self.vault, from_zip, None)}
        self.assertEqual(actions["_system/skills/a/SKILL.md"], "conflict", "without --old an untouched file can't be told apart")
        self.assertEqual(actions["_system/skills/c/SKILL.md"], "add")

    def test_max_refuses_and_writes_nothing(self) -> None:
        self.lived_in_vault()
        old, new = self.kit("old", self.OLD), self.kit("new", self.NEW)
        before = self.snapshot()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = kit_update.main(["--vault", str(self.vault), "--kit", str(new), "--old", str(old), "--apply", "--max", "1"])
        self.assertEqual(code, 2)
        self.assertEqual(self.snapshot(), before)


class TestCommandLine(unittest.TestCase):
    def test_every_tool_has_help_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "_system").mkdir()
            Path(tmp, "_system/index.md").write_text("# Index\n", encoding="utf-8")
            Path(tmp, "AGENTS.md").write_text("# Agents\n", encoding="utf-8")  # so kit_update accepts it as a kit
            for name in ("vault_lint", "secret_scan", "upcoming", "recent", "fix_frontmatter", "hub_index", "kit_update"):
                script = str(TOOLS / f"{name}.py")
                r = subprocess.run([sys.executable, script, "--help"], capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, f"{name} --help failed: {r.stderr}")
                extra = ["--kit", tmp] if name == "kit_update" else []
                r = subprocess.run([sys.executable, script, "--vault", tmp, "--json", *extra], capture_output=True, text=True, encoding="utf-8")
                self.assertIn(r.returncode, (0, 1), f"{name} --json failed: {r.stderr}")
                self.assertEqual(json.loads(r.stdout)["tool"], name)


if __name__ == "__main__":
    unittest.main()
