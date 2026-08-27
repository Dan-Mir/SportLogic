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


@app.command()
def migrate() -> None:
    """Applica le migration di tutti i moduli attivi (tabella versioni per-modulo)."""
    from arena.migrations import upgrade

    applied = upgrade()
    if applied:
        console.print(f"[green]Migration applicate per: {', '.join(applied)}[/green]")
    else:
        console.print("[dim]Nessun modulo con migration.[/dim]")


@app.command()
def create_admin(email: str, password: str, full_name: str = "Amministratore") -> None:
    """Crea (o aggiorna) un utente admin. Richiede le migration applicate."""
    from sqlalchemy import select

    from arena.db import get_session
    from arena.modules.core.models import User
    from arena.modules.core.security import hash_password

    email = email.strip().lower()
    session = get_session()
    user = session.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(email=email, full_name=full_name, role="admin", hashed_password="")
        session.add(user)
    user.hashed_password = hash_password(password)
    user.role = "admin"
    user.is_active = True
    session.commit()
    session.close()
    console.print(f"[green]Admin '{email}' pronto.[/green]")


if __name__ == "__main__":
    app()
