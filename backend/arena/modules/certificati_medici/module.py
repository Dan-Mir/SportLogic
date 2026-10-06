from __future__ import annotations

from arena.modules.base import ModuleManifest

manifest = ModuleManifest(
    name="certificati_medici",
    label="Certificati medici",
    version="0.1.0",
    description="Certificati sanitari cifrati, scadenze e consensi",
    depends_on=["core", "anagrafica"],
    has_frontend=True,
)
