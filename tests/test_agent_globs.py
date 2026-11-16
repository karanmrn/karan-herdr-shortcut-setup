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

    def test_noninteractive_shell_uses_live_path_and_nomatch(self):
        result = self.shell("printf '%s\\n' $PATH $options[nomatch]", {"CLAUDECODE": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"{self.home}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin\non\n")

    def install(self):
        return subprocess.run(
            ["/bin/bash", str(REPO / "install.sh")],
            env={"HOME": str(self.home), "PATH": "/usr/bin:/bin", "LC_ALL": "C"},
            cwd=self.home, capture_output=True, text=True, timeout=10,
        )

    def test_installer_backs_up_regular_zshenv_and_sets_path(self):
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
        result = self.shell("printf '%s\\n' $PATH")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"{self.home}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin\n")

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

    def test_installer_preserves_instruction_aliases_and_is_idempotent(self):
        aliases = [
            ".claude/CLAUDE.md", ".codex/AGENTS.md",
            ".config/opencode/AGENTS.md", ".grok/AGENTS.md",
        ]
        source = REPO / "home/.config/agents/AGENTS.md"
        for state in ["absent", "file", "directory", "valid", "dangling", "correct"]:
            with self.subTest(state=state), tempfile.TemporaryDirectory(dir=self.home) as scratch:
                home = Path(scratch)
                original = home / "previous-instructions.md"
                if state == "valid":
                    original.write_text("Existing instructions\n")
                for relative in aliases:
                    dest = home / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if state == "file":
                        dest.write_text("Existing instructions\n")
                    elif state == "directory":
                        dest.mkdir()
                        (dest / "instructions.md").write_text("Existing instructions\n")
                    elif state in ["valid", "dangling"]:
                        dest.symlink_to(original)
                    elif state == "correct":
                        dest.symlink_to(source)
                inodes = {}
                for _ in range(2):
                    result = subprocess.run(
                        ["/bin/bash", str(REPO / "install.sh")],
                        env={"HOME": str(home), "PATH": "/usr/bin:/bin", "LC_ALL": "C"},
                        cwd=home, capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    for relative in aliases:
                        dest = home / relative
                        self.assertTrue(dest.is_symlink())
                        self.assertEqual(dest.readlink(), source)
                        if relative in inodes:
                            self.assertEqual(dest.lstat().st_ino, inodes[relative])
                        inodes[relative] = dest.lstat().st_ino
                        backups = list(dest.parent.glob(dest.name + ".pre-dotfiles-*"))
                        self.assertEqual(len(backups), 0 if state in ["absent", "correct"] else 1)
                        if state in ["valid", "dangling"]:
                            self.assertTrue(backups[0].is_symlink())
                            self.assertEqual(backups[0].readlink(), original)
                            self.assertEqual(backups[0].exists(), state == "valid")
                        elif state == "file":
                            self.assertEqual(backups[0].read_text(), "Existing instructions\n")
                        elif state == "directory":
                            self.assertEqual(
                                (backups[0] / "instructions.md").read_text(),
                                "Existing instructions\n",
                            )
                    if state == "valid":
                        self.assertEqual(original.read_text(), "Existing instructions\n")

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

    def test_installer_links_published_claude_skills(self):
        for name in ["desktop-agent-workflows", "openrouter"]:
            with self.subTest(skill=name):
                dest = self.home / ".claude/skills" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.mkdir()
                (dest / "SKILL.md").write_text("Existing skill\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ["desktop-agent-workflows", "openrouter"]:
            with self.subTest(skill=name):
                dest = self.home / ".claude/skills" / name
                self.assertEqual(dest.readlink(), REPO / "home/.claude/skills" / name)
                self.assertTrue((dest / "SKILL.md").is_file())
                self.assertIn(f"ok     .claude/skills/{name}", result.stdout)
                backups = list(dest.parent.glob(name + ".pre-dotfiles-*"))
                self.assertEqual(len(backups), 1)
                self.assertEqual((backups[0] / "SKILL.md").read_text(), "Existing skill\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
