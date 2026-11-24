import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_authorship


class CheckAuthorshipTest(unittest.TestCase):
    def test_allows_normal_commands_and_clean_commits(self):
        self.assertIsNone(check_authorship.inspect_command("git status"))
        self.assertIsNone(check_authorship.inspect_command("grep -rn Devin src/"))
        self.assertIsNone(check_authorship.inspect_command('git commit -m "Fix boat buoyancy damping"'))
        self.assertIsNone(
            check_authorship.inspect_command('git add .devin/skills && git commit -m "Sync exported skill files"')
        )

    def test_blocks_co_author_trailers_and_generated_footers(self):
        heredoc_commit = (
            "git commit -m \"$(cat <<'EOF'\n"
            "Fix boat steering\n\n"
            "Generated with [Devin](https://devin.ai)\n\n"
            "Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>\n"
            "EOF\n)\""
        )
        self.assertIsNotNone(check_authorship.inspect_command(heredoc_commit))

    def test_blocks_devin_mention_in_pr_title_or_body(self):
        pr_cmd = 'gh pr create --title "Devin: add memory skill" --body "Summary of changes"'
        self.assertIsNotNone(check_authorship.inspect_command(pr_cmd))

    def test_blocks_devin_mention_inside_body_file_but_allows_dot_devin_path(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            clean_body = base / "clean.md"
            clean_body.write_text("Updated `.devin/skills/unslop/SKILL.md` and ran tests.\n", encoding="utf-8")
            self.assertIsNone(
                check_authorship.inspect_command('gh pr create --title "Sync skills" --body-file clean.md', base)
            )

            bad_body = base / "bad.md"
            bad_body.write_text("Summary\n\nGenerated with [Devin](https://devin.ai)\n", encoding="utf-8")
            self.assertIsNotNone(
                check_authorship.inspect_command('gh pr create --title "Sync skills" --body-file bad.md', base)
            )


if __name__ == "__main__":
    unittest.main()
