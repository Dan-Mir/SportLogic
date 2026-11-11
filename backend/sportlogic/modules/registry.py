from __future__ import annotations

from .base import ModuleManifest


class ModuleError(Exception):
    pass


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ModuleManifest] = {}

    def register(self, manifest: ModuleManifest) -> None:
        if manifest.name in self._modules:
            raise ModuleError(f"Modulo gia registrato: {manifest.name}")
        self._modules[manifest.name] = manifest

    def get(self, name: str) -> ModuleManifest:
        try:
            return self._modules[name]
        except KeyError:
            raise ModuleError(f"Modulo sconosciuto: {name}") from None

    def all(self) -> list[ModuleManifest]:
        return list(self._modules.values())

    def enabled(self) -> list[ModuleManifest]:
        return [m for m in self._modules.values() if m.enabled]

    def enable(self, name: str, with_deps: bool = True) -> None:
        manifest = self.get(name)
        if with_deps:
            for dep in manifest.depends_on:
                self.enable(dep)
        manifest.enabled = True

    def disable(self, name: str) -> None:
        dependents = [m.name for m in self._modules.values() if name in m.depends_on and m.enabled]
        if dependents:
            raise ModuleError(
                f"Impossibile disattivare '{name}': richiesto da {', '.join(dependents)}"
            )
        self.get(name).enabled = False

    def resolve(self, names: list[str]) -> list[ModuleManifest]:
        enabled: set[str] = set(names)
        for name in list(enabled):
            enabled.update(self.get(name).depends_on)

        ordered: list[ModuleManifest] = []
        visited: set[str] = set()
        visiting: set[str] = set()

        def visit(name: str) -> None:
            if name in visited:
                return
            if name in visiting:
                raise ModuleError(f"Dipendenza circolare rilevata in '{name}'")
            visiting.add(name)
            for dep in self.get(name).depends_on:
                if dep in enabled:
                    visit(dep)
            visiting.remove(name)
            visited.add(name)
            ordered.append(self.get(name))

        for name in enabled:
            visit(name)
        return ordered
