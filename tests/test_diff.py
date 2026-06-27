"""Tests for the diff engine."""

from __future__ import annotations

from pathlib import Path

from lazyenv.diff import diff_files, validate_against_example
from lazyenv.models import EntryStatus
from lazyenv.parser import parse_file

FIXTURES = Path(__file__).parent / "fixtures"


class TestDiffFiles:
    def _make_env(self, tmp_path: Path, name: str, content: str):
        f = tmp_path / name
        f.write_text(content)
        return parse_file(f)

    def test_identical_files(self, tmp_path: Path) -> None:
        content = "A=1\nB=2\n"
        left = self._make_env(tmp_path, ".env.a", content)
        right = self._make_env(tmp_path, ".env.b", content)
        diff = diff_files(left, right)
        assert not diff.has_issues
        assert diff.ok_count == 2

    def test_missing_key(self, tmp_path: Path) -> None:
        left = self._make_env(tmp_path, ".env.a", "A=1\nB=2\n")
        right = self._make_env(tmp_path, ".env.b", "A=1\n")
        diff = diff_files(left, right)
        assert diff.missing_count == 1
        missing = [e for e in diff.entries if e.status == EntryStatus.MISSING]
        assert missing[0].key == "B"

    def test_extra_key(self, tmp_path: Path) -> None:
        left = self._make_env(tmp_path, ".env.a", "A=1\n")
        right = self._make_env(tmp_path, ".env.b", "A=1\nC=3\n")
        diff = diff_files(left, right)
        assert diff.extra_count == 1

    def test_changed_value(self, tmp_path: Path) -> None:
        left = self._make_env(tmp_path, ".env.a", "A=original\n")
        right = self._make_env(tmp_path, ".env.b", "A=modified\n")
        diff = diff_files(left, right)
        assert diff.changed_count == 1
        assert diff.entries[0].status == EntryStatus.CHANGED

    def test_fixture_validation(self) -> None:
        env = parse_file(FIXTURES / ".env.test")
        example = parse_file(FIXTURES / ".env.example")
        diff = validate_against_example(env, example)
        # SENDGRID_API_KEY is in example but not in .env.test → missing
        missing_keys = {e.key for e in diff.entries if e.status == EntryStatus.MISSING}
        assert "SENDGRID_API_KEY" in missing_keys or "ALLOWED_HOSTS" in missing_keys
        # EXTRA_KEY is in .env.test but not in example → extra
        extra_keys = {e.key for e in diff.entries if e.status == EntryStatus.EXTRA}
        assert "EXTRA_KEY" in extra_keys
