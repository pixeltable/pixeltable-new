"""CLI entry point for pixeltable-new."""

from __future__ import annotations

import json
import sys
from typing import Annotated

import typer

from pixeltable_new.new import NEXT_STEPS, scaffold
from pixeltable_new.utils.cli import get_rich_toolkit

app = typer.Typer(rich_markup_mode="rich")


def _resolve_pattern(video: bool) -> str:
    return "video-search" if video else "chat-agent"


@app.command()
def new(
    project: Annotated[
        str | None,
        typer.Argument(
            help="Project name (creates a new directory). Omit to initialize in the current directory.",
        ),
    ] = None,
    video: Annotated[
        bool,
        typer.Option("--video", help="Video frames, CLIP search, and image ingest."),
    ] = False,
    template: Annotated[
        str | None,
        typer.Option(
            "--template",
            "-t",
            help="Removed. Scaffold the chat agent and add tables in app.py.",
        ),
    ] = None,
    list_all: Annotated[
        bool,
        typer.Option("--list", "-l", help="List available apps."),
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output (for AI agents and scripts)."),
    ] = False,
) -> None:
    """Create a new Pixeltable project from the starter kit.

    Declare, Experiment, Serve: `pxt schema update`, then `pxt service update`,
    then dashboard or curl. Default TARGET is `agent`. `--video` uses `videointel`.
    """
    if list_all:
        _run_list(json_output)
        return

    if template:
        msg = (
            f"Template {template!r} is gone. Scaffold the chat agent "
            f"(uvx pixeltable-new myapp) and add columns in app.py. "
            f"Video: uvx pixeltable-new myapp --video. "
            f"The pixeltable skill generates extra tables."
        )
        if json_output:
            print(json.dumps({"status": "error", "message": msg}), file=sys.stderr)
        else:
            with get_rich_toolkit() as toolkit:
                toolkit.print(f"[bold red]Error:[/bold red] {msg}", tag="error")
        raise typer.Exit(code=1)

    pattern = _resolve_pattern(video)
    if json_output:
        _run_json(project, pattern)
    else:
        _run_rich(project, pattern)


def _run_list(json_output: bool) -> None:
    """List chat-agent and video-search."""
    patterns_info = {
        "chat-agent": "Knowledge, memory, and LLM (default)",
        "video-search": "Video frames, CLIP search, and image ingest",
    }

    if json_output:
        print(json.dumps({"patterns": patterns_info}))
        return

    with get_rich_toolkit() as toolkit:
        toolkit.print_title("Available apps", tag="Pixeltable")
        toolkit.print_line()
        for name, desc in patterns_info.items():
            toolkit.print(f"  [cyan]{name:20s}[/cyan] {desc}")
        toolkit.print_line()
        toolkit.print("Usage:")
        toolkit.print("  [dim]$[/dim] uvx pixeltable-new myapp")
        toolkit.print("  [dim]$[/dim] uvx pixeltable-new myapp --video")
        toolkit.print_line()
        toolkit.print("[dim]Add tables in app.py, or install pixeltable-skill.[/dim]")


def _run_json(project: str | None, pattern: str) -> None:
    """Machine-readable JSON output for agents and scripts."""
    try:
        dest, written = scaffold(project, pattern)
    except (FileExistsError, ValueError, RuntimeError) as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        raise typer.Exit(code=1) from e

    next_steps = (["cd " + dest.name] if project else []) + NEXT_STEPS.get(pattern, [])
    result = {
        "status": "ok",
        "project": str(dest),
        "pattern": pattern,
        "files": sorted(written),
        "next_steps": next_steps,
    }
    print(json.dumps(result))


def _run_rich(project: str | None, pattern: str) -> None:
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

        toolkit.print(f"Pattern: [cyan]{pattern}[/cyan]", tag="pattern")
        toolkit.print_line()
        toolkit.print("Fetching starter kit...", tag="fetch")

        try:
            dest, written = scaffold(project, pattern)
        except (FileExistsError, ValueError, RuntimeError) as e:
            toolkit.print(f"[bold red]Error:[/bold red] {e}", tag="error")
            raise typer.Exit(code=1) from e

        toolkit.print(f"Wrote [green]{len(written)}[/green] files to [cyan]{dest}[/cyan]", tag="done")

        toolkit.print_line()
        toolkit.print("[bold]Next steps:[/bold]")
        if project:
            toolkit.print(f"  [dim]$[/dim] cd {project}")

        for step in NEXT_STEPS.get(pattern, []):
            toolkit.print(f"  [dim]$[/dim] {step}")

        toolkit.print_line()
        toolkit.print("[dim]Declare, Experiment, Serve: schema update, service update, then dashboard or curl.[/dim]")

        toolkit.print_line()
        toolkit.print("[dim]Files:[/dim]")
        for f in sorted(written):
            toolkit.print(f"  {f}")

        toolkit.print_line()
        toolkit.print("[bold]Starter kit:[/bold]")
        toolkit.print("  [blue]https://github.com/pixeltable/pixeltable-starter-kit[/blue]")
        toolkit.print("[bold]Skill (write extra tables):[/bold]")
        toolkit.print("  [blue]https://github.com/pixeltable/pixeltable-skill[/blue]")
        toolkit.print_line()
        toolkit.print("[dim]Docs: https://docs.pixeltable.com[/dim]")


def main() -> None:
    app()
