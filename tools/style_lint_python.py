# Python rules for the style linter, checked with the ast module so results are exact.

import ast

from style_lint_common import MAX_BOOLEAN_OPERANDS, MAX_CHAINED_CALLS, Finding



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
