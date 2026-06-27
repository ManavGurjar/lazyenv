"""Diff engine: compare two EnvFile objects and produce DiffEntry results."""

from __future__ import annotations

from lazyenv.models import DiffEntry, EntryStatus, EnvDiff, EnvEntry, EnvFile


def diff_files(left: EnvFile, right: EnvFile) -> EnvDiff:
    """Produce a side-by-side diff between *left* and *right*."""
    result = EnvDiff(left=left, right=right)

    left_keys = {e.key: e for e in left.entries if e.key and not e.is_comment_line}
    right_keys = {e.key: e for e in right.entries if e.key and not e.is_comment_line}

    # Preserve order: left keys first, then right-only keys
    seen: set[str] = set()
    ordered_keys: list[str] = []
    for e in left.entries:
        if e.key and not e.is_comment_line and e.key not in seen:
            ordered_keys.append(e.key)
            seen.add(e.key)
    for e in right.entries:
        if e.key and not e.is_comment_line and e.key not in seen:
            ordered_keys.append(e.key)
            seen.add(e.key)

    for key in ordered_keys:
        le: EnvEntry | None = left_keys.get(key)
        re_: EnvEntry | None = right_keys.get(key)

        if le is not None and re_ is not None:
            status = EntryStatus.OK if le.value == re_.value else EntryStatus.CHANGED
        elif le is not None:
            status = EntryStatus.MISSING   # in left (reference), absent in right
        else:
            status = EntryStatus.EXTRA     # only in right

        result.entries.append(DiffEntry(key=key, left_entry=le, right_entry=re_, status=status))

    return result


def validate_against_example(env: EnvFile, example: EnvFile) -> EnvDiff:
    """Check *env* against *example* — returns diff where example is the reference (left)."""
    return diff_files(left=example, right=env)
