from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sportlogic.db import Base, TimestampMixin


class MedicalCertificate(Base, TimestampMixin):
    __tablename__ = "medical_certificates"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_filename: Mapped[str] = mapped_column(String(80), unique=True)
    content_type: Mapped[str] = mapped_column(String(120), default="application/octet-stream")
    file_size: Mapped[int] = mapped_column(Integer)
    valid_from: Mapped[date | None] = mapped_column(Date)
    expires_on: Mapped[date] = mapped_column(Date, index=True)
    consent_confirmed: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str | None] = mapped_column(Text)
