from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from arena.modules import discover_builtin, registry

console = Console()

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07")


def _clean(value: str) -> str:
    return _ANSI_RE.sub("", value).strip()

FACILITY_PRESETS: dict[str, list[str]] = {
    "palestra": ["core", "anagrafica", "corsi"],
    "piscina": ["core", "anagrafica", "corsi"],
    "centro_sportivo": ["core", "anagrafica", "corsi", "booking.fields"],
    "multi": ["core", "anagrafica", "corsi", "booking.fields"],
}


def run() -> None:
    console.print("[bold]SportLogic — wizard di installazione[/bold]\n")
    discover_builtin()

    facility = Prompt.ask(
        "Tipologia impianto",
        choices=list(FACILITY_PRESETS),
        default="palestra",
    )
    preselected = set(FACILITY_PRESETS[facility])

    console.print("\nSeleziona i moduli da installare:")
    selected: list[str] = []
    for manifest in registry.all():
        enabled = Confirm.ask(
            f"  {manifest.name} — {manifest.label}",
            default=manifest.name in preselected,
        )
        if enabled:
            selected.append(manifest.name)

    brand_name = _clean(Prompt.ask("Nome del brand", default="SportLogic"))
    primary_color = _clean(Prompt.ask("Colore primario (hex)", default="#2563eb"))
    public_domain = _clean(Prompt.ask("Dominio pubblico", default="impianto.local"))

    env_path = Path(".env")
    env_path.write_text(
        "\n".join(
            [
                "# Generato da 'arena bootstrap'",
                "ARENA_APP_NAME=SportLogic",
                f"ARENA_BRAND_NAME={brand_name}",
                f"ARENA_BRAND_PRIMARY_COLOR={primary_color}",
                f"ARENA_PUBLIC_DOMAIN={public_domain}",
                "ARENA_MODULES_ENABLED=" + ",".join(selected),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    console.print(f"\n[green]Configurazione scritta in {env_path}[/green]")
    console.print("Moduli attivi: " + ", ".join(selected))
    console.print("\nProssimi passi:")
    console.print("  docker compose up -d")
    console.print("  uvicorn arena.main:app --reload")
