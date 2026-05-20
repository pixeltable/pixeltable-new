# Contributing

## Development

```bash
git clone https://github.com/pixeltable/pixeltable-new.git
cd pixeltable-new
uv sync
uv run python -m pytest tests/ -v
uv run ruff check src/ tests/
```

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
git add -A && git commit -m "v0.3.1: description of changes"
git tag v0.3.1
git push && git push --tags
```

The CI workflow runs the full test matrix, then publishes to PyPI via OIDC (no API token needed).

### Manual publish (fallback)

If trusted publishing isn't configured yet, publish manually with a [PyPI API token](https://pypi.org/manage/account/token/) scoped to the `pixeltable-new` project:

```bash
uv build
uv publish --token pypi-YOUR_TOKEN_HERE
```
