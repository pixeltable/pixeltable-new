# pixeltable-new

Create a new Pixeltable project in one command.

## How to use

Run:

```bash
uvx pixeltable-new myapp
```

This creates a new Pixeltable project with a declarative serving pattern (schema + `pyproject.toml` + `pxt serve`).

### Choose a pattern

Pixeltable supports three deployment patterns. Pick the one that fits your use case:

```bash
uvx pixeltable-new myapp --serving    # Declarative API from TOML config (default)
uvx pixeltable-new myapp --backend    # Full FastAPI + React web app
uvx pixeltable-new myapp --batch      # Batch processing script
```

### Run it

```bash
cd myapp
pip install pixeltable
pxt serve my-service    # serving pattern
```

### Existing directory

To initialize in the current directory:

```bash
uvx pixeltable-new
```

## Patterns

| Pattern | What you get | Run with |
|---|---|---|
| `--serving` (default) | `schema.py` + `pyproject.toml` routes | `pxt serve <service-name>` |
| `--backend` | FastAPI app + Pixeltable schema + routers | `uvicorn main:app --reload` |
| `--batch` | Ingest script + `export_sql` | `python pipeline.py` |

Templates are fetched from the [Pixeltable Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit). For the full reference with Docker, Helm, Terraform, and cloud deploy configs, clone the starter kit directly.

## Learn more

- [Pixeltable Documentation](https://docs.pixeltable.com/)
- [Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit)
- [AI Coding Skill](https://github.com/pixeltable/pixeltable-skill)
- [Discord](https://discord.gg/QPyqFYx2UN)

## License

Apache 2.0
