from __future__ import annotations

import os

# Forza SQLite in memoria prima di importare il DB.
os.environ["ARENA_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

import arena.db as db
from arena.db import Base
from arena.main import create_app
from arena.modules.core.models import User
from arena.modules.core.security import hash_password


@pytest.fixture()
def client():
    db._engine = None
    db._session_factory = None
    Base.metadata.create_all(db.get_engine())
    app = create_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_client(client):
    # Crea utente admin direttamente sul DB (non c'è ancora un admin preesistente).
    session = _session()
    session.add(
        User(
            email="admin@test.it",
            hashed_password=hash_password("password"),
            full_name="Admin Test",
            role="admin",
        )
    )
    session.commit()
    session.close()
    return client


def _session():
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=db.get_engine())()


def _login(client, email="admin@test.it", password="password") -> str:
    r = client.post("/api/core/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_login_success(admin_client) -> None:
    r = admin_client.post(
        "/api/core/auth/login",
        json={"email": "admin@test.it", "password": "password"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["access_token"]
    assert data["refresh_token"]


def test_login_wrong_password(admin_client) -> None:
    r = admin_client.post(
        "/api/core/auth/login",
        json={"email": "admin@test.it", "password": "sbagliata"},
    )
    assert r.status_code == 401


def test_me_requires_token(admin_client) -> None:
    token = _login(admin_client)
    r = admin_client.get("/api/core/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "admin@test.it"


def test_me_without_token(client) -> None:
    assert client.get("/api/core/auth/me").status_code == 401


def test_refresh_token_flow(admin_client) -> None:
    refresh_token = admin_client.post(
        "/api/core/auth/login",
        json={"email": "admin@test.it", "password": "password"},
    ).json()["refresh_token"]
    r = admin_client.post("/api/core/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200
    assert r.json()["access_token"]


def test_branding_requires_admin(admin_client) -> None:
    token = _login(admin_client)
    r = admin_client.put(
        "/api/core/branding",
        json={"brand_name": "Nuovo Nome", "brand_primary_color": "#ABCDEF"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["brand_name"] == "Nuovo Nome"

    exported = admin_client.get(
        "/api/core/branding/export",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert exported.json()["brand_primary_color"] == "#ABCDEF"


def test_create_user_requires_admin(admin_client) -> None:
    token = _login(admin_client)
    r = admin_client.post(
        "/api/core/users",
        json={"email": "nuovo@test.it", "password": "x", "full_name": "Nuovo", "role": "reception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
