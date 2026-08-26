from __future__ import annotations

from arena.modules.base import ModuleManifest

manifest = ModuleManifest(
    name="anagrafica",
    label="Anagrafica",
    version="0.1.0",
    description="Soci, staff, famiglie e minori con tutori",
    depends_on=["core"],
    has_frontend=True,
)
