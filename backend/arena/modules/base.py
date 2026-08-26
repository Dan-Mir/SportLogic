from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModuleManifest:
    name: str
    label: str
    version: str = "0.1.0"
    description: str = ""
    depends_on: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)
    has_frontend: bool = False
    workers: list[str] = field(default_factory=list)
    enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "label": self.label,
            "version": self.version,
            "description": self.description,
            "depends_on": self.depends_on,
            "config_schema": self.config_schema,
            "has_frontend": self.has_frontend,
            "workers": self.workers,
            "enabled": self.enabled,
        }
