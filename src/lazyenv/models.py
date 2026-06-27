"""Core data models for lazyenv."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class EntryStatus(Enum):
    """Status of an env entry relative to a reference file."""

    OK = "ok"
    MISSING = "missing"       # present in reference, absent here
    EXTRA = "extra"           # present here, absent in reference
    EMPTY = "empty"           # key exists but value is blank
    CHANGED = "changed"       # value differs from reference


@dataclass
class EnvEntry:
    """A single key=value line in an .env file."""

    key: str
    value: str
    raw_line: str
    line_number: int
    comment: str = ""
    is_comment_line: bool = False
    is_blank: bool = False
    masked: bool = False

    @property
    def display_value(self) -> str:
        if self.masked:
            return "•" * min(len(self.value), 12) if self.value else ""
        return self.value

    @property
    def is_empty(self) -> bool:
        return not self.value.strip()


@dataclass
class EnvFile:
    """A parsed .env file."""

    path: Path
    entries: list[EnvEntry] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def keys(self) -> set[str]:
        return {e.key for e in self.entries if not e.is_comment_line and not e.is_blank}

    @property
    def as_dict(self) -> dict[str, str]:
        return {e.key: e.value for e in self.entries if not e.is_comment_line and not e.is_blank}

    def get(self, key: str) -> EnvEntry | None:
        for entry in self.entries:
            if entry.key == key:
                return entry
        return None

    def __len__(self) -> int:
        return sum(1 for e in self.entries if not e.is_comment_line and not e.is_blank)


@dataclass
class DiffEntry:
    """A single row in a side-by-side diff."""

    key: str
    left_entry: EnvEntry | None
    right_entry: EnvEntry | None
    status: EntryStatus

    @property
    def left_value(self) -> str:
        return self.left_entry.value if self.left_entry else ""

    @property
    def right_value(self) -> str:
        return self.right_entry.value if self.right_entry else ""


@dataclass
class EnvDiff:
    """Result of diffing two .env files."""

    left: EnvFile
    right: EnvFile
    entries: list[DiffEntry] = field(default_factory=list)

    @property
    def missing_count(self) -> int:
        return sum(1 for e in self.entries if e.status == EntryStatus.MISSING)

    @property
    def extra_count(self) -> int:
        return sum(1 for e in self.entries if e.status == EntryStatus.EXTRA)

    @property
    def changed_count(self) -> int:
        return sum(1 for e in self.entries if e.status == EntryStatus.CHANGED)

    @property
    def ok_count(self) -> int:
        return sum(1 for e in self.entries if e.status == EntryStatus.OK)

    @property
    def has_issues(self) -> bool:
        return self.missing_count > 0 or self.extra_count > 0 or self.changed_count > 0


@dataclass
class ProjectEnvFiles:
    """All .env files discovered within a project directory."""

    root: Path
    files: list[EnvFile] = field(default_factory=list)

    @property
    def example_files(self) -> list[EnvFile]:
        return [f for f in self.files if "example" in f.name or "sample" in f.name]

    @property
    def env_files(self) -> list[EnvFile]:
        return [f for f in self.files if f not in self.example_files]
