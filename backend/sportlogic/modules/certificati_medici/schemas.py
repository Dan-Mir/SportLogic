from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CertificateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    original_filename: str
    content_type: str
    file_size: int
    valid_from: date | None
    expires_on: date
    consent_confirmed: bool
    notes: str | None


class CertificateMetadata(BaseModel):
    expires_on: date
    valid_from: date | None = None
    consent_confirmed: bool = Field(description="Consenso esplicito al trattamento del documento")
    notes: str | None = None


class CertificateUpdate(BaseModel):
    expires_on: date | None = None
    valid_from: date | None = None
    consent_confirmed: bool | None = None
    notes: str | None = None
