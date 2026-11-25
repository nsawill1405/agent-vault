# Line-by-line rules for TypeScript, JavaScript, C#, and Luau.
# Strings and comments are blanked first. These checks are approximate on purpose.

import re

from style_lint_common import MAX_CHAINED_CALLS, Finding



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
