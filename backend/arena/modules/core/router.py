from __future__ import annotations

from fastapi import APIRouter

from arena.config import get_settings

router = APIRouter(prefix="/api/core", tags=["core"])


@router.get("/info")
def info() -> dict:
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "version": "0.1.0",
        "env": settings.env,
        "brand": {
            "name": settings.brand_name,
            "primary_color": settings.brand_primary_color,
            "public_domain": settings.public_domain,
        },
    }


@router.get("/settings")
def settings() -> dict:
    s = get_settings()
    return {
        "brand_name": s.brand_name,
        "brand_primary_color": s.brand_primary_color,
        "public_domain": s.public_domain,
    }
