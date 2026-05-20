# Release Notes

## 0.3.1

- Fix next steps for app.py templates: print `python app.py` instead of `pxt serve <name>`.
- Add `full-stack-showcase` template to README and examples.
- Update README template table to show correct entry points per template.

## 0.3.0

- Add `full-stack-showcase` template: complete reference app with Gemini, DETR, Whisper, cross-modal search, React UI, dashboard, and alerting.
- Templates are now fetched live from the starter kit's `main` branch.

## 0.2.0

- Add `--template` / `-t` flag for application templates: `multimodal-rag`, `video-intel`, `agent`, `audio-intel`, `content-pipeline`, `data-lab`.
- Add `--list` / `-l` flag to discover all available patterns and templates.
- Templates are full-stack vertical apps that each replace a paid SaaS (Vectara, Twelve Labs, Mem0, Otter.ai, Cloudinary AI, Roboflow).
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
