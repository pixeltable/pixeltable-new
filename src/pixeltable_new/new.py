"""Core scaffolding logic: fetch starter-kit tarball, extract a pattern or template, write to disk."""

from __future__ import annotations

import io
import pathlib
import shutil
import tarfile
import urllib.error
import urllib.request

STARTER_KIT_TARBALL = "https://github.com/pixeltable/pixeltable-starter-kit/archive/refs/heads/main.tar.gz"

PATTERNS = ("serving", "backend", "batch")

TEMPLATES = (
    "knowledge-base",
    "video-search",
    "chat-agent",
    "audio-transcription",
    "media-indexing",
    "image-dataset",
    "full-stack-showcase",
)

TEMPLATE_ALIASES: dict[str, str] = {
    "video-intel": "video-search",
    "multimodal-rag": "knowledge-base",
    "agent": "chat-agent",
    "audio-intel": "audio-transcription",
    "content-pipeline": "media-indexing",
    "data-lab": "image-dataset",
}

TEMPLATE_DESCRIPTIONS: dict[str, str] = {
    "knowledge-base": "serving + backend · Upload docs, images, video, audio; unified search + RAG Q&A (application file + FastAPIRouter + UI)",
    "video-search": "serving · Declarative video pipeline: frames, transcription, detection, temporal search (TableModel + FastAPIRouter)",
    "chat-agent": "serving + backend · Persistent agent with durable memory, tool calling, MCP-ready (application file + FastAPIRouter + UI)",
    "audio-transcription": "serving + backend · Audio/podcast transcription, summarization, semantic search (application file + FastAPIRouter + UI)",
    "media-indexing": "batch · Enterprise media processing: ingest from S3, process all modalities, export (application file + pipeline.py)",
    "image-dataset": "batch · ML dataset engineering: auto-annotate, curate, version, export to PyTorch (application file + export.py)",
    "full-stack-showcase": "serving + backend · Complete reference app: Gemini + DETR + Whisper, cross-modal search, React UI (application file + FastAPIRouter + frontend/)",
}

SKIP_FILES = {"uv.lock", ".DS_Store"}

NEXT_STEPS: dict[str, list[str]] = {
    "serving": [
        "uv sync",
        "pxt schema update app.py pipeline",
        "pxt service update app.py pipeline",
    ],
    "backend": [
        "uv sync",
        "uv run python setup_pixeltable.py",
        "uv run uvicorn main:app --reload",
    ],
    "batch": [
        "uv sync",
        "uv run python pipeline.py",
    ],
}

TEMPLATE_NEXT_STEPS: dict[str, list[str]] = {
    "knowledge-base": ["uv sync", "pxt schema update app.py kb", "python app.py"],
    "chat-agent": ["uv sync", "pxt schema update app.py agent", "python app.py"],
    "audio-transcription": ["uv sync", "pxt schema update app.py audiointel", "python app.py"],
    "full-stack-showcase": [
        "cp .env.example .env  # add GEMINI_API_KEY",
        "uv sync",
        "pxt schema update app.py sitewatch",
        "cd frontend && npm install && npm run build && cd ..  # build the React UI into static/",
        "python app.py  # UI + API at http://localhost:8000",
    ],
    "video-search": ["uv sync", "pxt schema update app.py videointel", "pxt service update app.py videointel"],
    "media-indexing": ["uv sync", "pxt schema update app.py pipeline", "pxt service update app.py pipeline"],
    "image-dataset": ["uv sync", "pxt schema update app.py datalab", "pxt service update app.py datalab"],
}

# Maps each pattern/template to the `[project] name` it uses in the starter kit,
# so scaffolding rewrites only that exact name (never a substring of another).
SOURCE_PROJECT_NAMES: dict[str, str] = {
    "serving": "pixeltable-serving",
    "backend": "pixeltable-starter-kit",
    "batch": "pixeltable-batch",
    "knowledge-base": "knowledge-base",
    "chat-agent": "pixeltable-chat-agent",
    "audio-transcription": "audio-transcription",
    "full-stack-showcase": "full-stack-showcase",
    "video-search": "video-search",
    "media-indexing": "media-indexing",
    "image-dataset": "image-dataset",
}


def resolve_template(name: str) -> tuple[str, str | None]:
    """Map a template slug (canonical or legacy alias) to the starter-kit folder name."""
    if name in TEMPLATES:
        return name, None
    if name in TEMPLATE_ALIASES:
        return TEMPLATE_ALIASES[name], name
    known = sorted(set(TEMPLATES) | set(TEMPLATE_ALIASES))
    raise ValueError(f"Unknown template {name!r}. Choose from: {', '.join(known)}")


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


def substitute_project_name(dest: pathlib.Path, project_name: str, source_key: str) -> None:
    """Rewrite the scaffolded pyproject.toml ``[project] name`` to the user's project name.

    Only the exact ``name = "<source>"`` declaration for the scaffolded pattern or
    template is rewritten (README prose is left intact, and a project name that
    contains another template's name as a substring can't trigger a double-replace).
    """
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
) -> tuple[pathlib.Path, list[str], str | None]:
    """Scaffold a new Pixeltable project.

    Returns (project_path, files_written, legacy_alias_or_none).
    """
    legacy_alias: str | None = None
    if template:
        template, legacy_alias = resolve_template(template)
        extract_prefix = f"templates/{template}"
    else:
        if pattern not in PATTERNS:
            raise ValueError(f"Unknown pattern {pattern!r}. Choose from: {', '.join(PATTERNS)}")
        extract_prefix = pattern

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
        written = extract_pattern(tarball_bytes, extract_prefix, dest)

        if not written:
            label = f"template {template!r}" if template else f"pattern {pattern!r}"
            raise RuntimeError(
                f"No files found for {label} in the starter kit. The starter kit may have been restructured."
            )

        substitute_project_name(dest, dest.name, template if template else pattern)
        return dest, written, legacy_alias
    except Exception:
        if created_dest and dest.is_dir():
            if not any(dest.iterdir()):
                dest.rmdir()
            else:
                shutil.rmtree(dest)
        raise
