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
export ANTHROPIC_API_KEY=sk-...   # before the first pxt command; only /ask needs it
uvx pixeltable-new myapp
cd myapp
uv sync
pxt schema update app.py agent
pxt service update app.py agent
```

Export the key first. `pxt schema update` starts the Pixeltable daemon, `pxt service update` spawns the
service from it, and the service inherits the daemon's environment -- so a key exported afterwards never
reaches `/ask`, and re-running `pxt service update` will not pick it up. Recovery is `pxt daemon restart`,
`pxt service stop agent`, `pxt service update app.py agent`.

`agent` and `videointel` are catalog directories, not folders on disk.
`pxt service list` prints the URL. OpenAPI is at `/docs`.
Declare, Experiment, Serve: apply, serve, then insert / `/ask` / `pxt dashboard`.

Video frames, CLIP search, and image ingest:

```bash
uvx pixeltable-new myapp --video
cd myapp
uv sync
pxt schema update app.py videointel
pxt service update app.py videointel
```

Same file on Cloud (`PIXELTABLE_API_KEY`, plus `[[pixeltable.database]]` with `name = 'pxt://org:mydb'`):

```bash
pxt secret set pxt://org ANTHROPIC_API_KEY=sk-...
pxt db update pxt://org:mydb
pxt schema update app.py pxt://org:mydb
pxt service update app.py pxt://org:mydb
```

The secret goes first for the same reason the local export does: the process that answers `/ask` reads it
at request time.

`pxt db update` creates the hosted database or brings it up to what the project declares.

A project root is `pixeltable.toml` or `pyproject.toml` with `[tool.pixeltable]`. The scaffold
includes one. If you copied files by hand, run `pxt init` first.

```bash
uvx pixeltable-new --list
```

Agents: `uvx pixeltable-new myapp --json` or `uvx pixeltable-new --list --json`.

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
