from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from arena.db import get_db
from arena.modules.core.models import User
from arena.modules.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/core/auth/login")

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, expected_type="access")
    except jwt.InvalidTokenError:
        raise credentials_error from None

    subject = payload.get("sub")
    if subject is None or not subject.isdigit():
        raise credentials_error

    user = db.get(User, int(subject))
    if user is None or not user.is_active:
        raise credentials_error
    return user


def require_role(*roles: str):
    def dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permessi insufficienti",
            )
        return user

    return dependency
