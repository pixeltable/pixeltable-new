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

Default is the chat agent (text insert, no API key for `/api/knowledge`):

```bash
uvx pixeltable-new myapp
cd myapp
uv sync
pxt schema update app.py agent
pxt service update app.py agent
```

`pxt service list` prints the URL. OpenAPI is at `/docs`. `/ask` needs `ANTHROPIC_API_KEY`.
Declare, Experiment, Serve: apply, serve, then insert / `/ask` / `pxt dashboard`.

Video frames, CLIP search, and image ingest:

```bash
uvx pixeltable-new myapp --video
cd myapp
uv sync
pxt schema update app.py videointel
pxt service update app.py videointel
```

Same file on Cloud:

```bash
pxt db create pxt://org:mydb
pxt schema update app.py pxt://org:mydb
```

`pxt service` stays local. Browse and insert on Cloud: dashboard and recipes.

A project root is `pixeltable.toml` or `pyproject.toml` with `[tool.pixeltable]`. The scaffold
includes one. If you copied files by hand, run `pxt init` first.

```bash
uvx pixeltable-new --list
```

Install the [Pixeltable skill](https://github.com/pixeltable/pixeltable-skill) to add tables in `app.py`.

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
