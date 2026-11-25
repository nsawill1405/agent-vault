#!/usr/bin/env python3
# Flags code that is hard to explain or debug. The rules come from William/Coding Principles.md.
# Usage: python3 tools/style_lint.py <file or folder> [more files or folders]
#
# Python files are checked with the ast module, so those results are exact.
# TypeScript, JavaScript, C#, and Luau are checked line by line with regular expressions
# after strings and comments are blanked out. Those checks are approximate on purpose:
# they catch the common cases and stay simple enough to read.
#
# The rules live in style_lint_python.py and style_lint_text.py. Copy all four
# style_lint*.py files together when using the linter in another repo.
#
# To silence one line, add a comment containing "style-lint: ignore" and say why.

import sys
from pathlib import Path

from style_lint_common import (
    C_STYLE_SUFFIXES,
    IGNORE_MARKER,
    LUAU_SUFFIXES,
    MAX_FILE_LINES,
    MAX_LINE_LENGTH,
    PYTHON_SUFFIXES,
    SKIPPED_FOLDERS,
    Finding,
)
from style_lint_python import lint_python_source
from style_lint_text import lint_text_source


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


def lint_file_length(path, source):
    line_count = len(source.splitlines())
    if line_count <= MAX_FILE_LINES:
        return []
    message = str(line_count) + " lines; limit is " + str(MAX_FILE_LINES) + ". Split it into modules with one job each"
    return [Finding(path, 1, "long-file", message)]


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
    findings = findings + lint_file_length(path, source)
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
