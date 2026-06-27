"""Tests for the CLI commands."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from lazyenv.__main__ import main

FIXTURES = Path(__file__).parent / "fixtures"


class TestCLI:
    def setup_method(self) -> None:
        self.runner = CliRunner()

    def test_version(self) -> None:
        result = self.runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_list(self) -> None:
        result = self.runner.invoke(main, ["--list", "-C", str(FIXTURES.parent)])
        assert result.exit_code == 0
        assert "Keys" in result.output

    def test_diff_identical(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("A=1\nB=2\n")
        result = self.runner.invoke(main, ["--diff", str(f), str(f)])
        assert result.exit_code == 0
        assert "in sync" in result.output.lower()

    def test_diff_different(self, tmp_path: Path) -> None:
        a = tmp_path / ".env.a"
        b = tmp_path / ".env.b"
        a.write_text("A=1\nB=2\n")
        b.write_text("A=1\n")
        result = self.runner.invoke(main, ["--diff", str(a), str(b)])
        assert result.exit_code == 1

    def test_validate_pass(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        example = tmp_path / ".env.example"
        env.write_text("A=1\nB=2\n")
        example.write_text("A=\nB=\n")
        result = self.runner.invoke(main, ["--validate", str(env), str(example)])
        assert result.exit_code == 0

    def test_validate_fail(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        example = tmp_path / ".env.example"
        env.write_text("A=1\n")
        example.write_text("A=\nMISSING_KEY=\n")
        result = self.runner.invoke(main, ["--validate", str(env), str(example)])
        assert result.exit_code == 1
        assert "MISSING_KEY" in result.output

    def test_init_creates_example(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        env.write_text("NAME=alice\nAPI_KEY=sk-secret\nPORT=3000\n")
        output = tmp_path / ".env.example"
        result = self.runner.invoke(main, ["init", str(env), "--output", str(output)])
        assert result.exit_code == 0
        assert output.exists()
        content = output.read_text()
        assert "NAME=alice" in content        # non-secret kept
        assert "API_KEY=\n" in content        # secret blanked
        assert "PORT=3000" in content         # non-secret kept

    def test_init_no_overwrite_by_default(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        env.write_text("A=1\n")
        output = tmp_path / ".env.example"
        output.write_text("existing content")
        result = self.runner.invoke(main, ["init", str(env), "--output", str(output)])
        assert result.exit_code == 1
        assert output.read_text() == "existing content"

    def test_init_force_overwrite(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        env.write_text("A=1\n")
        output = tmp_path / ".env.example"
        output.write_text("old content")
        result = self.runner.invoke(main, ["init", str(env), "--output", str(output), "--force"])
        assert result.exit_code == 0
        assert "old content" not in output.read_text()
