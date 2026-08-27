from arena.modules.anagrafica.models import (  # noqa: F401
    Family,
    FamilyMember,
    Member,
    Staff,
)
from arena.modules.anagrafica.module import manifest
from arena.modules.anagrafica.router import router

__all__ = ["manifest", "router"]
