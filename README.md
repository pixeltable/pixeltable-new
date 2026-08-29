# pixeltable-new

Create a new Pixeltable project in one command.

<a href="https://pypi.org/project/pixeltable-new" target="_blank">
    <img src="https://img.shields.io/pypi/v/pixeltable-new?color=%235533A0" alt="Package version">
</a>
<a href="https://pypi.org/project/pixeltable-new" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pixeltable-new.svg?color=%235533A0" alt="Supported Python versions">
</a>

Python 3.11+ on Linux, macOS, or Windows.

## How to use

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) following their guide for your system.

```bash
uvx pixeltable-new myapp
cd myapp
uv sync
pxt schema update app.py pipeline
pxt service update app.py pipeline
```

This writes an application file (`app.py`) with `TableModel` tables and `FastAPIRouter` routes.
`pipeline` is a catalog directory, not a folder on disk. `pxt service list` prints the URL.
OpenAPI is at `/docs`.

A project root is `pixeltable.toml` or `pyproject.toml` with `[tool.pixeltable]`. The scaffold
includes one. If you copied files by hand, run `pxt init` first.

No HTTP:

```bash
uvx pixeltable-new myapp --batch
cd myapp && uv sync
pxt schema update app.py pipeline
uv run python pipeline.py
```

```bash
uvx pixeltable-new --list
```

RAG, video, agents, and UIs are not downloaded as templates. Install the
[Pixeltable skill](https://github.com/pixeltable/pixeltable-skill) and add tables in `app.py`.

Content is fetched from the [Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit).

### Existing directory

```bash
uvx pixeltable-new
```

## Learn more

- [Pixeltable Documentation](https://docs.pixeltable.com/)
- [Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit)
- [AI Coding Skill](https://github.com/pixeltable/pixeltable-skill)
- [Discord](https://discord.gg/QPyqFYx2UN)

## License

Apache 2.0
