# Shared settings and the Finding type for the style linter. See style_lint.py.

MAX_LINE_LENGTH = 120
MAX_FILE_LINES = 300
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
