"""Tests for pixeltable-new scaffolding."""

from __future__ import annotations

import pathlib

import pytest
from typer.testing import CliRunner

from pixeltable_new.cli import app
from pixeltable_new.new import PATTERNS, scaffold

runner = CliRunner()


EXPECTED_FILES: dict[str, list[str]] = {
    "serving": ["schema.py", "pyproject.toml"],
    "backend": ["main.py", "setup_pixeltable.py", "pyproject.toml", "config.py"],
    "batch": ["pipeline.py", "schema.py", "pyproject.toml"],
}


class TestScaffoldFunction:
    """Test the scaffold() function directly."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_scaffold_pattern(self, pattern: str, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        dest, written = scaffold(f"test-{pattern}", pattern)
        assert dest.exists()
        assert len(written) > 0
        for expected_file in EXPECTED_FILES[pattern]:
            assert (dest / expected_file).exists(), f"{expected_file} missing for pattern {pattern}"

    def test_scaffold_rejects_existing_dir(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        (tmp_path / "existing").mkdir()
        with pytest.raises(FileExistsError, match="already exists"):
            scaffold("existing", "serving")

    def test_scaffold_rejects_unknown_pattern(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        with pytest.raises(ValueError, match="Unknown pattern"):
            scaffold("badpattern", "nonexistent")


class TestCLI:
    """Test the CLI via typer's CliRunner."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_cli_scaffold(self, pattern: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["myapp", f"--{pattern}"])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "myapp").exists()
        for expected_file in EXPECTED_FILES[pattern]:
            assert (tmp_path / "myapp" / expected_file).exists(), f"{expected_file} missing in CLI output"

    def test_cli_default_pattern_is_serving(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["defaultapp"])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "defaultapp" / "schema.py").exists()

    def test_cli_existing_dir_fails(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "taken").mkdir()
        result = runner.invoke(app, ["taken"])
        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_cli_multiple_patterns_fails(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["multi", "--serving", "--backend"])
        assert result.exit_code == 1
        assert "Only one pattern" in result.output

    def test_cli_no_deploy_dirs(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """deploy/ directories should be excluded from scaffolded output."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["nodeploy", "--batch"])
        assert result.exit_code == 0, result.output
        assert not (tmp_path / "nodeploy" / "deploy").exists()

    def test_cli_help(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "starter kit" in result.output.lower() or "pixeltable" in result.output.lower()
