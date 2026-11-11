from __future__ import annotations

import uuid
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from sportlogic.config import get_settings
from sportlogic.db import get_db
from sportlogic.modules.anagrafica.models import Member
from sportlogic.modules.certificati_medici.crypto import decrypt, encrypt
from sportlogic.modules.certificati_medici.models import MedicalCertificate
from sportlogic.modules.certificati_medici.schemas import CertificateRead
from sportlogic.modules.core.deps import get_client_ip, log_action, require_role
from sportlogic.modules.core.models import User

router = APIRouter(prefix="/api/certificati-medici", tags=["certificati-medici"])
DbSession = Annotated[Session, Depends(get_db)]
StaffUser = Annotated[User, Depends(require_role("admin", "gestore", "reception"))]


def _storage_path() -> Path:
    path = Path(get_settings().document_storage_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_certificate(db: Session, certificate_id: int) -> MedicalCertificate:
    certificate = db.get(MedicalCertificate, certificate_id)
    if certificate is None:
        raise HTTPException(status_code=404, detail="Certificato non trovato")
    return certificate


@router.get("", response_model=list[CertificateRead])
def list_certificates(db: DbSession, _: StaffUser, member_id: int | None = None) -> list[MedicalCertificate]:
    stmt = select(MedicalCertificate).order_by(MedicalCertificate.expires_on)
    if member_id is not None:
        stmt = stmt.where(MedicalCertificate.member_id == member_id)
    return list(db.scalars(stmt))


@router.post("", response_model=CertificateRead, status_code=status.HTTP_201_CREATED)
async def upload_certificate(
    request: Request,
    db: DbSession,
    user: StaffUser,
    file: Annotated[UploadFile, File()],
    member_id: Annotated[int, Form()],
    expires_on: Annotated[date, Form()],
    valid_from: Annotated[date | None, Form()] = None,
    consent_confirmed: Annotated[bool, Form()] = False,
    notes: Annotated[str | None, Form()] = None,
) -> MedicalCertificate:
    if not consent_confirmed:
        raise HTTPException(status_code=422, detail="Il consenso al trattamento è obbligatorio")
    if db.get(Member, member_id) is None:
        raise HTTPException(status_code=404, detail="Socio non trovato")
    if expires_on < (valid_from or expires_on):
        raise HTTPException(status_code=422, detail="La scadenza non può precedere la validità")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=422, detail="Il file è vuoto")
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Il file supera il limite di 10 MB")

    storage_filename = f"{uuid.uuid4().hex}.bin"
    (_storage_path() / storage_filename).write_bytes(encrypt(content))
    certificate = MedicalCertificate(
        member_id=member_id,
        original_filename=file.filename or "documento",
        storage_filename=storage_filename,
        content_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        valid_from=valid_from,
        expires_on=expires_on,
        consent_confirmed=consent_confirmed,
        notes=notes,
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    log_action(db, user, "medical_certificate.create", "medical_certificate", str(certificate.id),
               detail=f"member_id={member_id}", ip_address=get_client_ip(request))
    return certificate


@router.get("/{certificate_id}/download")
def download_certificate(certificate_id: int, request: Request, db: DbSession, user: StaffUser) -> Response:
    certificate = _get_certificate(db, certificate_id)
    path = _storage_path() / certificate.storage_filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File del certificato non trovato")
    log_action(db, user, "medical_certificate.download", "medical_certificate", str(certificate.id),
               ip_address=get_client_ip(request))
    return Response(
        content=decrypt(path.read_bytes()),
        media_type=certificate.content_type,
        headers={"Content-Disposition": f'attachment; filename="{certificate.original_filename}"'},
    )
