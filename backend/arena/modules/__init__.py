from __future__ import annotations

from .base import ModuleManifest
from .registry import ModuleError, ModuleRegistry

registry = ModuleRegistry()

_BUILTIN: tuple = ()
_discovered = False


def discover_builtin() -> tuple:
    global _discovered, _BUILTIN
    if _discovered:
        return _BUILTIN
    from arena.modules import anagrafica, booking_fields, core, corsi

    _BUILTIN = (core, anagrafica, corsi, booking_fields)
    for mod in _BUILTIN:
        registry.register(mod.manifest)
    _discovered = True
    return _BUILTIN


def apply_enabled(names: list[str]) -> list[ModuleManifest]:
    discover_builtin()
    ordered = registry.resolve(names)
    for manifest in ordered:
        manifest.enabled = True
    return ordered


__all__ = [
    "ModuleManifest",
    "ModuleError",
    "ModuleRegistry",
    "registry",
    "discover_builtin",
    "apply_enabled",
]
