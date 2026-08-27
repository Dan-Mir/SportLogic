from arena.modules.core.models import User  # noqa: F401  (registra il modello su Base)
from arena.modules.core.module import manifest
from arena.modules.core.router import router
from arena.modules.core.settings_model import Setting  # noqa: F401

__all__ = ["manifest", "router"]
