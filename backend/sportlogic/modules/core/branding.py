from __future__ import annotations

from pydantic import BaseModel


class BrandingPayload(BaseModel):
    brand_name: str
    brand_primary_color: str
    public_domain: str | None = None


class BrandPack(BaseModel):
    """Pacchetto esportabile/importabile del white-label."""

    brand_name: str
    brand_primary_color: str
    public_domain: str | None = None
