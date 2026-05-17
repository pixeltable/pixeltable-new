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

Full-stack vertical apps that replace paid SaaS -- each is one `schema.py` + `pyproject.toml`:

```bash
uvx pixeltable-new --template multimodal-rag my-kb        # your own Vectara
uvx pixeltable-new --template video-intel my-video-app    # your own Twelve Labs
uvx pixeltable-new --template agent my-agent              # your own Mem0
uvx pixeltable-new --template audio-intel my-podcast-app  # your own Otter.ai
uvx pixeltable-new --template content-pipeline my-pipe    # your own Cloudinary AI
uvx pixeltable-new --template data-lab my-dataset         # your own Roboflow
```

| Template | What it replaces | What you get |
|---|---|---|
| `multimodal-rag` | Vectara, Cohere RAG | Unified search across docs, images, video, audio |
| `video-intel` | Twelve Labs, Valossa | Declarative video pipeline: frames, transcription, detection, search |
| `agent` | Mem0, MemGPT | Persistent agent with durable memory, tools, MCP |
| `audio-intel` | Otter.ai, AssemblyAI | Transcription, diarization, summarization, semantic search |
| `content-pipeline` | Cloudinary AI | Ingest from S3, process all modalities, export to your DB |
| `data-lab` | Labelbox, Roboflow | Auto-annotate, curate, version, export to PyTorch |

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
