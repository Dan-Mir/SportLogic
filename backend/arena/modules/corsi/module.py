from __future__ import annotations

from arena.modules.base import ModuleManifest

manifest = ModuleManifest(
    name="corsi",
    label="Corsi e lezioni",
    version="0.1.0",
    description="Corsi multi-livello, calendario, capienza, liste d'attesa, istruttori",
    depends_on=["core", "anagrafica"],
    has_frontend=True,
)
