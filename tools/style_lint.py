#!/usr/bin/env python3
# Flags code that is hard to explain or debug. The rules come from William/Coding Principles.md.
# Usage: python3 tools/style_lint.py <file or folder> [more files or folders]
#
# Python files are checked with the ast module, so those results are exact.
# TypeScript, JavaScript, C#, and Luau are checked line by line with regular expressions
# after strings and comments are blanked out. Those checks are approximate on purpose:
# they catch the common cases and stay simple enough to read.
#
# To silence one line, add a comment containing "style-lint: ignore" and say why.

import ast
import re
import sys
from pathlib import Path

MAX_LINE_LENGTH = 120
MAX_CHAINED_CALLS = 3
MAX_BOOLEAN_OPERANDS = 4
IGNORE_MARKER = "style-lint: ignore"

PYTHON_SUFFIXES = {".py"}
C_STYLE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".cs"}
LUAU_SUFFIXES = {".lua", ".luau"}

SKIPPED_FOLDERS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "out",
    "Library",
    "Packages",
    "__pycache__",
    ".venv",
    "venv",
    "vendor",
}


class Finding:
    def __init__(self, path, line, rule, message):
        self.path = path
        self.line = line
        self.rule = rule
        self.message = message

    def __str__(self):
        return str(self.path) + ":" + str(self.line) + ": " + self.rule + " " + self.message


# ---------------------------------------------------------------- Python


def contains_node_type(node, node_types):
    for child in ast.walk(node):
        if child is node:
            continue
        if isinstance(child, node_types):
            return True
    return False


def count_boolean_operands(node):
    # "a and (b or c)" has three operands.
    if not isinstance(node, ast.BoolOp):
        return 1
    total = 0
    for value in node.values:
        total = total + count_boolean_operands(value)
    return total


def count_chained_calls(node):
    # a.b().c().d() is a chain of three calls.
    count = 0
    current = node
    while isinstance(current, ast.Call) and isinstance(current.func, ast.Attribute):
        count = count + 1
        current = current.func.value
    return count


def is_swallowed_exception(handler):
    if handler.type is None:
        return True
    if len(handler.body) != 1:
        return False
    only_statement = handler.body[0]
    if isinstance(only_statement, ast.Pass):
        return True
    is_ellipsis = (
        isinstance(only_statement, ast.Expr)
        and isinstance(only_statement.value, ast.Constant)
        and only_statement.value.value is Ellipsis
    )
    return is_ellipsis


def lint_python_source(path, source):
    findings = []
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        findings.append(Finding(path, error.lineno or 1, "syntax-error", "could not parse file"))
        return findings

    comprehension_types = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
    reported_boolean_lines = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.IfExp) and contains_node_type(node, ast.IfExp):
            findings.append(Finding(
                path, node.lineno, "nested-ternary",
                "conditional expression inside another one; use if/else statements",
            ))

        if isinstance(node, comprehension_types):
            if len(node.generators) > 1 or contains_node_type(node, comprehension_types):
                findings.append(Finding(
                    path, node.lineno, "nested-comprehension",
                    "comprehension with more than one loop; use a for loop",
                ))
            if contains_node_type(node, ast.Lambda):
                findings.append(Finding(
                    path, node.lineno, "lambda-in-comprehension",
                    "lambda inside a comprehension; use a named function and a loop",
                ))

        if isinstance(node, ast.BoolOp) and node.lineno not in reported_boolean_lines:
            operand_count = count_boolean_operands(node)
            if operand_count > MAX_BOOLEAN_OPERANDS:
                reported_boolean_lines.add(node.lineno)
                findings.append(Finding(
                    path, node.lineno, "long-boolean",
                    str(operand_count) + " conditions in one expression; name the parts",
                ))

        if isinstance(node, ast.Call):
            chain_length = count_chained_calls(node)
            if chain_length > MAX_CHAINED_CALLS:
                findings.append(Finding(
                    path, node.lineno, "long-chain",
                    str(chain_length) + " chained calls; store intermediate results in named variables",
                ))

        if isinstance(node, ast.ExceptHandler) and is_swallowed_exception(node):
            findings.append(Finding(
                path, node.lineno, "swallowed-error",
                "bare except or empty handler hides failures; handle or re-raise",
            ))

    return remove_duplicate_chain_findings(findings)


def remove_duplicate_chain_findings(findings):
    # A chain of five calls contains a chain of four. Report each line once per rule.
    seen = set()
    unique = []
    for finding in findings:
        key = (finding.line, finding.rule)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    return unique


# ---------------------------------------------------------------- Other languages


def blank_strings_and_comments(line, comment_prefix):
    # Replaces string contents with spaces and drops trailing comments so that
    # punctuation inside strings does not trigger rules. Template literals and
    # multi-line strings are not tracked across lines.
    result = []
    quote = None
    index = 0
    while index < len(line):
        character = line[index]
        if quote is not None:
            if character == "\\":
                result.append("  ")
                index = index + 2
                continue
            if character == quote:
                quote = None
                result.append(character)
            else:
                result.append(" ")
            index = index + 1
            continue

        if line.startswith(comment_prefix, index):
            break
        if character in "\"'`":
            quote = character
        result.append(character)
        index = index + 1
    return "".join(result)


def count_ternary_question_marks(code):
    # Removes syntax that uses "?" without being a ternary before counting:
    #   a?.b          optional chaining
    #   a ?? b        null coalescing
    #   name?: T      optional parameter or property
    #   int? count =  C# nullable type
    without_optional_chaining = code.replace("?.", "  ").replace("??", "  ")
    without_optional_params = re.sub(r"\w\?\s*[:),;=>\]]", "  ", without_optional_chaining)
    without_nullable_types = re.sub(r"\w\?(?=\s+\w+\s*[=;,)])", "  ", without_optional_params)
    return without_nullable_types.count("?")


def count_luau_if_expressions(code):
    stripped = code.strip()
    if_count = len(re.findall(r"\bif\b", stripped))
    starts_with_statement = stripped.startswith("if ") or stripped.startswith("elseif ")
    if starts_with_statement:
        if_count = if_count - 1
    return if_count


def count_chained_calls_in_line(code):
    # Counts ").name(" and "):name(" which is how a call chain looks on one line.
    return len(re.findall(r"\)\s*[.:]\s*\w+\s*\(", code)) + 1


def lint_text_source(path, source, comment_prefix, is_luau):
    findings = []
    lines = source.split("\n")
    for line_number, line in enumerate(lines, start=1):
        code = blank_strings_and_comments(line, comment_prefix)

        if is_luau:
            if count_luau_if_expressions(code) > 1:
                findings.append(Finding(
                    path, line_number, "nested-ternary",
                    "more than one if-expression on a line; use if statements",
                ))
            if code.strip().startswith("pcall("):
                findings.append(Finding(
                    path, line_number, "swallowed-error",
                    "pcall result ignored; check the success value",
                ))
        else:
            if count_ternary_question_marks(code) > 1 and ":" in code:
                findings.append(Finding(
                    path, line_number, "nested-ternary",
                    "more than one ternary on a line; use if/else",
                ))

        chain_length = count_chained_calls_in_line(code)
        if chain_length > MAX_CHAINED_CALLS:
            findings.append(Finding(
                path, line_number, "long-chain",
                str(chain_length) + " chained calls on one line; split into named steps",
            ))

    if not is_luau:
        for match in re.finditer(r"\bcatch\s*(\([^)]*\))?\s*\{\s*\}", source):
            line_number = source.count("\n", 0, match.start()) + 1
            findings.append(Finding(
                path, line_number, "swallowed-error",
                "empty catch block hides failures; handle, log, or rethrow",
            ))

    return findings


# ---------------------------------------------------------------- Shared


def lint_line_lengths(path, source, comment_prefix):
    # Comment-only lines are skipped. Long prose comments are not hard to debug.
    findings = []
    for line_number, line in enumerate(source.split("\n"), start=1):
        if line.strip().startswith(comment_prefix):
            continue
        if len(line) > MAX_LINE_LENGTH:
            findings.append(Finding(
                path, line_number, "line-too-long",
                str(len(line)) + " characters; limit is " + str(MAX_LINE_LENGTH),
            ))
    return findings


def remove_ignored(findings, source):
    lines = source.split("\n")
    kept = []
    for finding in findings:
        line_text = lines[finding.line - 1] if finding.line - 1 < len(lines) else ""
        if IGNORE_MARKER in line_text:
            continue
        kept.append(finding)
    return kept


def lint_file(path):
    suffix = path.suffix.lower()
    source = path.read_text(encoding="utf-8", errors="replace")

    if suffix in PYTHON_SUFFIXES:
        comment_prefix = "#"
        findings = lint_python_source(path, source)
    elif suffix in C_STYLE_SUFFIXES:
        comment_prefix = "//"
        findings = lint_text_source(path, source, comment_prefix, False)
    elif suffix in LUAU_SUFFIXES:
        comment_prefix = "--"
        findings = lint_text_source(path, source, comment_prefix, True)
    else:
        return []

    findings = findings + lint_line_lengths(path, source, comment_prefix)
    findings = remove_ignored(findings, source)
    findings.sort(key=lambda finding: (finding.line, finding.rule))
    return findings


def is_supported(path):
    all_suffixes = PYTHON_SUFFIXES | C_STYLE_SUFFIXES | LUAU_SUFFIXES
    return path.suffix.lower() in all_suffixes


def collect_files(arguments):
    files = []
    for argument in arguments:
        path = Path(argument)
        if path.is_file():
            files.append(path)
            continue
        for candidate in sorted(path.rglob("*")):
            if not candidate.is_file():
                continue
            if any(part in SKIPPED_FOLDERS for part in candidate.parts):
                continue
            if is_supported(candidate):
                files.append(candidate)
    return files


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 tools/style_lint.py <file or folder> [...]")

    all_findings = []
    for path in collect_files(sys.argv[1:]):
        all_findings.extend(lint_file(path))

    for finding in all_findings:
        print(finding)

    if len(all_findings) > 0:
        print(str(len(all_findings)) + " style finding(s). See Skills/Style Linter.md.")
        sys.exit(1)


if __name__ == "__main__":
    main()
