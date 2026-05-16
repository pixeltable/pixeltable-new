# Release Notes

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
