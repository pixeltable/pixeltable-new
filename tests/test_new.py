"""Tests for pixeltable-new scaffolding."""

from __future__ import annotations

import io
import json
import pathlib
import tarfile

import pytest
from typer.testing import CliRunner

from pixeltable_new.cli import app
from pixeltable_new.new import (
    PATTERNS,
    TEMPLATE_ALIASES,
    TEMPLATES,
    resolve_template,
    scaffold,
    substitute_project_name,
)

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
        dest, written, _legacy = scaffold(f"test-{pattern}", pattern)
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

    @pytest.mark.parametrize("template", TEMPLATES)
    def test_scaffold_template(self, template: str, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        dest, written, _legacy = scaffold(f"test-{template}", "serving", template=template)
        assert dest.exists()
        assert len(written) > 0
        assert (dest / "schema.py").exists(), f"schema.py missing for template {template}"
        assert (dest / "pyproject.toml").exists(), f"pyproject.toml missing for template {template}"

    def test_scaffold_rejects_unknown_template(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        with pytest.raises(ValueError, match="Unknown template"):
            scaffold("badtemplate", "serving", template="nonexistent")

    def test_scaffold_legacy_alias(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        for alias, canonical in TEMPLATE_ALIASES.items():
            dest, written, legacy = scaffold(f"test-{alias}", "serving", template=alias)
            assert dest.exists()
            assert len(written) > 0
            assert legacy == alias
            assert resolve_template(alias)[0] == canonical

    def test_scaffold_failed_extract_removes_empty_dir(
        self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import os

        os.chdir(tmp_path)

        def _empty_tarball(_url: str = "") -> bytes:
            buf = io.BytesIO()
            with tarfile.open(fileobj=buf, mode="w:gz"):
                pass
            return buf.getvalue()

        monkeypatch.setattr("pixeltable_new.new.fetch_tarball", _empty_tarball)
        target = tmp_path / "should-vanish"
        with pytest.raises(RuntimeError, match="No files found"):
            scaffold("should-vanish", "serving", template="video-search")
        assert not target.exists()


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
        assert result.exit_code != 0
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

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_cli_json_output(self, pattern: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """--json flag emits machine-readable JSON for agents."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, [f"json-{pattern}", f"--{pattern}", "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert data["status"] == "ok"
        assert data["pattern"] == pattern
        assert isinstance(data["files"], list)
        assert len(data["files"]) > 0
        assert isinstance(data["next_steps"], list)

    def test_cli_json_error(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """--json errors go to stderr as JSON."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "taken").mkdir()
        result = runner.invoke(app, ["taken", "--json"])
        assert result.exit_code == 1

    def test_cli_list(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """--list shows patterns and templates."""
        result = runner.invoke(app, ["--list"])
        assert result.exit_code == 0, result.output
        assert "serving" in result.output
        assert "knowledge-base" in result.output
        assert "video-search" in result.output
        assert "video-intel" in result.output

    @pytest.mark.parametrize("alias", list(TEMPLATE_ALIASES))
    def test_cli_template_legacy_alias(
        self, alias: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Legacy template aliases scaffold successfully."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, [f"alias-{alias}", "--template", alias])
        assert result.exit_code == 0, result.output
        assert (tmp_path / f"alias-{alias}" / "schema.py").exists()

    def test_cli_list_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """--list --json emits structured JSON."""
        result = runner.invoke(app, ["--list", "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert "patterns" in data
        assert "templates" in data
        assert "knowledge-base" in data["templates"]

    @pytest.mark.parametrize("template", TEMPLATES)
    def test_cli_template(self, template: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """--template scaffolds the named application template."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, [f"tpl-{template}", "--template", template])
        assert result.exit_code == 0, result.output
        assert (tmp_path / f"tpl-{template}" / "schema.py").exists()

    @pytest.mark.parametrize("template", TEMPLATES)
    def test_cli_template_json(self, template: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """--template --json emits machine-readable JSON."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, [f"json-{template}", "--template", template, "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert data["status"] == "ok"
        assert data["template"] == template
        assert len(data["files"]) > 0

    def test_cli_template_with_pattern_fails(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """--template cannot be combined with --serving/--backend/--batch."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["bad", "--template", "chat-agent", "--backend"])
        assert result.exit_code != 0
        assert "Cannot combine" in result.output


class TestSubstituteProjectName:
    """Offline unit tests for precise pyproject `[project] name` substitution."""

    def test_rewrites_only_the_name_declaration(self, tmp_path: pathlib.Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "video-search"\ndescription = "video-search demo"\n')
        substitute_project_name(tmp_path, "kb-video-search", "video-search")
        # Only the name declaration changes; the description keeps its original text.
        assert pyproject.read_text() == '[project]\nname = "kb-video-search"\ndescription = "video-search demo"\n'

    def test_no_double_replace_for_substring_project_name(self, tmp_path: pathlib.Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('name = "video-search"\n')
        substitute_project_name(tmp_path, "kb-video-search", "video-search")
        assert pyproject.read_text() == 'name = "kb-video-search"\n'

    def test_unknown_source_key_is_noop(self, tmp_path: pathlib.Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('name = "video-search"\n')
        substitute_project_name(tmp_path, "myapp", "nonexistent")
        assert pyproject.read_text() == 'name = "video-search"\n'
