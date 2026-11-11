from sportlogic.modules.anagrafica.models import (  # noqa: F401
    Family,
    FamilyMember,
    Member,
    Staff,
)
from sportlogic.modules.anagrafica.module import manifest
from sportlogic.modules.anagrafica.router import router

__all__ = ["manifest", "router"]
