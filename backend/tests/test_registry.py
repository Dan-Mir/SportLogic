from __future__ import annotations

import pytest

from arena.modules.base import ModuleManifest
from arena.modules.registry import ModuleError, ModuleRegistry


def make(name: str, deps: list[str] | None = None) -> ModuleManifest:
    return ModuleManifest(name=name, label=name, depends_on=deps or [])


def test_register_and_get() -> None:
    r = ModuleRegistry()
    r.register(make("core"))
    assert r.get("core").name == "core"


def test_duplicate_raises() -> None:
    r = ModuleRegistry()
    r.register(make("core"))
    with pytest.raises(ModuleError):
        r.register(make("core"))


def test_enable_with_deps() -> None:
    r = ModuleRegistry()
    r.register(make("core"))
    r.register(make("anagrafica", ["core"]))
    r.register(make("corsi", ["anagrafica"]))
    r.enable("corsi")
    assert {m.name for m in r.enabled()} == {"core", "anagrafica", "corsi"}


def test_resolve_topological_order() -> None:
    r = ModuleRegistry()
    r.register(make("core"))
    r.register(make("anagrafica", ["core"]))
    r.register(make("corsi", ["core", "anagrafica"]))
    ordered = [m.name for m in r.resolve(["corsi"])]
    assert ordered.index("core") < ordered.index("anagrafica") < ordered.index("corsi")


def test_disable_with_dependent_raises() -> None:
    r = ModuleRegistry()
    r.register(make("core"))
    r.register(make("anagrafica", ["core"]))
    r.enable("anagrafica")
    with pytest.raises(ModuleError):
        r.disable("core")


def test_circular_dependency_raises() -> None:
    r = ModuleRegistry()
    r.register(make("a", ["b"]))
    r.register(make("b", ["a"]))
    with pytest.raises(ModuleError):
        r.resolve(["a"])
