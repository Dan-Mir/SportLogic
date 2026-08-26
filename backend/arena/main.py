from __future__ import annotations

from fastapi import FastAPI

from arena.config import get_settings
from arena.modules import apply_enabled, discover_builtin


def create_app() -> FastAPI:
    settings = get_settings()
    builtin = discover_builtin()
    by_name = {mod.manifest.name: mod for mod in builtin}
    enabled = apply_enabled(settings.modules_enabled)

    app = FastAPI(title=settings.app_name)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "modules": [m.name for m in enabled]}

    @app.get("/api/modules")
    def list_modules() -> dict:
        return {"modules": [m.to_dict() for m in enabled]}

    for manifest in enabled:
        router = getattr(by_name[manifest.name], "router", None)
        if router is not None:
            app.include_router(router)

    return app


app = create_app()
