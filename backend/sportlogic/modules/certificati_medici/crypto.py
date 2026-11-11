from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet

from sportlogic.config import get_settings


def _key() -> bytes:
    settings = get_settings()
    if settings.document_encryption_key:
        return settings.document_encryption_key.encode("ascii")
    # Development fallback: production should configure a dedicated key.
    digest = hashlib.sha256(
        f"{settings.secret_key}:medical-certificates".encode()
    ).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt(data: bytes) -> bytes:
    return Fernet(_key()).encrypt(data)


def decrypt(data: bytes) -> bytes:
    return Fernet(_key()).decrypt(data)
