from __future__ import annotations

import jwt
import pytest

from arena.modules.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password() -> None:
    hashed = hash_password("segretissima")
    assert hashed != "segretissima"
    assert verify_password("segretissima", hashed)
    assert not verify_password("sbagliata", hashed)


def test_hash_is_not_deterministic() -> None:
    assert hash_password("x") != hash_password("x")


def test_verify_invalid_hash_does_not_raise() -> None:
    assert not verify_password("x", "non-un-hash-valido")


def test_access_token_roundtrip() -> None:
    token = create_access_token("42")
    payload = decode_token(token, expected_type="access")
    assert payload["sub"] == "42"


def test_refresh_token_type_guard() -> None:
    token = create_refresh_token("42")
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, expected_type="access")
