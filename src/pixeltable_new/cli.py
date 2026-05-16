"""CLI entry point for pixeltable-new."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from pixeltable_new.new import NEXT_STEPS, scaffold

app = typer.Typer(rich_markup_mode="rich")
console = Console()


def _resolve_pattern(serving: bool, backend: bool, batch: bool) -> str:
    selected = [name for name, flag in [("serving", serving), ("backend", backend), ("batch", batch)] if flag]
    if len(selected) > 1:
        console.print(f"[bold red]Error:[/bold red] Only one pattern allowed, got: {', '.join(selected)}")
        raise typer.Exit(code=1)
    if len(selected) == 1:
        return selected[0]
    return "serving"


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
        typer.Option("--backend", help="Full FastAPI + React web app."),
    ] = False,
    batch: Annotated[
        bool,
        typer.Option("--batch", help="Batch processing script with export_sql."),
    ] = False,
) -> None:
    """Create a new Pixeltable project from the starter kit."""
    pattern = _resolve_pattern(serving, backend, batch)

    console.print()
    console.print("[bold]Creating a new Pixeltable project[/bold]", highlight=False)
    console.print()

    if project:
        console.print(f"  Project:  [cyan]{project}[/cyan]")
    else:
        console.print("  Project:  [yellow](current directory)[/yellow]")
    console.print(f"  Pattern:  [cyan]{pattern}[/cyan]")
    console.print()

    console.print("  Fetching starter kit...", highlight=False)

    try:
        dest, written = scaffold(project, pattern)
    except (FileExistsError, ValueError, RuntimeError) as e:
        console.print(f"  [bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1) from e

    console.print(f"  Wrote [green]{len(written)}[/green] files to [cyan]{dest}[/cyan]")
    console.print()

    console.print("[bold]Next steps:[/bold]")
    if project:
        console.print(f"  [dim]$[/dim] cd {project}")
    steps = NEXT_STEPS.get(pattern, [])
    for step in steps:
        console.print(f"  [dim]$[/dim] {step}")

    console.print()
    console.print("[dim]Files:[/dim]")
    for f in sorted(written):
        console.print(f"  {f}")

    console.print()
    console.print("[dim]Full starter kit with Docker, Helm, Terraform:[/dim]")
    console.print("  https://github.com/pixeltable/pixeltable-starter-kit")
    console.print()


def main() -> None:
    app()
