"""Core scaffolding logic: fetch starter-kit tarball, extract serving or batch."""

from __future__ import annotations

import io
import pathlib
import shutil
import tarfile
import urllib.error
import urllib.request

STARTER_KIT_TARBALL = "https://github.com/pixeltable/pixeltable-starter-kit/archive/refs/heads/main.tar.gz"

PATTERNS = ("serving", "batch")

SKIP_FILES = {"uv.lock", ".DS_Store"}

NEXT_STEPS: dict[str, list[str]] = {
    "serving": [
        "uv sync",
        "pxt schema update app.py pipeline",
        "pxt service update app.py pipeline",
    ],
    "batch": [
        "uv sync",
        "pxt schema update app.py pipeline",
        "uv run python pipeline.py",
    ],
}

SOURCE_PROJECT_NAMES: dict[str, str] = {
    "serving": "pixeltable-serving",
    "batch": "pixeltable-batch",
}

_REMOVED_TEMPLATES = (
    "knowledge-base, chat-agent, audio-transcription, video-search, media-indexing, image-dataset, full-stack-showcase"
)


def reject_template(name: str) -> None:
    """Templates were removed. Agents write extra tables into app.py."""
    raise ValueError(
        f"Template {name!r} is gone. Scaffold serving "
        f"(uvx pixeltable-new myapp) and add columns in app.py. "
        f"The pixeltable skill generates RAG, video, and agent tables. "
        f"Removed names: {_REMOVED_TEMPLATES}."
    )


def fetch_tarball(url: str = STARTER_KIT_TARBALL) -> bytes:
    """Download the starter-kit tarball from GitHub."""
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return resp.read()  # type: ignore[no-any-return]
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to download starter kit from {url}. Check your internet connection.\n  {e}") from e


def extract_pattern(tarball_bytes: bytes, pattern: str, dest: pathlib.Path) -> list[str]:
    """Extract a pattern subdirectory from the tarball into *dest*.

    Returns the list of files written (relative to *dest*).
    """
    written: list[str] = []
    with tarfile.open(fileobj=io.BytesIO(tarball_bytes), mode="r:gz") as tf:
        prefix: str | None = None
        for member in tf.getmembers():
            if prefix is None:
                prefix = member.name.split("/")[0]

            pattern_prefix = f"{prefix}/{pattern}/"
            if not member.name.startswith(pattern_prefix):
                continue

            rel_path = member.name[len(pattern_prefix) :]
            if not rel_path:
                continue

            if any(skip in rel_path for skip in SKIP_FILES):
                continue

            if rel_path.startswith("deploy/") or rel_path == "deploy":
                continue

            target = dest / rel_path

            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                f = tf.extractfile(member)
                if f is not None:
                    target.write_bytes(f.read())
                    written.append(rel_path)

    return written


def substitute_project_name(dest: pathlib.Path, project_name: str, source_key: str) -> None:
    """Rewrite the scaffolded pyproject.toml ``[project] name`` to the user's project name."""
    filepath = dest / "pyproject.toml"
    old_name = SOURCE_PROJECT_NAMES.get(source_key)
    if not filepath.exists() or old_name is None:
        return
    content = filepath.read_text()
    content = content.replace(f'name = "{old_name}"', f'name = "{project_name}"', 1)
    filepath.write_text(content)


def scaffold(
    project_name: str | None,
    pattern: str,
    tarball_url: str = STARTER_KIT_TARBALL,
    template: str | None = None,
) -> tuple[pathlib.Path, list[str]]:
    """Scaffold a new Pixeltable project.

    Returns (project_path, files_written).
    """
    if template:
        reject_template(template)

    if pattern not in PATTERNS:
        raise ValueError(f"Unknown pattern {pattern!r}. Choose from: {', '.join(PATTERNS)}")

    if project_name:
        dest = (pathlib.Path.cwd() / project_name).resolve()
    else:
        dest = pathlib.Path.cwd()

    if project_name and dest.exists():
        raise FileExistsError(f"Directory {dest.name!r} already exists.")

    created_dest = bool(project_name)
    if created_dest:
        dest.mkdir(parents=True, exist_ok=True)

    try:
        tarball_bytes = fetch_tarball(tarball_url)
        written = extract_pattern(tarball_bytes, pattern, dest)

        if not written:
            raise RuntimeError(
                f"No files found for pattern {pattern!r} in the starter kit. "
                f"The starter kit may have been restructured."
            )

        substitute_project_name(dest, dest.name, pattern)
        return dest, written
    except Exception:
        if created_dest and dest.is_dir():
            if not any(dest.iterdir()):
                dest.rmdir()
            else:
                shutil.rmtree(dest)
        raise
