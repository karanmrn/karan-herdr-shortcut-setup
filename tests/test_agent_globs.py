"""Exercise native zsh startup and installation in disposable homes."""

from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class AgentGlobsTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="agent-globs-", dir=REPO)
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name)
        source = REPO / "home/.zshenv"
        if source.exists():
            (self.home / ".zshenv").symlink_to(source)

    def shell(self, command, markers=None, flags=()):
        env = {"HOME": str(self.home), "PATH": "/usr/bin:/bin", "LC_ALL": "C"}
        env.update(markers or {})
        return subprocess.run(
            ["/bin/zsh", "-d", *flags, "-c", command],
            env=env, cwd=self.home, capture_output=True, text=True, timeout=10,
        )

    def test_claude_unmatched_include_reaches_consumer(self):
        result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", {"CLAUDECODE": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "--include*.ts\n")
        self.assertEqual(result.stderr, "")

    def test_agent_markers_in_login_and_nonlogin_shells(self):
        for flags in [(), ("-l",)]:
            for markers in [
                {"CLAUDECODE": "1"},
                {"CODEX_THREAD_ID": "test-thread"},
                {"CLAUDECODE": "0", "CODEX_THREAD_ID": "test-thread"},
            ]:
                for argument in ["--include*.ts", "--include=*.ts", "missing*.tsx"]:
                    with self.subTest(flags=flags, markers=markers, argument=argument):
                        result = self.shell(
                            "/usr/bin/printf '%s\\n' " + argument, markers, flags,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stdout, argument + "\n")
                        self.assertEqual(result.stderr, "")

    def test_unmarked_and_false_markers_preserve_nomatch(self):
        for flags in [(), ("-l",)]:
            for markers in [
                {}, {"CLAUDECODE": ""}, {"CLAUDECODE": "0"},
                {"CLAUDECODE": "true"}, {"CLAUDECODE": "01"},
                {"CODEX_THREAD_ID": ""},
                {"CLAUDECODE": "0", "CODEX_THREAD_ID": ""},
                {"FM_HOME": "/fake", "FM_BACKEND": "codex", "FM_TASK_ID": "test"},
            ]:
                with self.subTest(flags=flags, markers=markers):
                    result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", markers, flags)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("no matches found: --include*.ts", result.stderr)

    def test_matching_patterns_still_expand(self):
        (self.home / "one.ts").touch()
        (self.home / "two.ts").touch()
        (self.home / "--include-one.ts").touch()
        for markers in [{}, {"CLAUDECODE": "1"}, {"CODEX_THREAD_ID": "test-thread"}]:
            for flags in [(), ("-l",)]:
                with self.subTest(markers=markers, flags=flags):
                    result = self.shell("/usr/bin/printf '%s\\n' *.ts", markers, flags)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, "--include-one.ts\none.ts\ntwo.ts\n")
                    result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", markers, flags)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, "--include-one.ts\n")

    def test_quoted_pattern_remains_literal(self):
        result = self.shell("/usr/bin/printf '%s\\n' '--include*.ts'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "--include*.ts\n")

    def test_missing_path_still_fails_in_consumer(self):
        result = self.shell("/bin/cat missing*.tsx", {"CLAUDECODE": "1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("missing*.tsx", result.stderr)
        self.assertIn("No such file or directory", result.stderr)
        self.assertNotIn("no matches found", result.stderr)

    def test_native_startup_order_and_interactive_human_options(self):
        for name in [".zprofile", ".zshrc", ".zlogin"]:
            (self.home / name).write_text("printf '%s\\n' " + name + " >> \"$HOME/trace\"\n")
        for flags, expected in [
            ((), []),
            (("-l",), [".zprofile", ".zlogin"]),
            (("-i",), [".zshrc"]),
            (("-l", "-i"), [".zprofile", ".zshrc", ".zlogin"]),
        ]:
            for markers, option in [({}, "on"), ({"CLAUDECODE": "0"}, "on"),
                                    ({"CLAUDECODE": "1"}, "off")]:
                with self.subTest(flags=flags, markers=markers):
                    trace = self.home / "trace"
                    trace.unlink(missing_ok=True)
                    result = self.shell("printf '%s\\n' $options[nomatch] $PATH", markers, flags)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, option + "\n/usr/bin:/bin\n")
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(trace.read_text().splitlines() if trace.exists() else [], expected)

    def test_zdotdir_and_no_rcs_follow_native_startup(self):
        alternate = self.home / "alternate"
        alternate.mkdir()
        result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", {
            "CLAUDECODE": "1", "ZDOTDIR": str(alternate),
        })
        self.assertEqual(result.returncode, 1)
        self.assertIn("no matches found", result.stderr)
        (alternate / ".zshenv").symlink_to(REPO / "home/.zshenv")
        result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", {
            "CLAUDECODE": "1", "ZDOTDIR": str(alternate),
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "--include*.ts\n")
        result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", {"CLAUDECODE": "1"}, ("-f",))
        self.assertEqual(result.returncode, 1)
        self.assertIn("no matches found", result.stderr)

    def install(self):
        return subprocess.run(
            ["/bin/bash", str(REPO / "install.sh")],
            env={"HOME": str(self.home), "PATH": "/usr/bin:/bin", "LC_ALL": "C"},
            cwd=self.home, capture_output=True, text=True, timeout=10,
        )

    def test_installer_backs_up_regular_zshenv_and_activates_gate(self):
        dest = self.home / ".zshenv"
        dest.unlink(missing_ok=True)
        dest.write_text("# Existing user configuration\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(dest.is_symlink(), result.stdout)
        self.assertEqual(dest.readlink(), REPO / "home/.zshenv")
        backups = list(self.home.glob(".zshenv.pre-dotfiles-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "# Existing user configuration\n")
        result = self.shell("/usr/bin/printf '%s\\n' --include*.ts", {"CLAUDECODE": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "--include*.ts\n")

    def test_installer_preserves_valid_and_dangling_links(self):
        dest = self.home / ".zshenv"
        for name, exists in [("existing.zshenv", True), ("missing.zshenv", False)]:
            with self.subTest(destination=name):
                dest.unlink(missing_ok=True)
                original = self.home / name
                if exists:
                    original.write_text("# Existing link target\n")
                dest.symlink_to(name)
                result = self.install()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(dest.readlink(), REPO / "home/.zshenv")
                backups = list(self.home.glob(".zshenv.pre-dotfiles-*"))
                self.assertEqual(len(backups), 1)
                self.assertTrue(backups[0].is_symlink())
                self.assertEqual(backups[0].readlink(), Path(name))
                self.assertEqual(backups[0].exists(), exists)
                if exists:
                    self.assertEqual(original.read_text(), "# Existing link target\n")
                backups[0].unlink()

    def test_installer_links_absent_destination_and_is_idempotent(self):
        dest = self.home / ".zshenv"
        dest.unlink(missing_ok=True)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(dest.readlink(), REPO / "home/.zshenv")
        inode = dest.lstat().st_ino
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok     .zshenv", result.stdout)
        self.assertEqual(dest.lstat().st_ino, inode)
        self.assertEqual(list(self.home.glob(".zshenv.pre-dotfiles-*")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
