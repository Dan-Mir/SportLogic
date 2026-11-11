from __future__ import annotations

import uuid
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated, Literal

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from sportlogic.config import get_settings
from sportlogic.db import get_db
from sportlogic.modules.anagrafica.models import Member
from sportlogic.modules.certificati_medici.crypto import decrypt, encrypt
from sportlogic.modules.certificati_medici.models import MedicalCertificate
from sportlogic.modules.certificati_medici.schemas import CertificateRead, CertificateUpdate
from sportlogic.modules.core.deps import get_client_ip, log_action, require_role
from sportlogic.modules.core.models import User

router = APIRouter(prefix="/api/certificati-medici", tags=["certificati-medici"])
DbSession = Annotated[Session, Depends(get_db)]
StaffUser = Annotated[User, Depends(require_role("admin", "gestore", "reception"))]
ManagerUser = Annotated[User, Depends(require_role("admin", "gestore"))]
ALLOWED_CONTENT_TYPES = {"application/pdf", "image/jpeg", "image/png", "image/webp"}


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
def list_certificates(
    db: DbSession,
    _: StaffUser,
    member_id: int | None = None,
    certificate_status: Literal["all", "expired", "expiring"] = Query(default="all", alias="status"),
    within_days: int = Query(default=30, ge=0, le=365),
) -> list[MedicalCertificate]:
    stmt = select(MedicalCertificate).order_by(MedicalCertificate.expires_on)
    if member_id is not None:
        stmt = stmt.where(MedicalCertificate.member_id == member_id)
    today = date.today()
    if certificate_status == "expired":
        stmt = stmt.where(MedicalCertificate.expires_on < today)
    elif certificate_status == "expiring":
        stmt = stmt.where(
            MedicalCertificate.expires_on >= today,
            MedicalCertificate.expires_on <= today + timedelta(days=within_days),
        )
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
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Formato file non supportato")
    if expires_on < (valid_from or expires_on):
        raise HTTPException(status_code=422, detail="La scadenza non può precedere la validità")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=422, detail="Il file è vuoto")
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Il file supera il limite di 10 MB")

    storage_filename = f"{uuid.uuid4().hex}.bin"
    original_filename = Path(file.filename or "documento").name.replace('"', "_")[:255]
    (_storage_path() / storage_filename).write_bytes(encrypt(content))
    certificate = MedicalCertificate(
        member_id=member_id,
        original_filename=original_filename,
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


@router.put("/{certificate_id}", response_model=CertificateRead)
def update_certificate(
    certificate_id: int,
    payload: CertificateUpdate,
    request: Request,
    db: DbSession,
    user: ManagerUser,
) -> MedicalCertificate:
    certificate = _get_certificate(db, certificate_id)
    values = payload.model_dump(exclude_unset=True)
    valid_from = values.get("valid_from", certificate.valid_from)
    expires_on = values.get("expires_on", certificate.expires_on)
    if expires_on < (valid_from or expires_on):
        raise HTTPException(status_code=422, detail="La scadenza non può precedere la validità")
    if values.get("consent_confirmed") is False:
        raise HTTPException(status_code=422, detail="Il consenso al trattamento è obbligatorio")
    for key, value in values.items():
        setattr(certificate, key, value)
    db.commit()
    db.refresh(certificate)
    log_action(
        db,
        user,
        "medical_certificate.update",
        "medical_certificate",
        str(certificate.id),
        ip_address=get_client_ip(request),
    )
    return certificate


@router.delete("/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(
    certificate_id: int,
    request: Request,
    db: DbSession,
    user: ManagerUser,
) -> None:
    certificate = _get_certificate(db, certificate_id)
    storage_path = _storage_path() / certificate.storage_filename
    db.delete(certificate)
    db.commit()
    storage_path.unlink(missing_ok=True)
    log_action(
        db,
        user,
        "medical_certificate.delete",
        "medical_certificate",
        str(certificate_id),
        ip_address=get_client_ip(request),
    )


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
