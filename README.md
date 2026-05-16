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
pip install pixeltable
pxt serve my-service
```

Open your browser and go to `http://localhost:8000/docs` to see your API docs.

### Choose a pattern

Pixeltable supports three deployment patterns:

```bash
uvx pixeltable-new myapp --serving    # Declarative API from TOML config (default)
uvx pixeltable-new myapp --backend    # Full FastAPI + React web app
uvx pixeltable-new myapp --batch      # Batch processing script
```

| Pattern | What you get | Run with |
|---|---|---|
| `--serving` (default) | `schema.py` + `pyproject.toml` routes | `pxt serve <service-name>` |
| `--backend` | FastAPI app + Pixeltable schema + routers | `uvicorn main:app --reload` |
| `--batch` | Ingest script + `export_sql` | `python pipeline.py` |

Templates are fetched from the [Pixeltable Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit). For the full reference with Docker, Helm, Terraform, and cloud deploy configs, clone the starter kit directly.

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
