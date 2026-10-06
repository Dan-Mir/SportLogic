from __future__ import annotations

from arena.modules.base import ModuleManifest

manifest = ModuleManifest(
    name="abbonamenti",
    label="Abbonamenti e pagamenti",
    version="0.1.0",
    description="Piani, abbonamenti, rate e pagamenti manuali",
    depends_on=["core", "anagrafica"],
    has_frontend=True,
)
