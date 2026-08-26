from __future__ import annotations

from arena.modules.base import ModuleManifest

manifest = ModuleManifest(
    name="booking.fields",
    label="Prenotazione campi/impianti",
    version="0.1.0",
    description="Fasce orarie, tariffe stagionali, campi (padel, calcio, tennis)",
    depends_on=["core", "anagrafica"],
    has_frontend=True,
)
