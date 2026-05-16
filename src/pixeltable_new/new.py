"""Core scaffolding logic: fetch starter-kit tarball, extract a pattern, write to disk."""

from __future__ import annotations

import io
import pathlib
import tarfile
import urllib.error
import urllib.request

STARTER_KIT_TARBALL = "https://github.com/pixeltable/pixeltable-starter-kit/archive/refs/heads/main.tar.gz"

PATTERNS = ("serving", "backend", "batch")

SKIP_FILES = {"uv.lock", ".DS_Store"}

NEXT_STEPS: dict[str, list[str]] = {
    "serving": [
        "uv add pixeltable",
        "uv run pxt serve pipeline",
    ],
    "backend": [
        "uv sync",
        "uv run python setup_pixeltable.py",
        "uv run uvicorn main:app --reload",
    ],
    "batch": [
        "uv add pixeltable",
        "uv run python pipeline.py",
    ],
}


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
        # tarball root is "pixeltable-starter-kit-main/"
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

            # skip deploy/ subdirectories (advanced users clone the full kit)
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


def substitute_project_name(dest: pathlib.Path, project_name: str) -> None:
    """Replace placeholder project name in pyproject.toml and README.md."""
    for filename in ("pyproject.toml", "README.md"):
        filepath = dest / filename
        if not filepath.exists():
            continue
        content = filepath.read_text()
        # The starter kit uses the pattern directory name as the project name
        for old_name in (
            "pixeltable-starter-kit-serving",
            "pixeltable-starter-kit-backend",
            "pixeltable-starter-kit-batch",
        ):
            content = content.replace(old_name, project_name)
        filepath.write_text(content)


def scaffold(
    project_name: str | None, pattern: str, tarball_url: str = STARTER_KIT_TARBALL
) -> tuple[pathlib.Path, list[str]]:
    """Scaffold a new Pixeltable project.

    Returns (project_path, list_of_files_written).
    """
    if pattern not in PATTERNS:
        raise ValueError(f"Unknown pattern {pattern!r}. Choose from: {', '.join(PATTERNS)}")

    if project_name:
        dest = (pathlib.Path.cwd() / project_name).resolve()
    else:
        dest = pathlib.Path.cwd()

    if project_name and dest.exists():
        raise FileExistsError(f"Directory {dest.name!r} already exists.")

    dest.mkdir(parents=True, exist_ok=True)

    tarball_bytes = fetch_tarball(tarball_url)
    written = extract_pattern(tarball_bytes, pattern, dest)

    if not written:
        raise RuntimeError(
            f"No files found for pattern {pattern!r} in the starter kit. The starter kit may have been restructured."
        )

    substitute_project_name(dest, dest.name)

    return dest, written
