import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sync_skills

SAMPLE_SKILL = (
    "---\n"
    "name: sample-skill\n"
    "description: Run sample checks on changed files.\n"
    "type: skill\n"
    "tags:\n"
    "  - skill\n"
    "---\n\n"
    "# Sample skill\n\n"
    "Follow [[Coding Principles]].\n"
)


class SyncSkillsTest(unittest.TestCase):
    def test_exports_repo_and_global_skills_and_passes_check(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            vault = root / "vault"
            global_dir = root / "global-skills"
            skills_folder = vault / "Skills"
            skills_folder.mkdir(parents=True)
            (skills_folder / "Sample.md").write_text(SAMPLE_SKILL, encoding="utf-8")

            # Seed a stale folder inside repo .devin/skills to verify pruning,
            # and a third-party folder in global-skills to verify global installs do not delete user skills.
            stale_repo = vault / ".devin" / "skills" / "old-skill"
            stale_repo.mkdir(parents=True)
            (stale_repo / "SKILL.md").write_text("old", encoding="utf-8")

            other_global = global_dir / "third-party"
            other_global.mkdir(parents=True)
            (other_global / "SKILL.md").write_text("keep", encoding="utf-8")

            exported = sync_skills.sync_skills(vault, install_global=True, global_dir=global_dir)
            self.assertEqual(exported, ["sample-skill"])
            self.assertFalse(stale_repo.exists())
            self.assertTrue((other_global / "SKILL.md").is_file())
            self.assertTrue((global_dir / "sample-skill" / "SKILL.md").is_file())

            expected = sync_skills.collect_expected_skills(vault)
            problems = sync_skills.check_target_dir(vault / ".devin" / "skills", expected)
            self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
