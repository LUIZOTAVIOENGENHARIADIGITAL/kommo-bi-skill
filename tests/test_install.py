import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_both_complete_and_repeatable(self):
        targets = installer.destinations("both", self.root)
        installer.install(targets)
        installer.install(targets)
        for dest in targets:
            self.assertEqual(installer.inventory(dest), installer.inventory(installer.SOURCE))
        self.assertFalse(list(self.root.rglob("skill-backups")))

    def test_conflict_preflight_preserves_all_targets(self):
        targets = installer.destinations("both", self.root)
        targets[1].mkdir(parents=True)
        original = targets[1] / "SKILL.md"
        original.write_text("minha personalização")
        with self.assertRaises(ValueError):
            installer.install(targets)
        self.assertEqual(original.read_text(), "minha personalização")
        self.assertFalse(targets[0].exists())

    def test_update_preserves_custom_files_outside_skill_discovery(self):
        dest = installer.destinations("claude", self.root)[0]
        installer.install([dest])
        (dest / "custom.txt").write_text("preservar")
        installer.install([dest], update=True)
        backups = list((self.root / ".claude/skill-backups").glob("kommo-bi-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "custom.txt").read_text(), "preservar")
        self.assertFalse((dest / "custom.txt").exists())
        self.assertEqual(installer.inventory(dest), installer.inventory(installer.SOURCE))

    def test_dry_run_has_no_writes(self):
        installer.install(installer.destinations("both", self.root), dry_run=True)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_symlink_is_preserved(self):
        target = self.root / "original"
        target.mkdir()
        dest = self.root / "link"
        dest.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.install([dest], update=True)
        self.assertTrue(dest.is_symlink())

    def test_legacy_destination(self):
        dest = installer.destinations("codex", self.root, legacy=True)[0]
        installer.install([dest])
        self.assertTrue((self.root / ".codex/skills/kommo-bi/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
