from sportlogic.modules.core.models import User  # noqa: F401  (registra il modello su Base)
from sportlogic.modules.core.module import manifest
from sportlogic.modules.core.router import router
from sportlogic.modules.core.settings_model import Setting  # noqa: F401

__all__ = ["manifest", "router"]
