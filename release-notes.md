# Release Notes

## 0.6.2

- Export `ANTHROPIC_API_KEY` before the first `pxt` command in the chat-agent next steps. `pxt schema update` starts the Pixeltable daemon and `pxt service update` spawns the service from it with no environment of its own, so a key exported afterwards never reaches `/ask` -- and re-running `service update` does not respawn it, because the plan is already in agreement. The previous next steps ran `schema update` first, reproducing exactly that break. `--json` gained a `note` field carrying the reason and the recovery (`pxt daemon restart`, `pxt service stop agent`, `pxt service update`).
- Rewrite the scaffolded README's `cd`. The starter kit's README is written for the monorepo, so it said `cd chat-agent` -- a directory a scaffolded project does not have. It now points at the project name, or is dropped when scaffolding into the current directory.
- Drop the `pxt service run` reference from the README; `pxt service update` is the serving command.

## 0.6.1

- Require Python 3.11+ (drop 3.10 from package metadata and CI).
- Print the Declare, Experiment, Serve loop in CLI help, next steps, and the README.

## 0.6.0

- Default scaffold is `chat-agent/`: `pxt schema update app.py agent` then `pxt service update`. `--video` copies `video-search/`. `--batch` and `--serving` are gone.
- `--list` names those two apps. Cloud next-steps are `pxt schema update app.py pxt://...` only. `pxt service` stays local.

## 0.5.0

- Default scaffold is serving: `pxt schema update app.py pipeline` then `pxt service update`. Batch is `--batch` (schema update, then `python pipeline.py`). `--backend` and `--template` are gone; the skill writes extra tables into `app.py`.
- `--list` shows serving and batch only. Tests require `app.py`.

## 0.4.3

- Fix `full-stack-showcase` next steps: build the React UI (`npm install && npm run build`) before `python app.py`, so the scaffolded reference app serves its UI and API together on one port (previously the UI 404'd until built manually).
- Make `substitute_project_name` precise: it now rewrites only the scaffolded pattern/template's exact `[project] name` declaration, so a project name that contains another template's name as a substring can no longer double-replace.
- Describe `chat-agent` tools as "MCP-ready" (MCP is a commented example in the template), matching the starter kit README.

## 0.4.2

- Add legacy template aliases (`video-intel` → `video-search`, etc.) so older docs and stale `uvx` caches still scaffold successfully.
- Remove empty project directories when tarball extract fails (no more blocked retries after a failed `--template`).
- `--list` shows deprecated alias mappings; CLI prints a deprecation note when an alias is used.

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
