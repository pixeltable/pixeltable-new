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
uv sync
uv run python schema.py
uv run pxt serve pipeline
```

Open your browser and go to `http://localhost:8000/docs` to see your API docs.

### Application Templates

Vertical apps that each build on a structural pattern — so you already know how to run and deploy them:

```bash
uvx pixeltable-new --template knowledge-base my-kb             # web UI + API
uvx pixeltable-new --template chat-agent my-agent              # web UI + API
uvx pixeltable-new --template audio-transcription my-podcast   # web UI + API
uvx pixeltable-new --template full-stack-showcase my-sitewatch # web UI + API (complete reference app)
uvx pixeltable-new --template video-search my-video-app        # API only
uvx pixeltable-new --template media-indexing my-pipe           # API + batch
uvx pixeltable-new --template image-dataset my-dataset         # API + batch
```

| Template | Pattern | What you get |
|---|---|---|
| `knowledge-base` | serving + backend | Unified search + RAG Q&A across docs, images, video, audio. `schema.py` + `app.py` + web UI |
| `chat-agent` | serving + backend | Persistent agent with durable memory, tools, MCP-ready. `schema.py` + `app.py` + web UI |
| `audio-transcription` | serving + backend | Audio/podcast transcription, summarization, semantic search. `schema.py` + `app.py` + web UI |
| `full-stack-showcase` | serving + backend | Complete reference app: Gemini + DETR + Whisper, React UI, dashboard. `schema.py` + `app.py` + `routers/` + `frontend/` |
| `video-search` | serving | Declarative video pipeline: frames, transcription, detection, temporal search. Pure `schema.py`. Run: `pxt serve videointel` |
| `media-indexing` | batch | Ingest from S3, process all modalities, export to your DB. `schema.py` + `pipeline.py` |
| `image-dataset` | batch | Auto-annotate, curate, version, export to PyTorch. `schema.py` + `export.py` |

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

**Legacy template names** (deprecated since 0.4.2, still work): `video-intel` → `video-search`, `multimodal-rag` → `knowledge-base`, `agent` → `chat-agent`, `audio-intel` → `audio-transcription`, `content-pipeline` → `media-indexing`, `data-lab` → `image-dataset`. Prefer the canonical names above.

**`video-search` quickstart** after scaffolding:

```bash
cd my-video-app && uv sync && uv run python schema.py && uv run pxt serve videointel
```

**`full-stack-showcase` quickstart** (build the React UI, then serve UI + API on one port):

```bash
cd my-sitewatch && cp .env.example .env   # add GEMINI_API_KEY
uv sync && uv run python schema.py
cd frontend && npm install && npm run build && cd ..
uv run python app.py   # UI + API at http://localhost:8000
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
