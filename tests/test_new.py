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
    NEXT_STEPS,
    PATTERNS,
    scaffold,
    substitute_project_name,
)

runner = CliRunner()

EXPECTED_FILES: dict[str, list[str]] = {
    "chat-agent": ["app.py", "pyproject.toml", "pixeltable.toml"],
    "video-search": ["app.py", "pyproject.toml", "pixeltable.toml"],
}

CLI_FLAGS: dict[str, list[str]] = {
    "chat-agent": [],
    "video-search": ["--video"],
}


class TestScaffoldFunction:
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
            scaffold("existing", "chat-agent")

    def test_scaffold_rejects_unknown_pattern(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        with pytest.raises(ValueError, match="Unknown pattern"):
            scaffold("badpattern", "nonexistent")

    def test_scaffold_rejects_template(self, tmp_path: pathlib.Path) -> None:
        import os

        os.chdir(tmp_path)
        with pytest.raises(ValueError, match="gone"):
            scaffold("badtemplate", "chat-agent", template="knowledge-base")

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
            scaffold("should-vanish", "chat-agent")
        assert not target.exists()


class TestCLI:
    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_cli_scaffold(self, pattern: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["myapp", *CLI_FLAGS[pattern]])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "myapp").exists()
        for expected_file in EXPECTED_FILES[pattern]:
            assert (tmp_path / "myapp" / expected_file).exists(), f"{expected_file} missing in CLI output"

    def test_cli_default_pattern_is_chat_agent(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["defaultapp"])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "defaultapp" / "app.py").read_text() == "agent = True\n"

    def test_cli_video_flag(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["vidapp", "--video"])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "vidapp" / "app.py").read_text() == "videointel = True\n"

    def test_cli_existing_dir_fails(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "taken").mkdir()
        result = runner.invoke(app, ["taken"])
        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_cli_batch_removed(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["multi", "--batch"])
        assert result.exit_code != 0
        assert "no such option" in result.output.lower() or "no such option" in (result.stderr or "").lower()

    def test_cli_no_deploy_dirs(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["nodeploy", "--video"])
        assert result.exit_code == 0, result.output
        assert not (tmp_path / "nodeploy" / "deploy").exists()

    def test_cli_help(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "pixeltable" in result.output.lower()
        assert "TOML config" not in result.output
        assert "--video" in result.output
        assert "--batch" not in result.output
        assert "--backend" not in result.output
        assert "--serving" not in result.output

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_cli_json_output(self, pattern: str, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, [f"json-{pattern}", *CLI_FLAGS[pattern], "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert data["status"] == "ok"
        assert data["pattern"] == pattern
        assert isinstance(data["files"], list)
        assert len(data["files"]) > 0
        assert isinstance(data["next_steps"], list)

    def test_cli_json_error(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "taken").mkdir()
        result = runner.invoke(app, ["taken", "--json"])
        assert result.exit_code == 1

    def test_cli_list(self, monkeypatch: pytest.MonkeyPatch) -> None:
        result = runner.invoke(app, ["--list"])
        assert result.exit_code == 0, result.output
        assert "chat-agent" in result.output
        assert "video-search" in result.output
        assert "serving" not in result.output
        assert "batch" not in result.output
        assert "knowledge-base" not in result.output
        assert "TOML config" not in result.output

    def test_cli_list_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        result = runner.invoke(app, ["--list", "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert "patterns" in data
        assert "templates" not in data
        assert "chat-agent" in data["patterns"]
        assert "video-search" in data["patterns"]
        assert "serving" not in data["patterns"]
        assert "batch" not in data["patterns"]

    def test_cli_template_removed(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["tpl", "--template", "knowledge-base"])
        assert result.exit_code == 1
        assert "gone" in result.output.lower() or "gone" in (result.stderr or "").lower()


class TestNextSteps:
    def test_chat_agent_uses_schema_and_service_update(self) -> None:
        assert NEXT_STEPS["chat-agent"] == [
            "uv sync",
            "pxt schema update app.py agent",
            "pxt service update app.py agent",
        ]

    def test_video_search_uses_schema_and_service_update(self) -> None:
        assert NEXT_STEPS["video-search"] == [
            "uv sync",
            "pxt schema update app.py videointel",
            "pxt service update app.py videointel",
        ]

    def test_no_removed_commands(self) -> None:
        for steps in NEXT_STEPS.values():
            for step in steps:
                assert "pxt serve" not in step
                assert "python schema.py" not in step
                assert "pxt://" not in step
                assert "pipeline" not in step


class TestSubstituteProjectName:
    def test_rewrites_only_the_name_declaration(self, tmp_path: pathlib.Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "chat-agent"\ndescription = "chat-agent demo"\n')
        substitute_project_name(tmp_path, "myapp", "chat-agent")
        assert pyproject.read_text() == '[project]\nname = "myapp"\ndescription = "chat-agent demo"\n'

    def test_unknown_source_key_is_noop(self, tmp_path: pathlib.Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('name = "chat-agent"\n')
        substitute_project_name(tmp_path, "myapp", "nonexistent")
        assert pyproject.read_text() == 'name = "chat-agent"\n'


class TestReadme:
    def test_no_hosted_pxt_service(self) -> None:
        readme = pathlib.Path(__file__).resolve().parent.parent / "README.md"
        text = readme.read_text(encoding="utf-8")
        assert "pxt service update app.py pxt://" not in text
        assert "--batch" not in text
        assert "pxt service update app.py pipeline" not in text
