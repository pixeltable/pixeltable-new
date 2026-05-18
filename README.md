# pixeltable-new

Create a new Pixeltable project in one command.

<a href="https://pypi.org/project/pixeltable-new" target="_blank">
    <img src="https://img.shields.io/pypi/v/pixeltable-new?color=%235533A0" alt="Package version">
</a>
<a href="https://pypi.org/project/pixeltable-new" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pixeltable-new.svg?color=%235533A0" alt="Supported Python versions">
</a>

## How to use

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) following their guide for your system.

Run:

```bash
uvx pixeltable-new myapp
```

This will create a new project `myapp` with a Pixeltable schema and declarative serving config.

Enter the directory:

```bash
cd myapp
```

Install dependencies and run:

```bash
uv add pixeltable
uv run pxt serve my-service
```

Open your browser and go to `http://localhost:8000/docs` to see your API docs.

### Application Templates

Vertical apps that each build on a structural pattern — so you already know how to run and deploy them:

```bash
uvx pixeltable-new --template multimodal-rag my-kb        # serving + backend (web UI)
uvx pixeltable-new --template video-intel my-video-app    # serving (pure declarative)
uvx pixeltable-new --template agent my-agent              # serving + backend (web UI)
uvx pixeltable-new --template audio-intel my-podcast-app  # serving + backend (web UI)
uvx pixeltable-new --template content-pipeline my-pipe    # batch (pipeline.py)
uvx pixeltable-new --template data-lab my-dataset         # batch (export.py)
```

| Template | Pattern | What you get |
|---|---|---|
| `multimodal-rag` | serving + backend | Unified search across docs, images, video, audio. `schema.py` + `app.py` + web UI |
| `video-intel` | serving | Declarative video pipeline: frames, transcription, detection, search. Pure `schema.py` |
| `agent` | serving + backend | Persistent agent with durable memory, tools, MCP. `schema.py` + `app.py` + web UI |
| `audio-intel` | serving + backend | Transcription, diarization, summarization, semantic search. `schema.py` + `app.py` + web UI |
| `content-pipeline` | batch | Ingest from S3, process all modalities, export to your DB. `schema.py` + `pipeline.py` |
| `data-lab` | batch | Auto-annotate, curate, version, export to PyTorch. `schema.py` + `export.py` |

### Structural Patterns

API/pipeline scaffolds for when you want to wire Pixeltable into your own architecture:

```bash
uvx pixeltable-new myapp --serving    # Declarative API from TOML config (default)
uvx pixeltable-new myapp --backend    # FastAPI API scaffold (headless)
uvx pixeltable-new myapp --batch      # Batch processing script
```

| Pattern | What you get | Run with |
|---|---|---|
| `--serving` (default) | `schema.py` + `pyproject.toml` routes | `pxt serve <service-name>` |
| `--backend` | FastAPI API scaffold + Pixeltable schema + routers | `uvicorn main:app --reload` |
| `--batch` | Ingest script + `export_sql` | `python pipeline.py` |

### Discovery

```bash
uvx pixeltable-new --list    # show all patterns + templates
```

All content is fetched from the [Pixeltable Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit). For the full reference with Docker, Helm, Terraform, and cloud deploy configs, clone the starter kit directly.

### Existing directory

If you want to create a new Pixeltable project in an existing directory, run the command without a project name:

```bash
uvx pixeltable-new
```

## Learn more

- [Pixeltable Documentation](https://docs.pixeltable.com/)
- [Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit)
- [AI Coding Skill](https://github.com/pixeltable/pixeltable-skill)
- [Discord](https://discord.gg/QPyqFYx2UN)

## Releasing

Releases are published to PyPI automatically when a version tag is pushed.

### One-time setup (trusted publishing)

1. Go to [pypi.org/manage/project/pixeltable-new/settings/publishing/](https://pypi.org/manage/project/pixeltable-new/settings/publishing/)
2. Add a new trusted publisher:
   - **Owner**: `pixeltable`
   - **Repository**: `pixeltable-new`
   - **Workflow**: `publish.yml`
   - **Environment**: `pypi`
3. Create a GitHub environment called `pypi` at [github.com/pixeltable/pixeltable-new/settings/environments](https://github.com/pixeltable/pixeltable-new/settings/environments)

### Publishing a release

```bash
# 1. Bump version in src/pixeltable_new/__init__.py
# 2. Update release-notes.md
# 3. Commit, tag, push
git add -A && git commit -m "v0.3.0: description of changes"
git tag v0.3.0
git push && git push --tags
```

The CI workflow runs the full test matrix, then publishes to PyPI via OIDC (no API token needed).

### Manual publish (fallback)

If trusted publishing isn't configured yet, publish manually with a [PyPI API token](https://pypi.org/manage/account/token/) scoped to the `pixeltable-new` project:

```bash
uv build
uv publish --token pypi-YOUR_TOKEN_HERE
```

## License

This project is licensed under the terms of the Apache 2.0 license.
