from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from arena.config import get_settings
from arena.db import get_db
from arena.modules.core.branding import BrandingPayload, BrandPack
from arena.modules.core.deps import get_current_user, require_role
from arena.modules.core.models import ROLES, User
from arena.modules.core.schemas import (
    LoginRequest,
    RefreshRequest,
    TokenPair,
    UserCreate,
    UserRead,
)
from arena.modules.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from arena.modules.core.settings_model import Setting

router = APIRouter(prefix="/api/core", tags=["core"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/info")
def info(db: DbSession) -> dict:
    settings = get_settings()
    brand = _get_branding(db)
    return {
        "app_name": settings.app_name,
        "version": "0.1.0",
        "env": settings.env,
        "brand": {
            "name": brand["brand_name"],
            "primary_color": brand["brand_primary_color"],
            "public_domain": brand["public_domain"],
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


@router.post("/auth/login", response_model=TokenPair)
def login(payload: LoginRequest, db: DbSession) -> TokenPair:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password non corretti",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disattivato",
        )
    subject = str(user.id)
    return TokenPair(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )


@router.post("/auth/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: DbSession) -> TokenPair:
    try:
        data = decode_token(payload.refresh_token, expected_type="refresh")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token non valido",
        ) from None

    subject = data.get("sub")
    if subject is None or not subject.isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token non valido",
        )

    user = db.get(User, int(subject))
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utente non trovato o disattivato",
        )

    return TokenPair(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )


@router.get("/auth/me", response_model=UserRead)
def me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: DbSession,
    _: Annotated[User, Depends(require_role("admin"))],
) -> User:
    if payload.role not in ROLES:
        raise HTTPException(status_code=400, detail=f"Ruolo non valido: {payload.role}")
    if db.scalar(select(User).where(User.email == payload.email)) is not None:
        raise HTTPException(status_code=409, detail="Email già registrata")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


BRAND_KEYS = ("brand_name", "brand_primary_color", "public_domain")


def _get_branding(db: Session) -> dict[str, str]:
    rows = db.scalars(select(Setting).where(Setting.key.in_(BRAND_KEYS)))
    stored = {r.key: r.value for r in rows}
    s = get_settings()
    return {
        "brand_name": stored.get("brand_name", s.brand_name),
        "brand_primary_color": stored.get("brand_primary_color", s.brand_primary_color),
        "public_domain": stored.get("public_domain", s.public_domain),
    }


def _put_branding(db: Session, payload: BrandingPayload) -> BrandPack:
    values = {
        "brand_name": payload.brand_name,
        "brand_primary_color": payload.brand_primary_color,
        "public_domain": payload.public_domain or "",
    }
    existing = {r.key: r for r in db.scalars(select(Setting).where(Setting.key.in_(BRAND_KEYS)))}
    for key, value in values.items():
        row = existing.get(key)
        if row is None:
            db.add(Setting(key=key, value=value))
        else:
            row.value = value
    db.commit()
    return BrandPack(**values)


@router.get("/branding", response_model=BrandPack)
def get_branding(db: DbSession, _: Annotated[User, Depends(require_role("admin", "gestore"))]) -> BrandPack:
    return BrandPack(**_get_branding(db))


@router.put("/branding", response_model=BrandPack)
def update_branding(
    payload: BrandingPayload,
    db: DbSession,
    _: Annotated[User, Depends(require_role("admin"))],
) -> BrandPack:
    return _put_branding(db, payload)


@router.get("/branding/export", response_model=BrandPack)
def export_brand_pack(
    db: DbSession,
    _: Annotated[User, Depends(require_role("admin", "gestore"))],
) -> BrandPack:
    return BrandPack(**_get_branding(db))


@router.post("/branding/import", response_model=BrandPack)
def import_brand_pack(
    pack: BrandPack,
    db: DbSession,
    _: Annotated[User, Depends(require_role("admin"))],
) -> BrandPack:
    return _put_branding(db, BrandingPayload(**pack.model_dump()))
