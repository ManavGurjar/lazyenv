"""Tests for the .env parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from lazyenv.parser import parse_file, parse_directory
from lazyenv.models import EnvFile


FIXTURES = Path(__file__).parent / "fixtures"


class TestParseFile:
    def test_parses_key_value(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("FOO=bar\nBAZ=qux\n")
        env = parse_file(f)
        assert env.as_dict == {"FOO": "bar", "BAZ": "qux"}

    def test_strips_inline_comment(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("KEY=value # inline comment\n")
        env = parse_file(f)
        assert env.as_dict["KEY"] == "value"

    def test_quoted_double(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text('KEY="hello world"\n')
        env = parse_file(f)
        assert env.as_dict["KEY"] == "hello world"

    def test_quoted_single(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("KEY='hello world'\n")
        env = parse_file(f)
        assert env.as_dict["KEY"] == "hello world"

    def test_empty_value(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("KEY=\n")
        env = parse_file(f)
        entry = env.get("KEY")
        assert entry is not None
        assert entry.value == ""
        assert entry.is_empty

    def test_comment_line_excluded_from_dict(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("# This is a comment\nKEY=value\n")
        env = parse_file(f)
        assert list(env.as_dict.keys()) == ["KEY"]

    def test_export_prefix(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("export DATABASE_URL=postgres://localhost/db\n")
        env = parse_file(f)
        assert "DATABASE_URL" in env.as_dict

    def test_secret_keys_masked(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("API_KEY=abc123\nNAME=not-a-secret\n")
        env = parse_file(f)
        key_entry = env.get("API_KEY")
        name_entry = env.get("NAME")
        assert key_entry is not None and key_entry.masked
        assert name_entry is not None and not name_entry.masked

    def test_missing_file(self, tmp_path: Path) -> None:
        env = parse_file(tmp_path / "nonexistent.env")
        assert len(env.parse_errors) > 0

    def test_fixture_example(self) -> None:
        env = parse_file(FIXTURES / ".env.example")
        assert "DATABASE_URL" in env.keys
        assert "STRIPE_SECRET_KEY" in env.keys
        assert len(env) > 5

    def test_fixture_test(self) -> None:
        env = parse_file(FIXTURES / ".env.test")
        assert env.as_dict["APP_ENV"] == "test"
        assert env.as_dict["DEBUG"] == "true"


class TestParseDirectory:
    def test_finds_env_files(self, tmp_path: Path) -> None:
        (tmp_path / ".env").write_text("A=1\n")
        (tmp_path / ".env.local").write_text("B=2\n")
        (tmp_path / ".env.example").write_text("A=\nB=\n")
        files = parse_directory(tmp_path)
        names = {f.name for f in files}
        assert ".env" in names
        assert ".env.local" in names
        assert ".env.example" in names

    def test_skips_node_modules(self, tmp_path: Path) -> None:
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / ".env").write_text("SECRET=bad\n")
        (tmp_path / ".env").write_text("A=1\n")
        files = parse_directory(tmp_path)
        paths = {f.path for f in files}
        assert nm / ".env" not in paths

    def test_finds_nested_files(self, tmp_path: Path) -> None:
        nested = tmp_path / "services" / "api"
        nested.mkdir(parents=True)
        (nested / ".env").write_text("PORT=8000\n")
        files = parse_directory(tmp_path)
        assert any("api" in str(f.path) for f in files)
