import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import vault_lint

GOOD_HEADER = "---\ntype: note\ntags:\n  - test\n---\n\n"


def write(folder, relative, text):
    path = Path(folder) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rules_for(folder):
    rules = []
    for finding in vault_lint.lint_vault(Path(folder)):
        rules.append(finding.rule)
    return rules


class VaultLintTest(unittest.TestCase):
    def test_clean_vault(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.md", GOOD_HEADER + "See [[B]] and [[B#Part|label]] and [[Sub/B]].\n")
            write(folder, "Sub/B.md", GOOD_HEADER + "# B\n")
            write(folder, "README.md", "# No frontmatter needed\n")
            self.assertEqual(rules_for(folder), [])

    def test_missing_frontmatter_and_keys(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.md", "# No header\n")
            write(folder, "B.md", "---\ntype: note\n---\n")
            self.assertEqual(rules_for(folder), ["frontmatter", "frontmatter"])

    def test_broken_link(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.md", GOOD_HEADER + "See [[Missing]].\n")
            self.assertEqual(rules_for(folder), ["broken-link"])

    def test_links_inside_code_are_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.md", GOOD_HEADER + "`[[Missing]]`\n\n```\n[[Also missing]]\n```\n")
            self.assertEqual(rules_for(folder), [])

    def test_trashed_notes_do_not_count_as_link_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "A.md", GOOD_HEADER + "See [[Gone]].\n")
            write(folder, ".trash/Gone.md", GOOD_HEADER)
            self.assertEqual(rules_for(folder), ["broken-link"])

    def test_duplicate_names(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "One/Same.md", GOOD_HEADER)
            write(folder, "Two/Same.md", GOOD_HEADER)
            self.assertEqual(rules_for(folder), ["duplicate-name"])

    def test_prose_rules_only_apply_to_hand_written_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            write(folder, "William/Me.md", GOOD_HEADER + "We leverage tools \u2014 always.\n")
            write(folder, "Knowledge Graph/Imported.md", GOOD_HEADER + "We leverage tools \u2014 always.\n")
            self.assertEqual(rules_for(folder), ["prose", "prose"])


if __name__ == "__main__":
    unittest.main()
