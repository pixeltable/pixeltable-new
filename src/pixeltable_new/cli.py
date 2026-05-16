"""CLI entry point for pixeltable-new."""

from __future__ import annotations

from typing import Annotated

import typer

from pixeltable_new.new import NEXT_STEPS, scaffold
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
        typer.Option("--backend", help="Full FastAPI + React web app."),
    ] = False,
    batch: Annotated[
        bool,
        typer.Option("--batch", help="Batch processing script with export_sql."),
    ] = False,
) -> None:
    """Create a new Pixeltable project from the starter kit."""
    pattern = _resolve_pattern(serving, backend, batch)

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
