from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from arena.db import get_db
from arena.modules.anagrafica.models import Family, Member, Staff
from arena.modules.anagrafica.schemas import (
    FamilyCreate,
    FamilyRead,
    MemberCreate,
    MemberRead,
    StaffCreate,
    StaffRead,
)
from arena.modules.core.deps import require_role

router = APIRouter(prefix="/api/anagrafica", tags=["anagrafica"])

DbSession = Annotated[Session, Depends(get_db)]
AdminOrReception = Annotated[object, Depends(require_role("admin", "gestore", "reception"))]


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
def create_member(payload: MemberCreate, db: DbSession, _: AdminOrReception) -> Member:
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.get("/members/{member_id}", response_model=MemberRead)
def get_member(member_id: int, db: DbSession, _: AdminOrReception) -> Member:
    member = db.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Socio non trovato")
    return member


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
def create_staff(payload: StaffCreate, db: DbSession, _: AdminOrReception) -> Staff:
    staff = Staff(**payload.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


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
def create_family(payload: FamilyCreate, db: DbSession, _: AdminOrReception) -> Family:
    family = Family(**payload.model_dump())
    db.add(family)
    db.commit()
    db.refresh(family)
    return family
