"""CLI entry point for pixeltable-new."""

from __future__ import annotations

import json
import sys
from typing import Annotated

import typer

from pixeltable_new.new import (
    NEXT_STEPS,
    TEMPLATE_DESCRIPTIONS,
    TEMPLATE_NEXT_STEPS,
    TEMPLATES,
    scaffold,
)
from pixeltable_new.utils.cli import get_rich_toolkit

app = typer.Typer(rich_markup_mode="rich")


def _resolve_pattern(serving: bool, backend: bool, batch: bool) -> str:
    selected = [name for name, flag in [("serving", serving), ("backend", backend), ("batch", batch)] if flag]
    if len(selected) > 1:
        raise typer.BadParameter(f"Only one pattern allowed, got: {', '.join(selected)}")
    return selected[0] if selected else "serving"


@app.command()
def new(
    project: Annotated[
        str | None,
        typer.Argument(
            help="Project name (creates a new directory). Omit to initialize in the current directory.",
        ),
    ] = None,
    serving: Annotated[
        bool,
        typer.Option("--serving", help="Declarative API from TOML config (default)."),
    ] = False,
    backend: Annotated[
        bool,
        typer.Option("--backend", help="FastAPI API scaffold (headless, no frontend)."),
    ] = False,
    batch: Annotated[
        bool,
        typer.Option("--batch", help="Batch processing script with export_sql."),
    ] = False,
    template: Annotated[
        str | None,
        typer.Option(
            "--template", "-t", help="Application template name (e.g. knowledge-base, video-search, chat-agent)."
        ),
    ] = None,
    list_all: Annotated[
        bool,
        typer.Option("--list", "-l", help="List all available patterns and templates."),
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output (for AI agents and scripts)."),
    ] = False,
) -> None:
    """Create a new Pixeltable project from the starter kit."""
    if list_all:
        _run_list(json_output)
        return

    if template:
        if any([serving, backend, batch]):
            raise typer.BadParameter("Cannot combine --template with --serving/--backend/--batch.")
        if json_output:
            _run_json(project, "serving", template=template)
        else:
            _run_rich(project, "serving", template=template)
    else:
        pattern = _resolve_pattern(serving, backend, batch)
        if json_output:
            _run_json(project, pattern)
        else:
            _run_rich(project, pattern)


def _run_list(json_output: bool) -> None:
    """List all available patterns and templates."""
    patterns_info = {
        "serving": "Declarative API from TOML config (default)",
        "backend": "FastAPI API scaffold (headless, no frontend)",
        "batch": "Batch processing script with export_sql",
    }

    if json_output:
        print(json.dumps({"patterns": patterns_info, "templates": TEMPLATE_DESCRIPTIONS}))
        return

    with get_rich_toolkit() as toolkit:
        toolkit.print_title("Available patterns and templates", tag="Pixeltable")
        toolkit.print_line()
        toolkit.print("[bold]Structural Patterns[/bold] (API/pipeline scaffolds):")
        for name, desc in patterns_info.items():
            toolkit.print(f"  [cyan]{name:20s}[/cyan] {desc}")
        toolkit.print_line()
        toolkit.print("[bold]Application Templates[/bold] (each builds on a pattern above):")
        for name in TEMPLATES:
            toolkit.print(f"  [cyan]{name:20s}[/cyan] {TEMPLATE_DESCRIPTIONS[name]}")
        toolkit.print_line()
        toolkit.print("Usage:")
        toolkit.print("  [dim]$[/dim] uvx pixeltable-new --backend myapp")
        toolkit.print("  [dim]$[/dim] uvx pixeltable-new --template knowledge-base myapp")


def _run_json(project: str | None, pattern: str, template: str | None = None) -> None:
    """Machine-readable JSON output for agents and scripts."""
    try:
        dest, written = scaffold(project, pattern, template=template)
    except (FileExistsError, ValueError, RuntimeError) as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        raise typer.Exit(code=1) from e

    if template:
        next_steps = (["cd " + dest.name] if project else []) + TEMPLATE_NEXT_STEPS.get(template, [])
        result = {
            "status": "ok",
            "project": str(dest),
            "template": template,
            "files": sorted(written),
            "next_steps": next_steps,
        }
    else:
        next_steps = (["cd " + dest.name] if project else []) + NEXT_STEPS.get(pattern, [])
        result = {
            "status": "ok",
            "project": str(dest),
            "pattern": pattern,
            "files": sorted(written),
            "next_steps": next_steps,
        }

    print(json.dumps(result))


def _run_rich(project: str | None, pattern: str, template: str | None = None) -> None:
    """Human-friendly rich-formatted output."""
    with get_rich_toolkit() as toolkit:
        toolkit.print_title("Creating a new Pixeltable project", tag="Pixeltable")
        toolkit.print_line()

        if project:
            toolkit.print(f"Project: [cyan]{project}[/cyan]", tag="project")
        else:
            toolkit.print(
                "[yellow]Initializing in current directory[/yellow]",
                tag="warning",
            )

        if template:
            toolkit.print(f"Template: [cyan]{template}[/cyan]", tag="template")
            desc = TEMPLATE_DESCRIPTIONS.get(template, "")
            if desc:
                toolkit.print(f"  {desc}", tag="info")
        else:
            toolkit.print(f"Pattern: [cyan]{pattern}[/cyan]", tag="pattern")

        toolkit.print_line()
        toolkit.print("Fetching starter kit...", tag="fetch")

        try:
            dest, written = scaffold(project, pattern, template=template)
        except (FileExistsError, ValueError, RuntimeError) as e:
            toolkit.print(f"[bold red]Error:[/bold red] {e}", tag="error")
            raise typer.Exit(code=1) from e

        toolkit.print(f"Wrote [green]{len(written)}[/green] files to [cyan]{dest}[/cyan]", tag="done")

        toolkit.print_line()
        toolkit.print("[bold]Next steps:[/bold]")
        if project:
            toolkit.print(f"  [dim]$[/dim] cd {project}")

        steps = TEMPLATE_NEXT_STEPS.get(template, []) if template else NEXT_STEPS.get(pattern, [])
        for step in steps:
            toolkit.print(f"  [dim]$[/dim] {step}")

        toolkit.print_line()
        toolkit.print("[dim]Files:[/dim]")
        for f in sorted(written):
            toolkit.print(f"  {f}")

        toolkit.print_line()
        toolkit.print("[bold]Full starter kit with Docker, Helm, Terraform:[/bold]")
        toolkit.print("  [blue]https://github.com/pixeltable/pixeltable-starter-kit[/blue]")

        toolkit.print_line()
        toolkit.print("[dim]Docs: https://docs.pixeltable.com[/dim]")


def main() -> None:
    app()
