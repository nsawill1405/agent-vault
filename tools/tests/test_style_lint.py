import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import style_lint


def python_rules(source):
    findings = style_lint.lint_python_source(Path("example.py"), source)
    rules = []
    for finding in findings:
        rules.append(finding.rule)
    return rules


def text_rules(source, comment_prefix, is_luau):
    findings = style_lint.lint_text_source(Path("example"), source, comment_prefix, is_luau)
    rules = []
    for finding in findings:
        rules.append(finding.rule)
    return rules


class PythonRulesTest(unittest.TestCase):
    def test_simple_code_is_clean(self):
        source = (
            "active = []\n"
            "for player in players:\n"
            "    if player.alive:\n"
            "        active.append(player)\n"
            "label = 'yes' if ok else 'no'\n"
        )
        self.assertEqual(python_rules(source), [])

    def test_nested_ternary(self):
        self.assertIn("nested-ternary", python_rules("x = a if b else c if d else e\n"))

    def test_nested_comprehension(self):
        self.assertIn("nested-comprehension", python_rules("x = [a for row in rows for a in row]\n"))
        self.assertIn("nested-comprehension", python_rules("x = [[a for a in row] for row in rows]\n"))

    def test_single_comprehension_is_allowed(self):
        self.assertEqual(python_rules("x = [a.name for a in items]\n"), [])

    def test_lambda_in_comprehension(self):
        self.assertIn("lambda-in-comprehension", python_rules("x = [lambda: a for a in items]\n"))

    def test_long_boolean(self):
        self.assertIn("long-boolean", python_rules("x = a and b and (c or d or e)\n"))
        self.assertNotIn("long-boolean", python_rules("x = a and b and c and d\n"))

    def test_long_chain(self):
        rules = python_rules("x = s.strip().lower().split().pop()\n")
        self.assertEqual(rules.count("long-chain"), 1)
        self.assertNotIn("long-chain", python_rules("x = s.strip().lower().split()\n"))

    def test_swallowed_error(self):
        self.assertIn("swallowed-error", python_rules("try:\n    go()\nexcept ValueError:\n    pass\n"))
        self.assertIn("swallowed-error", python_rules("try:\n    go()\nexcept:\n    log()\n"))
        self.assertNotIn("swallowed-error", python_rules("try:\n    go()\nexcept ValueError:\n    log()\n"))

    def test_syntax_error_is_reported(self):
        self.assertEqual(python_rules("def broken(:\n"), ["syntax-error"])


class TextRulesTest(unittest.TestCase):
    def test_typescript_nested_ternary(self):
        self.assertIn("nested-ternary", text_rules("const x = a ? b : c ? d : e;\n", "//", False))

    def test_typescript_optional_syntax_is_not_a_ternary(self):
        source = "function f(a?: string, b?: number) { return a?.length ?? b ? 1 : 2; }\n"
        self.assertNotIn("nested-ternary", text_rules(source, "//", False))

    def test_csharp_nullable_type_is_not_a_ternary(self):
        source = "Quaternion? current = isRotation ? Convert(value) : null;\n"
        self.assertNotIn("nested-ternary", text_rules(source, "//", False))

    def test_question_marks_in_strings_are_ignored(self):
        self.assertEqual(text_rules("const x = ok ? 'why? how?' : 'no';\n", "//", False), [])

    def test_empty_catch(self):
        self.assertIn("swallowed-error", text_rules("try { go(); } catch (e) { }\n", "//", False))
        self.assertIn("swallowed-error", text_rules("try { go(); }\ncatch {\n}\n", "//", False))

    def test_long_chain_on_one_line(self):
        source = "const x = items.filter(a).map(b).sort(c).slice(d);\n"
        self.assertIn("long-chain", text_rules(source, "//", False))

    def test_luau_nested_if_expression(self):
        source = "local x = if a then 1 else if b then 2 else 3\n"
        self.assertIn("nested-ternary", text_rules(source, "--", True))

    def test_luau_if_statement_is_fine(self):
        source = "if a then\n\tlocal x = if b then 1 else 2\nend\n"
        self.assertEqual(text_rules(source, "--", True), [])

    def test_luau_ignored_pcall(self):
        self.assertIn("swallowed-error", text_rules("\tpcall(save)\n", "--", True))
        self.assertNotIn("swallowed-error", text_rules("local ok, err = pcall(save)\n", "--", True))


class LintFileTest(unittest.TestCase):
    def test_ignore_marker_and_line_length(self, tmp_name="sample.py"):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / tmp_name
            long_line = "x = '" + "a" * 130 + "'\n"
            ignored = "y = a if b else c if d else e  # style-lint: ignore test fixture\n"
            long_comment = "# " + "c" * 130 + "\n"
            path.write_text(long_line + ignored + long_comment)
            rules = []
            for finding in style_lint.lint_file(path):
                rules.append(finding.rule)
            self.assertEqual(rules, ["line-too-long"])

    def test_unknown_file_types_are_skipped(self):
        self.assertFalse(style_lint.is_supported(Path("notes.md")))
        self.assertTrue(style_lint.is_supported(Path("Main.luau")))


if __name__ == "__main__":
    unittest.main()
