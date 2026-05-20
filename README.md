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
uvx pixeltable-new --template multimodal-rag my-kb             # web UI + API
uvx pixeltable-new --template agent my-agent                   # web UI + API
uvx pixeltable-new --template audio-intel my-podcast-app       # web UI + API
uvx pixeltable-new --template full-stack-showcase my-sitewatch # web UI + API (complete reference app)
uvx pixeltable-new --template video-intel my-video-app         # API only
uvx pixeltable-new --template content-pipeline my-pipe         # API + batch
uvx pixeltable-new --template data-lab my-dataset              # API + batch
```

Templates with a web UI (`app.py`): run `python app.py` to start the server.
Templates without a UI: run `python schema.py` then `pxt serve <name>`.

| Template | Entry Point | What you get |
|---|---|---|
| `multimodal-rag` | `python app.py` | Unified search across docs, images, video, audio. Web UI |
| `agent` | `python app.py` | Persistent agent with durable memory, tools, MCP. Web UI |
| `audio-intel` | `python app.py` | Transcription, summarization, semantic search. Web UI |
| `full-stack-showcase` | `python app.py` | **Complete reference app**: Gemini + DETR + Whisper, cross-modal search, React UI, dashboard, alerting |
| `video-intel` | `pxt serve videointel` | Declarative video pipeline: frames, transcription, detection, search. API only |
| `content-pipeline` | `pxt serve pipeline` | Ingest from S3, process all modalities, export to your DB. API + batch |
| `data-lab` | `pxt serve datalab` | Auto-annotate, curate, version, export to PyTorch. API + batch |

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

## License

This project is licensed under the terms of the Apache 2.0 license.
