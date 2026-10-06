from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from arena.db import get_db
from arena.modules.anagrafica.models import Family, Member, Staff
from arena.modules.anagrafica.schemas import (
    FamilyCreate,
    FamilyRead,
    FamilyUpdate,
    MemberCreate,
    MemberRead,
    MemberUpdate,
    StaffCreate,
    StaffRead,
    StaffUpdate,
)
from arena.modules.core.deps import get_client_ip, log_action, require_role
from arena.modules.core.models import User

router = APIRouter(prefix="/api/anagrafica", tags=["anagrafica"])

DbSession = Annotated[Session, Depends(get_db)]
AdminOrReception = Annotated[User, Depends(require_role("admin", "gestore", "reception"))]


def _not_found(entity: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} non trovato/a")


@router.get("/members", response_model=list[MemberRead])
def list_members(
    db: DbSession,
    _: AdminOrReception,
    q: str | None = Query(default=None, description="Ricerca per nome, cognome o CF"),
) -> list[Member]:
    stmt = select(Member).order_by(Member.last_name, Member.first_name)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            Member.last_name.ilike(like)
            | Member.first_name.ilike(like)
            | Member.fiscal_code.ilike(like)
        )
    return list(db.scalars(stmt))


@router.post("/members", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(
    payload: MemberCreate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Member:
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    log_action(
        db, current_user, "member.create", "member", str(member.id),
        detail=f"{member.first_name} {member.last_name}",
        ip_address=get_client_ip(request),
    )
    return member


@router.get("/members/{member_id}", response_model=MemberRead)
def get_member(member_id: int, db: DbSession, _: AdminOrReception) -> Member:
    member = db.get(Member, member_id)
    if member is None:
        raise _not_found("Socio")
    return member


@router.put("/members/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int,
    payload: MemberUpdate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Member:
    member = db.get(Member, member_id)
    if member is None:
        raise _not_found("Socio")
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return member
    for key, value in updates.items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    log_action(
        db, current_user, "member.update", "member", str(member_id),
        detail=f"campi: {', '.join(updates)}",
        ip_address=get_client_ip(request),
    )
    return member


@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    member_id: int,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> None:
    member = db.get(Member, member_id)
    if member is None:
        raise _not_found("Socio")
    log_action(
        db, current_user, "member.delete", "member", str(member_id),
        detail=f"{member.first_name} {member.last_name}",
        ip_address=get_client_ip(request),
    )
    db.delete(member)
    db.commit()


@router.get("/staff", response_model=list[StaffRead])
def list_staff(
    db: DbSession,
    _: AdminOrReception,
    q: str | None = Query(default=None),
) -> list[Staff]:
    stmt = select(Staff).order_by(Staff.last_name, Staff.first_name)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Staff.last_name.ilike(like) | Staff.first_name.ilike(like))
    return list(db.scalars(stmt))


@router.post("/staff", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: StaffCreate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Staff:
    staff = Staff(**payload.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    log_action(
        db, current_user, "staff.create", "staff", str(staff.id),
        detail=f"{staff.first_name} {staff.last_name}",
        ip_address=get_client_ip(request),
    )
    return staff


@router.get("/staff/{staff_id}", response_model=StaffRead)
def get_staff(staff_id: int, db: DbSession, _: AdminOrReception) -> Staff:
    staff = db.get(Staff, staff_id)
    if staff is None:
        raise _not_found("Staff")
    return staff


@router.put("/staff/{staff_id}", response_model=StaffRead)
def update_staff(
    staff_id: int,
    payload: StaffUpdate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Staff:
    staff = db.get(Staff, staff_id)
    if staff is None:
        raise _not_found("Staff")
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return staff
    for key, value in updates.items():
        setattr(staff, key, value)
    db.commit()
    db.refresh(staff)
    log_action(
        db, current_user, "staff.update", "staff", str(staff_id),
        detail=f"campi: {', '.join(updates)}",
        ip_address=get_client_ip(request),
    )
    return staff


@router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(
    staff_id: int,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> None:
    staff = db.get(Staff, staff_id)
    if staff is None:
        raise _not_found("Staff")
    log_action(
        db, current_user, "staff.delete", "staff", str(staff_id),
        detail=f"{staff.first_name} {staff.last_name}",
        ip_address=get_client_ip(request),
    )
    db.delete(staff)
    db.commit()


@router.get("/families", response_model=list[FamilyRead])
def list_families(
    db: DbSession,
    _: AdminOrReception,
    q: str | None = Query(default=None),
) -> list[Family]:
    stmt = select(Family).order_by(Family.name)
    if q:
        stmt = stmt.where(Family.name.ilike(f"%{q}%"))
    return list(db.scalars(stmt))


@router.post("/families", response_model=FamilyRead, status_code=status.HTTP_201_CREATED)
def create_family(
    payload: FamilyCreate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Family:
    family = Family(**payload.model_dump())
    db.add(family)
    db.commit()
    db.refresh(family)
    log_action(
        db, current_user, "family.create", "family", str(family.id),
        detail=f"name={family.name}",
        ip_address=get_client_ip(request),
    )
    return family


@router.get("/families/{family_id}", response_model=FamilyRead)
def get_family(family_id: int, db: DbSession, _: AdminOrReception) -> Family:
    family = db.get(Family, family_id)
    if family is None:
        raise _not_found("Famiglia")
    return family


@router.put("/families/{family_id}", response_model=FamilyRead)
def update_family(
    family_id: int,
    payload: FamilyUpdate,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> Family:
    family = db.get(Family, family_id)
    if family is None:
        raise _not_found("Famiglia")
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return family
    for key, value in updates.items():
        setattr(family, key, value)
    db.commit()
    db.refresh(family)
    log_action(
        db, current_user, "family.update", "family", str(family_id),
        detail=f"campi: {', '.join(updates)}",
        ip_address=get_client_ip(request),
    )
    return family


@router.delete("/families/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family(
    family_id: int,
    request: Request,
    db: DbSession,
    current_user: AdminOrReception,
) -> None:
    family = db.get(Family, family_id)
    if family is None:
        raise _not_found("Famiglia")
    log_action(
        db, current_user, "family.delete", "family", str(family_id),
        detail=f"name={family.name}",
        ip_address=get_client_ip(request),
    )
    db.delete(family)
    db.commit()
