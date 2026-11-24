import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import post_edit_check


class PostEditCheckTest(unittest.TestCase):
    def test_flags_nested_ternary_in_code_file(self):
        with tempfile.TemporaryDirectory() as folder:
            code_file = Path(folder) / "sample.py"
            code_file.write_text("x = 1 if a else 2 if b else 3\n", encoding="utf-8")
            findings = post_edit_check.check_edited_file(code_file)
            self.assertEqual(len(findings), 1)
            self.assertIn("nested-ternary", findings[0])

    def test_flags_ai_slop_in_project_readme(self):
        with tempfile.TemporaryDirectory() as folder:
            readme = Path(folder) / "README.md"
            readme.write_text("# Tool\n\nA robust tool \u2014 built for speed.\n", encoding="utf-8")
            findings = post_edit_check.check_edited_file(readme)
            self.assertEqual(len(findings), 2)

    def test_allows_clean_code_and_markdown(self):
        with tempfile.TemporaryDirectory() as folder:
            code_file = Path(folder) / "clean.py"
            code_file.write_text("value = 1\nif ready:\n    value = 2\n", encoding="utf-8")
            readme = Path(folder) / "README.md"
            readme.write_text("# Tool\n\nChecks files on save.\n", encoding="utf-8")
            self.assertEqual(post_edit_check.check_edited_file(code_file), [])
            self.assertEqual(post_edit_check.check_edited_file(readme), [])


if __name__ == "__main__":
    unittest.main()
