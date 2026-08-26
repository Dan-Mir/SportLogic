from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from arena import bootstrap as bootstrap_wizard
from arena.modules import discover_builtin, registry

app = typer.Typer(help="SportLogic CLI", no_args_is_help=True)
console = Console()


@app.command()
def modules() -> None:
    discover_builtin()
    table = Table("Modulo", "Versione", "Dipendenze", "Stato", "Label")
    for m in registry.all():
        table.add_row(
            m.name,
            m.version,
            ", ".join(m.depends_on) or "-",
            "attivo" if m.enabled else "-",
            m.label,
        )
    console.print(table)


@app.command()
def enable(name: str) -> None:
    discover_builtin()
    registry.enable(name)
    console.print(f"[green]Modulo '{name}' attivato[/green]")


@app.command()
def disable(name: str) -> None:
    discover_builtin()
    registry.disable(name)
    console.print(f"[yellow]Modulo '{name}' disattivato[/yellow]")


@app.command()
def bootstrap() -> None:
    bootstrap_wizard.run()


if __name__ == "__main__":
    app()
