# Release Notes

## 0.4.1

- Fix default `--serving` next steps: `uv sync` → `uv run python schema.py` → `uv run pxt serve pipeline` (previously `uv add pixeltable` with no schema init, so the served tables did not exist).
- Fix `--batch` next steps to `uv sync` (the scaffolded project ships full dependencies; `uv add pixeltable` left it incomplete).
- Fix `substitute_project_name`: it referenced package names that never existed (`pixeltable-starter-kit-serving`, etc.) and was a silent no-op. It now rewrites the real `[project] name` values, scoped to `pyproject.toml` so README prose is left intact.
- README: fix the default-flow quickstart to match (`uv sync`, `python schema.py`, `pxt serve pipeline`).

## 0.4.0

- Rename all application templates to descriptive use-case names to match the starter kit's `main` branch: `multimodal-rag` → `knowledge-base`, `agent` → `chat-agent`, `audio-intel` → `audio-transcription`, `video-intel` → `video-search`, `content-pipeline` → `media-indexing`, `data-lab` → `image-dataset`.

## 0.3.1

- Fix next steps for app.py templates: print `python app.py` instead of `pxt serve <name>`.
- Add `full-stack-showcase` template to README and examples.
- Update README template table to show correct entry points per template.

## 0.3.0

- Add `full-stack-showcase` template: complete reference app with Gemini, DETR, Whisper, cross-modal search, React UI, dashboard, and alerting.
- Templates are now fetched live from the starter kit's `main` branch.

## 0.2.0

- Add `--template` / `-t` flag for application templates: `knowledge-base`, `video-search`, `chat-agent`, `audio-transcription`, `media-indexing`, `image-dataset`.
- Add `--list` / `-l` flag to discover all available patterns and templates.
- Templates are full-stack vertical apps built on Pixeltable's declarative infrastructure.
- `--json` output now includes template metadata when using `--template`.

## 0.1.3

- Add `--json` flag for machine-readable output (agent-friendly).
- Errors written to stderr as JSON when `--json` is used.

## 0.1.2

- Use `uv` commands in next-steps output (user already has `uv` via `uvx`).

## 0.1.1

- Add `RichToolkit`-themed CLI output with Pixeltable branding.
- Add PyPI badges to README.
- Switch build backend to `pdm-backend` with dynamic version.
- Add pytest strict config, coverage settings, ruff pyupgrade rules.

## 0.1.0

- Initial release.
- Scaffold Pixeltable projects from the Starter Kit (`--serving`, `--backend`, `--batch`).
- Templates fetched at runtime from GitHub.
- Skips `deploy/`, `uv.lock`, `.DS_Store`.
- Substitutes project name in `pyproject.toml` and `README.md`.
