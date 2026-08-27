from __future__ import annotations

import re
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

from arena.config import get_settings
from arena.modules import discover_builtin, registry

MODULES_DIR = Path(__file__).parent.parent / "modules"


def _module_migrations_dir(module_name: str) -> Path:
    return MODULES_DIR / module_name / "migrations"


def _sanitize(name: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", name)


def _version_table(module_name: str) -> str:
    return f"alembic_version_{_sanitize(module_name)}"


def _config_for(module_name: str) -> Config:
    cfg = Config()
    cfg.set_main_option("script_location", str(_module_migrations_dir(module_name)))
    cfg.set_main_option("sqlalchemy.url", get_settings().database_url)
    cfg.set_main_option("version_table", _version_table(module_name))
    return cfg


def upgrade(target: str = "head") -> list[str]:
    """Applica le migration di tutti i moduli attivi, ciascuno con la propria
    tabella versioni, in ordine topologico."""
    discover_builtin()
    enabled = [m.name for m in registry.resolve(get_settings().modules_enabled)]

    applied: list[str] = []
    for name in enabled:
        mdir = _module_migrations_dir(name)
        if not (mdir / "versions").exists():
            continue
        cfg = _config_for(name)
        command.upgrade(cfg, target)
        applied.append(name)
    return applied


def current() -> dict[str, str]:
    discover_builtin()
    result: dict[str, str] = {}
    for manifest in registry.resolve(get_settings().modules_enabled):
        name = manifest.name
        mdir = _module_migrations_dir(name)
        if not (mdir / "versions").exists():
            continue
        cfg = _config_for(name)
        script = ScriptDirectory.from_config(cfg)
        head = script.get_current_head()
        result[name] = head or "base"
    return result
