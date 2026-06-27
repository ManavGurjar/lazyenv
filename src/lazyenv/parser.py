"""Robust .env file parser with support for all common formats."""

from __future__ import annotations

import re
from pathlib import Path

from lazyenv.models import EnvEntry, EnvFile

# Regex patterns
_KEY_VALUE_RE = re.compile(
    r"""
    ^
    (?P<key>[A-Za-z_][A-Za-z0-9_]*)   # key: identifier
    \s*=\s*                             # separator
    (?P<value>.*)                       # value: anything
    $
    """,
    re.VERBOSE,
)

_QUOTED_VALUE_RE = re.compile(
    r"""
    ^
    (?P<q>['"])             # opening quote
    (?P<inner>.*?)          # non-greedy contents
    (?P=q)                  # matching closing quote
    (?:\s*\#.*)?            # optional inline comment
    $
    """,
    re.VERBOSE | re.DOTALL,
)

# Keys that likely contain secrets (masked by default)
_SECRET_PATTERNS = re.compile(
    r"""
    (password|passwd|pwd|secret|token|key|api_key|apikey|
     credential|cert|private|auth|access|bearer|signing|
     encryption|aes|rsa|hmac|jwt|oauth|session)
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _strip_inline_comment(value: str) -> str:
    """Remove unquoted inline # comments from an unquoted value."""
    result = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "\\" and i + 1 < len(value):
            result.append(value[i + 1])
            i += 2
            continue
        if ch == "#":
            break
        result.append(ch)
        i += 1
    return "".join(result).rstrip()


def _parse_value(raw: str) -> tuple[str, str]:
    """Return (resolved_value, comment)."""
    raw = raw.strip()
    if not raw:
        return "", ""

    # Quoted value
    m = _QUOTED_VALUE_RE.match(raw)
    if m:
        return m.group("inner"), ""

    # Unquoted — strip inline comment
    value = _strip_inline_comment(raw)
    return value, ""


def _is_secret(key: str) -> bool:
    return bool(_SECRET_PATTERNS.search(key))


def parse_file(path: Path) -> EnvFile:
    """Parse a .env file at *path* and return an EnvFile."""
    env_file = EnvFile(path=path)

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        env_file.parse_errors.append(str(exc))
        return env_file

    lines = text.splitlines()

    # Handle multiline values (backslash continuation is rare but real)
    joined: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        start = i + 1
        while line.endswith("\\") and i + 1 < len(lines):
            i += 1
            line = line[:-1] + lines[i]
        joined.append((start, line))
        i += 1

    for lineno, line in joined:
        raw = line

        # Blank line
        if not line.strip():
            env_file.entries.append(
                EnvEntry(
                    key="",
                    value="",
                    raw_line=raw,
                    line_number=lineno,
                    is_blank=True,
                )
            )
            continue

        # Comment line
        if line.lstrip().startswith("#"):
            env_file.entries.append(
                EnvEntry(
                    key="",
                    value="",
                    raw_line=raw,
                    line_number=lineno,
                    comment=line.lstrip()[1:].strip(),
                    is_comment_line=True,
                )
            )
            continue

        # export prefix (bash convention)
        stripped = line.lstrip()
        stripped = stripped[7:].lstrip() if stripped.startswith("export ") else stripped

        m = _KEY_VALUE_RE.match(stripped)
        if m:
            key = m.group("key")
            value, comment = _parse_value(m.group("value"))
            env_file.entries.append(
                EnvEntry(
                    key=key,
                    value=value,
                    raw_line=raw,
                    line_number=lineno,
                    comment=comment,
                    masked=_is_secret(key),
                )
            )
        else:
            # Unrecognised line — record as a parse error but don't drop it
            env_file.parse_errors.append(
                f"Line {lineno}: unrecognised syntax: {line!r}"
            )

    return env_file


def parse_directory(root: Path, max_depth: int = 4) -> list[EnvFile]:
    """Walk *root* up to *max_depth* levels and return all parseable .env files."""
    files: list[EnvFile] = []
    _walk(root, root, 0, max_depth, files)
    return sorted(files, key=lambda f: f.path)


_ENV_NAME_RE = re.compile(
    r"""
    ^\.env
    (   # optional suffix variants
        $
        | \.[a-z0-9_.-]+$      # .env.local, .env.production, etc.
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

_SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__",
    ".venv", "venv", ".tox", "dist", "build", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", ".next", ".nuxt",
}


def _walk(root: Path, current: Path, depth: int, max_depth: int, out: list[EnvFile]) -> None:
    if depth > max_depth:
        return
    try:
        entries = list(current.iterdir())
    except PermissionError:
        return
    for entry in entries:
        if entry.is_dir():
            if entry.name not in _SKIP_DIRS:
                _walk(root, entry, depth + 1, max_depth, out)
        elif entry.is_file() and _ENV_NAME_RE.match(entry.name):
            out.append(parse_file(entry))
