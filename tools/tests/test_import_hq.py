import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import import_hq


def make_lookup():
    note = import_hq.Note(Path("x.mdx"), "decision", "agentic-code-review:001-stateful-ai-code-review", "")
    note.name = "ADR 001 - Stateful review"
    return import_hq.build_lookup([note])


class RepoLinkTest(unittest.TestCase):
    def test_content_path_to_site_url(self):
        self.assertEqual(
            import_hq.content_path_to_site_url("ui/content/projects/p/adrs/001-x.mdx"),
            "/projects/p/adrs/001-x",
        )
        self.assertEqual(import_hq.content_path_to_site_url("ui/content/projects/p/index.mdx"), "/projects/p")
        self.assertIsNone(import_hq.content_path_to_site_url("docs/readme.md"))

    def test_relative_link_to_imported_record_becomes_wikilink(self):
        text = "[ADR 001](../ui/content/projects/agentic-code-review/adrs/001-stateful-ai-code-review.mdx)"
        result = import_hq.rewrite_repo_links(make_lookup(), text, "ai-review/README.md")
        self.assertEqual(result, "[[ADR 001 - Stateful review|ADR 001]]")

    def test_site_link_to_imported_record_becomes_wikilink(self):
        text = "[ADR 001](/projects/agentic-code-review/adrs/001-stateful-ai-code-review)"
        result = import_hq.rewrite_repo_links(make_lookup(), text, "ai-review/README.md")
        self.assertEqual(result, "[[ADR 001 - Stateful review|ADR 001]]")

    def test_other_relative_links_point_at_github(self):
        text = "[UI CD](../../.github/workflows/ui-cd.yml)"
        result = import_hq.rewrite_repo_links(make_lookup(), text, "docs/runbooks/delivery.md")
        self.assertEqual(result, "[UI CD](" + import_hq.HQ_GITHUB + ".github/workflows/ui-cd.yml)")

    def test_external_links_are_unchanged(self):
        text = "[site](https://example.com) and [here](#section)"
        self.assertEqual(import_hq.rewrite_repo_links(make_lookup(), text, "docs/a.md"), text)


if __name__ == "__main__":
    unittest.main()
